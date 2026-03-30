#!/bin/bash
# Sync confirmed memos from Obsidian vault to website content directory
# Usage: ./scripts/sync-memos.sh

VAULT_DIR="$HOME/Developer/YuhoVault/Memos/notes"
SITE_DIR="$(cd "$(dirname "$0")/.." && pwd)/src/content/memos"

if [ ! -d "$VAULT_DIR" ]; then
  echo "Vault not found, skipping sync (CI environment)"
  exit 0
fi

# Clean target directory
rm -f "$SITE_DIR"/*.md

count=0
for f in "$VAULT_DIR"/*.md; do
  # Only copy memos with confirmed: true
  if grep -q "^confirmed: true" "$f"; then
    cp "$f" "$SITE_DIR/"
    count=$((count + 1))
  fi
done

echo "Synced $count confirmed memos to $SITE_DIR"
