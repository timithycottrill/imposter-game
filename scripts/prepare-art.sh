#!/usr/bin/env bash
set -euo pipefail
if test -f public/art/words.webp; then exit 0; fi
sudo apt-get update -qq
sudo apt-get install -y fonts-noto-color-emoji
python -m pip install pillow
npm install --no-save --package-lock=false sharp
python scripts/make-picture-atlas.py
