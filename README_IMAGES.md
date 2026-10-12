# Extracted Images

The full set of extracted PNGs, raw decompressed data, palettes and mappings is available as a zip archive.

**Download and decode:**

```bash
base64 -d PSIV_Images.zip.b64 > PSIV_Images.zip
unzip PSIV_Images.zip
```

Contents:
- tiles/*.png : 77 images (portraits, battle backgrounds, etc.)
- tiles/*.raw : decompressed tile data
- mappings/ : Enigma plane maps
- palettes/ : color palettes

Generated from the ps4disasm graphics folders using Kosinski / Nemesis / Enigma decompressors.
