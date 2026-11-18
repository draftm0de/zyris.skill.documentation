#!/usr/bin/env bash
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
ACTION=install
case "${1:-}" in
  install|update|build|check) ACTION="$1"; shift ;;
  claude|chatgpt|codex) TARGET="$1"; shift; set -- --target "$TARGET" "$@" ;;
  claude-chat|claude-plugin|all|--yes)
    echo "Legacy skill installation removed. Use: bash install.sh install --target claude|chatgpt|codex; or bash install.sh build. Existing skills are not removed automatically." >&2
    exit 2 ;;
esac
exec "${PYTHON:-python3}" "$ROOT/scripts/plugin.py" "$ACTION" "$@"
