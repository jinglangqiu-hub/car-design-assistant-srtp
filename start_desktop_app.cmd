@echo off
setlocal

set "PROJECT_ROOT=%~dp0"
if "%PROJECT_ROOT:~-1%"=="\" set "PROJECT_ROOT=%PROJECT_ROOT:~0,-1%"
set "PYTHON_EXE=D:\anaconda\envs\car_srtp_clean\python.exe"

if not exist "%PYTHON_EXE%" (
  echo [ERROR] Python not found: %PYTHON_EXE%
  echo Please check the conda environment path.
  pause
  exit /b 1
)

cd /d "%PROJECT_ROOT%"
"%PYTHON_EXE%" app\car_design_assistant.py

if errorlevel 1 (
  echo.
  echo [ERROR] Desktop app exited with an error.
  pause
)

