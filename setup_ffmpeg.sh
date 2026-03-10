#!/usr/bin/env bash
set -e

mkdir -p bin
cd /tmp

curl -L -o ffmpeg.tar.xz https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz
tar -xf ffmpeg.tar.xz

DIR=$(find . -maxdepth 1 -type d -name "ffmpeg-*-amd64-static" | head -n 1)

cp "$DIR/ffmpeg" /app/bin/ffmpeg
cp "$DIR/ffprobe" /app/bin/ffprobe

chmod +x /app/bin/ffmpeg /app/bin/ffprobe
