# Phantasy Star IV - Extracted Images

Automated extraction of graphics from the Phantasy Star IV disassembly (`ps4disasm` / lory90).

## Quick start (automated)

1. Install dependencies:
   ```bash
   pip install pillow
   ```

2. Build the decompression tools (once):
   - [accurate-kosinski](https://github.com/Clownacy/accurate-kosinski) → produces `kosinski-decompress`
   - [clownnemesis](https://github.com/Clownacy/clownnemesis) → produces `clownnemesis`
   - [clownlzss](https://github.com/Clownacy/clownlzss) → produces `clownlzss`

   Put the three binaries in your PATH or in the same folder as the script.

3. Run the extractor:
   ```bash
   python3 extract_images.py /path/to/your/ps4disasm
   ```

The script will:
- Decompress all Kosinski, Nemesis and Enigma files
- Convert tile data to PNG (with automatic palette matching)
- Copy palettes
- Create a ready-to-use `PSIV_Images.zip`

## Output structure

```
extracted_images/
├── tiles/          # PNG images + raw decompressed data
├── mappings/       # Enigma plane mappings
└── palettes/       # Palette files
PSIV_Images.zip
```

## What you get

- Dialogue portraits
- Battle backgrounds
- Intro graphics
- Plane mappings
- Palettes

Educational / research use only. Original game © Sega.
