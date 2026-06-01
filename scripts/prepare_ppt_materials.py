from __future__ import annotations

import csv
import shutil
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "ppt_materials"


def reset_dir(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def mkdir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def copy_if_exists(src: Path, dst_dir: Path) -> None:
    if src.exists():
        dst_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst_dir / src.name)


def copy_tree_files(src_dir: Path, dst_dir: Path, patterns: tuple[str, ...]) -> int:
    if not src_dir.exists():
        return 0
    count = 0
    for pattern in patterns:
        for src in src_dir.rglob(pattern):
            if src.is_file():
                rel = src.relative_to(src_dir)
                dst = dst_dir / rel
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)
                count += 1
    return count


def size_mb(path: Path) -> float:
    return round(path.stat().st_size / 1024 / 1024, 2)


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def table_from_files(title: str, files: list[Path]) -> str:
    lines = [f"## {title}", "", "| 文件 | 大小 MB | 用途 |", "|---|---:|---|"]
    for f in files:
        lines.append(f"| `{f.name}` | {size_mb(f)} | PPT 可作为成果/证据引用 |")
    lines.append("")
    return "\n".join(lines)


def build_dataset_summary() -> str:
    mapping = ROOT / "data" / "type_datasets" / "srtp_type_mapping.json"
    dataset_files = [
        ROOT / "data" / "type_datasets" / "compcars_sports_256_square.zip",
        ROOT / "data" / "type_datasets" / "compcars_sedan_256_square.zip",
        ROOT / "data" / "type_datasets" / "compcars_suv_256_square.zip",
    ]
    lines = [
        "# 数据集素材说明",
        "",
        "PPT 可用要点：项目没有上传原始 CompCars 全量数据，只保留并上传实际用于三类模型训练的数据集。",
        "",
        "## 三类训练数据规模",
        "",
        "| 类别 | 英文标识 | 样本数量 | 数据集文件 | 文件大小 MB |",
        "|---|---|---:|---|---:|",
        "| 跑车 | sports | 1519 | compcars_sports_256_square.zip | {:.1f} |".format(size_mb(dataset_files[0])),
        "| 轿车 | sedan | 5492 | compcars_sedan_256_square.zip | {:.1f} |".format(size_mb(dataset_files[1])),
        "| SUV | suv | 9889 | compcars_suv_256_square.zip | {:.1f} |".format(size_mb(dataset_files[2])),
        "",
        "## 类别映射文件",
        "",
        f"- 路径：`{mapping.relative_to(ROOT)}`",
        "- 映射：2/10 -> SUV，4 -> sedan，9/11/12 -> sports。",
        "",
    ]
    return "\n".join(lines)


def build_model_summary() -> str:
    model_dir = ROOT / "app" / "models"
    final_dir = ROOT / "outputs" / "final_models"
    models = ["sports.pkl", "sedan.pkl", "suv.pkl"]
    lines = [
        "# 模型素材说明",
        "",
        "PPT 可用要点：项目最终采用三类独立微调模型实现可控生成，而不是单一条件模型。",
        "",
        "| 模型 | 对应车型 | 文件大小 MB | 桌面程序选择逻辑 |",
        "|---|---|---:|---|",
    ]
    labels = {"sports.pkl": "跑车", "sedan.pkl": "轿车", "suv.pkl": "SUV"}
    for name in models:
        path = model_dir / name
        lines.append(f"| {name} | {labels[name]} | {size_mb(path):.1f} | 用户选择{labels[name]}时加载 |")
    lines.extend([
        "",
        f"- 运行模型目录：`{model_dir.relative_to(ROOT)}`",
        f"- 训练记录目录：`{final_dir.relative_to(ROOT)}`",
        "- 每类追加训练后均可筛选出 10 张以上可展示图。",
        "",
    ])
    return "\n".join(lines)


def build_installer_summary() -> str:
    installer = ROOT / "installer"
    files = sorted(installer.glob("CarDesignAssistant_Setup_v1.0.0*"))
    lines = [
        "# 安装包与部署素材说明",
        "",
        "PPT 可用要点：项目已完成从源码程序到可安装 Win11 桌面应用的工程闭环。",
        "",
        "| 文件 | 大小 MB | 说明 |",
        "|---|---:|---|",
    ]
    for f in files:
        note = "安装启动程序" if f.suffix.lower() == ".exe" else "安装包数据分卷"
        lines.append(f"| {f.name} | {size_mb(f):.1f} | {note} |")
    lines.extend([
        "",
        "使用说明：下载 exe 和全部 bin 分卷，放在同一文件夹，双击 exe 安装。",
        "",
    ])
    return "\n".join(lines)


def build_generated_summary() -> str:
    metadata = ROOT / "outputs" / "app_generated" / "metadata.csv"
    rows = []
    if metadata.exists():
        with metadata.open("r", encoding="utf-8", newline="") as f:
            rows = list(csv.DictReader(f))
    lines = [
        "# 生成样例素材说明",
        "",
        "PPT 可用要点：桌面程序生成结果会自动保存，并记录车型、seed、truncation 和图片路径。",
        "",
        "| 时间 | 车型 | seed | truncation | 图片 |",
        "|---|---|---:|---:|---|",
    ]
    for row in rows:
        img = Path(row["image_path"]).name
        lines.append(f"| {row['time']} | {row['car_type']} | {row['seed']} | {row['truncation']} | {img} |")
    if not rows:
        lines.append("| 暂无 | 暂无 | - | - | 请从桌面程序生成样例图 |")
    lines.append("")
    return "\n".join(lines)


