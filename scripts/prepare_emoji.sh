#!/bin/bash

set -e

EMOJI_ZIP_URL="https://github.com/hfg-gmuend/openmoji/releases/latest/download/openmoji-72x72-color.zip"
DOWNLOAD_PATH="/tmp/emoji.zip"
EXTRACT_PATH="$(pwd)/data/openmoji"

command -v unzip >/dev/null 2>&1 || { echo >&2 "unzip is required but not installed. Aborting."; exit 1; }
command -v curl >/dev/null 2>&1 || { echo >&2 "curl is required but not installed. Aborting."; exit 1; }
command -v ffmpeg >/dev/null 2>&1 || { echo >&2 "ffmpeg is required but not installed. Aborting."; exit 1; }


if [ -f "$DOWNLOAD_PATH" ]; then
    rm "$DOWNLOAD_PATH"
fi

if [ -d "$EXTRACT_PATH" ]; then
    rm -rf "$EXTRACT_PATH"
fi

mkdir -p "$EXTRACT_PATH"

curl -s -L -o "$DOWNLOAD_PATH" "$EMOJI_ZIP_URL"
unzip -q "$DOWNLOAD_PATH" -d "$EXTRACT_PATH"

for file in "$EXTRACT_PATH"/*.png; do
    mv "$file" "${file%.png}.back.png"
    ffmpeg -v error -i "${file%.png}.back.png" -vf scale=16:16 "${file%.png}.png"
    rm "${file%.png}.back.png"
done

rm "$DOWNLOAD_PATH"
