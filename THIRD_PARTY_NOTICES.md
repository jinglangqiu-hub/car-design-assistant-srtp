# Third-party sources and licensing

[Project overview](README.md) · [中文说明](README.zh-CN.md) · [Source map and references](docs/references.md) · [Top-level notice](LICENSE)

**Scope:** this inventory covers the third-party source trees and assets tracked in the repository, the direct dependencies listed in `requirements_app.txt`, and tools named by the build scripts. It does not certify every transitive dependency or the contents of the historical Windows binary. Verification date: **November 2, 2026**.

**中文摘要：** 本清单记录可核实的代码、素材、数据及工具来源，保留原许可证，明确适用范围；不将文献引用等同于取得授权，也不把缺少记录的模型或安装包权限写成已经解决。项目自有部分尚未单独授予统一的再使用许可。

## Vendored code and assets

| Local material | Original source / rights holder | Applicable license or recorded status |
|---|---|---|
| `refs/stylegan2-ada-pytorch/`, including local changes and backup copies | [NVlabs/stylegan2-ada-pytorch](https://github.com/NVlabs/stylegan2-ada-pytorch), NVIDIA Corporation | [Included NVIDIA Source Code License](refs/stylegan2-ada-pytorch/LICENSE.txt); redistribution and notice requirements in §3.1, derivative-work conditions in §3.2, non-commercial research/evaluation limitation in §3.3 |
| `refs/sefa/`, except separately identified embedded material | [genforce/sefa](https://github.com/genforce/sefa), Yujun Shen | [Included MIT license](refs/sefa/LICENSE); keep its copyright and permission notice with copies/substantial portions |
| SeFa's Bootstrap CSS | [Bootstrap v3.2.0](https://github.com/twbs/bootstrap/tree/v3.2.0), Twitter, Inc. | MIT; [complete text](LICENSES/Bootstrap-3.2.0-MIT.txt). Version and credit appear in the CSS header |
| normalize.css inside the Bootstrap CSS bundle | [normalize.css v3.0.1](https://github.com/necolas/normalize.css/tree/3.0.1), Nicolas Gallagher and Jonathan Neal | MIT; [complete text](LICENSES/normalize.css-3.0.1-MIT.txt). The embedded header identifies the component |
| Lato font referenced by SeFa's `font.css` | [Lato / Google Fonts](https://github.com/google/fonts/tree/main/ofl/lato), Łukasz Dziedzic | SIL Open Font License 1.1; [upstream license text](LICENSES/Lato-OFL-1.1.txt). Font files are loaded by external URLs; no font binaries are tracked here |
| `refs/sefa/SessionState.py` | [tvst's Gist](https://gist.github.com/tvst/036da038ab3e999a64497f42de966a92), identified in its file header | No separate license text was found in the local helper or the retrieved Gist. SeFa's repository-level MIT notice is retained; it is not evidence of an independent grant by the helper's original author |
| `refs/stylegan2-ada-pytorch/docs/` images | NVIDIA's upstream documentation | Retained with the upstream tree and notices; no separate project image license is granted |
| Project reports, slides, and `重大PPT模版.pptx` | Project records; may include university branding, third-party illustrations, or dataset-derived montages | No separate asset-level grants are archived for all embedded material. The repository does not relicense those images, logos, or templates |

SeFa includes model implementations and URLs credited to the upstream GAN ecosystem. Those model-zoo URLs do not grant rights to listed weights and do not establish this project's baseline lineage. The final Tkinter app uses StyleGAN2-ADA, not SeFa or its Streamlit helper.

Original license files and source headers are preserved. The additional MIT/OFL texts address the identified nested assets; they do not place the entire repository under MIT or OFL. Exact original vendoring revisions are not recorded.

## Runtime dependencies and development tools

These upstream links identify licenses for the named projects. Except for the recorded cloud PyTorch version, exact versions in the historical desktop build are not recorded. When assembling a new binary, use the license/NOTICE files shipped with the **actual installed versions**, including bundled native libraries; current upstream text alone is not a historical binary inventory.

| Dependency / tool | Use | Official license source |
|---|---|---|
| Python / Tkinter | Runtime and desktop UI | [Python license and notices](https://github.com/python/cpython/blob/main/LICENSE); Tcl/Tk has its own notices in the installed runtime |
| PyTorch | Training and inference | [PyTorch v2.7.0 license and included component notices](https://github.com/pytorch/pytorch/blob/v2.7.0/LICENSE); main code uses BSD-style terms, with separately listed bundled components |
| NumPy | Array operations | [BSD 3-Clause and bundled-component notices](https://github.com/numpy/numpy/blob/main/LICENSE.txt) |
| Pillow | Image I/O and Tkinter preview | [Pillow/PIL license](https://github.com/python-pillow/Pillow/blob/main/LICENSE) |
| Click | Upstream command-line tools | [BSD 3-Clause](https://github.com/pallets/click/blob/main/LICENSE.txt) |
| Requests | Upstream HTTP utilities | [Apache 2.0](https://github.com/psf/requests/blob/main/LICENSE) |
| tqdm | Progress reporting | [MPL 2.0 / MIT allocation in LICENCE](https://github.com/tqdm/tqdm/blob/master/LICENCE) |
| SciPy | Numerical/metric dependencies | [BSD 3-Clause and bundled notices](https://github.com/scipy/scipy/blob/main/LICENSE.txt) |
| psutil | Process/system utilities | [BSD 3-Clause](https://github.com/giampaolo/psutil/blob/master/LICENSE) |
| pyspng | PNG decoding | [Actual source LICENSE](https://github.com/nurpax/pyspng/blob/main/LICENSE), with BSD-style terms; inspect the installed wheel's libspng/other native notices as well |
| imageio | Upstream image/video utilities; collected by the packaging script | [BSD 2-Clause](https://github.com/imageio/imageio/blob/master/LICENSE) |
| imageio-ffmpeg | FFmpeg wrapper listed in application requirements | [BSD 2-Clause wrapper license](https://github.com/imageio/imageio-ffmpeg/blob/main/LICENSE); any FFmpeg executable is subject to its own [build-dependent terms](https://ffmpeg.org/legal.html) |
| Ninja | Upstream custom-extension build tool | [Apache 2.0](https://github.com/ninja-build/ninja/blob/master/COPYING) |
| PyInstaller | Application packaging | [GPL with bootloader exception and file-specific terms](https://github.com/pyinstaller/pyinstaller/blob/develop/COPYING.txt); [official explanation](https://pyinstaller.org/en/stable/license.html) |
| Inno Setup | Windows installer creation | [Inno Setup license](https://github.com/jrsoftware/issrc/blob/main/license.txt); the installed compiler version's terms apply |
| CUDA and NVIDIA driver/toolchain | GPU execution and custom-extension compilation | [NVIDIA CUDA EULA](https://docs.nvidia.com/cuda/eula/index.html) and applicable installed-component terms; no toolchain redistribution grant is made here |

The reference-only SeFa interface additionally imports Streamlit and OpenCV. Their respective [Apache 2.0 license](https://github.com/streamlit/streamlit/blob/develop/LICENSE) and [version-dependent OpenCV terms](https://opencv.org/license/) should be checked before running or distributing that separate interface. Neither is part of the final Tkinter app's declared dependency list.

## Data and generated artifacts

| Material | Origin | Permissions and distribution status |
|---|---|---|
| CompCars data and processed image subsets | [CUHK official dataset](https://mmlab.ie.cuhk.edu.hk/datasets/comp_cars/) | Non-commercial research access under the [official agreement](https://mmlab.ie.cuhk.edu.hk/datasets/comp_cars/agreement.pdf). Further publication/distribution of database portions is restricted outside its stated internal-use exception. Cropping or selecting a subset does not remove those terms |
| `sports.pkl`, `sedan.pkl`, `suv.pkl` | Project training stages recorded in the [manifest](ppt_materials/03_training_records/manifest.txt), initialized from local `baseline_240` | Weights are distinct from source code and raw images. Complete baseline provenance and separate redistribution permissions are not established by the archived records |
| Gallery PNGs and metadata | Original desktop outputs, documented in [assets/README.md](assets/README.md) | Displayed as project evidence; no additional general reuse license is granted. Model-output status alone does not establish that all underlying third-party rights are cleared |
| Historical Windows installer | PyInstaller/Inno Setup output with project models and dependencies | Historical download retained. A complete dependency/version/license manifest is not available, so this inventory does not certify the existing binary's full contents or permissions |

The three processed CompCars training ZIPs were removed from v1.0.0 on **November 2, 2026**. Current release scripts exclude them and reject stale dataset ZIPs. Data access should follow the official process. Dataset authors and rights holders retain their rights; a dataset agreement or third-party model grant is not created by this README.

## Provenance gaps

- The exact original commits used to vendor the two reference repositories are unrecorded.
- The shared `baseline_240` checkpoint, its source URL/hash, its earlier initialization/training history, and a complete weight-redistribution grant are not archived.
- A CompCars access agreement is not included in this public repository; this does not establish whether an agreement was obtained privately.
- The historical desktop environment and installer lack a complete versioned dependency and license inventory. Packaging also collects native/optional components, whose terms cannot be inferred from a short requirements list.
- The borrowed SessionState helper and third-party material embedded in reports/slides have the source/permission limits identified above.
- No additional general license has been selected for project-specific code, documentation, or outputs. Any upstream-derived portions remain under their original terms.

This file records available evidence and applicable boundaries. It is not a declaration that missing permissions have been obtained. For reuse, follow the original rights holders' terms and resolve any material-specific gaps; public availability and academic citation are not substitutes for permission.
