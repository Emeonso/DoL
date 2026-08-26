@echo off
setlocal
cd /d "%~dp0.."

echo [1/3] Universal source preflight
python devTools\source_preflight.py
if errorlevel 1 goto :failed

echo [2/3] Twee structure check
python devTools\twee_structure_check.py game
if errorlevel 1 echo Existing structure warnings were reported; continuing because this checkout has a known baseline.

echo [3/3] Macro checks
python devTools\macro_check.py game

echo Compile
call compile.bat
if errorlevel 1 goto :failed

echo Validation and compile completed.
exit /b 0

:failed
echo Universal source preflight failed. No compile was run.
exit /b 1
