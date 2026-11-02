@echo off
setlocal

set "PROJECT_ROOT=%~dp0"
if "%PROJECT_ROOT:~-1%"=="\" set "PROJECT_ROOT=%PROJECT_ROOT:~0,-1%"
if not defined PYTHON_EXE set "PYTHON_EXE=python"
"%PYTHON_EXE%" --version >nul 2>nul
if errorlevel 1 (
  echo [ERROR] Python not found. Activate your environment or set PYTHON_EXE.
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

