# 汽车外观设计辅助系统 SRTP 项目

本仓库记录重庆大学 SRTP 项目“基于生成对抗网络的汽车造型设计辅助系统的开发”的代码、脚本、文档和最终交付组织方式。项目最终落地为一个 Windows 桌面程序：用户选择跑车、轿车或 SUV，设置随机种子和 truncation 参数后，程序加载对应的 StyleGAN2-ADA 微调模型生成 256 x 256 汽车外观概念图。

当前 README 按仓库和本机真实状态重写。旧的阶段性 README、TODO、清理报告和上传指南已经移除，避免继续把早期方案当作当前事实。

## 当前真实状态

截至 2026-06-29，本项目的可交付主线已经完成：

- 已完成 CompCars 汽车图片清洗和三类训练数据集构建。
- 已完成跑车、轿车、SUV 三个独立 StyleGAN2-ADA 微调模型训练。
- 已完成云端追加训练，并把最终模型整理为 `sports.pkl`、`sedan.pkl`、`suv.pkl`。
- 已完成 Tkinter 桌面程序，可加载三类模型并生成图片。
- 已完成 PyInstaller 目录式打包和 Inno Setup 安装包制作脚本。
- 本机工作区保留了完整运行资产：模型、训练输出、安装包、PPT/报告材料。
- GitHub 普通 Git 仓库只追踪源码、脚本、说明文档和轻量展示材料；大体积数据、模型、安装包通过 `.gitignore` 排除，应通过 GitHub Release 或本地归档保存。

需要特别说明：当前 `app/car_design_assistant.py` 里的部分中文 UI 字符串已经呈现编码损坏/乱码状态，但程序结构仍能反映真实运行逻辑。后续继续迭代时，修复源码中文编码和界面文案应作为优先事项之一。

## 技术栈

### 训练与生成

- Python
- PyTorch
- CUDA / NVIDIA GPU
- StyleGAN2-ADA PyTorch：`refs/stylegan2-ada-pytorch/`
- NumPy、Pillow
- CompCars 数据集

### 桌面应用

- Python 3.10 系列本地环境
- Tkinter / ttk
- PyTorch 推理
- Pillow 图片显示与保存
- CSV 记录生成元数据

### 打包与交付

- PyInstaller：生成 `dist/CarDesignAssistant/`
- Inno Setup：生成 `installer/CarDesignAssistant_Setup_v1.0.0.exe` 和分卷 `.bin`
- PowerShell 脚本：Windows 本地构建、Release 资产整理
- Bash 脚本：云端训练、继续训练、采样

## 项目真实开发流程

### 1. 立项与早期方案

项目最初目标是做“汽车外观设计辅助系统”，早期设想包含更复杂的条件标签，例如车型和颜色组合标签。后续根据时间、数据质量、训练成本和结项展示要求，主线收敛为更稳妥的三类车型控制：跑车、轿车、SUV。

这也是本次文档清理要删除旧 TODO 和旧 README 的原因：早期文档中的 18 标签、Gradio Demo、512 分辨率增强实验等内容属于规划阶段，不再代表当前项目事实。

### 2. 数据清洗与三类数据集构建

项目基于 CompCars 数据整理汽车图片，清洗后图片按 `make_id__model_id__year__image_id.jpg` 方式命名。三类数据集由脚本生成：

```powershell
python scripts\build_type_dataset_zips.py --mapping-json data\type_datasets\srtp_type_mapping.json
```

实际三类数据规模：

| 类别 | 标识 | 图片数量 | 训练 zip |
|---|---:|---:|---|
| 跑车 | `sports` | 1519 | `compcars_sports_256_square.zip` |
| 轿车 | `sedan` | 5492 | `compcars_sedan_256_square.zip` |
| SUV | `suv` | 9889 | `compcars_suv_256_square.zip` |

三类映射文件为：

```text
data/type_datasets/srtp_type_mapping.json
```

数据集 zip 属于大文件，默认不进入 Git。若新机器需要复现训练，应从 Release 资产或本地备份恢复到 `data/type_datasets/`。

### 3. 云端训练环境迁移

正式训练迁移到云端 GPU 环境完成。本项目记录的云端主环境为：

```text
Project root: /root/autodl-tmp/car_srtp_project
OS: Ubuntu 22.04
GPU: NVIDIA GeForce RTX 5090 32GB
Python: 3.12.3
PyTorch: 2.7.0+cu128
CUDA runtime: 12.8
```

详细环境、命令和训练监控记录保留在：

```text
docs/cloud_env_config.md
outputs/final_models/manifest.txt
ppt_materials/03_training_records/manifest.txt
```

### 4. 三类独立模型初训

项目最终没有采用单一条件模型，而是采用“三类独立微调模型”的工程路线。这样可以直接满足结项展示中按车型选择生成的需求，且对现有 StyleGAN2-ADA 代码改动更少。

云端训练总控脚本：

```bash
/root/autodl-tmp/car_srtp_project/scripts/cloud_train_all_type_models.sh 800 1000 1000 16
```

