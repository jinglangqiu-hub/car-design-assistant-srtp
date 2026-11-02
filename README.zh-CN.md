# 汽车外观设计辅助系统

**重庆大学大学生科研训练计划（SRTP）项目 · 2026**

基于 **StyleGAN2-ADA** 的汽车外观概念图生成原型，包含三类独立微调模型与 **Windows 桌面应用**。

**项目状态：已于 2026 年 7 月在重庆大学完成答辩并结题。**

**3 类车型模型 · 16,900 张训练图片 · 256 × 256 输出**

[English](README.md) · [项目背景](#项目背景) · [生成样例](#生成样例) · [运行指南](docs/reproduction.md) · [Windows 下载](https://github.com/jinglangqiu-hub/car-design-assistant-srtp/releases/tag/v1.0.0)

## 项目背景

本仓库记录我参加**重庆大学大学生科研训练计划（SRTP）**，开展**“基于生成对抗网络的汽车造型设计辅助系统的开发”**项目的实践过程与交付成果。项目已于 **2026 年 7 月在重庆大学完成答辩并结题**。

这是我最早期接触深度学习的一次实践，重点是完成从汽车图片整理、既有生成模型适配、云端训练到桌面应用集成的完整流程。项目的工作主要体现为对已有方法的学习、实现与工程集成，不涉及新的 GAN 模型架构。

## 生成样例

| Sports 模型 · seed `796724` | Sports 模型 · seed `437112` |
|:---:|:---:|
| ![Sports 模型生成图，seed 796724](assets/samples/sports-seed796724.png) | ![Sports 模型生成图，seed 437112](assets/samples/sports-seed437112.png) |

两张图均为 **2026 年 6 月 1 日**归档的桌面端原始输出，分辨率 **256 × 256**，**truncation ψ = 0.65**。模型标签表示生成时选用的权重，不等于经过验证的车型分类。样例呈现了可辨识的汽车结构，也反映出车型控制与局部细节的不足。[原始图片与参数](assets/README.md)。

<details>
<summary>图集范围说明</summary>

当前仓库与样例压缩包仅包含这两张 Sports 模型输出，未收录轿车/SUV 样例、GUI 截图或演示视频。这些图片用于说明原型输出，不构成三个模型的代表性评价。原图与元数据均保留，没有修图。

</details>

## 实现流程

| 环节 | 完成的工作 | 代码与记录 |
|---|---|---|
| 数据准备 | 筛选 CompCars 视角、按标注框裁剪、补方并缩放到 256 × 256，按项目类别整理图片 | [预处理脚本](experiments/) · [数据集构建](scripts/build_type_dataset_zips.py) · [类别映射](configs/srtp_type_mapping.json) |
| 模型适配 | 从共同的本地汽车 baseline 出发，分别微调三类 StyleGAN2-ADA 模型，再进行追加训练 | [训练脚本](scripts/) · [训练 manifest](ppt_materials/03_training_records/manifest.txt) |
| 桌面应用 | 选择模型、设置 seed 和 truncation、单张或批量生成、保存 PNG，并以 CSV 记录参数 | [Tkinter 应用](app/car_design_assistant.py) |
| Windows 交付 | 使用 PyInstaller 打包应用，通过 Inno Setup 制作分卷安装包 | [打包脚本](scripts/build_pyinstaller_app.ps1) · [安装配置](packaging/CarDesignAssistant.iss) · [v1.0.0](https://github.com/jinglangqiu-hub/car-design-assistant-srtp/releases/tag/v1.0.0) |

### 归档的数据规模与训练设置

| 项目类别 | 训练图片数 | 第一阶段微调 | 追加训练 | 权重文件 |
|---|---:|---:|---:|---|
| 跑车（Sports） | 1,519 | 800 kimg | +1,000 kimg | `sports.pkl` |
| 轿车（Sedan） | 5,492 | 1,000 kimg | +1,500 kimg | `sedan.pkl` |
| SUV | 9,889 | 1,000 kimg | +1,500 kimg | `suv.pkl` |

以上数值来自项目归档。**kimg** 表示向判别器展示的训练图片数量，以千张计，包含重复呈现；车型名称对应项目采用的 CompCars 标签归组。记录的云端环境为 **Ubuntu 22.04、RTX 5090 32 GB、Python 3.12.3、PyTorch 2.7.0+cu128**，batch size 为 16。[实验设置与依据](docs/experiments.md)。

采用三个独立模型，便于在较少改动既有框架的情况下实现车型选择，代价是分别训练和维护三个权重文件，没有实现共享的条件模型。seed 和 truncation 用于控制采样；应用没有实现文本、草图或零件级条件控制。

## AI 辅助开发说明

**代码生成、调试与文档整理广泛使用了生成式 AI。** 我的项目实践主要围绕在 AI 辅助下执行数据准备、环境配置、训练、模型集成与软件交付展开。应用与项目脚本作为一次 AI 辅助开发实践进行展示，底层模型及第三方代码的贡献归属于原作者。

## 成果与局限

项目完成了从训练到桌面推理的工作流程，留下模型快照、生成参数记录与 Windows 发布版本，也体现出“跑通原型”与“完成受控科研评价”之间的区别：

- **实验评价：** 三类模型训练使用 `--metrics=none`，未报告可核验的 FID/KID、受控 baseline 对比、消融或多次重复实验。训练更久本身不作为质量提升的证据。
- **图像质量：** 主要通过人工观察判断，未系统评价多样性、泛化与训练图像记忆情况；车型控制和细节质量仍有限。
- **输出用途：** 结果为 256 × 256 的栅格概念图，不是 CAD 模型或可直接用于工程的汽车设计。
- **复现条件：** 仓库未提供共同的 `baseline_240` 权重、完整权重来源链及环境锁文件，尚不能建立历史训练的精确复现。

这次经历的主要收获是将数据准备、模型训练、推理与软件打包连接起来，并认识到数据溯源、可复现性与定量评价需要从项目开始时就纳入设计。

## 运行与资料

| 目标 | 入口 |
|---|---|
| 使用 Windows 应用 | [v1.0.0 附件](https://github.com/jinglangqiu-hub/car-design-assistant-srtp/releases/tag/v1.0.0)：将 `.exe` 与三个 `.bin` 分卷放入同一目录 |
| 从源码运行或查看实现 | [配置指南](docs/reproduction.md)：准备 Python 环境，并将可信权重放入 `app/models/` |
| 查看实验记录 | [训练文档](docs/experiments.md)：类别映射、参数、manifest 与复现缺口 |
| 查看 SRTP 材料 | [文档索引](docs/README.md)：报告、答辩 PPT 与历史记录 |

配置完成后，在仓库根目录运行：

```powershell
python app\car_design_assistant.py
```

克隆仓库不包含模型权重与训练数据集。三份处理后的 CompCars 训练集已于 **2026 年 11 月 2 日**从 Release 移除，数据应通过[官方流程](https://mmlab.ie.cuhk.edu.hk/datasets/comp_cars/)获取。只加载来源可信的 `.pkl` 文件。[完整运行说明](docs/reproduction.md)。

## 参考文献与致谢

本项目基于以下作者与维护者的工作开展：

1. **StyleGAN2-ADA：核心训练与推理实现。** Tero Karras、Miika Aittala、Janne Hellsten、Samuli Laine、Jaakko Lehtinen、Timo Aila，*Training Generative Adversarial Networks with Limited Data*，NeurIPS 2020。[论文](https://arxiv.org/abs/2006.06676) · [官方 PyTorch 实现](https://github.com/NVlabs/stylegan2-ada-pytorch)。
2. **StyleGAN2：模型架构基础。** Tero Karras、Samuli Laine、Miika Aittala、Janne Hellsten、Jaakko Lehtinen、Timo Aila，*Analyzing and Improving the Image Quality of StyleGAN*，CVPR 2020。[论文](https://arxiv.org/abs/1912.04958)。
3. **CompCars：训练数据来源。** Linjie Yang、Ping Luo、Chen Change Loy、Xiaoou Tang，*A Large-Scale Car Dataset for Fine-Grained Categorization and Verification*，CVPR 2015。[数据集及条款](https://mmlab.ie.cuhk.edu.hk/datasets/comp_cars/) · [扩展版论文](https://arxiv.org/abs/1506.08959)。
4. **SeFa：参考代码。** Yujun Shen、Bolei Zhou，*Closed-Form Factorization of Latent Semantics in GANs*，CVPR 2021。[论文](https://arxiv.org/abs/2007.06600) · [代码](https://github.com/genforce/sefa)。相关代码保留供参考，未用于最终桌面推理主线。

[来源与引用说明](docs/references.md) · [BibTeX](references.bib) · [软件与素材许可清单](THIRD_PARTY_NOTICES.md)。

## 授权说明

| 材料 | 适用条款 |
|---|---|
| 仓库中的 StyleGAN2-ADA 代码及其修改 | [NVIDIA Source Code License](refs/stylegan2-ada-pytorch/LICENSE.txt)，包含非商业研究/评估用途限制 |
| SeFa 参考代码及嵌套素材 | [SeFa MIT 许可](refs/sefa/LICENSE)；嵌套素材另见[许可清单](THIRD_PARTY_NOTICES.md) |
| CompCars 原始图片与处理后训练集 | [官方数据条款](https://mmlab.ie.cuhk.edu.hk/datasets/comp_cars/)；训练集 ZIP 不再分发，历史报告嵌图另见[素材说明](THIRD_PARTY_NOTICES.md) |
| 项目自有代码、文档、权重与输出 | 仓库未额外授予统一的再使用许可，详见 [LICENSE](LICENSE) 与[适用范围及来源缺口](THIRD_PARTY_NOTICES.md#provenance-gaps) |

第三方材料的权利与许可仍归相应作者及权利人。公开展示仓库不等于全仓库统一采用 MIT，也不证明模型权重或历史安装包拥有不受限制的再分发授权。
