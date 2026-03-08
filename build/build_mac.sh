#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════════════════
# build_mac.sh — Build Freelance Dev OS as a macOS .app bundle
# ═══════════════════════════════════════════════════════════════════════════════
# Requirements:
#   macOS 10.14+ with Python 3.9+
#   pip install pyinstaller pywebview
#
# Usage:
#   chmod +x build/build_mac.sh
#   ./build/build_mac.sh
# ═══════════════════════════════════════════════════════════════════════════════
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
DIST_DIR="$PROJECT_ROOT/dist"
BUILD_DIR="$PROJECT_ROOT/build_cache"

echo ""
echo "  🚀  Freelance Dev OS — macOS Build"
echo "  ══════════════════════════════════"
echo ""

# ── 1. Check Python version ──────────────────────────────────────────────────
python_version=$(python3 --version 2>&1 | awk '{print $2}')
required="3.9"
if python3 -c "import sys; exit(0 if sys.version_info >= (3,9) else 1)"; then
    echo "  ✓ Python $python_version"
else
    echo "  ❌ Python 3.9+ required (found $python_version)"
    exit 1
fi

# ── 2. Activate virtual environment (if present) ────────────────────────────
if [ -d "$PROJECT_ROOT/venv" ]; then
    source "$PROJECT_ROOT/venv/bin/activate"
    echo "  ✓ Virtual environment activated"
fi

# ── 3. Install / verify dependencies ─────────────────────────────────────────
echo "  📦 Installing dependencies …"
pip install -q -r "$PROJECT_ROOT/requirements.txt"
pip install -q pyinstaller pywebview

echo "  ✓ Dependencies installed"

# ── 4. Clean previous build artefacts ────────────────────────────────────────
rm -rf "$DIST_DIR" "$BUILD_DIR"
echo "  ✓ Cleaned previous build"

# ── 5. Run PyInstaller ────────────────────────────────────────────────────────
echo "  🔨 Running PyInstaller …"
cd "$PROJECT_ROOT"

pyinstaller \
    --noconfirm \
    --clean \
    --distpath="$DIST_DIR" \
    --workpath="$BUILD_DIR" \
    "$SCRIPT_DIR/FreelanceDevOS.spec"

echo "  ✓ PyInstaller complete"

# ── 6. Verify output ──────────────────────────────────────────────────────────
if [ -d "$DIST_DIR/FreelanceDevOS.app" ]; then
    echo ""
    echo "  ✅  Build successful!"
    echo "      App: $DIST_DIR/FreelanceDevOS.app"
    echo ""
    echo "  To run:    open '$DIST_DIR/FreelanceDevOS.app'"
    echo "  To distribute: zip -r FreelanceDevOS-mac.zip '$DIST_DIR/FreelanceDevOS.app'"
    echo ""
else
    echo "  ❌  Build failed — FreelanceDevOS.app not found in $DIST_DIR"
    exit 1
fi

# ── 7. Optional: Create DMG (requires create-dmg) ────────────────────────────
if command -v create-dmg &>/dev/null; then
    echo "  💿 Creating DMG …"
    create-dmg \
        --volname "Freelance Dev OS" \
        --window-pos 200 120 \
        --window-size 800 400 \
        --icon-size 100 \
        --app-drop-link 600 185 \
        "$DIST_DIR/FreelanceDevOS-mac.dmg" \
        "$DIST_DIR/FreelanceDevOS.app"
    echo "  ✓ DMG created: $DIST_DIR/FreelanceDevOS-mac.dmg"
fi
