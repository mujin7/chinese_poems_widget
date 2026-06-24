# `chinese-poetry/chinese-poetry` 数据源能力评估

> 结论：`chinese-poetry/chinese-poetry` **能满足本项目的“基础正文语料库”需求，但不能直接满足“推荐系统 features / 注释翻译 / 用户行为闭环”需求**。它适合作为 Phase 1 的正文与作者基础数据源；真正用于推荐的 `features` 需要我们在 canonical schema 之上二次生产。

## 1. 直接回答：它有没有 features？

没有我们需要的完整 features。

`chinese-poetry/chinese-poetry` 的核心价值是：大规模、JSON 化、MIT license 的古诗词正文与作者基础信息。它通常提供：

- 标题：`title`。
- 作者：`author`。
- 正文段落：`paragraphs`。
- 部分数据的上游 ID：`id`。
- 宋词词牌：`rhythmic`。
- 作者简介：如 `authors.tang.json` 中的 `desc`。
- 可选辅助数据：少量上游 `tags`、`strains` 平仄、`rank` 搜索引擎结果数。

但它通常不直接、完整、稳定地提供本项目推荐系统需要的这些字段。注意：本次 Step 1 探查发现部分唐诗/宋诗文件存在稀疏 `tags` 字段，但覆盖率低、标签体系不等于我们的产品标签，因此只能作为弱参考，不能视为完整 features：

- 主题标签：山水、思乡、送别、爱情、边塞、家国等。
- 风格标签：豪放、婉约、清新、沉郁、旷达等。
- 情绪标签：孤独、喜悦、怀念、悲凉、闲适等。
- 难度等级。
- 熟悉度等级。
- 质量分。
- 适合场景：早晨、夜晚、雨天、秋天、学习、壁纸、通知等。
- 推荐解释素材。
- 白话翻译、注释、赏析。
- 用户行为数据。
- embedding 向量。

所以它不是“拿来就可以推荐”的数据库，而是“拿来构建推荐数据库的底层语料”。

---

## 2. 为什么仍然选择它作为主数据源？

### 2.1 它覆盖了 MVP 最难替代的基础资产

本项目最基础、最难自己从零构建的是古诗词正文库。`chinese-poetry/chinese-poetry` README 显示，它包含约 5.5 万首唐诗、26 万首宋诗、2.1 万首宋词以及其他古典文集，并通过 JSON 格式分发，目标就是方便开发者构建诗词类应用。

这正好满足我们的 Phase 1 基础需求：

- 先有足够多的正文候选。
- 先能抽取一个 100-500 首 seed corpus。
- 先能构建 `poem_id/title/author/dynasty/genre/content/source` 这些稳定字段。

### 2.2 它有开源生态实践

该仓库 README 的案例展示中包括浏览器诗词网站、Android 离线全唐诗、诗词桌面、小程序、MySQL DB 整合与 Web 检索等项目。这说明它适合被转换成 Web、桌面、移动端或数据库形态。

对我们来说，这证明：

- 它适合作为工程输入源。
- JSON 转关系库是可行路线。
- 它本身更像“内容底座”，不是“推荐系统成品”。

### 2.3 它的风险是可控的

仓库 README 也说明数据来源于互联网，采集过程没有完整记录。因此它不能被当作完全权威来源。

我们的处理策略是：

- 只把它作为正文初始来源。
- 保留 `source_dataset/source_file/source_record_index/upstream_id`。
- 先抽样审核，不一次性导入全量。
- 对重点作品人工核验。
- 不导入商业网站的现代注释、翻译、赏析。

---

## 3. 上游字段实际长什么样？

我抽查了 `chinese-poetry/chinese-poetry` 的 GitHub 内容 API 与 raw JSON。典型结构如下。

### 3.1 唐诗 / 宋诗记录

来自 `全唐诗/poet.tang.0.json` 或 `全唐诗/poet.song.0.json` 的记录形态大致是：

```json
{
  "author": "太宗皇帝",
  "paragraphs": [
    "秦川雄帝宅，函谷壯皇居。",
    "綺殿千尋起，離宮百雉餘。"
  ],
  "title": "帝京篇十首 一",
  "id": "3ad6d468-7ff1-4a7b-8b24-a27d70d00ed4"
}
```

可直接使用：

- `author` → 作者名。
- `paragraphs` → 正文段落。
- `title` → 标题。
- `id` → 可作为上游 ID 保存，但不建议直接作为产品 `poem_id`。

不能直接得到：

