# 数据集素材说明

项目历史记录：三类处理后训练集曾用于训练并上传 Release，已于 2026-11-02 从公开附件移除。仅保留下表的规模与映射信息；训练图片应通过 CompCars 官方流程获取，不再公开分发。

## 三类训练数据规模

| 类别 | 英文标识 | 样本数量 | 数据集文件 | 文件大小 MB |
|---|---|---:|---|---:|
| 跑车 | sports | 1519 | compcars_sports_256_square.zip | 26.6 |
| 轿车 | sedan | 5492 | compcars_sedan_256_square.zip | 104.1 |
| SUV | suv | 9889 | compcars_suv_256_square.zip | 184.9 |

## 类别映射文件

- 路径：`data\type_datasets\srtp_type_mapping.json`
- 映射：2/10 -> SUV，4 -> sedan，9/11/12 -> sports。
