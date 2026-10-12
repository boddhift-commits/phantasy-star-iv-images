#!/usr/bin/env python3
"""
Fully automated Phantasy Star IV image extractor.

Usage:
  python3 extract_images.py /path/to/ps4disasm

Requirements:
  - Pillow (pip install pillow)
  - The three decompression tools must be in PATH or in the same directory:
      kosinski-decompress
      clownnemesis
      clownlzss

The script will:
  1. Locate art/kosinski, art/nemesis, mappings/enigma, art/palettes
  2. Decompress everything
  3. Convert tile data to PNG (with palette matching)
  4. Output a clean folder structure + a zip
"""

import argparse
import subprocess
import struct
import shutil
import sys
from pathlib import Path
from PIL import Image

def genesis_color(val: int) -> tuple:
    r = ((val & 0x00E) >> 1) * 36
    g = ((val & 0x0E0) >> 5) * 36
    b = ((val & 0xE00) >> 9) * 36
    return (min(r, 255), min(g, 255), min(b, 255))

def parse_palette(data: bytes) -> list:
    colors = []
    for i in range(0, len(data) - 1, 2):
        val = struct.unpack(">H", data[i:i+2])[0]
        colors.append(genesis_color(val))
    return colors

def tiles_to_image(tile_data: bytes, palette: list, tiles_per_row: int = 8) -> Image.Image | None:
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

def find_tool(name: str) -> str:
    """Return path to tool if available."""
    for candidate in [name, f"./{name}", f"./tools/{name}"]:
        if shutil.which(candidate) or Path(candidate).exists():
            return candidate
    print(f"WARNING: {name} not found in PATH. Decompression for this format will be skipped.")
    return None

def process_directory(src: Path, fmt: str, tool: str, dest: Path, palettes_dir: Path):
    if not src.exists() or not tool:
        print(f"Skipping {src} (missing or no tool)")
        return 0

    count = 0
    dest.mkdir(parents=True, exist_ok=True)

    for binfile in sorted(src.glob("*.bin")):
        safe_name = binfile.stem.replace(" ", "_").replace("/", "_")
        raw_out = dest / f"{safe_name}.raw"
        png_out = dest / f"{safe_name}.png"

        try:
            if fmt == "kosinski":
                subprocess.run([tool, str(binfile), str(raw_out)], check=True, capture_output=True)
            elif fmt == "nemesis":
                subprocess.run([tool, "-d", str(binfile), str(raw_out)], check=True, capture_output=True)
            elif fmt == "enigma":
                subprocess.run([tool, "-e", str(binfile), str(raw_out)], check=True, capture_output=True)

            # Palette matching
            first_word = binfile.stem.split()[0]
            pal_candidates = list(palettes_dir.glob(f"*{first_word}*"))
            pal_data = pal_candidates[0].read_bytes() if pal_candidates else None
            palette = parse_palette(pal_data) if pal_data and len(pal_data) >= 2 else [(i * 16, i * 16, i * 16) for i in range(16)]

            tile_data = raw_out.read_bytes()
            if len(tile_data) >= 32 and fmt != "enigma":
                img = tiles_to_image(tile_data, palette, tiles_per_row=16 if len(tile_data) > 2048 else 8)
                if img:
                    img.save(png_out)
                    count += 1
            else:
                count += 1

        except subprocess.CalledProcessError as e:
            print(f"Decompression failed for {binfile.name}: {e}")
        except Exception as e:
            print(f"Error on {binfile.name}: {e}")

    return count

def main():
    parser = argparse.ArgumentParser(description="Extract Phantasy Star IV images from disassembly")
    parser.add_argument("disasm_path", help="Path to the ps4disasm folder (containing art/ and mappings/)")
    parser.add_argument("-o", "--output", default="extracted_images", help="Output directory")
    args = parser.parse_args()

    base = Path(args.disasm_path).resolve()
    if not (base / "art").exists():
        print(f"Error: {base} does not look like a ps4disasm folder (missing art/)")
        sys.exit(1)

    out = Path(args.output)
    if out.exists():
        shutil.rmtree(out)
    out.mkdir()

    tools = {
        "kosinski": find_tool("kosinski-decompress"),
        "nemesis": find_tool("clownnemesis"),
        "enigma": find_tool("clownlzss"),
    }

    palettes_dir = base / "art" / "palettes"

    print("=== Phantasy Star IV Image Extractor ===")
    print(f"Source: {base}")
    print(f"Output: {out}\n")

    k = process_directory(base / "art" / "kosinski", "kosinski", tools["kosinski"], out / "tiles", palettes_dir)
    n = process_directory(base / "art" / "nemesis", "nemesis", tools["nemesis"], out / "tiles", palettes_dir)
    e = process_directory(base / "mappings" / "enigma", "enigma", tools["enigma"], out / "mappings", palettes_dir)

    # Copy palettes
    (out / "palettes").mkdir(exist_ok=True)
    if palettes_dir.exists():
        for p in palettes_dir.glob("*.bin"):
            shutil.copy(p, out / "palettes" / p.name.replace(" ", "_"))

    # Create zip
    zip_path = out.parent / "PSIV_Images.zip"
    if zip_path.exists():
        zip_path.unlink()
    shutil.make_archive(str(zip_path.with_suffix("")), "zip", out)

    png_count = len(list((out / "tiles").glob("*.png")))
    print(f"\nDone!")
    print(f"  Kosinski files processed : {k}")
    print(f"  Nemesis files processed  : {n}")
    print(f"  Enigma files processed   : {e}")
    print(f"  PNG images created       : {png_count}")
    print(f"  Output folder            : {out}")
    print(f"  Zip archive              : {zip_path}")

if __name__ == "__main__":
    main()
