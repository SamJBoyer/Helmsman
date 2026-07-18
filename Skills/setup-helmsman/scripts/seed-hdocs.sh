# Copies Helmsman/canon/c_hDocs -> ./hDocs, moves HELMSMAN.md to repo root,
# then deletes the Helmsman clone. Run from the target project root.

set -euo pipefail

HELMSMAN_DIR="${1:-Helmsman}"
PROJECT_ROOT="${2:-$(pwd)}"

CLONE="${PROJECT_ROOT}/${HELMSMAN_DIR}"
SOURCE="${CLONE}/canon/c_hDocs"
HDOCS="${PROJECT_ROOT}/hDocs"
HELMSMAN_MD="${HDOCS}/HELMSMAN.md"
ROOT_HELMSMAN_MD="${PROJECT_ROOT}/HELMSMAN.md"

if [ ! -d "$SOURCE" ]; then
  echo "Source not found: $SOURCE" >&2
  exit 1
fi

if [ -e "$HDOCS" ]; then
  echo "hDocs already exists at $HDOCS — refuse to overwrite." >&2
  exit 1
fi

if [ -e "$ROOT_HELMSMAN_MD" ]; then
  echo "HELMSMAN.md already exists at $ROOT_HELMSMAN_MD — refuse to overwrite." >&2
  exit 1
fi

cp -R "$SOURCE" "$HDOCS"

if [ ! -f "$HELMSMAN_MD" ]; then
  echo "Expected HELMSMAN.md after copy, but missing: $HELMSMAN_MD" >&2
  exit 1
fi

mv "$HELMSMAN_MD" "$ROOT_HELMSMAN_MD"

rm -rf "$CLONE"

echo "Seeded hDocs from $SOURCE"
echo "Moved HELMSMAN.md to $ROOT_HELMSMAN_MD"
echo "Removed Helmsman clone at $CLONE"
