# car_srtp_project

重庆大学 SRTP 项目：**基于生成对抗网络的汽车外观设计辅助系统（现实风）**

当前阶段目标不是直接做最终系统，而是先完成第一轮 **Baseline 最小闭环验证**：

**CompCars 原始整车图 → 数据清洗 → 数据打包 → StyleGAN2-ADA 训练 → 生成结果查看**。:contentReference[oaicite:0]{index=0}

---

## 1. 当前项目阶段

当前项目处于 **Baseline 验证阶段**，定位为：

- 第一轮无条件汽车生成验证
- 不追求最终视觉极致
- 不追求可控生成
- 不追求最终论文指标最优
- 目标是先验证数据、环境、训练流程和生成结果是否能形成完整闭环，为后续条件生成、SeFa 控制和 Demo 系统奠定基础。:contentReference[oaicite:1]{index=1}

---

## 2. 当前技术路线

本阶段技术路线如下：

- **训练骨架**：`NVlabs/stylegan2-ada-pytorch`
- **原始数据集**：`CompCars`
- **训练任务**：无条件生成（unconditional generation）
- **图像分辨率**：`256 × 256`
- **视角选择**：仅保留 `front-side` 车辆图像。:contentReference[oaicite:2]{index=2}

---

## 3. 当前项目目录建议

