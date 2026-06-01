# 数据集素材说明

PPT 可用要点：项目没有上传原始 CompCars 全量数据，只保留并上传实际用于三类模型训练的数据集。

## 三类训练数据规模

| 类别 | 英文标识 | 样本数量 | 数据集文件 | 文件大小 MB |
|---|---|---:|---|---:|
| 跑车 | sports | 1519 | compcars_sports_256_square.zip | 26.6 |
| 轿车 | sedan | 5492 | compcars_sedan_256_square.zip | 104.1 |
| SUV | suv | 9889 | compcars_suv_256_square.zip | 184.9 |

## 类别映射文件

- 路径：`data\type_datasets\srtp_type_mapping.json`
- 映射：2/10 -> SUV，4 -> sedan，9/11/12 -> sports。
