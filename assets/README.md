# Gallery provenance

The PNGs in `samples/` are byte-for-byte copies from `ppt_materials/02_generated_samples/sports/`. They also appear in v1.0.0 `app_generated_samples.zip`. No image-generation or retouching tool was used in this cleanup.

| Display file | Original file | Seed | Truncation | Size |
|---|---|---:|---:|---|
| `samples/sports-seed796724.png` | `20260601_134750_sports_seed796724_trunc0.65.png` | 796724 | 0.65 | 256 × 256 |
| `samples/sports-seed437112.png` | `20260601_134824_sports_seed437112_trunc0.65.png` | 437112 | 0.65 | 256 × 256 |

The [original CSV](../ppt_materials/02_generated_samples/metadata.csv) records timestamps and historical local paths. No model hash is present, so these rows cannot uniquely identify the generating checkpoint.

The sports label records the selected model, not verified vehicle-class correctness; the images do not consistently show sports-car proportions. These are selected outputs, not random sampling or a quality benchmark. There is no sedan/SUV gallery, GUI screenshot, recorded demo, failure-case set, or controlled before/after comparison here. Add these only from real outputs with traceable provenance.