- 主题、风格、难度、熟悉度、推荐理由。
- 现代注释、翻译、赏析。
- 用户推荐相关行为。

### 3.2 宋词记录

来自 `宋词/ci.song.0.json` 的记录形态大致是：

```json
{
  "author": "和岘",
  "paragraphs": [
    "气和玉烛，睿化著鸿明。",
    "缇管一阳生。"
  ],
  "rhythmic": "导引"
}
```

可直接使用：

- `author` → 作者名。
- `paragraphs` → 正文段落。
- `rhythmic` → 词牌，可映射为 `cipai`。

需要注意：

- 宋词数据可能没有普通诗词意义上的 `title`，`rhythmic` 是词牌，不等价于主题标题。
- 产品中可以显示为 `《导引》`，但内部 schema 要区分 `title` 与 `cipai/rhythmic`。

### 3.3 作者记录

来自 `全唐诗/authors.tang.json` 的记录形态大致是：

```json
{
  "name": "太宗皇帝",
  "desc": "帝姓李氏，諱世民，神堯次子...",
  "id": "f78aa699-e012-4059-9e29-5d30e16cc1d8"
}
```

可直接使用：

- 作者名。
- 作者简介。
- 上游作者 ID。

不能直接得到：

- 作者风格标签。
- 作者代表性评分。
- 作者朝代标准化程度仍需核验。

### 3.4 稀疏上游 `tags`

本次探查发现部分 `poet.tang.0.json` 和 `poet.song.0.json` 记录中存在 `tags` 字段，但覆盖率很低；例如 sample profile 中唐诗首个文件约 6.7%，宋诗首个文件约 2.9%。

可用于：

- feature enrichment 的弱参考。
- 人工审核或 LLM 标注时的提示信息。

不能用于：

- 直接作为我们的主题/风格/情绪体系。
- 直接支撑个性化推荐。
- 替代人工 seed、规则推断、LLM/Agent 标注和用户行为学习。

### 3.5 平仄 `strains`

`strains/json/poet.tang.0.json` 这类文件包含与诗词 ID 对应的平仄信息，例如：

```json
{
  "id": "3ad6d468-7ff1-4a7b-8b24-a27d70d00ed4",
  "strains": [
    "平平平仄仄，平仄仄平平。",
    "仄仄平平仄，平平仄仄平。"
  ]
}
```

可用于：

- 格律相关展示。
- 体裁/形式推断的辅助特征。
- 高级用户或学习功能。

但它不等于主题/风格/难度 features。

### 3.6 搜索引擎 `rank`

`rank/poet/*.json` 和 `rank/ci/*.json` 中存在类似记录：

```json
{
  "baidu": 20600,
  "author": "太宗皇帝",
  "title": "帝京篇十首 一",
  "so360": 1120,
  "bing": 157000,
  "bing_en": 97600,
  "google": 50400
}
```

可用于：

- 粗略估计作品互联网出现频率。
- 作为 `familiarity_score` 的弱 proxy。
- 辅助区分“可能更熟悉”与“明显冷门”。

不能直接等同于：

- 文学质量。
- 当代用户熟悉度。
- 推荐质量。

搜索结果数会受搜索引擎、时间、标题歧义、作者歧义影响，只能作为一个弱特征。

---

## 4. 与我们目标 schema 的覆盖矩阵

| 我们需要的字段 | chinese-poetry 是否直接提供 | 可用程度 | 处理方式 |
|---|---:|---:|---|
| 诗词标题 | 部分提供 | 高 | 唐诗/宋诗用 `title`；宋词要区分 `rhythmic` 与标题 |
| 作者 | 提供 | 高 | 直接映射，后续做作者 ID 标准化 |
| 朝代 | 隐含提供 | 中 | 根据文件路径推断：唐诗、宋诗、宋词等 |
| 体裁 | 隐含提供 | 中 | 根据目录推断：诗/词/曲/经文等 |
| 词牌 | 宋词提供 `rhythmic` | 高 | 映射为 `cipai`，但不要误当标题主题 |
| 正文 | 提供 `paragraphs` | 高 | 转换为 `paragraphs` + `lines` |
| 上游 ID | 部分提供 | 中 | 保存为 `upstream_id`，产品另建稳定 `poem_id` |
| 作者简介 | 部分提供 | 中 | 可用作详情页初稿，需清洗繁简与格式 |
| 稀疏上游 tags | 少量提供 | 低 | 只作弱参考，不直接作为产品 features |
| 平仄 | 部分提供 | 中 | 用于格律辅助特征，不进入 MVP 强依赖 |
| 搜索 rank | 部分提供 | 中 | 可作为熟悉度 proxy，但需归一化和降权 |
| 主题标签 | 不提供 | 无 | 规则 + LLM + 人工审核生成 |
| 风格标签 | 不提供 | 无 | LLM 标注 + 人工抽样审核 |
| 情绪标签 | 不提供 | 无 | LLM 标注 + embedding 聚类辅助 |
| 难度 | 不提供 | 无 | 根据字词、篇幅、典故密度、人工/AI 评分生成 |
| 熟悉度 | 不直接提供 | 低-中 | `rank` + 经典选本 + 用户行为综合生成 |
| 质量分 | 不提供 | 无 | 经典选本、人工规则、用户反馈共同生成 |
| 注释 | 不提供 | 无 | MVP 只做少量人工/AI 辅助审核内容 |
| 翻译 | 不提供 | 无 | AI 初稿 + 人工审核，不直接爬商业网站 |
| 推荐理由 | 不提供 | 无 | 推荐服务根据用户画像与 features 生成 |
| 用户行为 | 不提供 | 无 | 我们自己的产品事件系统产生 |
| embedding | 不提供 | 无 | 我们用 embedding 模型生成 |

