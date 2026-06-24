# scripts/data_import

存放数据导入、清洗、标准化、校验脚本。

近期计划：

- `validate_poems.py`
- 原始数据到 MVP JSON 的转换脚本
- 重复 ID 和缺字段检查脚本


## Phase 1 scripts

- `inspect_chinese_poetry.py`: probes representative `chinese-poetry/chinese-poetry` upstream files and writes `data/processed/source_profile.chinese_poetry.json`.
- `validate_poems.py`: validates canonical `poem.v0` JSONL records, currently targeting `data/samples/poems.sample.jsonl`.

Next scripts planned:

- `normalize_poems.py`: convert upstream raw JSON records into canonical JSONL.
- `enrich_features.py`: generate rule-derived and weak-signal features in batch.
