# Win11 桌面程序打包方案

本项目采用两阶段打包：

1. 使用 PyInstaller 将 Python 桌面程序打包成 `dist/CarDesignAssistant/` 可运行目录。
2. 使用 Inno Setup 将该目录、三类模型和 StyleGAN2-ADA 运行代码打包成安装包。

## 1. 打包前准备

确认最终模型已经下载到：

```text
app/models/sports.pkl
app/models/sedan.pkl
app/models/suv.pkl
```

如果还没有，先运行：

```powershell
powershell -ExecutionPolicy Bypass -File scripts\download_final_assets.ps1
```

确认项目专用 Python 环境存在：

```text
D:\anaconda\envs\car_srtp_clean\python.exe
```

确认 Inno Setup 已安装。推荐版本：

```text
Inno Setup 6.x
```

## 2. 安装 PyInstaller

如果环境中还没有 PyInstaller，运行：

```powershell
powershell -ExecutionPolicy Bypass -File scripts\build_pyinstaller_app.ps1 -InstallPyInstaller
```

如果已经安装，可以直接运行：

```powershell
powershell -ExecutionPolicy Bypass -File scripts\build_pyinstaller_app.ps1
```

输出目录：

```text
dist/CarDesignAssistant/
```

可先双击测试：

```text
dist/CarDesignAssistant/CarDesignAssistant.exe
```

## 3. 使用 Inno Setup 生成安装包

运行：

```powershell
powershell -ExecutionPolicy Bypass -File scripts\build_inno_installer.ps1
```

如果脚本找不到 `ISCC.exe`，手动指定：

```powershell
powershell -ExecutionPolicy Bypass -File scripts\build_inno_installer.ps1 -InnoCompiler "C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
```

输出目录：

```text
installer/
```

安装包名称类似：

```text
CarDesignAssistant_Setup_v1.0.0.exe
```

## 4. 安装包内容

安装后目录包含：

```text
CarDesignAssistant.exe
_internal/
app/models/sports.pkl
app/models/sedan.pkl
app/models/suv.pkl
refs/stylegan2-ada-pytorch/
outputs/app_generated/
README.md
```

说明：

- `_internal/` 是 PyInstaller 的运行依赖目录。
- `app/models/` 中放置三类最终模型。
- `refs/stylegan2-ada-pytorch/` 是模型加载和反序列化所需代码。
- `outputs/app_generated/` 用于保存用户生成的图片和 `metadata.csv`。

## 5. 目标电脑运行条件

目标电脑：

```text
Windows 11 x64
建议内存 16GB 以上
建议有 NVIDIA GPU 和较新显卡驱动
无 GPU 时可 CPU 运行，但生成速度较慢
```

目标电脑不需要安装：

```text
Python
PyTorch
Anaconda
Inno Setup
```

## 6. 验收测试

在另一台 Win11 电脑安装后测试：

1. 启动“汽车外观设计辅助系统”。
2. 分别选择跑车、轿车、SUV。
3. 每类生成至少 1 张图片。
4. 点击“打开输出目录”。
5. 检查是否存在生成图片和 `metadata.csv`。

## 7. 常见问题

如果提示找不到模型：

```text
检查安装目录 app/models/ 下是否有 sports.pkl、sedan.pkl、suv.pkl
```

如果首次启动很慢：

```text
PyTorch 程序首次加载模型需要时间，属于正常现象。
```

如果没有 NVIDIA GPU：

```text
程序会尝试使用 CPU，能运行但生成较慢。
```

