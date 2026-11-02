# Car Design Assistant

**An AI-assisted early undergraduate project · Chongqing University SRTP · 2026**

A vehicle image generation prototype built with NVIDIA's **StyleGAN2-ADA**, three separately fine-tuned vehicle models, and a **Windows desktop interface**.

[中文说明](README.zh-CN.md) · [Run the application](docs/reproduction.md) · [Training record](docs/experiments.md) · [v1.0.0 release](https://github.com/jinglangqiu-hub/car-design-assistant-srtp/releases/tag/v1.0.0)

## Gallery

| Sports · seed `796724` | Sports · seed `437112` |
|:---:|:---:|
| ![Archived sports output, seed 796724](assets/samples/sports-seed796724.png) | ![Archived sports output, seed 437112](assets/samples/sports-seed437112.png) |

Actual desktop-generated outputs archived on **June 1, 2026**, at **256 × 256** and **truncation ψ = 0.65**. “Sports” is the selected model label; these examples do not consistently exhibit sports-car proportions, illustrating limited category control. Fine details remain imperfect. These selected examples are not a representative evaluation. [Image provenance and original metadata](assets/README.md).

The archived sample ZIP contains these same two sports images. Sedan/SUV examples, a GUI screenshot, and a recorded demo are not currently included; this gallery does not demonstrate all three models.

## Project background & AI assistance

This project was developed for the **Student Research Training Program (SRTP) at Chongqing University**, under the title “基于生成对抗网络的汽车造型设计辅助系统的开发”. It represents one of my earliest attempts to explore deep learning through an AI-assisted development workflow.

The work focused on adapting an existing implementation to vehicle images and integrating the trained models into a desktop prototype. **It does not propose a new GAN architecture or establish an improvement over StyleGAN2-ADA.**

Generative AI was used extensively in coding, debugging, and documentation. Project-specific scripts and the application should be read as AI-assisted work, rather than evidence of independently authored algorithms. My project work centered on carrying out data preparation, training, environment setup, model integration, and delivery. A reliable line-by-line human/AI authorship breakdown was not recorded, so none is claimed here.

## What was built

| Stage | Implementation | Evidence |
|---|---|---|
| Data preparation | Filter CompCars views, crop bounding boxes, pad/resize to 256 × 256, group into three project categories | [Preparation scripts](experiments/), [dataset builder](scripts/build_type_dataset_zips.py) |
| Model adaptation | Fine-tune sports, sedan, and SUV models from a shared car baseline, then continue training | [Training scripts](scripts/), [archived manifest](ppt_materials/03_training_records/manifest.txt) |
| Desktop inference | Tkinter UI with model selection, seed, truncation, batch generation, PNG saving, and CSV metadata | [Application](app/car_design_assistant.py) |
| Windows delivery | PyInstaller directory bundle and Inno Setup split installer | [Build script](scripts/build_pyinstaller_app.ps1), [installer configuration](packaging/CarDesignAssistant.iss), [release](https://github.com/jinglangqiu-hub/car-design-assistant-srtp/releases/tag/v1.0.0) |

### Data & training summary

| Project category | Training images | First fine-tuning stage | Continued stage | Model |
|---|---:|---:|---:|---|
| Sports | 1,519 | 800 kimg | +1,000 kimg | `sports.pkl` |
| Sedan | 5,492 | 1,000 kimg | +1,500 kimg | `sedan.pkl` |
| SUV | 9,889 | 1,000 kimg | +1,500 kimg | `suv.pkl` |

Counts come from the archived dataset summary; training budgets and snapshots are recorded in the manifest. A **kimg** is 1,000 training images shown to the discriminator, not 1,000 unique images. Category names reflect the project's custom CompCars grouping; see [experimental details](docs/experiments.md).

Recorded cloud environment: **Ubuntu 22.04 · RTX 5090 32 GB · Python 3.12.3 · PyTorch 2.7.0+cu128**, batch size 16. These are historical records, not a newly validated compatibility guarantee.

### Engineering choices

- **Three independent models:** reduced changes to the existing framework and made vehicle selection straightforward. The cost is three weight files, separate training runs, and no shared conditional model.
- **256 × 256 output:** kept training and delivery manageable, with limited detail and fidelity.
- **Seed and truncation controls:** expose latent sampling through a simple interface. They do not provide text, sketch, geometry, or component-level control.

## Results & limitations

The project delivered an end-to-end training-to-desktop workflow and a Windows release. Its evidence supports an **early learning and engineering exercise**, with these limits:

- Category training scripts use `--metrics=none`; no verified FID/KID results are reported. An older general training script requests FID, but no corresponding validated result is included.
- There is no controlled baseline comparison, ablation, repeated-run evaluation, or evidence that continued training quantitatively improved quality.
- Samples were inspected visually; diversity, memorization, and generalization were not systematically measured.
- Outputs are low-resolution raster images, not CAD models or engineering-ready designs.
- A complete dependency lockfile and the shared `baseline_240` checkpoint are absent from Git. Exact historical training reproduction from a fresh clone is not guaranteed.

The main lesson is the distinction between making a pipeline run and demonstrating a research claim: data provenance, environment capture, quantitative evaluation, and controlled comparisons need to be planned from the start.

## Run & explore

Clone the repository, obtain trusted weights separately, install a compatible environment, and run:

```powershell
python app\car_design_assistant.py
```

**A clone alone is insufficient:** model weights and training data are excluded from Git. Follow the [run guide](docs/reproduction.md) for model placement, environment checks, installer files, and training prerequisites. Only load trusted `.pkl` weights.

| Location | Purpose |
|---|---|
| [`app/`](app/) | Desktop application; `app/models/` is a placeholder for weights |
| [`assets/`](assets/) | Traceable README gallery assets |
| [`docs/`](docs/README.md) | Current guides and historical document index |
| [`experiments/`](experiments/) and [`scripts/`](scripts/) | Data preparation, training, generation, packaging |
| [`ppt_materials/`](ppt_materials/README.md) | Historical defense materials and training records |
| [`refs/`](refs/) | Third-party StyleGAN2-ADA and SeFa code |

## References & permissions

- **StyleGAN2-ADA:** Tero Karras et al., *Training Generative Adversarial Networks with Limited Data*, NeurIPS 2020. [Paper](https://arxiv.org/abs/2006.06676) · [NVIDIA implementation](https://github.com/NVlabs/stylegan2-ada-pytorch) · [included license](refs/stylegan2-ada-pytorch/LICENSE.txt).
- **CompCars:** Linjie Yang, Ping Luo, Chen Change Loy, Xiaoou Tang, *A Large-Scale Car Dataset for Fine-Grained Categorization and Verification*, CVPR 2015. [Official dataset and terms](https://mmlab.ie.cuhk.edu.hk/datasets/comp_cars/).
- **SeFa reference code:** Yujun Shen and Bolei Zhou, *Closed-Form Factorization of Latent Semantics in GANs*, CVPR 2021. [Upstream](https://github.com/genforce/sefa) · [included license](refs/sefa/LICENSE). It is not part of the final desktop inference path.

There is **no blanket MIT license** for this repository. See [LICENSE](LICENSE) and [third-party/data notices](THIRD_PARTY_NOTICES.md). Obtain CompCars through its official access process; do not redistribute original or processed training images. Historical release availability does not establish unrestricted redistribution or commercial-use rights for weights/installers.