```text
D:\car_srtp_project\
├─ data\
│  ├─ raw_compcars\
│  ├─ compcars_cleaned_v1\
│  └─ compcars_cleaned_v1_256_square.zip
├─ experiments\
│  ├─ prepare_compcars_v1.py
│  └─ prepare_compcars_v2_inplace.py
├─ refs\
│  └─ stylegan2-ada-pytorch\
├─ outputs\
│  └─ stylegan2ada_runs\
└─ README.md
4. 当前环境说明
4.1 Python 与 Conda 环境

当前正式训练环境为：

Conda 环境名：car_srtp_clean

Python 版本：3.10.19

该环境用于本项目的全部 Baseline 训练工作。

4.2 GPU 与深度学习环境

当前已验证可用的训练核心环境：

GPU：NVIDIA GeForce RTX 5070 Ti Laptop GPU

PyTorch：2.10.0+cu128

CUDA Runtime：12.8

已确认支持 sm_120

已确认可以在 GPU 上正常创建和计算张量

这说明当前环境已经具备运行本项目 Baseline 的基础条件。

4.3 Windows 下的额外要求

由于 stylegan2-ada-pytorch 在 Windows 下会编译自定义 CUDA / C++ 算子，因此除了 Python 环境外，还要求：

安装 Visual Studio Build Tools

安装 MSVC C++ x64 编译工具

训练前必须进入 x64 Developer Command Prompt 或手动执行：

call "C:\Program Files (x86)\Microsoft Visual Studio\18\BuildTools\VC\Auxiliary\Build\vcvars64.bat"

如果没有正确加载 x64 编译环境，训练可能报错：

Could not find MSVC/GCC/CLANG installation

自定义 op 编译失败

回退到 reference implementation

进一步出现 backward 相关错误

5. 当前 Baseline 数据说明
5.1 原始数据

原始数据目录：

D:\car_srtp_project\data\raw_compcars\

CompCars 当前实际用到的主要目录为：

image/：整车图像

label/：与图像对应的视角与边界框标注

misc/：备用，后续可用于车型类别与属性信息。

README_baseline

5.2 数据清洗结果

当前数据清洗分两步：

第一步：筛选 front-side + bbox 裁剪

脚本：

D:\car_srtp_project\experiments\prepare_compcars_v1.py

作用：

扫描原始整车图

读取对应 label

仅保留 viewpoint = 4，即 front-side

根据 bounding box 裁剪车辆主体

过滤异常图像。

README_baseline

统计结果：

原始整车图总数：136726

保留的 front-side 图像数：49172。

README_baseline

输出目录：

D:\car_srtp_project\data\compcars_cleaned_v1\all\
第二步：统一为 256 × 256 正方形

脚本：

D:\car_srtp_project\experiments\prepare_compcars_v2_inplace.py

作用：

对第一版裁剪结果原地处理

按长边补边扩展为正方形

使用浅灰背景填充

缩放到 256 × 256

原地覆盖保存。

README_baseline

处理完成后，compcars_cleaned_v1/all/ 中的全部 49172 张图像已经统一为：

正方形

256 × 256

保留车辆主体

可直接作为 StyleGAN2-ADA 的训练输入。

README_baseline

5.3 最终训练数据包

训练数据 zip 路径：

D:\car_srtp_project\data\compcars_cleaned_v1_256_square.zip

该 zip 由 dataset_tool.py 从清洗后的图片目录打包生成，供 train.py 直接读取。

README_baseline

6. 相关脚本
6.1 数据清洗脚本
prepare_compcars_v1.py

路径：

D:\car_srtp_project\experiments\prepare_compcars_v1.py

作用：

筛出 front-side

bbox 裁剪车辆主体

生成第一版训练图像。

README_baseline

prepare_compcars_v2_inplace.py

路径：

D:\car_srtp_project\experiments\prepare_compcars_v2_inplace.py

作用：

将第一版裁剪图补边为正方形

缩放为 256 × 256

原地覆盖保存。

README_baseline

6.2 数据打包脚本
dataset_tool.py

路径：

D:\car_srtp_project\refs\stylegan2-ada-pytorch\dataset_tool.py

作用：

将图片目录转换为 StyleGAN2-ADA 可读取的 zip 数据集。

README_baseline

示例命令：

cd /d D:\car_srtp_project\refs\stylegan2-ada-pytorch
python dataset_tool.py --source=D:\car_srtp_project\data\compcars_cleaned_v1\all --dest=D:\car_srtp_project\data\compcars_cleaned_v1_256_square.zip
6.3 训练脚本
train.py

路径：

D:\car_srtp_project\refs\stylegan2-ada-pytorch\train.py

作用：

执行 StyleGAN2-ADA 模型训练

输出 snapshot、日志、样本网格图等结果。

README_baseline

6.4 生成脚本
generate.py

路径：

D:\car_srtp_project\refs\stylegan2-ada-pytorch\generate.py

作用：

加载训练好的 .pkl

生成随机样本图像

用于训练结果查看。

README_baseline

7. 环境启动方法（Windows）
7.1 正确启动训练命令行

普通 PowerShell 直接训练不够，Windows 下推荐流程如下：

第一步：进入 Visual Studio x64 编译环境
cmd.exe /k """C:\Program Files (x86)\Microsoft Visual Studio\18\BuildTools\Common7\Tools\VsDevCmd.bat"""

如果需要强制切换到 x64：

call "C:\Program Files (x86)\Microsoft Visual Studio\18\BuildTools\VC\Auxiliary\Build\vcvars64.bat"

确认 cl 输出为 用于 x64 的 Microsoft C/C++ 编译器。

第二步：激活 conda 环境
call D:\anaconda\Scripts\activate.bat
conda activate car_srtp_clean
第三步：进入训练仓库
cd /d D:\car_srtp_project\refs\stylegan2-ada-pytorch
8. Baseline 训练命令

当前第一轮 Baseline 建议训练命令为：

python train.py --outdir=D:\car_srtp_project\outputs\stylegan2ada_runs --data=D:\car_srtp_project\data\compcars_cleaned_v1_256_square.zip --gpus=1 --cfg=auto --snap=10 --metrics=none --kimg=500 --mirror=1

该命令来自当前 Baseline 既定方案。

README_baseline

9. 训练参数说明

--outdir
训练输出目录：

D:\car_srtp_project\outputs\stylegan2ada_runs\

--data
训练数据 zip 路径：

D:\car_srtp_project\data\compcars_cleaned_v1_256_square.zip

--gpus=1
使用单张 GPU 训练

--cfg=auto
自动选择合适配置

--snap=10
每 10 个 tick 保存一次 snapshot 和样图

--metrics=none
第一轮 Baseline 不计算 FID 等指标，优先关注训练是否正常、样图是否开始像车

--kimg=500
第一轮验证版训练量

--mirror=1
开启水平翻转增强。

README_baseline

10. 如何查看训练结果

训练输出目录：

D:\car_srtp_project\outputs\stylegan2ada_runs\

每次训练会生成一个新的子目录，例如：

00000-...
00001-...

其中常见文件包括：

network-snapshot-xxxxxx.pkl

fakesxxxxxx.png

training_options.json

log.txt。

README_baseline

10.1 样本网格图

重点观察：

fakes*.png

训练过程中，正常趋势通常是：

初期接近噪声

中前期开始出现车体轮廓、轮子、车灯

中后期能看出前侧汽车结构逐渐稳定。

README_baseline

10.2 模型快照
network-snapshot-xxxxxx.pkl

这是后续继续训练和生成样本最重要的文件。

10.3 配置与日志

training_options.json：保存本次训练参数

log.txt：记录训练过程中的 tick、kimg、速度、显存等信息

11. 使用训练好的模型生成图像

示例命令：

cd /d D:\car_srtp_project\refs\stylegan2-ada-pytorch
python generate.py --outdir=D:\car_srtp_project\outputs\generated_samples --trunc=0.7 --seeds=1,2,3,4 --network=D:\car_srtp_project\outputs\stylegan2ada_runs\00000-...\network-snapshot-000500.pkl

作用：

根据训练好的 .pkl 生成随机样本图像

用于查看 Baseline 的学习效果。

README_baseline

12. 当前项目环境常见问题
12.1 ModuleNotFoundError: No module named 'psutil'

说明训练环境缺依赖。
解决：

pip install psutil
12.2 Could not find MSVC/GCC/CLANG installation

说明没有在正确的 Visual Studio 编译环境中启动训练。
解决：

打开 Developer Command Prompt

或手动执行 vcvars64.bat

确认 cl 为 x64 编译器后再训练

12.3 cl 在 PowerShell 中不可用

这通常不是没装，而是没有进入开发者命令行环境。
应通过 VsDevCmd.bat 或 vcvars64.bat 初始化后再使用。

12.4 首次训练卡顿

首次运行 train.py 时，StyleGAN2-ADA 可能会编译自定义 op，因此：

第一次启动会慢一些

风扇变响属正常现象

只要没有 traceback 直接退出，就先耐心等待

13. 当前阶段完成后的下一步

完成第一轮 Baseline 后，建议按以下顺序推进：

检查训练样本图与模型快照

用 generate.py 导出生成样本

判断数据是否需要二次清洗

再决定是否继续：

更长训练

条件标签构建

SeFa 潜空间控制

Demo 系统封装。

README_baseline

14. 当前 Baseline 路径总览

原始数据：

D:\car_srtp_project\data\raw_compcars\

处理后训练图像：

D:\car_srtp_project\data\compcars_cleaned_v1\all\

训练数据 zip：

D:\car_srtp_project\data\compcars_cleaned_v1_256_square.zip

数据脚本：

D:\car_srtp_project\experiments\prepare_compcars_v1.py
D:\car_srtp_project\experiments\prepare_compcars_v2_inplace.py

StyleGAN2-ADA 仓库：

D:\car_srtp_project\refs\stylegan2-ada-pytorch\

训练输出：

D:\car_srtp_project\outputs\stylegan2ada_runs\

以上路径与当前 Baseline 说明一致。

README_baseline

---

## 15. 固定启动流程（推荐）

为避免误用系统默认 Python（例如 `D:\Scripts\python.exe`，Python 3.13）导致训练失败，项目根目录新增统一启动脚本：

`D:\car_srtp_project\start_car_srtp_env.cmd`

该脚本会自动执行：

1. 初始化 Visual Studio x64 编译环境（`VsDevCmd.bat -arch=x64 -host_arch=x64`）
2. 激活 Conda 环境（`car_srtp_clean`）
3. 检查 `cl`、`python`、`torch`、`cuda` 是否可用
4. 自动切换到训练目录：`D:\car_srtp_project\refs\stylegan2-ada-pytorch`

使用方式：

```bat
cd /d D:\car_srtp_project
start_car_srtp_env.cmd
```

进入后再执行训练命令，避免环境漂移。

如果只想做一次环境自检（不进入交互命令行）：

```bat
start_car_srtp_env.cmd --no-shell
```

---

## 16. 性能优化建议（5070 Ti Laptop + Windows）

当前项目在你的设备上，建议优先使用：

- `--allow-tf32=1`
- `--aug=ada`
- `--batch=16`
- `--workers=3`
- `--metrics=none`（Baseline 阶段）

新增一键训练脚本：

`D:\car_srtp_project\run_train_fast.cmd`

示例：

```bat
cd /d D:\car_srtp_project
run_train_fast.cmd --outdir=D:\car_srtp_project\outputs\stylegan2ada_runs --data=D:\car_srtp_project\data\compcars_cleaned_v1_256_square.zip --kimg=500 --mirror=1 --snap=10
```

基于本机实测（2026-03-07）：

- 基线（`batch=16, ada, tf32=0`）：`sec/kimg ≈ 72.06`
- 优化后（`batch=16, ada, tf32=1`）：`sec/kimg ≈ 67.39`

说明：`batch=20/24` 或 `noaug` 在本机组合上实测更慢，不建议作为默认配置。

---

## 17. 当前真实状态（2026-03-07）

本节用于同步“当前机器 + 当前代码”下的真实状态，优先级高于历史说明。

### 17.1 训练是否使用 CUDA

结论：**正在使用 CUDA / GPU 训练**（不是 CPU 训练）。

- 设备：`NVIDIA GeForce RTX 5070 Ti Laptop GPU`
- 环境：`PyTorch 2.10.0+cu128`，`CUDA Runtime 12.8`
- 训练日志中可看到 `gpumem` 持续占用（约 7~10GB）

补充说明：

- `bias_act` 和 `upfirdn2d` 自定义 CUDA 插件在 Windows 下未成功编译；
- 当前会回退到参考实现（`reference implementation`），**功能正常但速度不是最优**。

### 17.2 兼容性修复状态

为兼容新版本 PyTorch（并适配 50 系新卡环境），已修改以下文件：

- `D:\car_srtp_project\refs\stylegan2-ada-pytorch\training\training_loop.py`
- `D:\car_srtp_project\refs\stylegan2-ada-pytorch\torch_utils\ops\grid_sample_gradfix.py`
- `D:\car_srtp_project\refs\stylegan2-ada-pytorch\torch_utils\ops\conv2d_gradfix.py`
- `D:\car_srtp_project\refs\stylegan2-ada-pytorch\torch_utils\ops\upfirdn2d.py`

当前可确认：`kimg=1` 冒烟训练可完整跑完并退出。

验证目录示例：

- `D:\car_srtp_project\outputs\compat_smoke_after_patch6\00000-compcars_cleaned_v1_256_square-auto1-kimg1`

### 17.3 当前推荐启动与训练方式

1. 固定进入环境（避免误用系统 Python 3.13）：

```bat
cd /d D:\car_srtp_project
start_car_srtp_env.cmd
```

2. 直接使用快速训练入口（已内置实测较优参数）：

```bat
cd /d D:\car_srtp_project
run_train_fast.cmd --outdir=D:\car_srtp_project\outputs\stylegan2ada_runs --data=D:\car_srtp_project\data\compcars_cleaned_v1_256_square.zip --kimg=500 --mirror=1 --snap=10
```

### 17.4 当前性能结论（本机实测）

- 基线（`batch=16, ada, tf32=0`）：`sec/kimg ≈ 72.06`
- 优化（`batch=16, ada, tf32=1`）：`sec/kimg ≈ 67.39`

不建议默认使用：

- `batch=20`（实测更慢）
- `batch=24`（实测更慢）
- `noaug`（实测更慢）
