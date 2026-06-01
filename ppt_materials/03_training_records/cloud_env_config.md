# 云端训练环境配置记录

更新时间：2026-05-30

## 1. 云服务器订单与硬件

- 订单 ID：7801261754203532996
- 订单类型：新购容器实例
- 计费方式：包年包月
- 购买时长：1 周
- 主机区域：西北 B 区
- GPU：NVIDIA GeForce RTX 5090
- GPU 数量：1 卡
- 显存：32GB
- CPU：25 核/GPU
- CPU 型号：Intel(R) Xeon(R) Platinum 8470Q
- 内存：90GB/GPU
- 存储：
  - 免费：50GB
  - 付费：150GB

## 2. 镜像与基础软件

- 操作系统：Ubuntu 22.04
- 镜像：PyTorch 2.7.0 + Python 3.12 + CUDA 12.8
- 实际 Python 版本：Python 3.12.3
- NVIDIA Driver：580.105.08
- `nvidia-smi` 显示 CUDA Version：13.0
- PyTorch CUDA Runtime：12.8

说明：`nvidia-smi` 中的 CUDA Version 表示驱动最高支持的 CUDA 版本；训练实际使用的是 PyTorch 自带的 CUDA runtime，即 12.8。

## 3. GPU 与 PyTorch 验证结果

云端已执行 PyTorch 检查，结果如下：

```text
torch = 2.7.0+cu128
torch cuda runtime = 12.8
cuda available = True
device = NVIDIA GeForce RTX 5090
capability = (12, 0)
arch list = ['sm_75', 'sm_80', 'sm_86', 'sm_90', 'sm_100', 'sm_120', 'compute_120']
matmul ok = torch.Size([2048, 2048]) torch.float32 cuda:0
```

结论：当前云端环境能够正确识别 RTX 5090，支持 Blackwell 架构 `sm_120`，可用于本项目 StyleGAN2-ADA 训练。

## 4. 当前终端与磁盘信息

当前云端终端：

```text
root@autodl-container-fzhvmb6n9v-9380c5ea:~#
```

当前工作目录：

```text
/root
```

推荐项目目录：

```text
/root/autodl-tmp/car_srtp_project
```

已确认 `/root/autodl-tmp` 目录存在。

## 5. 推荐云端项目目录结构

```text
/root/autodl-tmp/car_srtp_project/
  data/
    compcars_cleaned_v1_256_square.zip
  refs/
    stylegan2-ada-pytorch/
  outputs/
    stylegan2ada_runs/
      baseline_240/
        network-snapshot-000240.pkl
        training_options.json
        log.txt
        stats.jsonl
    final_samples/
```

## 6. 本地待上传核心资产

本地项目路径：

```text
D:\car_srtp_project
```

需要上传的核心资产：

```text
D:\car_srtp_project\data\compcars_cleaned_v1_256_square.zip
D:\car_srtp_project\refs\stylegan2-ada-pytorch\
D:\car_srtp_project\outputs\stylegan2ada_runs\00000-compcars_cleaned_v1_256_square-mirror-auto1-kimg500\network-snapshot-000240.pkl
D:\car_srtp_project\outputs\stylegan2ada_runs\00000-compcars_cleaned_v1_256_square-mirror-auto1-kimg500\training_options.json
D:\car_srtp_project\outputs\stylegan2ada_runs\00000-compcars_cleaned_v1_256_square-mirror-auto1-kimg500\log.txt
D:\car_srtp_project\outputs\stylegan2ada_runs\00000-compcars_cleaned_v1_256_square-mirror-auto1-kimg500\stats.jsonl
```

文件大小记录：

- 数据集 zip：约 9.03GB
- 续训权重 `network-snapshot-000240.pkl`：约 270MB

注意：必须上传本地已修改过的 `refs/stylegan2-ada-pytorch`，不要在云端重新 clone 原版仓库，因为本地版本已经针对新版 PyTorch / 50 系 GPU 环境做过兼容修补。

## 7. 训练策略

先进行 4 kimg 冒烟测试，确认数据、权重、依赖和自定义算子路径均可运行。

冒烟测试通过后，再使用 `tmux` 后台启动正式续训。

推荐正式训练目标：

- 保底：续训到 500 kimg
- 推荐：续训到 800 kimg
- 如果时间和效果允许：续训到 1000 kimg

推荐初始训练参数：

