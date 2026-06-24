# Phase 1 Data Schema

> 本文是 Phase 1 Step 2 的产出：在确认 `chinese-poetry/chinese-poetry` 与我们需求之间的 gap 后，定义本项目自己的 canonical schema。这个 schema 的目标不是复刻上游 JSON，而是为后续推荐系统、AI/Agent 标注、PWA、浏览器插件、Web Push 和评估日志提供稳定数据契约。

## 1. Step 2 结论

`chinese-poetry/chinese-poetry` 只能直接提供基础正文与部分辅助数据，不能直接提供推荐 features。因此本项目必须建立自己的 canonical layer：

```text
upstream raw JSON
  ↓ normalize
canonical poem schema
  ↓ enrich
rule-derived / weak-signal / semantic / behavior-derived features
  ↓ serve
recommendation API + PWA + extension + push
```

## 2. Schema 设计原则

1. **稳定 ID 优先**：`poem_id` 是产品级稳定 ID，不直接使用上游 UUID 或数组序号。
2. **来源可追溯**：每条记录必须保留 `source`，包括数据源、文件路径、上游 ID、许可和导入批次。
3. **正文与 features 分离**：上游能提供正文，不代表能提供推荐 features；features 必须单独分区。
4. **规则推断 features 进入 Step 2 schema**：Step 2 不一定批量生成所有 features，但必须预留字段并定义含义，保证 Step 3/4 可兼容。
5. **AI 标注可追溯**：所有 AI 生成字段都要能记录模型、prompt 版本、输入 hash 与审核状态。
6. **用户行为不写入诗词静态 schema**：用户行为产生用户画像和推荐日志，不污染诗词静态数据。

## 3. Canonical poem record

JSONL 每行是一首诗词，建议文件名：`data/samples/poems.sample.jsonl`、`data/processed/poems.seed.v0.jsonl`。

```json
{
  "schema_version": "poem.v0",
  "poem_id": "poem_tang_li_bai_jing_ye_si_7c4f3a",
  "title": "静夜思",
  "author": {
    "author_id": "author_li_bai",
    "name": "李白",
    "dynasty": "唐",
    "bio": null,
    "source_author_id": null
  },
  "dynasty": "唐",
  "genre": "诗",
  "form": "五言绝句",
  "cipai": null,
  "content": {
    "paragraphs": ["床前明月光，疑是地上霜。", "举头望明月，低头思故乡。"],
    "lines": ["床前明月光", "疑是地上霜", "举头望明月", "低头思故乡"],
    "normalized_text": "床前明月光，疑是地上霜。举头望明月，低头思故乡。"
  },
  "features": {
    "raw_mapped": {
      "has_upstream_id": true,
      "has_author_bio": false,
      "has_strains": false,
      "has_rank": false
    },
    "rule_derived": {
      "line_count": 4,
      "char_count": 20,
      "avg_line_char_count": 5,
      "length_bucket": "short",
      "form_guess": "五言绝句",
      "widget_suitability": 0.95,
      "readability_proxy": 1
    },
    "weak_signals": {
      "familiarity_proxy": null,
      "classic_seed": true,
      "quality_prior": 5
    },
    "semantic": {
      "themes": ["思乡", "月夜"],
      "styles": ["自然", "含蓄"],
      "mood": ["怀念", "孤独"],
      "imagery": ["明月", "霜"],
      "difficulty": 1,
      "suitable_contexts": ["夜晚", "入门", "思乡"],
      "recommendation_seed": "这是一首语言浅近、意象清晰的思乡名篇。"
    },
    "behavior_derived": {
      "global_like_rate": null,
      "global_favorite_rate": null,
      "skip_rate": null
    }
  },
  "ai_annotations": {
    "feature_status": "manual_seed",
    "model": null,
    "prompt_version": null,
    "input_hash": null,
    "generated_at": null,
    "review_status": "sample_checked"
  },
  "source": {
    "source_id": "manual_schema_fixture",
    "source_name": "Manual schema fixture for poem.v0",
    "source_file": "data/samples/poems.sample.jsonl",
    "source_record_index": 1,
    "upstream_id": null,
    "license": "public_domain_text_manual_entry",
    "retrieved_at": null,
    "data_entry_method": "manual_entry_by_project_agent",
    "source_verification_status": "not_source_verified",
    "provenance_note": "Manual schema fixture; not imported from chinese-poetry."
  },
  "review": {
    "text_status": "sample_checked",
    "feature_status": "sample_checked",
    "reviewer": "project_owner",
    "notes": "Manual seed record for schema validation."
  }
}
```

