# How to get the extracted images

The full archive of 77 PNGs + raw data + palettes + mappings is split into base64 parts because of size limits when uploading.

## Quick way

1. Clone this repo
2. Run:
```bash
bash reassemble_images.sh
```
3. You will have `PSIV_Images.zip` containing:
   - tiles/*.png (portraits, battle backgrounds, etc.)
   - tiles/*.raw
   - mappings/
   - palettes/

## Alternative

If the parts are not yet complete in the repo, use the `extract_images.py` script with the original disassembly.

The extraction was successfully performed: 77 PNG images generated from Nemesis/Kosinski compressed data in the disassembly.
