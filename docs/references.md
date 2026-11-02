# Sources, provenance, and bibliography

[English overview](../README.md) · [中文说明](../README.zh-CN.md) · [License inventory](../THIRD_PARTY_NOTICES.md) · [BibTeX](../references.bib)

## Project context

This repository records participation in **Chongqing University's Student Research Training Program (SRTP)** through “基于生成对抗网络的汽车造型设计辅助系统的开发”. The project completed its final defense and was concluded at Chongqing University in **July 2026**. SRTP participation and the completion date describe the student project; they are separate from the June 2026 software release and the dates of the upstream publications.

本项目属于重庆大学大学生科研训练计划（SRTP），已于 2026 年 7 月完成答辩并结题。下表区分项目自身的实践工作、直接采用的第三方实现和仅保留的参考代码，避免将上游研究贡献归为本项目成果。

## Source map

| Material | Upstream or project record | Role in this project |
|---|---|---|
| `refs/stylegan2-ada-pytorch/` | [NVlabs/stylegan2-ada-pytorch](https://github.com/NVlabs/stylegan2-ada-pytorch) | Main training/generation implementation; contains local compatibility edits and backup copies |
| StyleGAN2 architecture | [StyleGAN2 paper](https://arxiv.org/abs/1912.04958) and [official repository](https://github.com/NVlabs/stylegan2) | Architecture underlying StyleGAN2-ADA; not an independently developed architecture here |
| CompCars images and annotations | [Official dataset](https://mmlab.ie.cuhk.edu.hk/datasets/comp_cars/) | Vehicle images, bounding boxes, viewpoint labels, and attributes used in preprocessing |
| `refs/sefa/` | [genforce/sefa](https://github.com/genforce/sefa) | Historical reference implementation; not imported by the final Tkinter inference application |
| SeFa `models/` implementations and model-zoo URLs | SeFa source and its references to [GenForce](https://github.com/genforce/genforce), PGGAN, StyleGAN, and StyleGAN2 | Part of the reference tree; neither the URLs nor listed pretrained models establish the provenance of this project's baseline |
| SeFa `SessionState.py` | [tvst's SessionState Gist](https://gist.github.com/tvst/036da038ab3e999a64497f42de966a92), explicitly credited in the file header | Legacy Streamlit helper in the reference tree; no separate license text is present in that local file |
| SeFa CSS assets | Bootstrap 3.2.0 with normalize.css 3.0.1; Lato font stylesheet | Reference visualization assets; individual notices are recorded in the [license inventory](../THIRD_PARTY_NOTICES.md) |
| `app/`, `experiments/`, `scripts/`, `configs/`, `packaging/` | Project-specific, AI-assisted development | Data adaptation, experiment orchestration, desktop integration, and packaging; any upstream-derived content remains under its applicable terms |
| Reports, slides, gallery, and training manifest | [Document index](README.md), [defense archive](../ppt_materials/README.md), [gallery provenance](../assets/README.md) | Historical project evidence; not peer-reviewed publications or newly generated experimental results |

The original vendoring commits for StyleGAN2-ADA and SeFa were not recorded. The local trees should not be described as an unchanged copy of a particular upstream release. Existing copyright headers and license files remain intact. Upstream links identify origin, not a reconstructed exact revision.

## Model and data lineage

The category scripts load the local checkpoint `outputs/stylegan2ada_runs/baseline_240/network-snapshot-000240.pkl`, produce category checkpoints, and then initialize additional training from those weights. The [training manifest](../ppt_materials/03_training_records/manifest.txt) documents the later stages. The baseline itself, its original download/source record, and its complete training lineage are not included. Consequently, this documentation does not identify an official NVIDIA pretrained weight as the baseline without evidence.

The category names use the [project mapping](../configs/srtp_type_mapping.json). Counts describe the archived processed datasets, not a new verification of the original CompCars release. Three processed dataset ZIPs were removed from public release assets on November 2, 2026. Historical reports may contain third-party illustrations or dataset-derived montages; those embedded materials do not receive a new reuse license from this repository.

The two gallery images retain their original generation parameters. The records do not contain a checkpoint hash, so the exact weight that produced each image cannot be independently identified from the CSV alone.

## Bibliography

### 1. StyleGAN2-ADA — method and implementation used

Tero Karras, Miika Aittala, Janne Hellsten, Samuli Laine, Jaakko Lehtinen, and Timo Aila. **Training Generative Adversarial Networks with Limited Data.** Advances in Neural Information Processing Systems 33, 2020.

[Proceedings](https://papers.nips.cc/paper/2020/hash/8d30aa96e72440759f74bd2306c1fa3d-Abstract.html) · [arXiv](https://arxiv.org/abs/2006.06676) · [Official PyTorch code](https://github.com/NVlabs/stylegan2-ada-pytorch) · [Included license](../refs/stylegan2-ada-pytorch/LICENSE.txt)

### 2. StyleGAN2 — underlying architecture

Tero Karras, Samuli Laine, Miika Aittala, Janne Hellsten, Jaakko Lehtinen, and Timo Aila. **Analyzing and Improving the Image Quality of StyleGAN.** Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, 2020.

[Paper](https://arxiv.org/abs/1912.04958) · [Official repository](https://github.com/NVlabs/stylegan2)

### 3. CompCars — dataset used

Linjie Yang, Ping Luo, Chen Change Loy, and Xiaoou Tang. **A Large-Scale Car Dataset for Fine-Grained Categorization and Verification.** Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition, 2015.

[Official dataset and citation](https://mmlab.ie.cuhk.edu.hk/datasets/comp_cars/) · [Extended arXiv version](https://arxiv.org/abs/1506.08959) · [Dataset agreement](https://mmlab.ie.cuhk.edu.hk/datasets/comp_cars/agreement.pdf)

### 4. SeFa — retained reference

Yujun Shen and Bolei Zhou. **Closed-Form Factorization of Latent Semantics in GANs.** Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, 2021.

[Paper](https://arxiv.org/abs/2007.06600) · [Project](https://genforce.github.io/sefa/) · [Official code](https://github.com/genforce/sefa) · [Included license](../refs/sefa/LICENSE)

These references credit the upstream research. Citing a paper does not transfer code, dataset, font, or model redistribution rights; consult the corresponding license or agreement separately.
