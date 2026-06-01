# 汽车外观设计辅助系统 SRTP 项目

本项目面向重庆大学 SRTP 结项，目标是构建一个可运行、可展示、可安装的汽车外观概念图生成系统。系统基于 CompCars 数据集和 StyleGAN2-ADA 微调模型，实现按“跑车、轿车、SUV”三类选择生成汽车外观图片，并提供 Windows 11 桌面程序与 Inno Setup 安装包。

## 当前结项状态

截至 2026-06-01，项目已完成：

- 云端 RTX 5090 训练环境迁移与验证。
- CompCars 汽车外观数据清洗与三类数据集构建。
- 跑车、轿车、SUV 三个 StyleGAN2-ADA 微调模型训练与追加训练。
- 每类均筛选出 10 张以上可展示生成图。
- 桌面程序开发完成，可按车型选择生成图片。
- PyInstaller 打包完成，打包版可正常出图。
- Inno Setup 安装包生成完成，安装后的应用可正常生图。
- 项目目录已清理构建缓存、云端上传缓存和旧训练中间产物。

## 最终核心成果

```text
installer/
  CarDesignAssistant_Setup_v1.0.0.exe

app/
  car_design_assistant.py
  models/
    sports.pkl
    sedan.pkl
    suv.pkl

outputs/
  final_models/
    sports.pkl
    sedan.pkl
    suv.pkl
    manifest.txt
  app_generated/
    桌面程序生成图片与 metadata.csv

docs/
  cloud_env_config.md
  final_acceptance_checklist.md
  paper_outline.md
  slides_outline.md
  project_cleanup_report.md

packaging/
  CarDesignAssistant.iss
  README_packaging.md
```

## 桌面程序

源码入口：

```powershell
D:\anaconda\envs\car_srtp_clean\python.exe app\car_design_assistant.py
```

推荐本地启动方式：

```powershell
.\start_desktop_app.cmd
```

已验证打包版：

```powershell
.\dist\CarDesignAssistant\CarDesignAssistant.exe
```

安装包：

```text
installer/CarDesignAssistant_Setup_v1.0.0.exe
```

安装后可从开始菜单或桌面快捷方式启动，支持：

- 选择跑车、轿车、SUV。
- 设置随机种子 seed。
- 调整 truncation 生成稳定度。
- 单张生成。
- 批量生成。
- 自动保存图片。
- 打开输出目录。
- 另存当前图片。
- 记录生成参数到 `metadata.csv`。

## 运行环境

源码运行推荐环境：

```text
Windows 11
Python 3.10.19
PyTorch 2.10.0+cu128
CUDA 可用
Pillow
NumPy
Tkinter / ttk
```

项目专用 Python：

```text
D:\anaconda\envs\car_srtp_clean\python.exe
```

不要直接使用 Anaconda base 环境运行源码。base 环境可能缺少 `torch`、`click` 等依赖。

安装包运行说明：

- 已将 Python 运行时、PyTorch 依赖、StyleGAN2-ADA 代码和三类模型一起打包。
- 普通 Win11 电脑安装后可直接运行。
- 若对方电脑没有 NVIDIA GPU，程序会尝试使用 CPU，但生成速度会明显变慢。

## 模型文件

三类最终模型：

```text
sports.pkl -> 跑车生成模型
sedan.pkl  -> 轿车生成模型
suv.pkl    -> SUV 生成模型
```

桌面程序优先读取：

```text
app/models/sports.pkl
app/models/sedan.pkl
app/models/suv.pkl
```

备用读取：

```text
outputs/final_models/sports.pkl
outputs/final_models/sedan.pkl
outputs/final_models/suv.pkl
```

PyInstaller 打包版还兼容读取：

```text
_internal/app/models/
```

## 数据集

原始和清洗数据仍保留，用于论文说明和实验复现：

```text
data/downloads/
data/raw_compcars/
data/compcars_cleaned_v1/
data/compcars_cleaned_v1_256_square.zip
```

三类训练数据集：

```text
data/type_datasets/
  compcars_sports_256_square.zip
  compcars_sedan_256_square.zip
  compcars_suv_256_square.zip
  srtp_type_mapping.json
```

重新生成三类数据集：

```powershell
D:\anaconda\python.exe scripts\build_type_dataset_zips.py --mapping-json data\type_datasets\srtp_type_mapping.json
```

## 云端训练记录

云端实例：

```text
平台：AutoDL / SeetaCloud 连接节点
GPU：NVIDIA GeForce RTX 5090 32GB
系统：Ubuntu 22.04
Python：3.12.3
PyTorch：2.7.0+cu128
CUDA Runtime：12.8
```

训练路线：

```text
三类独立微调模型：
跑车 -> sports.pkl
轿车 -> sedan.pkl
SUV  -> suv.pkl
```

第一轮正式训练：

```bash
/root/autodl-tmp/car_srtp_project/scripts/cloud_train_all_type_models.sh 800 1000 1000 16
```

追加训练：

```bash
/root/autodl-tmp/car_srtp_project/scripts/cloud_continue_all_type_models.sh 1000 1500 1500 16
```

详细环境、命令、监控方式和训练记录见：

```text
docs/cloud_env_config.md
```

## 打包方案

PyInstaller 打包：

```powershell
powershell -ExecutionPolicy Bypass -File scripts\build_pyinstaller_app.ps1
```

Inno Setup 安装包：

```powershell
powershell -ExecutionPolicy Bypass -File scripts\build_inno_installer.ps1 -InnoCompiler "D:\Inno Setup 6\ISCC.exe"
```

打包配置：

```text
packaging/CarDesignAssistant.iss
packaging/README_packaging.md
```

已处理的问题：

- PyInstaller 缺少 `click`、`legacy` 等依赖。
- StyleGAN2-ADA 代码在打包目录中的路径兼容。
- 三类 `.pkl` 模型在打包版中的读取路径。
- Inno Setup 中文语言包缺失问题。
- 单个安装包体积接近 4.2GB 的重复打包问题。

## 输出文件

桌面程序生成结果：

```text
outputs/app_generated/
```

按车型保存：

```text
outputs/app_generated/sports/
outputs/app_generated/sedan/
outputs/app_generated/suv/
```

生成参数记录：

```text
outputs/app_generated/metadata.csv
```

## 目录保留原则

已删除：

- PyInstaller 临时构建目录 `build/`。
- 云端上传缓存 `cloud_upload/`。
- 旧 StyleGAN2-ADA 中间训练 run `outputs/stylegan2ada_runs/`。
- Python `__pycache__/` 缓存。
- 临时 `CarDesignAssistant.spec`。
- 本地 `.cache/`。

保留：

- 最终安装包。
- 已验证 PyInstaller 打包版。
- 三类最终模型。
- 原始/清洗/分类数据集。
- 云端训练脚本。
- 本地桌面程序源码。
- 结项论文和 PPT 提纲。
- 云端环境与训练记录。

## 结项材料建议

论文重点写：

- 数据清洗与数据集构建。
- 三类车型映射方法。
- StyleGAN2-ADA 迁移训练。
- 云端 RTX 5090 训练环境。
- 三类模型训练结果。
- 桌面程序设计与打包部署。
- 系统局限与改进方向。

PPT 演示建议：

1. 项目目标。
2. 技术路线。
3. 数据集构建。
4. 云端训练过程。
5. 三类生成结果展示。
6. 桌面系统演示。
7. 安装包与结项成果。
