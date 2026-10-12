#!/bin/bash
# Reassemble the base64 parts into PSIV_Images.zip
mkdir -p images_parts
cat images_parts/b64_part_* > PSIV_Images.zip.b64
base64 -d PSIV_Images.zip.b64 > PSIV_Images.zip
echo "Created PSIV_Images.zip"
unzip -l PSIV_Images.zip | head -20
echo "..."
unzip -l PSIV_Images.zip | tail -5
