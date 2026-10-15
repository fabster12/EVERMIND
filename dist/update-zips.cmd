@echo off
rem ===================================================================
rem  EverMind - rebuild the two share zips in this folder.
rem
rem  Double-click it, or run it from a terminal. Safe to re-run: every
rem  step overwrites its own output.
rem
rem    update-zips.cmd           full rebuild, then package  (default)
rem    update-zips.cmd quick     package only - skips documents
rem    update-zips.cmd docs      rebuild documents, no PDF conversion
rem
rem  Full rebuild needs Microsoft Word (it drives Word to make the PDFs).
rem  Use "quick" when only the specs, fixtures or readmes changed.
rem ===================================================================

setlocal
cd /d "%~dp0.."

set MODE=%~1
if "%MODE%"=="" set MODE=full

echo.
echo   EverMind - updating share packages
echo   mode: %MODE%
echo   ----------------------------------------------------------------

rem --- is python there at all? ------------------------------------------
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo   ERROR: python is not on PATH.
    echo   Install Python 3.11+ and run:  pip install python-docx pillow
    goto :failed
)

if /i "%MODE%"=="quick" goto :package

rem --- is a generated .docx open in Word? -------------------------------
rem  Word holds a lock and leaves a ~$ file behind. The build would fail
rem  halfway with a PermissionError, so say so now instead.
dir /b /s "docs\~$*.docx" >nul 2>&1
if not errorlevel 1 (
    echo.
    echo   ERROR: a document under docs\ is open in Word.
    echo   Close Word and run this again, or use:  update-zips.cmd quick
    goto :failed
)

rem --- regenerate everything --------------------------------------------
echo.
echo   [1/6] demonstration data  ^(src\fixtures^)
python tools\build_fixtures.py >nul
if errorlevel 1 goto :buildfailed

echo   [2/6] architecture diagram
python tools\build_diagram.py >nul
if errorlevel 1 goto :buildfailed

echo   [3/6] design document     ^(7 pages^)
python tools\build_design_evermind.py >nul
if errorlevel 1 goto :buildfailed

echo   [4/6] instructor summary  ^(3 pages^)
python tools\build_summary_group1.py >nul
if errorlevel 1 goto :buildfailed

echo   [5/6] proposal review     ^(2 pages^)
python tools\build_review_benchmark.py >nul
if errorlevel 1 goto :buildfailed

if /i "%MODE%"=="docs" (
    echo   [6/6] skipped - no PDF conversion in "docs" mode
    goto :package
)

echo   [6/6] converting to PDF   ^(drives Microsoft Word^)
powershell -NoProfile -ExecutionPolicy Bypass -File tools\packaging\to_pdf.ps1 >nul
if errorlevel 1 (
    echo.
    echo   ERROR: PDF conversion failed. Usually Word was already running
    echo   with one of the files open. Close Word and try again.
    goto :failed
)

:package
echo.
echo   packaging...
echo.
python tools\packaging\build_packages.py
if errorlevel 1 (
    echo.
    echo   ERROR: packaging reported a problem - read the lines above.
    echo   A "possible secret" line means something was about to be
    echo   shared that should not be. Do not send the zips until it is
    echo   resolved.
    goto :failed
)

rem --- tidy the .docx back out of the tree ------------------------------
rem  They are build artifacts. The .pdf and .md are the readable copies,
rem  and the zips already carry what they need.
del /q "docs\gate1\*.docx"   >nul 2>&1
del /q "docs\reviews\*.docx" >nul 2>&1

echo.
echo   ----------------------------------------------------------------
echo   Done. Both zips in this folder are up to date:
echo.
for %%F in ("%~dp0*.zip") do echo     %%~nxF   %%~zF bytes
echo.
echo   Docs zip  - for colleagues and reviewers. Nothing to run.
echo   Tech zip  - fixtures, build scripts and specs, for the code.
echo.
goto :done

:buildfailed
echo.
echo   ERROR: a build step failed. Re-run the step by hand to see why:
echo       python tools\build_fixtures.py
echo   If it says "No module named docx" or "No module named PIL":
echo       pip install python-docx pillow

:failed
echo.
echo   Nothing was shipped. The existing zips are untouched.
echo.
if "%CI%"=="" pause
exit /b 1

:done
if "%CI%"=="" pause
exit /b 0