```text
--gpus=1
--cfg=auto
--mirror=1
--aug=ada
--batch=16
--workers=4
--snap=10
--metrics=fid50k_full
--resume=/root/autodl-tmp/car_srtp_project/outputs/stylegan2ada_runs/baseline_240/network-snapshot-000240.pkl
```

若遇到显存、内存或数据加载问题，可降级为：

```text
--batch=8
--workers=2
--metrics=none
```

## 8. 环境风险与处理

- Python 3.12 比 StyleGAN2-ADA 原项目常用环境更新，若出现依赖兼容问题，切换到 Python 3.10 conda 环境。
- 5090 必须使用支持 `sm_120` 的 PyTorch CUDA 12.8 环境；当前镜像已验证符合要求。
- 云端训练不要放在 `/root` 系统盘，统一放在 `/root/autodl-tmp/car_srtp_project`。
- 长时间训练应使用 `tmux`，避免本地浏览器或 SSH 断开导致训练中断。

## 9. 三类型可选生成路线

立项要求系统能够根据选择生成三类汽车外观图：

- 跑车
- 轿车
- SUV

当前采用“分类型微调模型”路线实现该要求，而不是单一条件模型。具体做法：

1. 使用全部清洗数据训练得到通用 StyleGAN2-ADA baseline。
2. 根据 CompCars 车型属性将清洗后的汽车图片划分为跑车、轿车、SUV 三类。
3. 分别以通用 baseline 的 `network-snapshot-000240.pkl` 为初始化权重微调三类模型。
4. 桌面程序中根据用户选择加载对应模型：

```text
跑车 -> outputs/final_models/sports.pkl
轿车 -> outputs/final_models/sedan.pkl
SUV  -> outputs/final_models/suv.pkl
```

该路线优点是稳定、可复用已有训练权重、能够直接满足“按三类选择生成”的结项演示要求。

## 10. 三类型数据集划分

本地已生成三类 StyleGAN2-ADA 训练数据集：

```text
data/type_datasets/compcars_sports_256_square.zip
data/type_datasets/compcars_sedan_256_square.zip
data/type_datasets/compcars_suv_256_square.zip
data/type_datasets/srtp_type_mapping.json
```

类别映射文件：

```json
{
  "2": "suv",
  "4": "sedan",
  "9": "sports",
  "10": "suv",
  "11": "sports",
  "12": "sports"
}
```

类别数量：

```text
sports: 1519 张
sedan: 5492 张
suv: 9889 张
```

云端数据路径：

```text
/root/autodl-tmp/car_srtp_project/data/type_datasets/
```

云端已上传文件：

```text
compcars_sports_256_square.zip
compcars_sedan_256_square.zip
compcars_suv_256_square.zip
srtp_type_mapping.json
```

## 11. 正式训练方法与参数

当前正式训练采用总控脚本：

```text
/root/autodl-tmp/car_srtp_project/scripts/cloud_train_all_type_models.sh
```

脚本功能：

1. 顺序训练跑车模型。
2. 训练完成后复制最终模型为 `outputs/final_models/sports.pkl`。
3. 自动生成跑车样例图。
4. 顺序训练轿车模型。
5. 训练完成后复制最终模型为 `outputs/final_models/sedan.pkl`。
6. 自动生成轿车样例图。
7. 顺序训练 SUV 模型。
8. 训练完成后复制最终模型为 `outputs/final_models/suv.pkl`。
9. 自动生成 SUV 样例图。
10. 写入 `outputs/final_models/manifest.txt`。

当前启动命令：

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

每类训练均使用：

```text
--gpus=1
--cfg=auto
--mirror=1
--aug=ada
--batch=16
--workers=4
--snap=10
--metrics=none
--resume=/root/autodl-tmp/car_srtp_project/outputs/stylegan2ada_runs/baseline_240/network-snapshot-000240.pkl
```

说明：

- 当前三类模型为 256 x 256 分辨率。
- 第一轮正式训练不盲目跑满一周，而是先产出可用模型和样例图。
- 若样例质量不足，再追加训练到更高 kimg。
- 若要提升到 512 分辨率，需要重新构建 512 数据集，不是简单修改训练参数。

## 12. 当前正式训练启动方式

云端环境没有安装 `tmux`，因此使用 `nohup` 后台运行。

启动命令：