def build_index() -> str:
    return f"""# SRTP 结项答辩 PPT 素材包

生成时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

本文件夹用于集中存放制作结项答辩 PPT 时最有价值的过程证据、结果材料和交付成果说明。素材均从项目目录复制或汇总而来，不移动原始文件。

## 推荐 PPT 结构与对应素材

| PPT 页面 | 建议主题 | 可用素材 |
|---|---|---|
| 1 | 项目题目与目标 | `01_report_and_docs/重庆大学SRTP结项报告_汽车外观设计辅助系统.docx`、本索引 |
| 2 | 研究背景与技术路线 | README、结项报告第 1-2 章 |
| 3 | 数据集构建 | `04_dataset_and_model_info/dataset_summary.md`、`srtp_type_mapping.json` |
| 4 | 云端训练环境 | `03_training_records/cloud_env_config.md` |
| 5 | 三类模型训练路线 | `04_dataset_and_model_info/model_summary.md`、`manifest.txt` |
| 6 | 训练过程与追加训练 | `03_training_records/*.log`、`manifest.txt` |
| 7 | 生成效果展示 | `02_generated_samples/` 下的图片与 `generated_samples_summary.md` |
| 8 | 桌面系统功能 | `05_desktop_and_packaging/app_README.md`、程序运行截图可后续补充 |
| 9 | 打包与部署成果 | `05_desktop_and_packaging/installer_summary.md`、`CarDesignAssistant.iss` |
| 10 | GitHub 云端归档 | `06_github_release/github_upload_guide.md`、`release_asset_summary.md` |
| 11 | 问题与改进 | 结项报告第 8 章 |
| 12 | 总结与答辩收束 | 结项报告摘要、成果清单 |

## 素材文件夹说明

- `01_report_and_docs/`：结项报告、论文/PPT 提纲、项目清理说明。
- `02_generated_samples/`：桌面程序实际生成的图片和 metadata。
- `03_training_records/`：云端训练环境、训练日志、最终模型 manifest。
- `04_dataset_and_model_info/`：三类数据集、模型和类别映射的 PPT 摘要。
- `05_desktop_and_packaging/`：桌面程序、打包、安装包分卷说明。
- `06_github_release/`：GitHub 上传与 Release 附件说明。

## 可以直接放进 PPT 的关键结论

1. 项目实现了跑车、轿车、SUV 三类汽车外观概念图生成。
2. 采用“三类数据集 + 三类 StyleGAN2-ADA 微调模型”的工程路线，稳定满足立项要求。
3. 云端 RTX 5090 环境完成训练和追加训练，解决了本地电脑算力与长时间开机限制。
4. 桌面程序支持车型选择、seed、truncation、单张/批量生成、保存和参数记录。
5. 项目完成 PyInstaller 与 Inno Setup 打包，安装后的 Win11 应用已验证能正常生图。
6. 源码已上传 GitHub，模型、三类训练数据和分卷安装包作为 Release 资产归档。
"""


def main() -> None:
    reset_dir(OUT)

    docs_dir = mkdir(OUT / "01_report_and_docs")
    samples_dir = mkdir(OUT / "02_generated_samples")
    training_dir = mkdir(OUT / "03_training_records")
    info_dir = mkdir(OUT / "04_dataset_and_model_info")
    app_dir = mkdir(OUT / "05_desktop_and_packaging")
    gh_dir = mkdir(OUT / "06_github_release")

    for rel in [
        "README.md",
        "docs/重庆大学SRTP结项报告_汽车外观设计辅助系统.docx",
        "docs/paper_outline.md",
        "docs/slides_outline.md",
        "docs/project_cleanup_report.md",
        "docs/final_acceptance_checklist.md",
    ]:
        copy_if_exists(ROOT / rel, docs_dir)

    copy_tree_files(ROOT / "outputs" / "app_generated", samples_dir, ("*.png", "*.jpg", "*.jpeg", "*.csv"))
    write_text(samples_dir / "generated_samples_summary.md", build_generated_summary())

    for rel in [
        "docs/cloud_env_config.md",
        "outputs/final_models/manifest.txt",
    ]:
        copy_if_exists(ROOT / rel, training_dir)
    copy_tree_files(ROOT / "outputs" / "logs", training_dir / "logs", ("*.log", "*.pid"))

    copy_if_exists(ROOT / "data" / "type_datasets" / "srtp_type_mapping.json", info_dir)
    write_text(info_dir / "dataset_summary.md", build_dataset_summary())
    write_text(info_dir / "model_summary.md", build_model_summary())

    for rel in [
        "app/README.md",
        "app/car_design_assistant.py",
        "packaging/CarDesignAssistant.iss",
        "packaging/README_packaging.md",
    ]:
        dst_name = "app_README.md" if rel == "app/README.md" else None
        src = ROOT / rel
        if src.exists():
            target = app_dir / (dst_name or src.name)
            shutil.copy2(src, target)
    write_text(app_dir / "installer_summary.md", build_installer_summary())

    for rel in [
        "docs/github_upload_guide.md",
        "scripts/upload_github_release_assets.ps1",
        "scripts/prepare_github_release_assets.ps1",
    ]:
        copy_if_exists(ROOT / rel, gh_dir)
    release_files = sorted((ROOT / "release_assets").rglob("*")) if (ROOT / "release_assets").exists() else []
    release_files = [p for p in release_files if p.is_file()]
    release_summary = table_from_files("GitHub Release 附件清单", release_files)
    write_text(gh_dir / "release_asset_summary.md", release_summary)

    write_text(OUT / "PPT素材索引.md", build_index())
    print(OUT)


if __name__ == "__main__":
    main()