含义：

```text
sports: 800 kimg
sedan: 1000 kimg
suv: 1000 kimg
batch: 16
```

脚本会顺序训练三类模型，生成样例图，并写入：

```text
outputs/final_models/manifest.txt
```

### 5. 追加训练

第一轮正式训练后，项目继续从三个最终模型出发进行追加训练，而不是回到通用 baseline 重新训练。追加训练脚本：

```bash
/root/autodl-tmp/car_srtp_project/scripts/cloud_continue_all_type_models.sh 1000 1500 1500 16
```

含义：

```text
sports: +1000 kimg
sedan:  +1500 kimg
suv:    +1500 kimg
batch:  16
```

追加训练后的最终模型仍覆盖输出到：

```text
outputs/final_models/sports.pkl
outputs/final_models/sedan.pkl
outputs/final_models/suv.pkl
```

并追加记录到 `manifest.txt`。

### 6. 本地模型整理

训练完成后，本地通过脚本下载最终模型、样例图和日志：

```powershell
powershell -ExecutionPolicy Bypass -File scripts\download_final_assets.ps1
```

该脚本会把云端 `outputs/final_models/` 下载到本地，并复制三类模型到桌面程序默认读取目录：

```text
app/models/sports.pkl
app/models/sedan.pkl
app/models/suv.pkl
```

当前 GitHub 仓库只追踪 `app/models/.gitkeep`，不会追踪 `.pkl` 模型本体。

### 7. 桌面程序开发

桌面程序入口：

```text
app/car_design_assistant.py
```

核心运行逻辑：

- 程序启动后定位项目根目录。
- 查找 `refs/stylegan2-ada-pytorch/legacy.py`。
- 根据用户选择加载对应模型：
  - `sports` -> `sports.pkl`
  - `sedan` -> `sedan.pkl`
  - `suv` -> `suv.pkl`
- 根据 seed 和 truncation 调用 StyleGAN2-ADA 生成图片。
- 图片保存到 `outputs/app_generated/<type>/`。
- 参数记录追加到 `outputs/app_generated/metadata.csv`。

本地源码运行推荐命令：

```powershell
.\start_desktop_app.cmd
```

或直接指定项目专用 Python：

```powershell
D:\anaconda\envs\car_srtp_clean\python.exe app\car_design_assistant.py
```

依赖列表：

```powershell
pip install -r requirements_app.txt
```

### 8. PyInstaller 打包

PyInstaller 构建脚本：

```powershell
powershell -ExecutionPolicy Bypass -File scripts\build_pyinstaller_app.ps1
```

若环境中没有 PyInstaller：

```powershell
powershell -ExecutionPolicy Bypass -File scripts\build_pyinstaller_app.ps1 -InstallPyInstaller
```

脚本会检查模型是否存在，并把运行所需依赖、StyleGAN2-ADA 代码和三类模型复制进打包目录：

```text
dist/CarDesignAssistant/
```

打包后可直接运行：

```text
dist/CarDesignAssistant/CarDesignAssistant.exe
```

### 9. Inno Setup 安装包

安装包构建脚本：

```powershell
powershell -ExecutionPolicy Bypass -File scripts\build_inno_installer.ps1
```

如果脚本找不到 `ISCC.exe`，手动指定：

```powershell
powershell -ExecutionPolicy Bypass -File scripts\build_inno_installer.ps1 -InnoCompiler "C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
```

安装包配置：

```text
packaging/CarDesignAssistant.iss
```

本地交付资产：

```text
installer/CarDesignAssistant_Setup_v1.0.0.exe
installer/CarDesignAssistant_Setup_v1.0.0-1.bin
installer/CarDesignAssistant_Setup_v1.0.0-2.bin
installer/CarDesignAssistant_Setup_v1.0.0-3.bin
```

安装包和分卷文件体积较大，不进入普通 Git 提交。

### 10. GitHub Release 资产整理

用于整理 Release 附件的脚本：

```powershell
powershell -ExecutionPolicy Bypass -File scripts\prepare_github_release_assets.ps1
```

脚本会从本机工作区收集：

- 安装包 `.exe` 和 `.bin`
- 三类 `.pkl` 模型
- `manifest.txt`
- 三类训练数据集 zip
- 最终样例和桌面端生成样例 zip

输出目录：

```text
release_assets/
```

上传脚本：

```powershell
powershell -ExecutionPolicy Bypass -File scripts\upload_github_release_assets.ps1
```

使用该脚本前需要确认 GitHub CLI 已登录，并确认目标 tag/release。普通 README 更新只需要 `git push`，大文件交付需要 Release 附件。

## 当前仓库结构

