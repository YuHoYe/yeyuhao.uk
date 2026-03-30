#!/usr/bin/env bash
# Upload an image to Cloudflare R2 and print the public URL.
# Usage: ./scripts/upload-r2.sh <local-file> [remote-path]
# Example: ./scripts/upload-r2.sh photo.jpg blog/2026/03/photo.jpg

set -euo pipefail

BUCKET="site-images"
BASE_URL="https://img.yeyuhao.uk"

if [ $# -lt 1 ]; then
  echo "Usage: $0 <file> [remote-path]"
  echo "  file         Local image file to upload"
  echo "  remote-path  Optional path in R2 (default: blog/YYYY/MM/filename)"
  exit 1
fi

FILE="$1"
FILENAME=$(basename "$FILE")

if [ $# -ge 2 ]; then
  REMOTE_PATH="$2"
else
  YEAR=$(date +%Y)
  MONTH=$(date +%m)
  REMOTE_PATH="blog/${YEAR}/${MONTH}/${FILENAME}"
fi

npx wrangler r2 object put "${BUCKET}/${REMOTE_PATH}" \
  --file "$FILE" \
  --content-type "$(file --mime-type -b "$FILE")"

echo ""
echo "Uploaded: ${BASE_URL}/${REMOTE_PATH}"
echo "Markdown: ![${FILENAME}](${BASE_URL}/${REMOTE_PATH})"
