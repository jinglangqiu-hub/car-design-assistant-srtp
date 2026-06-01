# SRTP 结项答辩 PPT 素材包

生成时间：2026-06-01 19:50:20

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
