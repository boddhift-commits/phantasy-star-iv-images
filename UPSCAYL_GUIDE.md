# Upscayl Guide for Phantasy Star IV Portraits

Use Upscayl to upscale the extracted dialogue portraits while keeping maximum fidelity.

## Recommended settings for Mega Drive portraits

- **Scale**: 2x or 4x (start with 2x on old hardware)
- **Model**: `upscayl-standard-4x` or `remacri-4x` (good balance for pixel art / sprites)
- **Avoid**: models that invent too many details (ultramix, ultrasharp) if you want strict fidelity
- **Format**: PNG

## GUI (simplest)

1. Extract the portraits with `python3 extract_images.py /path/to/ps4disasm`
2. Open Upscayl
3. Select the folder `extracted_images/tiles/` (or individual PNGs)
4. Choose scale 2x or 4x + a conservative model
5. Output to a new folder `upscaled_portraits/`

## CLI (for automation / old PC batch)

Upscayl has a CLI via `upscayl-bin` (or the separate `upscayl-cli` project).

Example (adjust paths):

```bash
# Single image
upscayl-bin -i portraits/Chaz_dialogue_portrait.png -o upscaled/Chaz_4x.png -s 4 -n upscayl-standard-4x -f png

# Batch (if supported by your version)
upscayl-bin -i extracted_images/tiles/ -o upscaled_portraits/ -s 2 -n remacri-4x -f png
```

## Tips for old PC

- Prefer 2x scale
- Close other apps
- Force discrete GPU if available
- Process one portrait at a time if memory is low
- If Vulkan fails → use Upscayl Cloud (browser)

## Next step in the Godot port

Once upscaled, drop the PNGs into the Godot project under `assets/sprites/portraits/` and update the dialogue UI to load them.

---

Original portraits extracted from the disassembly. Upscayl for HD enhancement only.
