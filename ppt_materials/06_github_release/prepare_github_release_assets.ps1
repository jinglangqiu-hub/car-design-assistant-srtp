# Compatibility entry point. Maintained logic lives in scripts/.
$ProjectRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
& (Join-Path $ProjectRoot "scripts\prepare_github_release_assets.ps1") @args
