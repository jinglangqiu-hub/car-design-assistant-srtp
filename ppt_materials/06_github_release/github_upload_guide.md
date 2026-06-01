# GitHub Upload Guide

Date: 2026-06-01

## Repository Strategy

This repository stores source code, scripts, configuration, and documentation only.

Large artifacts are intentionally excluded from Git:

- `data/`
- `outputs/`
- `dist/`
- `installer/`
- `app/models/*.pkl`
- `*.zip`
- `*.pkl`
- `*.exe`
- `*.bin`

This avoids GitHub's large-file limits and keeps the repository maintainable.

## Included In Git

- Desktop application source: `app/car_design_assistant.py`
- Documentation: `README.md`, `docs/`
- Training and packaging scripts: `scripts/`
- Inno Setup configuration: `packaging/`
- Patched StyleGAN2-ADA runtime/training code: `refs/stylegan2-ada-pytorch/`
- Dataset preparation scripts: `experiments/`

## Excluded But Preserved Locally

- Final installer: `installer/CarDesignAssistant_Setup_v1.0.0.exe`
- Verified PyInstaller bundle: `dist/CarDesignAssistant/`
- Final models: `app/models/*.pkl`, `outputs/final_models/*.pkl`
- Raw and cleaned datasets: `data/`
- Generated images: `outputs/app_generated/`

## Recommended GitHub Release Assets

Because the installer is about 3.35 GB, it should not be uploaded as a single GitHub Release asset. If GitHub Release distribution is required, rebuild the installer with disk spanning enabled so every asset is below GitHub's per-file limit.

Alternative release assets:

- `sports.pkl`
- `sedan.pkl`
- `suv.pkl`
- `manifest.txt`

These model files are each about 270 MB and can be uploaded as separate release assets if needed.

## First Push Commands

Create an empty GitHub repository first, then run:

```powershell
cd D:\car_srtp_project
git remote add origin https://github.com/<your-user>/<your-repo>.git
git push -u origin main
```

If the remote already exists:

```powershell
git remote set-url origin https://github.com/<your-user>/<your-repo>.git
git push -u origin main
```

## Verification Before Push

```powershell
git status --short
git log --oneline -1
```

Make sure `data/`, `dist/`, `installer/`, `outputs/`, and `.pkl` files are not staged.
