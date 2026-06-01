@echo off
setlocal enableextensions enabledelayedexpansion

set "PROJECT_ROOT=%~dp0"
if "%PROJECT_ROOT:~-1%"=="\" set "PROJECT_ROOT=%PROJECT_ROOT:~0,-1%"
set "TARGET_ENV=car_srtp_clean"
set "CONDA_BAT=D:\anaconda\condabin\conda.bat"
set "NO_SHELL=0"
if /I "%~1"=="--no-shell" set "NO_SHELL=1"

set "VSDEVCMD="
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
  echo Install Visual Studio Build Tools C++ workload first.
  exit /b 1
)

if not exist "%CONDA_BAT%" (
  echo [ERROR] conda.bat not found at:
  echo         %CONDA_BAT%
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
  echo [ERROR] cl.exe is not available. VS C++ toolchain is not ready.
  exit /b 1
)

where python >nul 2>nul
if errorlevel 1 (
  echo [ERROR] python is not available after conda activation.
  exit /b 1
)

echo [INFO] Environment check:
python -c "import sys,importlib.util as u;print('python =',sys.executable);print('version =',sys.version.split()[0]);print('torch =', bool(u.find_spec('torch')))"
python -c "import torch;print('torch_version =',torch.__version__);print('cuda_runtime =',torch.version.cuda);print('cuda_available =',torch.cuda.is_available());print('gpu =', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'None')"
if errorlevel 1 (
  echo [ERROR] Torch/CUDA probe failed in env %TARGET_ENV%.
  exit /b 1
)

cd /d "%PROJECT_ROOT%\refs\stylegan2-ada-pytorch"
echo [READY] Current dir: %cd%
echo [READY] You can now run training commands safely.
echo.
if "%NO_SHELL%"=="1" exit /b 0
cmd /k
