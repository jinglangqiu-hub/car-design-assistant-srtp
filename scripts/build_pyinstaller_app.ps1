param(
    [string]$PythonExe = "D:\anaconda\envs\car_srtp_clean\python.exe",
    [switch]$InstallPyInstaller
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

if (!(Test-Path $PythonExe)) {
    throw "Python not found: $PythonExe"
}

& $PythonExe -c "import torch, numpy, PIL; print('Python env OK')"

$hasPyInstallerText = & $PythonExe -c "import importlib.util; print('YES' if importlib.util.find_spec('PyInstaller') else 'NO')"
$hasPyInstaller = ($hasPyInstallerText.Trim() -eq "YES")

if (!$hasPyInstaller) {
    if ($InstallPyInstaller) {
        & $PythonExe -m pip install pyinstaller
        if ($LASTEXITCODE -ne 0) {
            throw "Failed to install PyInstaller."
        }
    } else {
        throw "PyInstaller is not installed. Run: $PSCommandPath -InstallPyInstaller"
    }
}

& $PythonExe -m PyInstaller --version | Out-Host
if ($LASTEXITCODE -ne 0) {
    throw "PyInstaller is still unavailable after installation."
}

$requiredModels = @(
    "app\models\sports.pkl",
    "app\models\sedan.pkl",
    "app\models\suv.pkl"
)

foreach ($model in $requiredModels) {
    if (!(Test-Path $model)) {
        throw "Missing model file: $model. Run scripts\download_final_assets.ps1 first."
    }
}

Remove-Item -Recurse -Force build, dist -ErrorAction SilentlyContinue

& $PythonExe -m PyInstaller `
    --noconfirm `
    --clean `
    --windowed `
    --onedir `
    --name CarDesignAssistant `
    --hidden-import legacy `
    --hidden-import click `
    --hidden-import dnnlib `
    --hidden-import dnnlib.util `
    --hidden-import torch_utils `
    --hidden-import torch_utils.persistence `
    --hidden-import torch_utils.misc `
    --hidden-import torch_utils.custom_ops `
    --hidden-import training `
    --hidden-import training.networks `
    --hidden-import training.dataset `
    --collect-all torch `
    --collect-all numpy `
    --collect-all PIL `
    --collect-all click `
    --collect-all requests `
    --collect-all tqdm `
    --collect-all scipy `
    --collect-all psutil `
    --collect-all pyspng `
    --collect-all imageio `
    --collect-all imageio_ffmpeg `
    --add-data "refs\stylegan2-ada-pytorch;refs\stylegan2-ada-pytorch" `
    --add-data "app\models;app\models" `
    app\car_design_assistant.py

if ($LASTEXITCODE -ne 0) {
    throw "PyInstaller build failed."
}

if (!(Test-Path "dist\CarDesignAssistant\CarDesignAssistant.exe")) {
    throw "PyInstaller finished but exe was not found: dist\CarDesignAssistant\CarDesignAssistant.exe"
}

$distModelDir = "dist\CarDesignAssistant\app\models"
New-Item -ItemType Directory -Force $distModelDir | Out-Null
Copy-Item -Force "app\models\sports.pkl" $distModelDir
Copy-Item -Force "app\models\sedan.pkl" $distModelDir
Copy-Item -Force "app\models\suv.pkl" $distModelDir

Write-Host ""
Write-Host "PyInstaller build finished:"
Write-Host "  $ProjectRoot\dist\CarDesignAssistant\CarDesignAssistant.exe"
Write-Host "  Models copied to: $ProjectRoot\$distModelDir"
Write-Host ""
Write-Host "Next: run scripts\build_inno_installer.ps1"
