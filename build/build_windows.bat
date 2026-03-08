@echo off
REM ═══════════════════════════════════════════════════════════════════════════════
REM build_windows.bat — Build Freelance Dev OS as a Windows .exe
REM ═══════════════════════════════════════════════════════════════════════════════
REM Requirements:
REM   Windows 10+ with Python 3.9+ (from python.org, NOT Windows Store)
REM   pip install pyinstaller pywebview
REM
REM Usage:
REM   build\build_windows.bat
REM ═══════════════════════════════════════════════════════════════════════════════

setlocal EnableDelayedExpansion
set "SCRIPT_DIR=%~dp0"
set "PROJECT_ROOT=%SCRIPT_DIR%.."
set "DIST_DIR=%PROJECT_ROOT%\dist"
set "BUILD_CACHE=%PROJECT_ROOT%\build_cache"

echo.
echo   🚀  Freelance Dev OS ^— Windows Build
echo   ════════════════════════════════════
echo.

REM ── 1. Check Python ──────────────────────────────────────────────────────────
python --version >nul 2>&1
if errorlevel 1 (
    echo   [ERROR] Python not found. Install from https://python.org
    pause & exit /b 1
)
for /f "tokens=2" %%v in ('python --version 2^>^&1') do set PY_VER=%%v
echo   ^[OK^] Python %PY_VER%

REM ── 2. Activate virtual environment (if present) ─────────────────────────────
if exist "%PROJECT_ROOT%\venv\Scripts\activate.bat" (
    call "%PROJECT_ROOT%\venv\Scripts\activate.bat"
    echo   ^[OK^] Virtual environment activated
)

REM ── 3. Install dependencies ───────────────────────────────────────────────────
echo   Installing dependencies...
pip install -q -r "%PROJECT_ROOT%\requirements.txt"
pip install -q pyinstaller pywebview
echo   ^[OK^] Dependencies installed

REM ── 4. Clean previous builds ──────────────────────────────────────────────────
if exist "%DIST_DIR%"       rmdir /s /q "%DIST_DIR%"
if exist "%BUILD_CACHE%"    rmdir /s /q "%BUILD_CACHE%"
echo   ^[OK^] Cleaned previous build

REM ── 5. Run PyInstaller ────────────────────────────────────────────────────────
echo   Building with PyInstaller...
cd /d "%PROJECT_ROOT%"

pyinstaller ^
    --noconfirm ^
    --clean ^
    --distpath="%DIST_DIR%" ^
    --workpath="%BUILD_CACHE%" ^
    "%SCRIPT_DIR%FreelanceDevOS.spec"

if errorlevel 1 (
    echo   [ERROR] PyInstaller failed.
    pause & exit /b 1
)
echo   ^[OK^] PyInstaller complete

REM ── 6. Verify output ──────────────────────────────────────────────────────────
if exist "%DIST_DIR%\FreelanceDevOS\FreelanceDevOS.exe" (
    echo.
    echo   ✅  Build successful!
    echo       Executable: %DIST_DIR%\FreelanceDevOS\FreelanceDevOS.exe
    echo.
    echo   To distribute: zip the entire %DIST_DIR%\FreelanceDevOS\ folder
    echo.
) else (
    echo   [ERROR] Build failed — FreelanceDevOS.exe not found.
    pause & exit /b 1
)

REM ── 7. Optional: Create NSIS installer (if makensis is available) ─────────────
where makensis >nul 2>&1
if not errorlevel 1 (
    echo   Creating NSIS installer...
    if exist "%SCRIPT_DIR%installer.nsi" (
        makensis "%SCRIPT_DIR%installer.nsi"
        echo   ^[OK^] Installer created.
    )
)

pause
