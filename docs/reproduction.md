# Run & reproduction guide

[Overview](../README.md) · [Experiment record](experiments.md)

Weights, CompCars data, build outputs, and the shared baseline are not tracked in Git. Historical environment records are incomplete; this guide does not guarantee exact reproduction on every machine.

## Windows application from source

Clone the repository and open a terminal at its root. Create and activate a Python environment. Local project records used Python 3.10; the separately recorded cloud environment used Python 3.12.3/PyTorch 2.7.0+cu128. Select a PyTorch build compatible with your GPU and driver. No validated full version lockfile exists; `requirements_app.txt` lists unpinned dependencies.

```powershell
python -m pip install -r requirements_app.txt
python -m tkinter
python -c "import torch, numpy, PIL; print(torch.__version__); print('CUDA:', torch.cuda.is_available())"
```

Tkinter is part of typical Windows Python installs, not a pip dependency. GPU execution may compile StyleGAN custom extensions and need a compatible CUDA toolkit, compiler, and build tools. The app selects CUDA if available, otherwise CPU; CPU execution can be slow and was not revalidated in this cleanup.

Obtain the trusted project weights separately (historically attached to [v1.0.0](https://github.com/jinglangqiu-hub/car-design-assistant-srtp/releases/tag/v1.0.0)):

| Vehicle | Required location |
|---|---|
| Sports | `app/models/sports.pkl` |
| Sedan | `app/models/sedan.pkl` |
| SUV | `app/models/suv.pkl` |

Only load trusted `.pkl` files: pickle deserialization can execute code. Public availability does not establish unrestricted model redistribution or commercial-use rights; see [permissions](../THIRD_PARTY_NOTICES.md).

```powershell
python app\car_design_assistant.py
```

Alternatively, `start_desktop_app.cmd` uses `PYTHON_EXE` if set, otherwise the active `python` on PATH. Keep the vendored `refs/stylegan2-ada-pytorch/` directory, which supplies `legacy.py` and the runtime.

Choose a vehicle, seed, and truncation, then generate. Images go to `outputs/app_generated/<type>/`; metadata is appended to `outputs/app_generated/metadata.csv`. Use a writable project/install directory. Same seed/settings control sampling, but exact pixels can vary by environment.

The current source contains readable UTF-8 Chinese strings. The former README's blanket encoding-corruption claim was removed; Windows font rendering and live generation were not tested in this cleanup.

## Existing installer

Download all four v1.0.0 files into the **same folder**, then run the `.exe`:

- `CarDesignAssistant_Setup_v1.0.0.exe`
- `CarDesignAssistant_Setup_v1.0.0-1.bin`
- `CarDesignAssistant_Setup_v1.0.0-2.bin`
- `CarDesignAssistant_Setup_v1.0.0-3.bin`

GitHub displays these as a flat asset list, not an `installer/` directory. The historical installer was not rebuilt or smoke-tested here.

## Reconstructing data preparation

Obtain CompCars through its [official process and agreement](https://mmlab.ie.cuhk.edu.hk/datasets/comp_cars/). Do not download/republish public copies of the project's processed training ZIPs. Keep training images private.

The historical scripts in `experiments/` contain absolute paths. Update `ROOT`, `OUT_DIR`, and `SRC_DIR` for your working copy. Run v1 filtering/cropping before v2 square conversion. The v2 script overwrites images: use a working copy, not original data. See [preprocessing details](experiments.md).

Inspect grouping before writing ZIPs:

```powershell
python scripts\build_type_dataset_zips.py --cleaned-dir data\compcars_cleaned_v1\all --attributes data\raw_compcars\misc\attributes.txt --mapping-json configs\srtp_type_mapping.json --dry-run
```

If conventions/counts are correct, repeat without `--dry-run`. The builder only groups existing images; it does not crop/resize. Historical counts are 1,519 / 5,492 / 9,889; no dataset hashes are available for exact verification.

## Training prerequisites

Category training requires the three private ZIPs in `data/type_datasets/`, a compatible GPU environment, and the original shared `outputs/stylegan2ada_runs/baseline_240/network-snapshot-000240.pkl`. That baseline is absent from the current tree and v1.0.0 release; exact historical training is blocked without it or a documented replacement initialization.

On Linux, after meeting these prerequisites:

```bash
chmod +x scripts/*.sh
export PROJECT_ROOT="$PWD"
bash scripts/cloud_train_all_type_models.sh 800 1000 1000 16
bash scripts/cloud_continue_all_type_models.sh 1000 1500 1500 16
```

The driver invokes child scripts directly, hence executable permissions are required. These commands start expensive training and copy/overwrite weights and manifests: use a separate experiment checkout and archive prior outputs. They were not executed here and do not compute category FID/KID.

## Building & publishing

With weights and a compatible Windows environment:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\build_pyinstaller_app.ps1 -PythonExe "C:\path\to\your\python.exe" -InstallPyInstaller
powershell -ExecutionPolicy Bypass -File scripts\build_inno_installer.ps1
```

Install Inno Setup 6 or pass `-InnoCompiler` with its compiler path. These Windows-specific build scripts still require local validation.

`prepare_github_release_assets.ps1` stages installers, models, samples, and metadata, **not training image datasets**. `upload_github_release_assets.ps1` uses a filename allowlist and rejects training ZIPs, including stale copies in staging. Review permissions for model/binary distribution separately. Script entry points under `ppt_materials/` delegate to maintained scripts.
