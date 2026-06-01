param(
    [string]$InnoCompiler = ""
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

if (!(Test-Path "dist\CarDesignAssistant\CarDesignAssistant.exe")) {
    throw "Missing PyInstaller output. Run scripts\build_pyinstaller_app.ps1 first."
}

foreach ($model in @("app\models\sports.pkl", "app\models\sedan.pkl", "app\models\suv.pkl")) {
    if (!(Test-Path $model)) {
        throw "Missing model file: $model"
    }
}

if ([string]::IsNullOrWhiteSpace($InnoCompiler)) {
    $pathCommand = Get-Command ISCC.exe -ErrorAction SilentlyContinue
    if ($pathCommand) {
        $InnoCompiler = $pathCommand.Source
    }
}

if ([string]::IsNullOrWhiteSpace($InnoCompiler)) {
    $registryCandidates = @(
        "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Inno Setup 6_is1",
        "HKLM:\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\Inno Setup 6_is1",
        "HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Inno Setup 6_is1"
    )
    foreach ($registryPath in $registryCandidates) {
        if (Test-Path $registryPath) {
            $installLocation = (Get-ItemProperty $registryPath).InstallLocation
            if ($installLocation) {
                $candidate = Join-Path $installLocation "ISCC.exe"
                if (Test-Path $candidate) {
                    $InnoCompiler = $candidate
                    break
                }
            }
        }
    }
}

if ([string]::IsNullOrWhiteSpace($InnoCompiler)) {
    $candidates = @(
        "C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
        "C:\Program Files\Inno Setup 6\ISCC.exe",
        "$env:LOCALAPPDATA\Programs\Inno Setup 6\ISCC.exe",
        "C:\Program Files (x86)\Inno Setup 5\ISCC.exe",
        "C:\Program Files\Inno Setup 5\ISCC.exe"
    )
    foreach ($candidate in $candidates) {
        if (Test-Path $candidate) {
            $InnoCompiler = $candidate
            break
        }
    }
}

if ([string]::IsNullOrWhiteSpace($InnoCompiler) -or !(Test-Path $InnoCompiler)) {
    throw "ISCC.exe not found. Install Inno Setup 6 or pass -InnoCompiler 'path\to\ISCC.exe'."
}

New-Item -ItemType Directory -Force installer | Out-Null
& $InnoCompiler "packaging\CarDesignAssistant.iss"
if ($LASTEXITCODE -ne 0) {
    throw "Inno Setup compiler failed."
}

Write-Host ""
Write-Host "Installer build finished. Check:"
Write-Host "  $ProjectRoot\installer"
