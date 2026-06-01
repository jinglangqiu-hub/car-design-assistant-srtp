# 桌面程序说明

运行入口：

```powershell
python app\car_design_assistant.py
```

推荐使用项目专用环境启动：

```powershell
D:\anaconda\envs\car_srtp_clean\python.exe app\car_design_assistant.py
```

也可以双击项目根目录下的：

```text
start_desktop_app.cmd
```

模型放置位置：

```text
app/models/sports.pkl
app/models/sedan.pkl
app/models/suv.pkl
```

如果 `app/models/` 下没有模型，程序会尝试读取：

```text
outputs/final_models/sports.pkl
outputs/final_models/sedan.pkl
outputs/final_models/suv.pkl
```

输出图片保存到：

```text
outputs/app_generated/
```

生成参数记录：

```text
outputs/app_generated/metadata.csv
```

依赖：

```powershell
pip install -r requirements_app.txt
```

注意：不要使用 Anaconda base 的 Python 3.12 启动本程序；当前 base 环境没有安装 `torch`。已验证项目专用环境 `D:\anaconda\envs\car_srtp_clean\python.exe` 中存在 `torch`。
