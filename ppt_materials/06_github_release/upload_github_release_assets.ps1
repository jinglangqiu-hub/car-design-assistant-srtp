param(
    [string]$Repo = "jinglangqiu-hub/car-design-assistant-srtp",
    [string]$Tag = "v1.0.0",
    [string]$AssetsRoot = "release_assets",
    [string]$Proxy = "http://127.0.0.1:10809",
    [int]$MaxRetries = 3
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

if (!(Test-Path $AssetsRoot)) {
    throw "Assets directory not found: $AssetsRoot"
}

if (![string]::IsNullOrWhiteSpace($Proxy)) {
    $env:HTTP_PROXY = $Proxy
    $env:HTTPS_PROXY = $Proxy
}

function Get-ReleaseAssets {
    $json = gh release view $Tag --repo $Repo --json assets
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to query release assets."
    }
    return ($json | ConvertFrom-Json).assets
}

function Upload-OneAsset {
    param(
        [System.IO.FileInfo]$File
    )

    $assetName = $File.Name
    for ($attempt = 1; $attempt -le $MaxRetries; $attempt++) {
        $assets = Get-ReleaseAssets
        $existing = $assets | Where-Object { $_.name -eq $assetName } | Select-Object -First 1

        if ($existing -and [int64]$existing.size -eq [int64]$File.Length -and $existing.state -eq "uploaded") {
            Write-Host "SKIP  $assetName already uploaded ($([math]::Round($File.Length / 1MB, 1)) MB)"
            return
        }

        if ($existing) {
            Write-Host "DELETE existing incomplete/different asset: $assetName"
            gh release delete-asset $Tag $assetName --repo $Repo --yes
            if ($LASTEXITCODE -ne 0) {
                throw "Failed to delete existing asset: $assetName"
            }
        }

        Write-Host "UPLOAD attempt $attempt/$MaxRetries : $assetName ($([math]::Round($File.Length / 1MB, 1)) MB)"
        gh release upload $Tag $File.FullName --repo $Repo
        if ($LASTEXITCODE -eq 0) {
            Write-Host "DONE  $assetName"
            return
        }

        Write-Host "WARN  upload failed for $assetName"
        if ($attempt -lt $MaxRetries) {
            Start-Sleep -Seconds (10 * $attempt)
        }
    }

    throw "Failed to upload after $MaxRetries attempts: $assetName"
}

$files = Get-ChildItem $AssetsRoot -Recurse -File | Sort-Object Length, Name
Write-Host "Release upload target: $Repo $Tag"
Write-Host "Proxy: $Proxy"
Write-Host "Files: $($files.Count)"

foreach ($file in $files) {
    Upload-OneAsset $file
}

Write-Host ""
Write-Host "Final release assets:"
Get-ReleaseAssets | Sort-Object name | Select-Object name, state, size | Format-Table -AutoSize
