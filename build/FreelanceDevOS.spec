# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec file for Freelance Dev OS
# Builds a single-folder distribution for macOS and Windows.
#
# Usage:
#   pip install pyinstaller
#   pyinstaller build/FreelanceDevOS.spec

import sys
import os
from pathlib import Path

ROOT = Path(SPECPATH).parent

block_cipher = None

# ── Data files to bundle ──────────────────────────────────────────────────────
datas = [
    # Templates
    (str(ROOT / 'dashboard' / 'templates'), 'dashboard/templates'),
    # Static assets
    (str(ROOT / 'dashboard' / 'static'),    'dashboard/static'),
    # PARA vault templates
    (str(ROOT / 'vault'),                   'vault'),
    # Environment example
    (str(ROOT / '.env.example'),            '.'),
]

# ── Hidden imports that PyInstaller might miss ────────────────────────────────
hiddenimports = [
    # FastAPI / Starlette
    'fastapi',
    'fastapi.middleware.cors',
    'starlette',
    'starlette.middleware.base',
    'uvicorn',
    'uvicorn.lifespan.on',
    'uvicorn.protocols.websockets.auto',
    'uvicorn.protocols.http.auto',
    'websockets',
    # Jinja2
    'jinja2',
    'jinja2.ext',
    # Security
    'jose',
    'jose.jwt',
    'passlib',
    'passlib.handlers.bcrypt',
    'cryptography',
    'slowapi',
    # Data
    'pydantic',
    'yaml',
    'stripe',
    'dotenv',
    # Desktop
    'webview',
]

# ── Main analysis ─────────────────────────────────────────────────────────────
a = Analysis(
    [str(ROOT / 'run.py')],
    pathex=[str(ROOT)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter', 'matplotlib', 'PIL', 'numpy', 'pandas'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='FreelanceDevOS',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,          # No terminal window on Windows
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # Windows icon (create icon.ico in desktop/ folder)
    icon=str(ROOT / 'desktop' / 'icon.ico') if (ROOT / 'desktop' / 'icon.ico').exists() else None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='FreelanceDevOS',
)

# ── macOS .app bundle ─────────────────────────────────────────────────────────
if sys.platform == 'darwin':
    app = BUNDLE(
        coll,
        name='FreelanceDevOS.app',
        icon=str(ROOT / 'desktop' / 'icon.icns') if (ROOT / 'desktop' / 'icon.icns').exists() else None,
        bundle_identifier='com.freelancedevos.app',
        info_plist={
            'CFBundleName':                'Freelance Dev OS',
            'CFBundleDisplayName':         'Freelance Dev OS',
            'CFBundleVersion':             '2.0.0',
            'CFBundleShortVersionString':  '2.0',
            'NSHighResolutionCapable':     True,
            'NSHumanReadableCopyright':    'Copyright © 2025 Freelance Dev OS',
            'LSMinimumSystemVersion':      '10.14.0',
            'NSPrincipalClass':            'NSApplication',
        },
    )
