# Experiment record

[Overview](../README.md) · [Run guide](reproduction.md)

This record is reconstructed from committed scripts and archives, not a new evaluation.

## Data preparation

The [initial preparation script](../experiments/prepare_compcars_v1.py) selects viewpoint label `4` (front-side in the project), reads bounding boxes, rejects invalid/small crops (minimum 128 pixels per dimension), and flattens filenames to `make_id__model_id__year__image_id.jpg`. The [square conversion script](../experiments/prepare_compcars_v2_inplace.py) adds a light background with 6% padding and resizes to 256 × 256. It overwrites inputs: use a private working copy and update its hard-coded paths.

The [dataset builder](../scripts/build_type_dataset_zips.py) reads model attributes and groups cleaned images. The recorded mapping is included at [`configs/srtp_type_mapping.json`](../configs/srtp_type_mapping.json):

| Raw type token | Project category |
|---|---|
| `2`, `10` | `suv` |
| `4` | `sedan` |
| `9`, `11`, `12` | `sports` |

This is the project's historical grouping, not a claim that every merged label strictly matches its display name. Inspect your authorized copy's conventions. The builder's default mapping differs, so pass this mapping explicitly.

The [archived summary](../ppt_materials/04_dataset_and_model_info/dataset_summary.md) records 1,519 sports, 5,492 sedan, and 9,889 SUV images. No fresh recount or dataset hash validation was performed in this cleanup. Keep CompCars images and processed datasets private; see [data notices](../THIRD_PARTY_NOTICES.md).

## Training

Category scripts use one GPU, `--cfg=auto`, mirrored images, ADA, batch 16, four workers, snapshot interval 10, and `--metrics=none`.

| Category | Initial category stage | Continued stage | Recorded snapshots |
|---|---:|---:|---|
| sports | 800 kimg | 1,000 kimg | `000800`, then `001000` |
| sedan | 1,000 kimg | 1,500 kimg | `001000`, then `001500` |
| suv | 1,000 kimg | 1,500 kimg | `001000`, then `001500` |

The [manifest](../ppt_materials/03_training_records/manifest.txt) records May 30–31, 2026 runs and copied final weights. Initial category training loads shared `baseline_240/network-snapshot-000240.pkl`; continuation loads each category's previous weight. The continuation script does not restore full optimizer/RNG state, and snapshot numbers restart in the new run. Do not interpret filenames as cumulative exposure or bitwise continuation.

The first driver samples seeds 0–31 at truncation 0.7; continuation records seeds 0–47 at 0.65. These sample folders are absent from the current tree/sample ZIP. The two archived desktop images instead use seeds 796724 and 437112 at 0.65.

## Historical environment

| Component | Recorded configuration |
|---|---|
| OS | Ubuntu 22.04 |
| GPU | NVIDIA GeForce RTX 5090, 32 GB |
| Python | 3.12.3 |
| PyTorch | 2.7.0+cu128 |
| PyTorch CUDA runtime | 12.8 |
| Driver | 580.105.08 |

Source: [cloud log](cloud_env_config.md). The driver's maximum CUDA version differs from PyTorch's runtime version. Local desktop records refer to Python 3.10 without a full dependency inventory. Vendored StyleGAN contains local compatibility edits; its exact upstream commit is not recorded. These omissions limit exact reproduction.

## Evidence and gaps

The archive records category counts, trained snapshots, continuation stages, application code, and packaging scripts. v1.0.0 contains weights and a split installer; two desktop images have seed/truncation metadata.

There is no verified FID/KID table, same-seed before/after comparison, repeated-run result, ablation, runtime benchmark, or memorization analysis. `cloud_train_800.sh` requests `fid50k_full`, but this option is not evidence of a measured result. No quality gain is inferred solely from more training or selected images.
