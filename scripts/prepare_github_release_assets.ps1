param(
    [string]$OutputDir = "release_assets"
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

$out = Join-Path $ProjectRoot $OutputDir
New-Item -ItemType Directory -Force $out | Out-Null

function Copy-RequiredFile {
    param(
        [string]$Source,
        [string]$DestinationDir
    )
    if (!(Test-Path $Source)) {
        throw "Missing required file: $Source"
    }
    New-Item -ItemType Directory -Force $DestinationDir | Out-Null
    Copy-Item -Force $Source $DestinationDir
}

function Copy-OptionalPattern {
    param(
        [string]$Pattern,
        [string]$DestinationDir
    )
    $files = Get-ChildItem $Pattern -File -ErrorAction SilentlyContinue
    if ($files) {
        New-Item -ItemType Directory -Force $DestinationDir | Out-Null
        foreach ($file in $files) {
            Copy-Item -Force $file.FullName $DestinationDir
        }
    }
}

function New-ZipFromDirectory {
    param(
        [string]$SourceDir,
        [string]$ZipPath
    )
    if (Test-Path $SourceDir) {
        if (Test-Path $ZipPath) {
            Remove-Item -Force $ZipPath
        }
        Compress-Archive -Path (Join-Path $SourceDir "*") -DestinationPath $ZipPath -CompressionLevel Optimal
    }
}

$installerDir = Join-Path $out "installer"
$modelsDir = Join-Path $out "models"
$datasetsDir = Join-Path $out "type_datasets"
$samplesDir = Join-Path $out "samples"

Copy-OptionalPattern "installer\CarDesignAssistant_Setup_v*.exe" $installerDir
Copy-OptionalPattern "installer\CarDesignAssistant_Setup_v*.bin" $installerDir

Copy-RequiredFile "app\models\sports.pkl" $modelsDir
Copy-RequiredFile "app\models\sedan.pkl" $modelsDir
Copy-RequiredFile "app\models\suv.pkl" $modelsDir
Copy-OptionalPattern "outputs\final_models\manifest.txt" $modelsDir

Copy-RequiredFile "data\type_datasets\compcars_sports_256_square.zip" $datasetsDir
Copy-RequiredFile "data\type_datasets\compcars_sedan_256_square.zip" $datasetsDir
Copy-RequiredFile "data\type_datasets\compcars_suv_256_square.zip" $datasetsDir
Copy-RequiredFile "data\type_datasets\srtp_type_mapping.json" $datasetsDir

New-Item -ItemType Directory -Force $samplesDir | Out-Null
New-ZipFromDirectory "outputs\final_samples" (Join-Path $samplesDir "final_samples.zip")
New-ZipFromDirectory "outputs\app_generated" (Join-Path $samplesDir "app_generated_samples.zip")

Write-Host ""
Write-Host "GitHub Release assets prepared:"
Get-ChildItem $out -Recurse -File | Select-Object FullName, @{Name="SizeMB";Expression={[math]::Round($_.Length / 1MB, 1)}} | Format-Table -AutoSize
