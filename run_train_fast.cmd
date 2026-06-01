@echo off
setlocal enableextensions enabledelayedexpansion

set "PROJECT_ROOT=%~dp0"
if "%PROJECT_ROOT:~-1%"=="\" set "PROJECT_ROOT=%PROJECT_ROOT:~0,-1%"
set "CONDA_BAT=D:\anaconda\condabin\conda.bat"
set "TARGET_ENV=car_srtp_clean"
set "VSDEVCMD="

if "%~1"=="" (
  echo Usage:
  echo   run_train_fast.cmd --outdir=... --data=... [extra train.py args]
  echo Example:
  echo   run_train_fast.cmd --outdir=D:\car_srtp_project\outputs\stylegan2ada_runs --data=D:\car_srtp_project\data\compcars_cleaned_v1_256_square.zip --kimg=500 --mirror=1
  exit /b 1
)

for %%F in (
  "C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\Common7\Tools\VsDevCmd.bat"
  "C:\Program Files\Microsoft Visual Studio\2022\BuildTools\Common7\Tools\VsDevCmd.bat"
  "C:\Program Files (x86)\Microsoft Visual Studio\2022\Community\Common7\Tools\VsDevCmd.bat"
  "C:\Program Files\Microsoft Visual Studio\2022\Community\Common7\Tools\VsDevCmd.bat"
  "C:\Program Files (x86)\Microsoft Visual Studio\18\BuildTools\Common7\Tools\VsDevCmd.bat"
) do (
  if exist %%~F (
    set "VSDEVCMD=%%~F"
    goto :found_vsdevcmd
  )
)

:found_vsdevcmd
if not defined VSDEVCMD (
  echo [ERROR] VsDevCmd.bat not found.
  exit /b 1
)
if not exist "%CONDA_BAT%" (
  echo [ERROR] conda.bat not found: %CONDA_BAT%
  exit /b 1
)

echo [INFO] Initializing Visual Studio x64 build environment...
call "%VSDEVCMD%" -arch=x64 -host_arch=x64 >nul
if errorlevel 1 (
  echo [ERROR] Failed to initialize VsDevCmd.
  exit /b 1
)

echo [INFO] Activating conda env: %TARGET_ENV%
call "%CONDA_BAT%" activate "%TARGET_ENV%"
if errorlevel 1 (
  echo [ERROR] Failed to activate conda env: %TARGET_ENV%
  exit /b 1
)

where cl >nul 2>nul
if errorlevel 1 (
  echo [ERROR] cl.exe is missing after VsDevCmd initialization.
  exit /b 1
)

where nvcc >nul 2>nul
if errorlevel 1 (
  echo [WARN] nvcc not found in PATH. CUDA plugins may fall back to slow reference ops.
)

if not exist "%PROJECT_ROOT%\.cache" mkdir "%PROJECT_ROOT%\.cache" >nul 2>nul
if not exist "%PROJECT_ROOT%\.cache\torch_extensions" mkdir "%PROJECT_ROOT%\.cache\torch_extensions" >nul 2>nul
if not exist "%PROJECT_ROOT%\.cache\dnnlib" mkdir "%PROJECT_ROOT%\.cache\dnnlib" >nul 2>nul
set "TORCH_EXTENSIONS_DIR=%PROJECT_ROOT%\.cache\torch_extensions"
set "DNNLIB_CACHE_DIR=%PROJECT_ROOT%\.cache\dnnlib"

echo [INFO] Fast profile enabled: --allow-tf32=1 --aug=ada --batch=16 --workers=3 --metrics=none

cd /d "%PROJECT_ROOT%\refs\stylegan2-ada-pytorch"

python train.py --allow-tf32=1 --aug=ada --batch=16 --workers=3 --metrics=none %*
