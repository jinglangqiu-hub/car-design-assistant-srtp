# Third-party & data notices

Project-specific AI-assisted integration is distinct from the upstream model. The [top-level notice](LICENSE) does not relicense third-party code or grant a new blanket license.

| Component | Origin and role | Included terms |
|---|---|---|
| `refs/stylegan2-ada-pytorch/` | [NVlabs/stylegan2-ada-pytorch](https://github.com/NVlabs/stylegan2-ada-pytorch), core training/inference; includes local compatibility edits and backup copies | [NVIDIA license](refs/stylegan2-ada-pytorch/LICENSE.txt), including non-commercial research/evaluation use limitation |
| `refs/sefa/` | [genforce/sefa](https://github.com/genforce/sefa), reference exploration; outside final desktop inference path | [SeFa license](refs/sefa/LICENSE); nested/borrowed code retains its notices |
| CompCars | [CUHK dataset](https://mmlab.ie.cuhk.edu.hk/datasets/comp_cars/), training images/attributes | Official terms and [release agreement](https://mmlab.ie.cuhk.edu.hk/datasets/comp_cars/agreement.pdf) |

Exact upstream commits are not recorded. Preserve existing headers and licenses, including in copied/modified files. Dependencies and packaging tools have their own terms; bundling does not remove them.

## Data and release assets

CompCars restricts access to non-commercial research and prohibits further distribution of database portions outside its stated internal-use exception. Selecting, cropping, or resizing images is not a basis for redistributing them. Obtain authorized data through the official process and keep processed datasets private.

The historical v1.0.0 release included processed training ZIPs. Current staging/upload scripts exclude them; removing existing attachments is a separate release-maintenance operation. Historical availability is not a data access or redistribution permission.

Weights/installers require their own provenance and distribution review. This cleanup does not establish that all rights needed for redistribution have been obtained, and does not automatically equate weights with raw images. Gallery examples are model outputs, not training-image copies; no unrestricted reuse license is granted here.

## Credit

- Linjie Yang, Ping Luo, Chen Change Loy, Xiaoou Tang. **A Large-Scale Car Dataset for Fine-Grained Categorization and Verification.** CVPR, 2015.
- Tero Karras et al. **Training Generative Adversarial Networks with Limited Data.** NeurIPS, 2020. [Paper](https://arxiv.org/abs/2006.06676).
- Yujun Shen and Bolei Zhou. **Closed-Form Factorization of Latent Semantics in GANs.** CVPR, 2021. [Upstream](https://github.com/genforce/sefa).
