# Project Cleanup Report

Date: 2026-06-01

## Cleanup Goal

After the desktop program and Inno Setup installer were verified, the project was cleaned to remove clearly redundant intermediate artifacts while preserving final deliverables and reproducibility assets.

## Removed

- `build/`
  - PyInstaller temporary build cache.
- `cloud_upload/`
  - Temporary cloud migration upload package. The source assets remain in the project and the cloud scripts are kept.
- `.cache/`
  - Local cache directory.
- `CarDesignAssistant.spec`
  - Auto-generated PyInstaller spec file. The project now uses `scripts/build_pyinstaller_app.ps1` as the canonical build entry.
- `outputs/stylegan2ada_runs/`
  - Local/intermediate StyleGAN2-ADA training runs. Final trained models are preserved in `outputs/final_models/` and `app/models/`.
- `__pycache__/`
  - Python bytecode cache directories across the project.

## Preserved

- `installer/CarDesignAssistant_Setup_v1.0.0.exe`
  - Final verified Windows installer.
- `dist/CarDesignAssistant/`
  - Verified PyInstaller app bundle, useful for direct testing and future installer rebuilds.
- `app/car_design_assistant.py`
  - Desktop application source code.
- `app/models/`
  - Runtime model files used by the desktop program.
- `outputs/final_models/`
  - Final cloud-trained model records.
- `outputs/app_generated/`
  - Desktop application generated samples and metadata.
- `data/`
  - Raw, cleaned, and type-specific datasets for reproducibility and paper evidence.
- `refs/stylegan2-ada-pytorch/`
  - Patched StyleGAN2-ADA code required by training and app runtime.
- `scripts/`
  - Dataset construction, cloud training, final asset download, PyInstaller, and Inno Setup scripts.
- `docs/`
  - Cloud environment records, acceptance checklist, paper outline, and slide outline.

## Size After Cleanup

Approximate remaining major directories:

- `data/`: 43.38 GB
- `dist/`: 6.17 GB
- `installer/`: 3.35 GB
- `outputs/`: 0.79 GB
- `app/`: 0.79 GB
- `refs/`: 0.05 GB

The remaining large files are mainly reproducibility datasets, the verified installer, the verified PyInstaller bundle, and final model files.
