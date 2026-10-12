#!/usr/bin/env python3
"""
Extract and convert Phantasy Star IV graphics from disassembly compressed files.
Requires Pillow and the decompression tools (kosinski-decompress, clownnemesis, clownlzss).
"""
import subprocess
import struct
from pathlib import Path
from PIL import Image
import shutil

BASE = Path(".")  # Disassembly root (art/, mappings/, etc.)
OUT = Path("./extracted_images")

TOOLS = {
    "kosinski": "kosinski-decompress",
    "nemesis": "clownnemesis",
    "enigma": "clownlzss",
}

OUT.mkdir(exist_ok=True)
for d in ["tiles", "palettes", "mappings"]:
    (OUT / d).mkdir(exist_ok=True)

def genesis_color(val):
    r = ((val & 0x00E) >> 1) * 36
    g = ((val & 0x0E0) >> 5) * 36
    b = ((val & 0xE00) >> 9) * 36
    return (min(r, 255), min(g, 255), min(b, 255))

def parse_palette(data):
    colors = []
    for i in range(0, len(data) - 1, 2):
        val = struct.unpack(">H", data[i:i+2])[0]
        colors.append(genesis_color(val))
    return colors

def tiles_to_image(tile_data, palette, tiles_per_row=8):
    if len(tile_data) < 32:
        return None
    num_tiles = len(tile_data) // 32
    if num_tiles == 0:
        return None
    rows = (num_tiles + tiles_per_row - 1) // tiles_per_row
    img = Image.new("P", (tiles_per_row * 8, rows * 8))
    pal = []
    for c in palette[:16]:
        pal.extend(list(c))
    while len(pal) < 768:
        pal.extend([0, 0, 0])
    img.putpalette(pal[:768])
    pixels = img.load()
    for t in range(num_tiles):
        tile_off = t * 32
        tx = (t % tiles_per_row) * 8
        ty = (t // tiles_per_row) * 8
        for y in range(8):
            row_bytes = [tile_data[tile_off + y * 4 + p] for p in range(4)]
            for x in range(8):
                bit = 7 - x
                pix = 0
                for p in range(4):
                    if row_bytes[p] & (1 << bit):
                        pix |= (1 << p)
                pixels[tx + x, ty + y] = pix
    return img

def process_files(src_dir, format_name, tool_cmd, out_subdir):
    src = BASE / src_dir
    if not src.exists():
        print(f"Skipping {src_dir}")
        return 0
    count = 0
    dest = OUT / out_subdir
    for binfile in sorted(src.glob("*.bin")):
        name = binfile.stem
        raw_out = dest / f"{name}.raw"
        png_out = dest / f"{name}.png"
        try:
            if format_name == "kosinski":
                subprocess.run([tool_cmd, str(binfile), str(raw_out)], check=True, capture_output=True)
            elif format_name == "nemesis":
                subprocess.run([tool_cmd, "-d", str(binfile), str(raw_out)], check=True, capture_output=True)
            elif format_name == "enigma":
                subprocess.run([tool_cmd, "-e", str(binfile), str(raw_out)], check=True, capture_output=True)
            pal_candidates = list((BASE / "art" / "palettes").glob(f"*{name.split()[0]}*"))
            pal_data = pal_candidates[0].read_bytes() if pal_candidates else None
            palette = parse_palette(pal_data) if pal_data and len(pal_data) >= 2 else [(i * 16, i * 16, i * 16) for i in range(16)]
            tile_data = raw_out.read_bytes()
            if len(tile_data) >= 32 and format_name != "enigma":
                img = tiles_to_image(tile_data, palette, 16 if len(tile_data) > 2048 else 8)
                if img:
                    img.save(png_out)
                    count += 1
            else:
                count += 1
        except Exception as e:
            print(f"Error on {binfile.name}: {e}")
    return count

if __name__ == "__main__":
    print("Kosinski:", process_files("art/kosinski", "kosinski", TOOLS["kosinski"], "tiles"))
    print("Nemesis:", process_files("art/nemesis", "nemesis", TOOLS["nemesis"], "tiles"))
    print("Enigma:", process_files("mappings/enigma", "enigma", TOOLS["enigma"], "mappings"))
    for p in (BASE / "art" / "palettes").glob("*.bin"):
        shutil.copy(p, OUT / "palettes" / p.name)
    print("Done. Output:", OUT)