## 4. Field definitions

### 4.1 Identity and source

| Field | Required | Description |
|---|---:|---|
| `schema_version` | yes | 当前记录遵循的 schema 版本，首版为 `poem.v0`。 |
| `poem_id` | yes | 产品级稳定 ID，用于收藏、行为、推荐日志和 embedding join。 |
| `source.upstream_id` | no | 上游数据源 ID；只用于追溯，不作为产品主键。 |
| `source.source_file` | yes | 原始或样本文件路径。 |
| `source.license` | yes | 该条正文的使用依据。 |
| `source.data_entry_method` | yes | 数据进入项目的方式，例如 upstream_import 或 manual_entry_by_project_agent。 |
| `source.source_verification_status` | yes | 是否已与来源文本逐条核验。 |
| `source.provenance_note` | yes | 人类可读的来源说明，避免 fixture 被误认为正式数据。 |

### 4.2 Content

| Field | Required | Description |
|---|---:|---|
| `title` | conditional | 诗题；宋词可能缺少独立标题。 |
| `cipai` | conditional | 词牌；宋词由 `rhythmic` 映射。 |
| `content.paragraphs` | yes | 保留上游段落结构。 |
| `content.lines` | yes | 拆分后的展示与规则推断单位。 |
| `content.normalized_text` | yes | 拼接后的检索、embedding 和 hash 输入。 |

### 4.3 Feature groups

| Group | Step 2 是否定义 | Step 2 是否批量生成 | 来源 |
|---|---:|---:|---|
| `raw_mapped` | yes | yes | 上游字段是否存在 |
| `rule_derived` | yes | sample only | 规则推断：行数、字数、形式、长度、展示适配 |
| `weak_signals` | yes | partial | rank、经典 seed、人工质量先验 |
| `semantic` | yes | sample/manual | LLM/Agent/人工审核生成 |
| `behavior_derived` | yes | no | 产品上线后的用户行为聚合 |

## 5. 规则推断 features 是否在 Step 1/2 中？

是，但边界要清楚：

- **Step 1：探查规则 features 的输入是否存在。** 例如 `paragraphs` 能否拆行、`rhythmic` 能否映射词牌、`strains` 能否 join、`rank` 能否作为弱信号。
- **Step 2：定义规则 features 的 schema。** 例如 `line_count`、`char_count`、`form_guess`、`length_bucket`、`widget_suitability`、`readability_proxy`。
- **Step 3/4：批量生成或修正规则 features。** Step 2 的样本可以手工填入少量 rule-derived 字段，但批量稳定生成应由后续 `enrich_features.py` 完成。

所以，规则推断 features **在 Step 1/2 中被探查和定义，但不是在 Step 1/2 中完成全量生产**。

## 6. Validation requirements

Phase 1 Step 2 的样本数据必须满足：

- 每行是合法 JSON object。
- `schema_version` 为 `poem.v0`。
- `poem_id` 全局唯一。
- `author.name`、`dynasty`、`genre`、`content.paragraphs`、`content.lines` 必填。
- `features.raw_mapped`、`features.rule_derived`、`features.weak_signals`、`features.semantic`、`features.behavior_derived` 五个分区必须存在。
- `source` 与 `review` 必须存在，且 `source` 必须说明数据进入方式和核验状态。
- `content.lines` 不能为空。
- `rule_derived.line_count` 应与 `content.lines` 数量一致。