```bash
mkdir -p /root/autodl-tmp/car_srtp_project/outputs/logs

LOG=/root/autodl-tmp/car_srtp_project/outputs/logs/train_all_types_$(date +%Y%m%d_%H%M%S).log

nohup /root/autodl-tmp/car_srtp_project/scripts/cloud_train_all_type_models.sh 800 1000 1000 16 > "$LOG" 2>&1 &

echo $! > /root/autodl-tmp/car_srtp_project/outputs/logs/train_all_types.pid
echo "PID: $(cat /root/autodl-tmp/car_srtp_project/outputs/logs/train_all_types.pid)"
echo "LOG: $LOG"
```

当前训练已经成功启动，并进入跑车模型训练阶段。日志中已出现：

```text
Training for 800 kimg...
tick 0     kimg 0.0      ... gpumem 17.55
tick 1     kimg 4.0      ... sec/kimg 12.14 ... gpumem 4.76
```

根据 `tick 1` 速度粗略估算：

```text
1 kimg 约 12 秒
sports 800 kimg 约 2.7 小时
sedan 1000 kimg 约 3.4 小时
suv 1000 kimg 约 3.4 小时
总计约 10-12 小时，实际以日志为准
```

## 13. 训练查看与监控方式

### 13.1 查看 GPU 是否正在训练

```bash
nvidia-smi
```

正常训练时应看到 Python 进程占用 GPU 显存，GPU 利用率不为 0。

### 13.2 查看后台训练进程

```bash
ps -fp $(cat /root/autodl-tmp/car_srtp_project/outputs/logs/train_all_types.pid)
```

如果能看到对应 PID 的进程，说明总控脚本仍在运行。

### 13.3 实时查看训练日志

```bash
tail -f /root/autodl-tmp/car_srtp_project/outputs/logs/train_all_types_*.log
```

退出日志查看：

```text
Ctrl+C
```

注意：这里的 `Ctrl+C` 只会退出 `tail -f`，不会停止后台训练。

### 13.4 查看日志最后 40 行

```bash
tail -n 40 /root/autodl-tmp/car_srtp_project/outputs/logs/train_all_types_*.log
```

### 13.5 查看当前训练到了哪一类

```bash
grep -n "Training " /root/autodl-tmp/car_srtp_project/outputs/logs/train_all_types_*.log
```

预期会依次出现：

```text
Training sports for 800 kimg
Training sedan for 1000 kimg
Training suv for 1000 kimg
```

### 13.6 查看各类训练输出目录

```bash
ls -lt /root/autodl-tmp/car_srtp_project/outputs/type_models/sports
ls -lt /root/autodl-tmp/car_srtp_project/outputs/type_models/sedan
ls -lt /root/autodl-tmp/car_srtp_project/outputs/type_models/suv
```

每个训练目录中应包含：

```text
fakes*.png
network-snapshot-*.pkl
log.txt
stats.jsonl
training_options.json
```

### 13.7 查看最终模型是否已生成

```bash
ls -lh /root/autodl-tmp/car_srtp_project/outputs/final_models/
```

训练全部完成后应看到：

```text
sports.pkl
sedan.pkl
suv.pkl
manifest.txt
```

### 13.8 查看最终样例图

```bash
ls -lh /root/autodl-tmp/car_srtp_project/outputs/final_samples/sports/
ls -lh /root/autodl-tmp/car_srtp_project/outputs/final_samples/sedan/
ls -lh /root/autodl-tmp/car_srtp_project/outputs/final_samples/suv/
```

每类默认生成 `seed=0-31`、`trunc=0.7` 的 32 张样例图。

## 14. 训练完成后的工作

训练全部完成后，需要执行以下工作。

### 14.1 检查最终模型

```bash
ls -lh /root/autodl-tmp/car_srtp_project/outputs/final_models/
cat /root/autodl-tmp/car_srtp_project/outputs/final_models/manifest.txt
```

确认存在：

```text
sports.pkl
sedan.pkl
suv.pkl
manifest.txt
```

### 14.2 检查最终样例图

```bash
find /root/autodl-tmp/car_srtp_project/outputs/final_samples -maxdepth 2 -type f | head
```

需要人工筛选：

- 每类至少选 10 张效果较好的图片。
- 总计至少 30 张汽车外观样例图。
- PPT 中建议每类展示 6-9 张。
- 论文中建议每类展示 3-6 张。

### 14.3 下载最终成果到本地

建议下载以下目录：

```text
/root/autodl-tmp/car_srtp_project/outputs/final_models/
/root/autodl-tmp/car_srtp_project/outputs/final_samples/
/root/autodl-tmp/car_srtp_project/outputs/logs/
/root/autodl-tmp/car_srtp_project/outputs/type_models/
```

