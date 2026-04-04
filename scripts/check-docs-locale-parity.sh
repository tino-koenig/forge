#!/usr/bin/env bash
set -euo pipefail

required=(
  index.md
  getting-started.md
  core-commands.md
  trust-and-safety.md
  runtime-settings-and-sessions.md
  llm-setup.md
  troubleshooting.md
  faq.md
)

missing=0
for page in "${required[@]}"; do
  if [[ ! -f "docs/en/$page" ]]; then
    echo "[docs-parity] missing EN page: docs/en/$page"
    missing=1
  fi
  if [[ ! -f "docs/de/$page" ]]; then
    echo "[docs-parity] missing DE page: docs/de/$page"
    missing=1
  fi
done

if [[ "$missing" -ne 0 ]]; then
  exit 1
fi

echo "[docs-parity] PASS"