结论：

> `chinese-poetry` 对“内容正文层”覆盖较好，对“推荐 features 层”覆盖很弱，对“用户行为层”完全不覆盖。这正是为什么我们需要自己的 processed 层、feature enrichment pipeline、用户行为库和推荐日志。

---

## 5. features 应该怎么补？

本项目的 features 不应该只靠 LLM 一步生成。推荐采用四类来源叠加。

### 5.1 直接映射 features

从上游结构直接得出：

| Feature | 来源 |
|---|---|
| `author` | `author` 字段 |
| `dynasty` | 目录/文件名推断 |
| `genre` | 目录推断，诗/词/曲/经文 |
| `cipai` | 宋词 `rhythmic` |
| `line_count` | `paragraphs` 拆分 |
| `char_count` | 正文长度统计 |
| `has_strains` | 是否能 join 到 strains |

### 5.2 规则推断 features

用程序规则生成：

| Feature | 规则示例 |
|---|---|
| `form` | 4 行且每行 5 字 → 五言绝句候选；8 行且每行 7 字 → 七言律诗候选 |
| `length_bucket` | 字数分 short/medium/long |
| `widget_suitability` | 短诗、名句清晰、段落少 → 更适合通知/小组件 |
| `readability_proxy` | 生僻字比例、典故词数量、篇幅长度 |

这些规则不一定文学上 100% 精确，但适合 MVP 做初筛。

### 5.3 外部弱信号 features

用 `rank`、经典选本、人工 seed 列表补充：

| Feature | 来源 |
|---|---|
| `familiarity_score` | rank 搜索结果数 + 唐诗三百/宋词三百/教材常见清单 |
| `classic_score` | 是否在经典选本 seed 中 |
| `quality_prior` | 经典选本、重点作者、人工挑选 |

注意：rank 只能是弱信号，不能单独决定推荐。

### 5.4 LLM / Agent 生成 features

用 LLM 生成需要理解语义的字段：

| Feature | 生成方式 |
|---|---|
| `themes` | 结构化输出：山水/田园/思乡/送别/边塞/爱情/家国/人生等 |
| `styles` | 豪放/婉约/清新/沉郁/旷达/典雅等 |
| `mood` | 孤独/怀念/闲适/悲凉/昂扬等 |
| `imagery` | 明月、江水、春风、落花、孤舟等 |
| `difficulty` | 1-5 分，结合字词、典故、语法和篇幅 |
| `recommendation_seed` | 一句话解释素材，不直接作为最终推荐理由 |

必须保留：

```text
model
prompt_version
input_hash
generated_at
review_status
```

这样后续才能迭代 prompt，也能在面试中解释 AI 标注的可控性。

### 5.5 用户行为反推 features

真正个性化推荐需要从用户行为中学习：

- 用户喜欢某类诗，提升对应主题/风格/作者权重。
- 用户跳过某类诗，降低但不完全屏蔽对应标签。
- 用户收藏短句类作品，提升 `widget_suitability` 和短诗偏好。
- 用户经常打开注释，说明难度接受度可能更高，或者需要解释辅助。

这部分只能由我们自己的产品产生，不能从 `chinese-poetry` 预先获得。

---

## 6. 是否需要补充其他数据源？

### 6.1 Phase 1 不需要急着补很多源

Phase 1 的目标不是“数据最全”，而是证明：

