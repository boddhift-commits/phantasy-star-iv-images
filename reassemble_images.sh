#!/bin/bash
# Reassemble the base64 parts into the images zip
cat images_parts/b64_part_* > PSIV_Images.zip.b64
base64 -d PSIV_Images.zip.b64 > PSIV_Images.zip
echo "Created PSIV_Images.zip ($(wc -c < PSIV_Images.zip) bytes)"
unzip -l PSIV_Images.zip | head -30