本地 PowerShell 下载示例：

```powershell
scp -P 10940 -r root@connect.westb.seetacloud.com:/root/autodl-tmp/car_srtp_project/outputs/final_models D:\car_srtp_project\outputs\
scp -P 10940 -r root@connect.westb.seetacloud.com:/root/autodl-tmp/car_srtp_project/outputs/final_samples D:\car_srtp_project\outputs\
scp -P 10940 -r root@connect.westb.seetacloud.com:/root/autodl-tmp/car_srtp_project/outputs/logs D:\car_srtp_project\outputs\
```

### 14.4 桌面程序开发

桌面程序应使用三个最终模型：

```text
app/models/sports.pkl
app/models/sedan.pkl
app/models/suv.pkl
```

界面功能：

- 车型选择：跑车、轿车、SUV
- 参数设置：随机种子、truncation、生成数量
- 生成图片
- 保存图片
- 记录生成参数
- 历史图库浏览

系统逻辑：

```text
选择跑车 -> 加载 sports.pkl
选择轿车 -> 加载 sedan.pkl
选择 SUV  -> 加载 suv.pkl
```

### 14.5 论文与 PPT 使用材料

论文和 PPT 需要使用以下材料：

- 数据集构建过程：
  - `srtp_type_mapping.json`
  - 三类样本数量
- 模型训练过程：
  - `training_options.json`
  - `log.txt`
  - `stats.jsonl`
  - `manifest.txt`
- 生成结果：
  - `final_samples/sports/`
  - `final_samples/sedan/`
  - `final_samples/suv/`
- 系统实现：
  - 桌面程序截图
  - 三类选择生成流程图

论文推荐表述：

```text
本项目采用分类型微调策略实现三类汽车外观可控生成。首先基于清洗后的 CompCars 汽车外观数据训练通用 StyleGAN2-ADA 基线模型；随后依据车型属性将数据划分为跑车、轿车和 SUV 三类，并以通用基线模型为初始化权重分别微调三个类型生成模型。桌面端根据用户选择加载对应模型，从而实现三类汽车外观概念图的定向生成。
```

### 14.6 是否追加训练

第一轮完成后先检查生成图质量。若某类效果不足，可单独追加训练：

```text
sports: 追加到 1500-2000 kimg
sedan: 追加到 2500-3500 kimg
suv: 追加到 3000-4000 kimg
```

不建议盲目把 256 分辨率模型训练六天六夜，因为数据量有限，尤其跑车类只有 1519 张，训练过久可能过拟合。

若要提升分辨率，应单独构建 512 x 512 数据集并作为增强实验，不影响当前 256 x 256 三类模型主线。
## 15. 追加训练记录

### 15.1 追加训练原因

第一轮三类正式训练已经完成。当前三类最终 `fakes` 图片已经初步具备车辆形状，且跑车、轿车、SUV 三类模型生成结果之间已经存在明显差异。

但第一轮最终生成图的质量仍未达到结项展示要求，因此决定继续追加训练。追加训练从第一轮已经完成的三类最终模型继续，而不是回到通用 baseline 重新训练。

### 15.2 当前追加训练路线

追加训练起点：

```text
/root/autodl-tmp/car_srtp_project/outputs/final_models/sports.pkl
/root/autodl-tmp/car_srtp_project/outputs/final_models/sedan.pkl
/root/autodl-tmp/car_srtp_project/outputs/final_models/suv.pkl
```

新增脚本：

```text
/root/autodl-tmp/car_srtp_project/scripts/cloud_train_type_from_resume.sh
/root/autodl-tmp/car_srtp_project/scripts/cloud_continue_all_type_models.sh
```

追加训练命令：

```bash
mkdir -p /root/autodl-tmp/car_srtp_project/outputs/logs

LOG=/root/autodl-tmp/car_srtp_project/outputs/logs/continue_all_types_$(date +%Y%m%d_%H%M%S).log

nohup /root/autodl-tmp/car_srtp_project/scripts/cloud_continue_all_type_models.sh 1000 1500 1500 16 > "$LOG" 2>&1 &

echo $! > /root/autodl-tmp/car_srtp_project/outputs/logs/continue_all_types.pid
echo "PID: $(cat /root/autodl-tmp/car_srtp_project/outputs/logs/continue_all_types.pid)"
echo "LOG: $LOG"
```

追加训练参数：

```text
sports: +1000 kimg
sedan:  +1500 kimg
suv:    +1500 kimg
batch:  16
```

