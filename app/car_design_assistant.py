#!/usr/bin/env python3
"""Desktop car appearance generator for the SRTP project.

This app loads one of three StyleGAN2-ADA models:

- sports.pkl
- sedan.pkl
- suv.pkl

and generates a 256 x 256 car appearance image from seed/truncation settings.
"""

from __future__ import annotations

import csv
import random
import sys
import threading
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

import tkinter as tk
from tkinter import filedialog, messagebox, ttk

try:
    import numpy as np
    import torch
    from PIL import Image, ImageTk
except Exception as exc:  # pragma: no cover - shown in GUI at runtime.
    np = None
    torch = None
    Image = None
    ImageTk = None
    IMPORT_ERROR = exc
else:
    IMPORT_ERROR = None


CAR_TYPES = {
    "sports": "跑车",
    "sedan": "轿车",
    "suv": "SUV",
}

CAR_DESCRIPTIONS = {
    "sports": "低矮车身 · 运动姿态 · 概念跑车",
    "sedan": "均衡比例 · 日常乘用 · 轿车方案",
    "suv": "高车身姿态 · 厚重体量 · SUV 方案",
}


@dataclass
class GenerationResult:
    car_type: str
    seed: int
    truncation: float
    image_path: Path
    image: "Image.Image"


class StyleGANGenerator:
    def __init__(self, project_root: Path) -> None:
        self.project_root = project_root
        self.stylegan_dir = self._find_stylegan_dir(project_root)
        self.model_dirs = [
            project_root / "app" / "models",
            project_root / "outputs" / "final_models",
            project_root / "_internal" / "app" / "models",
            project_root / "_internal" / "outputs" / "final_models",
        ]
        self.output_root = project_root / "outputs" / "app_generated"
        self.models: Dict[str, object] = {}
        self.device = "cuda" if torch is not None and torch.cuda.is_available() else "cpu"

        if self.stylegan_dir is None:
            raise FileNotFoundError(
                "未找到 StyleGAN2-ADA 运行代码目录。\n"
                "请确认安装目录或项目目录中存在 refs/stylegan2-ada-pytorch/legacy.py"
            )

        stylegan_path = str(self.stylegan_dir)
        if stylegan_path not in sys.path:
            sys.path.insert(0, stylegan_path)

        import legacy  # type: ignore

        self.legacy = legacy

    def _find_stylegan_dir(self, project_root: Path) -> Optional[Path]:
        candidates = [
            project_root / "refs" / "stylegan2-ada-pytorch",
            project_root / "_internal" / "refs" / "stylegan2-ada-pytorch",
            Path.cwd() / "refs" / "stylegan2-ada-pytorch",
            Path.cwd() / "_internal" / "refs" / "stylegan2-ada-pytorch",
        ]
        for candidate in candidates:
            if (candidate / "legacy.py").exists():
                return candidate
        return None

    def model_path(self, car_type: str) -> Path:
        for model_dir in self.model_dirs:
            candidate = model_dir / f"{car_type}.pkl"
            if candidate.exists():
                return candidate
        searched = "\n".join(str(d / f"{car_type}.pkl") for d in self.model_dirs)
        raise FileNotFoundError(f"未找到 {CAR_TYPES[car_type]} 模型文件：\n{searched}")

    def load_model(self, car_type: str):
        if car_type in self.models:
            return self.models[car_type]

        model_path = self.model_path(car_type)
        with model_path.open("rb") as f:
            model = self.legacy.load_network_pkl(f)["G_ema"].to(self.device)
        model.eval()
        self.models[car_type] = model
        return model

    def generate(self, car_type: str, seed: int, truncation: float) -> GenerationResult:
        if IMPORT_ERROR is not None:
            raise RuntimeError(f"依赖导入失败：{IMPORT_ERROR}")

        model = self.load_model(car_type)
        rng = np.random.RandomState(seed)
        z = torch.from_numpy(rng.randn(1, model.z_dim)).to(self.device)
        c = torch.zeros([1, model.c_dim], device=self.device)

        with torch.no_grad():
            img = model(z, c, truncation_psi=truncation, noise_mode="const")
            img = (img.permute(0, 2, 3, 1) * 127.5 + 128).clamp(0, 255).to(torch.uint8)
            arr = img[0].cpu().numpy()

        image = Image.fromarray(arr, "RGB")
        out_dir = self.output_root / car_type
        out_dir.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_path = out_dir / f"{stamp}_{car_type}_seed{seed:06d}_trunc{truncation:.2f}.png"
        image.save(image_path)
        self._append_metadata(car_type, seed, truncation, image_path)
        return GenerationResult(car_type, seed, truncation, image_path, image)

    def _append_metadata(self, car_type: str, seed: int, truncation: float, image_path: Path) -> None:
        metadata_path = self.output_root / "metadata.csv"
        metadata_path.parent.mkdir(parents=True, exist_ok=True)
        is_new = not metadata_path.exists()
        with metadata_path.open("a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if is_new:
                writer.writerow(["time", "car_type", "seed", "truncation", "image_path"])
            writer.writerow([
                datetime.now().isoformat(timespec="seconds"),
                car_type,
                seed,
                f"{truncation:.3f}",
                str(image_path),
            ])


class CarDesignAssistantApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("汽车外观设计辅助系统")
        self.geometry("1120x720")
        self.minsize(1000, 660)
        self.configure(bg="#eef2f6")

        self.project_root = self._resolve_project_root()
        self.generator: Optional[StyleGANGenerator] = None
        self.current_image: Optional[Image.Image] = None
        self.current_photo: Optional[ImageTk.PhotoImage] = None
        self.last_result: Optional[GenerationResult] = None
        self.is_generating = False

        self.car_type = tk.StringVar(value="sports")
        self.seed = tk.IntVar(value=random.randint(0, 999999))
        self.truncation = tk.DoubleVar(value=0.65)
        self.batch_count = tk.IntVar(value=4)
        self.status = tk.StringVar(value="请先确认 app/models 或 outputs/final_models 下存在三类 pkl 模型。")
        self.type_hint = tk.StringVar(value=CAR_DESCRIPTIONS[self.car_type.get()])
        self.progress_text = tk.StringVar(value="准备就绪")

        self._configure_style()
        self._build_ui()
        self._init_generator()

    def _resolve_project_root(self) -> Path:
        if getattr(sys, "frozen", False):
            return Path(sys.executable).resolve().parent
        return Path(__file__).resolve().parents[1]

    def _configure_style(self) -> None:
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure("Root.TFrame", background="#eef2f6")
        style.configure("Panel.TFrame", background="#ffffff", relief="flat")
        style.configure("Header.TFrame", background="#1f3a5b")
        style.configure("HeaderTitle.TLabel", background="#1f3a5b", foreground="#ffffff", font=("Microsoft YaHei UI", 18, "bold"))
        style.configure("HeaderSub.TLabel", background="#1f3a5b", foreground="#d7e3f4", font=("Microsoft YaHei UI", 10))
        style.configure("Section.TLabel", background="#ffffff", foreground="#1f2937", font=("Microsoft YaHei UI", 10, "bold"))
        style.configure("Hint.TLabel", background="#ffffff", foreground="#64748b", font=("Microsoft YaHei UI", 9))
        style.configure("Status.TLabel", background="#eef2f6", foreground="#475569", font=("Microsoft YaHei UI", 9))
        style.configure("Info.TLabel", background="#ffffff", foreground="#334155", font=("Microsoft YaHei UI", 10))
        style.configure("Preview.TLabel", background="#f8fafc", foreground="#475569", font=("Microsoft YaHei UI", 14, "bold"))
        style.configure("Primary.TButton", font=("Microsoft YaHei UI", 10, "bold"), padding=(10, 8))
        style.configure("Tool.TButton", font=("Microsoft YaHei UI", 10), padding=(10, 7))
        style.configure("Type.TRadiobutton", background="#ffffff", foreground="#1f2937", font=("Microsoft YaHei UI", 10))

    def _build_ui(self) -> None:
        root = ttk.Frame(self, style="Root.TFrame")
        root.pack(fill="both", expand=True)
        root.columnconfigure(0, weight=0)
        root.columnconfigure(1, weight=1)
        root.rowconfigure(1, weight=1)

        header = ttk.Frame(root, style="Header.TFrame", padding=(22, 16))
        header.grid(row=0, column=0, columnspan=2, sticky="ew")
        header.columnconfigure(0, weight=1)
        ttk.Label(header, text="汽车外观设计辅助系统", style="HeaderTitle.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(
            header,
            text="基于三类 StyleGAN2-ADA 微调模型的汽车外观概念图生成工具",
            style="HeaderSub.TLabel",
        ).grid(row=1, column=0, sticky="w", pady=(4, 0))

        sidebar = ttk.Frame(root, padding=18, style="Panel.TFrame")
        sidebar.grid(row=1, column=0, sticky="ns", padx=(18, 12), pady=18)
        sidebar.columnconfigure(0, weight=1)

        ttk.Label(sidebar, text="车型类型", style="Section.TLabel").grid(row=0, column=0, sticky="w")
        type_frame = ttk.Frame(sidebar)
        type_frame.grid(row=1, column=0, sticky="ew", pady=(6, 16))
        for i, (key, label) in enumerate(CAR_TYPES.items()):
            ttk.Radiobutton(
                type_frame,
                text=label,
                value=key,
                variable=self.car_type,
                command=self._update_type_hint,
                style="Type.TRadiobutton",
            ).grid(row=i, column=0, sticky="w", pady=3)
        ttk.Label(sidebar, textvariable=self.type_hint, style="Hint.TLabel", wraplength=260).grid(row=2, column=0, sticky="ew", pady=(0, 16))

        ttk.Label(sidebar, text="随机种子", style="Section.TLabel").grid(row=3, column=0, sticky="w")
        seed_frame = ttk.Frame(sidebar)
        seed_frame.grid(row=4, column=0, sticky="ew", pady=(6, 16))
        seed_frame.columnconfigure(0, weight=1)
        ttk.Entry(seed_frame, textvariable=self.seed, width=14).grid(row=0, column=0, sticky="ew")
        ttk.Button(seed_frame, text="随机", command=self.randomize_seed, style="Tool.TButton").grid(row=0, column=1, padx=(8, 0))

        ttk.Label(sidebar, text="生成稳定度", style="Section.TLabel").grid(row=5, column=0, sticky="w")
        trunc_frame = ttk.Frame(sidebar)
        trunc_frame.grid(row=6, column=0, sticky="ew", pady=(6, 6))
        trunc_frame.columnconfigure(0, weight=1)
        ttk.Scale(trunc_frame, from_=0.45, to=0.9, variable=self.truncation, orient="horizontal").grid(row=0, column=0, sticky="ew")
        ttk.Label(trunc_frame, textvariable=self.truncation, width=5, style="Hint.TLabel").grid(row=0, column=1, padx=(8, 0))
        ttk.Label(sidebar, text="数值低更稳定，数值高更多样", style="Hint.TLabel").grid(row=7, column=0, sticky="w", pady=(0, 16))

        ttk.Label(sidebar, text="批量数量", style="Section.TLabel").grid(row=8, column=0, sticky="w")
        ttk.Spinbox(sidebar, from_=2, to=16, textvariable=self.batch_count, width=8).grid(row=9, column=0, sticky="w", pady=(6, 18))

        ttk.Button(sidebar, text="生成单张", command=self.generate_one, style="Primary.TButton").grid(row=10, column=0, sticky="ew", pady=(0, 9))
        ttk.Button(sidebar, text="批量生成", command=self.generate_batch, style="Tool.TButton").grid(row=11, column=0, sticky="ew", pady=(0, 9))
        ttk.Button(sidebar, text="打开输出目录", command=self.open_output_dir, style="Tool.TButton").grid(row=12, column=0, sticky="ew", pady=(0, 9))
        ttk.Button(sidebar, text="另存当前图片", command=self.save_current_as, style="Tool.TButton").grid(row=13, column=0, sticky="ew")

        sidebar.rowconfigure(14, weight=1)
        ttk.Separator(sidebar).grid(row=15, column=0, sticky="ew", pady=(18, 10))
        ttk.Label(sidebar, textvariable=self.progress_text, style="Section.TLabel").grid(row=16, column=0, sticky="w")
        ttk.Label(sidebar, textvariable=self.status, wraplength=260, style="Hint.TLabel").grid(row=17, column=0, sticky="ew", pady=(6, 0))

        main = ttk.Frame(root, padding=18, style="Panel.TFrame")
        main.grid(row=1, column=1, sticky="nsew", padx=(0, 18), pady=18)
        main.columnconfigure(0, weight=1)
        main.rowconfigure(0, weight=1)

        self.preview = ttk.Label(main, anchor="center", text="等待生成", style="Preview.TLabel")
        self.preview.grid(row=0, column=0, sticky="nsew")

        info_bar = ttk.Frame(main, style="Panel.TFrame")
        info_bar.grid(row=1, column=0, sticky="ew", pady=(14, 0))
        info_bar.columnconfigure(0, weight=1)
        self.info = ttk.Label(info_bar, text="生成结果会自动保存到 outputs/app_generated", anchor="w", style="Info.TLabel")
        self.info.grid(row=0, column=0, sticky="ew")

    def _init_generator(self) -> None:
        if IMPORT_ERROR is not None:
            self.status.set(f"依赖未安装：{IMPORT_ERROR}")
            return
        try:
            self.generator = StyleGANGenerator(self.project_root)
            self.status.set(f"模型后端已就绪，当前设备：{self.generator.device}")
        except Exception as exc:
            self.status.set(f"模型后端初始化失败：{exc}")

    def _update_type_hint(self) -> None:
        self.type_hint.set(CAR_DESCRIPTIONS[self.car_type.get()])

    def randomize_seed(self) -> None:
        self.seed.set(random.randint(0, 999999))

    def generate_one(self) -> None:
        self._start_generation(batch=False)

    def generate_batch(self) -> None:
        self._start_generation(batch=True)

    def _start_generation(self, batch: bool) -> None:
        if self.is_generating:
            return
        if self.generator is None:
            messagebox.showerror("无法生成", self.status.get())
            return
        self.is_generating = True
        self.progress_text.set("生成中")
        self.status.set("正在生成，请稍候...")
        thread = threading.Thread(target=self._generate_worker, args=(batch,), daemon=True)
        thread.start()

    def _generate_worker(self, batch: bool) -> None:
        try:
            count = self.batch_count.get() if batch else 1
            first_result = None
            for i in range(count):
                seed = self.seed.get() if i == 0 else random.randint(0, 999999)
                self.after(0, self.status.set, f"正在生成第 {i + 1}/{count} 张...")
                result = self.generator.generate(self.car_type.get(), int(seed), float(self.truncation.get()))
                if first_result is None:
                    first_result = result
                time.sleep(0.05)
            self.after(0, self._finish_generation, first_result, count)
        except Exception as exc:
            self.after(0, self._fail_generation, exc)

    def _finish_generation(self, result: GenerationResult, count: int) -> None:
        self.is_generating = False
        self.progress_text.set("生成完成")
        self.last_result = result
        self.current_image = result.image
        self._show_image(result.image)
        self.info.config(text=f"{CAR_TYPES[result.car_type]} | seed={result.seed} | trunc={result.truncation:.2f}")
        self.status.set(f"已生成 {count} 张，最新图片：{result.image_path}")

    def _fail_generation(self, exc: Exception) -> None:
        self.is_generating = False
        self.progress_text.set("生成失败")
        self.status.set(f"生成失败：{exc}")
        messagebox.showerror("生成失败", str(exc))

    def _show_image(self, image: "Image.Image") -> None:
        size = min(max(self.preview.winfo_width(), 512), max(self.preview.winfo_height(), 512), 560)
        display = image.resize((size, size))
        self.current_photo = ImageTk.PhotoImage(display)
        self.preview.config(image=self.current_photo, text="")

    def open_output_dir(self) -> None:
        out_dir = self.project_root / "outputs" / "app_generated"
        out_dir.mkdir(parents=True, exist_ok=True)
        if sys.platform.startswith("win"):
            import os

            os.startfile(out_dir)
        else:
            messagebox.showinfo("输出目录", str(out_dir))

    def save_current_as(self) -> None:
        if self.current_image is None:
            messagebox.showinfo("没有图片", "请先生成图片。")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG 图片", "*.png")],
            initialfile="car_design.png",
        )
        if path:
            self.current_image.save(path)
            self.status.set(f"已另存为：{path}")


def main() -> None:
    app = CarDesignAssistantApp()
    app.mainloop()


if __name__ == "__main__":
    main()
