# SRTP Baseline 说明文档

## 1. Baseline 目标

本 Baseline 用于验证以下最小闭环是否成立：

**CompCars 原始整车图 → 数据清洗 → 训练集打包 → StyleGAN2-ADA 训练 → 生成结果查看**

当前 Baseline 的目标不是最终系统，而是先验证：

1. 数据是否可用于训练汽车生成模型
2. StyleGAN2-ADA 是否能在本机环境中正常训练
3. 模型是否能够学习到“前侧汽车外观图”的基本分布
4. 为后续条件生成与可控生成提供基础模型与流程

---

## 2. Baseline 技术路线

当前 Baseline 的技术路线为：

- **训练骨架**：`NVlabs/stylegan2-ada-pytorch`
- **原始数据集**：`CompCars`
- **训练任务**：无条件生成（unconditional generation）
- **图像分辨率**：`256 × 256`
- **视角选择**：仅保留 `front-side`

---

## 3. 原始数据结构

CompCars 解压后，当前实际使用的数据目录如下：

```text
D:\car_srtp_project\data\raw_compcars\
├─ image
├─ label
├─ misc
├─ part
└─ train_test_split

其中本 Baseline 只使用：

image/：整车图像

label/：与整车图对应的视角与边界框标注

misc/：保留备用，后续可用于车型类别与属性信息

根据数据集自带 README：

image/ 目录存放整车图像，路径格式为 make_id/model_id/released_year/image_name.jpg。

README

label/ 目录存放与图像一一对应的标注文件，第一行为视角标注，第三行为 bounding box 坐标。

README

misc/attributes.txt 中包含车型属性与 type 信息。

README

4. Baseline 数据处理流程
4.1 第一步：从原始数据中筛出 front-side 视角图像

当前第一版数据清洗脚本为：

D:\car_srtp_project\experiments\prepare_compcars_v1.py
脚本作用

该脚本完成以下工作：

递归扫描 raw_compcars/image/ 中的整车图像

在 raw_compcars/label/ 中查找同路径对应标注文件

读取标注文件中的：

视角信息

边界框坐标

仅保留 viewpoint = 4 的图像，即 front-side

根据 bounding box 裁剪出车辆主体

过滤异常图像：

缺失标注

标注损坏

非目标视角

bbox 非法

裁剪后过小

将结果保存到：

D:\car_srtp_project\data\compcars_cleaned_v1\all
当前清洗结果

运行 prepare_compcars_v1.py 后得到的统计结果为：

原始整车图总数：136726

保留的 front-side 图像数：49172

其余大部分被筛掉的图像是因为视角不符合要求。

4.2 第二步：将裁剪图统一处理为 256×256 正方形

由于 StyleGAN2-ADA 训练要求输入图像尺寸统一，且为正方形，因此不能直接使用 bbox 裁剪后的长方形图像。

当前正式使用的第二版处理脚本为：

D:\car_srtp_project\experiments\prepare_compcars_v2_inplace.py
脚本作用

该脚本对 compcars_cleaned_v1/all/ 中的图片进行原地处理：

读取第一版已裁剪出的车图

按长边补边扩展成正方形

使用浅灰背景填充空白区域

将图像缩放到 256 × 256

使用临时文件写入后替换原图，避免处理中断损坏原文件

参数设置

TARGET_SIZE = 256

PADDING_RATIO = 0.06

JPEG_QUALITY = 95

处理结果

运行后，compcars_cleaned_v1/all/ 目录中的全部 49172 张图像被统一处理为：

正方形

256 × 256

保留车辆主体、不再额外中心裁剪

5. Baseline 数据保存位置
5.1 原始数据
D:\car_srtp_project\data\raw_compcars\
5.2 第一版清洗结果（front-side + bbox 裁剪）
D:\car_srtp_project\data\compcars_cleaned_v1\all\
5.3 第二版清洗结果

第二版采用原地覆盖策略，因此仍保存在：

D:\car_srtp_project\data\compcars_cleaned_v1\all\

此时该目录中的图像已经全部变为：

256 × 256

正方形

补边后的训练输入图像

5.4 StyleGAN2-ADA 训练数据包

后续使用 dataset_tool.py 打包后，保存为：

D:\car_srtp_project\data\compcars_cleaned_v1_256_square.zip
6. Baseline 相关脚本与作用
6.1 数据清洗脚本
prepare_compcars_v1.py

路径：

D:\car_srtp_project\experiments\prepare_compcars_v1.py

作用：

从原始数据中筛出 front-side

按 bbox 裁剪车辆主体

生成第一版可用训练图像

prepare_compcars_v2_inplace.py

路径：

D:\car_srtp_project\experiments\prepare_compcars_v2_inplace.py

作用：

将第一版裁剪图补边成正方形

缩放为 256 × 256

原地覆盖保存，形成最终训练输入图像

6.2 数据打包脚本
dataset_tool.py

路径：

D:\car_srtp_project\refs\stylegan2-ada-pytorch\dataset_tool.py

作用：

将图片目录转换为 StyleGAN2-ADA 可直接训练的 zip 数据集

用于后续 train.py 读取

示例命令：

cd D:\car_srtp_project\refs\stylegan2-ada-pytorch
python dataset_tool.py --source=D:\car_srtp_project\data\compcars_cleaned_v1\all --dest=D:\car_srtp_project\data\compcars_cleaned_v1_256_square.zip
6.3 训练脚本
train.py

路径：

D:\car_srtp_project\refs\stylegan2-ada-pytorch\train.py

作用：

执行 StyleGAN2-ADA 模型训练

输出 snapshot、日志、样本网格图等训练结果

6.4 生成脚本
generate.py

路径：

D:\car_srtp_project\refs\stylegan2-ada-pytorch\generate.py

作用：

加载训练好的 .pkl 模型

生成随机样本图像

用于训练后效果查看

7. Baseline 训练命令

当前建议的第一轮 baseline 训练命令如下：

cd D:\car_srtp_project\refs\stylegan2-ada-pytorch
python train.py --outdir=D:\car_srtp_project\outputs\stylegan2ada_runs --data=D:\car_srtp_project\data\compcars_cleaned_v1_256_square.zip --gpus=1 --cfg=auto --snap=10 --metrics=none --kimg=500 --mirror=1
8. Baseline 训练参数说明
--outdir

训练输出目录：

D:\car_srtp_project\outputs\stylegan2ada_runs

所有训练结果、snapshot、日志、样图都会保存在这里。

--data

训练数据集 zip 文件路径：

D:\car_srtp_project\data\compcars_cleaned_v1_256_square.zip
--gpus=1

使用单张 GPU 训练。

当前项目运行环境为：

RTX 5070 Ti Laptop GPU

12GB 显存

--cfg=auto

自动根据图像分辨率与 GPU 数量选择合适的 StyleGAN2-ADA 默认配置。

这是最适合第一轮 baseline 的选择。

--snap=10

每 10 个 tick 保存一次：

网络快照

样本网格图

训练状态

用于中途观察模型是否在正常学习。

--metrics=none

第一轮 baseline 关闭 FID 等指标计算，原因是：

节省训练时间

降低额外计算开销

先关注“是否能生成像车的图”

后续更正式实验可再启用指标评估。

--kimg=500

控制训练总量。

kimg 表示训练过程中“看到的图片数量 / 1000”。

kimg=500 适合作为第一轮 baseline 试跑，目标是：

验证训练流程

观察收敛趋势

查看生成结果是否开始像车

这不是最终长训版本，而是第一轮验证版。

--mirror=1

开启水平翻转增强。

对汽车前侧图像通常有帮助，可以提高有效数据多样性。

9. 如何查看 Baseline 训练结果

训练结果保存在：

D:\car_srtp_project\outputs\stylegan2ada_runs\

每次训练会在该目录下生成一个新的子目录，通常名字类似：

00000-...
00001-...
...

进入某次训练目录后，通常可以看到：

network-snapshot-xxxxxx.pkl

fakesxxxxxx.png

training_options.json

log.txt 或类似日志文件

9.1 查看样本网格图

最直观的是查看：

fakes*.png

这些是训练过程中定期保存的生成图网格。可以用来观察：

是否从噪声逐渐变成车

是否学到前侧车图结构

是否存在明显模式崩塌

9.2 查看模型快照

训练中会保存：

network-snapshot-xxxxxx.pkl

这是后续生成图像和继续训练最重要的文件。

9.3 查看训练配置

训练目录中的：

training_options.json

保存了该次训练的参数设置，用于复现实验。

9.4 查看日志

训练目录中的日志文件可用于查看：

当前训练进度

tick 变化

kimg 进度

显存占用

训练速度

10. 如何用训练好的 Baseline 模型生成图像

当训练完成并得到 .pkl 模型后，可以使用 generate.py 生成图像。

示例命令：

cd D:\car_srtp_project\refs\stylegan2-ada-pytorch
python generate.py --outdir=D:\car_srtp_project\outputs\generated_samples --trunc=0.7 --seeds=1,2,3,4 --network=D:\car_srtp_project\outputs\stylegan2ada_runs\00000-...\network-snapshot-000500.pkl
参数说明

--outdir：生成图片保存目录

--trunc=0.7：控制生成样本的保守程度

--seeds=1,2,3,4：随机种子

--network：训练好的模型文件路径

11. Baseline 训练结果怎么看算“正常”

第一轮 baseline 训练中，正常现象通常是：

初期

输出几乎像噪声

只有模糊色块与几何块

中前期

轮廓开始像车

轮子、车灯、大致前脸逐渐出现

中期

能明显看出前侧汽车结构

背景与细节仍可能较乱

后期

车体结构更稳定

轮毂、前脸、车灯等局部更加清晰

只要样本网格图整体趋势是“越来越像车”，说明 baseline 成功。

12. 当前 Baseline 的定位

当前 Baseline 的定位是：

第一轮无条件汽车生成验证

不追求最终视觉极致

不追求可控生成

不追求最终论文指标最优

它的任务是为后续工作提供基础：

更长时间训练

更精细数据清洗

sedan / SUV / sports car 分类

颜色标签

条件生成

SeFa 潜空间控制

Demo 系统封装

13. 后续计划

在当前 Baseline 完成后，建议按以下顺序继续推进：

完成第一轮 baseline 训练

检查训练样本与模型快照

使用 generate.py 导出生成样本

判断数据是否还需二次清洗

再决定是否进行：

更长训练

条件标签构建

SeFa 控制接入

Demo 可交互化

14. 当前 Baseline 相关路径总览
原始数据
D:\car_srtp_project\data\raw_compcars\
处理后训练图像
D:\car_srtp_project\data\compcars_cleaned_v1\all\
训练数据 zip
D:\car_srtp_project\data\compcars_cleaned_v1_256_square.zip
数据脚本
D:\car_srtp_project\experiments\prepare_compcars_v1.py
D:\car_srtp_project\experiments\prepare_compcars_v2_inplace.py
StyleGAN2-ADA 仓库
D:\car_srtp_project\refs\stylegan2-ada-pytorch\
训练输出
D:\car_srtp_project\outputs\stylegan2ada_runs\
15. 说明

本 README 用于记录 SRTP 项目当前 Baseline 的数据准备、脚本组织、训练命令与结果查看方式，作为后续复现实验、继续训练和撰写阶段性报告的统一基线。