每类训练参数保持：

```text
--gpus=1
--cfg=auto
--mirror=1
--aug=ada
--batch=16
--workers=4
--snap=10
--metrics=none
```

与第一轮不同的是，本轮 `--resume` 分别指向第一轮已经完成的最终模型：

```text
--resume=/root/autodl-tmp/car_srtp_project/outputs/final_models/sports.pkl
--resume=/root/autodl-tmp/car_srtp_project/outputs/final_models/sedan.pkl
--resume=/root/autodl-tmp/car_srtp_project/outputs/final_models/suv.pkl
```

### 15.3 追加训练产物

追加训练脚本会先备份第一轮模型：

```text
/root/autodl-tmp/car_srtp_project/outputs/final_models_archive/
```

每类追加训练完成后会刷新：

```text
/root/autodl-tmp/car_srtp_project/outputs/final_models/sports.pkl
/root/autodl-tmp/car_srtp_project/outputs/final_models/sedan.pkl
/root/autodl-tmp/car_srtp_project/outputs/final_models/suv.pkl
```

并重新生成最终样例图：

```text
/root/autodl-tmp/car_srtp_project/outputs/final_samples/sports/
/root/autodl-tmp/car_srtp_project/outputs/final_samples/sedan/
/root/autodl-tmp/car_srtp_project/outputs/final_samples/suv/
```

追加训练样例图设置：

```text
seeds: 0-47
trunc: 0.65
```

追加训练信息会追加写入：

```text
/root/autodl-tmp/car_srtp_project/outputs/final_models/manifest.txt
```

### 15.4 追加训练查看方式

查看 GPU：

```bash
nvidia-smi
```

查看追加训练进程：

```bash
ps -fp $(cat /root/autodl-tmp/car_srtp_project/outputs/logs/continue_all_types.pid)
```

实时查看追加训练日志：

```bash
tail -f /root/autodl-tmp/car_srtp_project/outputs/logs/continue_all_types_*.log
```

只看最后 60 行：

```bash
tail -n 60 /root/autodl-tmp/car_srtp_project/outputs/logs/continue_all_types_*.log
```

查看当前追加训练到了哪一类：

```bash
grep -n "Continuing " /root/autodl-tmp/car_srtp_project/outputs/logs/continue_all_types_*.log
```

预期顺序：

```text
Continuing sports for +1000 kimg
Continuing sedan for +1500 kimg
Continuing suv for +1500 kimg
```

查看追加训练输出目录：

```bash
ls -lt /root/autodl-tmp/car_srtp_project/outputs/type_models_continue/sports
ls -lt /root/autodl-tmp/car_srtp_project/outputs/type_models_continue/sedan
ls -lt /root/autodl-tmp/car_srtp_project/outputs/type_models_continue/suv
```

### 15.5 追加训练完成后的工作

1. 检查最终模型是否刷新：

```bash
ls -lh /root/autodl-tmp/car_srtp_project/outputs/final_models/
tail -n 120 /root/autodl-tmp/car_srtp_project/outputs/final_models/manifest.txt
```

2. 检查三类最终样例图：

```bash
ls -lh /root/autodl-tmp/car_srtp_project/outputs/final_samples/sports/
ls -lh /root/autodl-tmp/car_srtp_project/outputs/final_samples/sedan/
ls -lh /root/autodl-tmp/car_srtp_project/outputs/final_samples/suv/
```

3. 下载最终模型、样例图和日志到本地：

```powershell
scp -P 10940 -r root@connect.westb.seetacloud.com:/root/autodl-tmp/car_srtp_project/outputs/final_models D:\car_srtp_project\outputs\
scp -P 10940 -r root@connect.westb.seetacloud.com:/root/autodl-tmp/car_srtp_project/outputs/final_samples D:\car_srtp_project\outputs\
scp -P 10940 -r root@connect.westb.seetacloud.com:/root/autodl-tmp/car_srtp_project/outputs/logs D:\car_srtp_project\outputs\
```

4. 人工筛选最终生成图：

```text
每类至少筛选 10 张较好样例
总计至少 30 张用于论文和 PPT
保留 3-6 张失败样例用于论文“不足与分析”
```

5. 进入桌面应用开发阶段：

```text
app/models/sports.pkl
app/models/sedan.pkl
app/models/suv.pkl
```

桌面端根据用户车型选择加载对应模型，实现跑车、轿车、SUV 三类汽车外观生成。