```text
app/
  car_design_assistant.py        # Tkinter 桌面程序入口
  models/.gitkeep               # 模型目录占位；真实 .pkl 不进 Git

data/                           # 本地数据目录；不进 Git

docs/
  cloud_env_config.md           # 云端训练环境与过程记录
  paper_outline.md              # 论文/结项报告提纲
  slides_outline.md             # 答辩 PPT 提纲
  *.docx / *.pptx               # 结项报告、中期报告、答辩 PPT 等材料

experiments/
  prepare_compcars_*.py         # 数据准备实验脚本

outputs/                        # 本地训练/生成结果；不进 Git

packaging/
  CarDesignAssistant.iss        # Inno Setup 配置

ppt_materials/
  01_report_and_docs/           # PPT/结项材料归档
  02_generated_samples/         # 展示样例
  03_training_records/          # 训练记录
  04_dataset_and_model_info/    # 数据集和模型摘要
  05_desktop_and_packaging/     # 桌面端与打包材料
  06_github_release/            # Release 资产摘要和脚本副本

refs/
  stylegan2-ada-pytorch/        # 训练和推理依赖
  sefa/                         # 参考代码

scripts/
  build_type_dataset_zips.py
  cloud_train_all_type_models.sh
  cloud_continue_all_type_models.sh
  download_final_assets.ps1
  build_pyinstaller_app.ps1
  build_inno_installer.ps1
  prepare_github_release_assets.ps1
  upload_github_release_assets.ps1

requirements_app.txt
start_desktop_app.cmd
```

## Git 与大文件规则

当前 `.gitignore` 明确排除了以下大体积或可再生成资产：

```text
data/
outputs/
dist/
installer/
release_assets/
app/models/*.pkl
*.pkl
*.zip
*.exe
*.bin
```

因此，克隆 GitHub 仓库后不能直接得到完整可运行系统。新机器要运行或继续开发，需要补齐：

```text
app/models/sports.pkl
app/models/sedan.pkl
app/models/suv.pkl
refs/stylegan2-ada-pytorch/
```

若要复现训练，还需要补齐：

```text
data/type_datasets/compcars_sports_256_square.zip
data/type_datasets/compcars_sedan_256_square.zip
data/type_datasets/compcars_suv_256_square.zip
data/type_datasets/srtp_type_mapping.json
```

## 常用命令

### 启动桌面程序

```powershell
.\start_desktop_app.cmd
```

### 从源码启动

```powershell
D:\anaconda\envs\car_srtp_clean\python.exe app\car_design_assistant.py
```

### 构建三类训练数据集

```powershell
python scripts\build_type_dataset_zips.py --mapping-json data\type_datasets\srtp_type_mapping.json
```

### 云端初训

```bash
PROJECT_ROOT=/root/autodl-tmp/car_srtp_project \
bash scripts/cloud_train_all_type_models.sh 800 1000 1000 16
```

### 云端追加训练

```bash
PROJECT_ROOT=/root/autodl-tmp/car_srtp_project \
bash scripts/cloud_continue_all_type_models.sh 1000 1500 1500 16
```

### 下载最终模型

```powershell
powershell -ExecutionPolicy Bypass -File scripts\download_final_assets.ps1
```

### 构建桌面程序

```powershell
powershell -ExecutionPolicy Bypass -File scripts\build_pyinstaller_app.ps1
```

### 构建安装包

```powershell
powershell -ExecutionPolicy Bypass -File scripts\build_inno_installer.ps1
```

### 整理 GitHub Release 附件

```powershell
powershell -ExecutionPolicy Bypass -File scripts\prepare_github_release_assets.ps1
```

## 后续继续开发的关键信息

优先级从高到低：

1. 修复 `app/car_design_assistant.py` 和部分 Markdown 中的中文编码损坏问题，确保桌面 UI、状态提示和文档在 UTF-8 下正常显示。
2. 为模型资产建立明确的 Release 版本命名，例如 `v1.0.0-models`、`v1.0.0-installer`，避免只依赖本机目录。
3. 增加最小化健康检查脚本：检查 `legacy.py`、三类 `.pkl`、PyTorch、CUDA/CPU fallback、输出目录写入权限。
4. 把桌面程序中的模型加载、生成、元数据写入拆成可测试模块，减少 GUI 与推理逻辑耦合。
5. 增加 smoke test：在有模型的机器上用固定 seed 对三类模型各生成一张图，并验证文件和 metadata 是否写入。
6. 如需继续提升生成质量，应优先从数据清洗和样本筛选入手；直接把 256 模型继续训练更久可能造成过拟合，尤其跑车类样本只有 1519 张。
7. 如需做 512 x 512 增强实验，应重新构建 512 数据集并单独开实验分支，不要把当前 256 主线改乱。
8. 若要公开分发，建议优先完善 Release 附件说明和安装包校验值，而不是把大文件强行提交进 Git。

## 已删除的过期说明

本次文档整理删除了以下不再代表当前项目状态的阶段性说明：

- 旧根目录 README 草稿
- 旧环境配置 README
- 旧项目 TODO
- `app/README.md`
- `packaging/README_packaging.md`
- 旧清理报告
- 旧验收 checklist
- 旧 GitHub 上传指南
- `ppt_materials/` 中对应的重复阶段性 README/checklist/上传指南副本

保留的文档主要用于结项证明、训练环境追溯、论文/PPT 组织和后续复现。
