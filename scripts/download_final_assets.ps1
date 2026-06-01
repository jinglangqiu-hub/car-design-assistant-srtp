param(
    [string]$HostName = "connect.westb.seetacloud.com",
    [int]$Port = 10940,
    [string]$RemoteRoot = "/root/autodl-tmp/car_srtp_project",
    [string]$LocalRoot = "D:\car_srtp_project"
)

$ErrorActionPreference = "Stop"

$outputDir = Join-Path $LocalRoot "outputs"
New-Item -ItemType Directory -Force $outputDir | Out-Null

scp -P $Port -r "root@${HostName}:$RemoteRoot/outputs/final_models" $outputDir
scp -P $Port -r "root@${HostName}:$RemoteRoot/outputs/final_samples" $outputDir
scp -P $Port -r "root@${HostName}:$RemoteRoot/outputs/logs" $outputDir

$appModels = Join-Path $LocalRoot "app\models"
New-Item -ItemType Directory -Force $appModels | Out-Null

Copy-Item (Join-Path $outputDir "final_models\sports.pkl") (Join-Path $appModels "sports.pkl") -Force
Copy-Item (Join-Path $outputDir "final_models\sedan.pkl") (Join-Path $appModels "sedan.pkl") -Force
Copy-Item (Join-Path $outputDir "final_models\suv.pkl") (Join-Path $appModels "suv.pkl") -Force

Write-Host "Downloaded final assets and copied models into app\models."