```text
数据源 → canonical schema → features → 推荐闭环
```

所以只用 `chinese-poetry` 抽取 100-500 首，再人工补少量 features，已经够用。

### 6.2 推荐补充一个“人工 curated seed list”

建议我们自己维护：

```text
data/samples/curated_seed_poems.jsonl
```

内容包括：

- 100 首适合 MVP 的经典/半经典诗词。
- 人工确认的主题、风格、难度、熟悉度。
- 是否适合通知、新标签页、壁纸。

这比一开始全量自动标注几十万首更有效。

### 6.3 注释翻译另建小规模审核集

建议单独维护：

```text
data/samples/annotations.sample.jsonl
data/samples/translations.sample.jsonl
```

只覆盖 20-50 首重点作品。

原因：

- 注释翻译质量直接影响用户信任。
- 现代注释翻译有版权风险。
- 推荐系统 MVP 不要求每首都有完整翻译。

---

## 7. 对 Phase 1 的修正

基于这次评估，Phase 1 不应该写成“导入 chinese-poetry 就完成数据层”。更准确的 Phase 1 应该拆成四步。

### Step 1：上游结构探测

产出：

- `scripts/data_import/inspect_chinese_poetry.py`
- `data/processed/source_profile.chinese_poetry.json`

检查：

- 每类文件有哪些字段。
- 哪些字段缺失。
- 是否有 `id`。
- 宋词 `rhythmic` 如何处理。
- strains/rank 是否可 join。

### Step 2：建立 canonical schema

产出：

- `docs/data-schema.md`
- `data/samples/poems.sample.jsonl`

要求：

- 上游字段和我们自己的 features 分开。
- `source`、`review`、`features` 必须独立。
- `features` 允许为空或 pending，但 schema 要预留。

### Step 3：构建 seed corpus

产出：

- `data/processed/poems.seed.v0.jsonl`
- `data/processed/import_report.seed.v0.json`

要求：

- 先抽 100-500 首。
- 重点覆盖唐诗、宋词、诗经、重点作者。
- 每首有基础字段和来源追溯。
- features 可以先是 `pending`。

### Step 4：feature enrichment MVP

产出：

- `scripts/data_import/enrich_features.py`
- `data/processed/poem_features.seed.v0.jsonl`

先生成：

- 规则 features：字数、行数、体裁、长度桶。
- 弱信号 features：rank proxy、经典 seed 标记。
- 手工 features：20-50 首核心诗。
- AI features：可选，先小规模测试。

---

## 8. 最终判断

### 8.1 能满足什么？

`chinese-poetry/chinese-poetry` 能满足：

- 大规模古诗词正文来源。
- 作者、标题、段落、词牌等基础字段。
- 部分作者简介。
- 部分平仄数据。
- 部分搜索 rank 数据。
- MIT license 的开源使用基础。
- 从 JSON 转换为我们自己的 processed 数据层。

### 8.2 不能满足什么？

它不能直接满足：

- 推荐系统 features。
- 用户画像。
- 用户行为。
- 推荐日志。
- 个性化推荐解释。
- 注释、翻译、赏析。
- 高质量难度/主题/风格/情绪标签。
- embedding 语义向量。

### 8.3 产品策略结论

所以正确策略是：

```text
chinese-poetry = 原始正文底座
我们的 processed layer = 产品可用内容层
我们的 feature pipeline = 推荐可用画像层
我们的 event/recommendation DB = 个性化闭环层
```

这也是面试中更好的讲法：

> 我没有把开源诗词 JSON 直接当成产品数据库，而是把它作为 raw corpus，设计了 source manifest、canonical schema、feature enrichment、用户行为事件和推荐日志，使它从“内容数据集”升级为“可推荐、可解释、可评估”的推荐系统数据底座。

---

## 9. 本次验证方式

本次评估基于：

- GitHub README：确认数据规模、JSON 分发、MIT license、数据来源说明和生态案例。
- GitHub contents API：确认存在 `全唐诗`、`宋词`、`strains`、`rank` 等目录。
- raw JSON 抽样：检查 `poet.tang.0.json`、`poet.song.0.json`、`ci.song.0.json`、`authors.tang.json`、`strains/json/poet.tang.0.json`、`rank/poet/poet.tang.rank.0.json` 的实际字段。

相关外部来源：

- [`chinese-poetry/chinese-poetry`](https://github.com/chinese-poetry/chinese-poetry)
- [`chinese-poetry/chinese-poetry-npm`](https://github.com/chinese-poetry/chinese-poetry-npm)
