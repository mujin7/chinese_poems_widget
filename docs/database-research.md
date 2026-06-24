# 数据库调研与数据方案决策

> 本文回答用户追问的“数据库”问题：不是只讨论选 PostgreSQL 还是 SQLite，而是系统性规划 **数据从哪里来、如何清洗、以什么结构保存、在线服务如何存储、前端/插件如何缓存、推荐系统如何调用、后续如何兼容 AI 与 Agent**。

## 1. 结论先行

### 1.1 推荐采用的总体方案

本项目不应该只有一个“数据库”。更合理的方案是分层：

| 层级 | 作用 | 推荐技术 | 原因 |
|---|---|---|---|
| 原始数据层 | 保存外部数据源的原始 JSON、许可、来源快照 | Git 管理的 `data/raw/` + source manifest | 可追溯、可复现、便于重新清洗 |
| 标准数据层 | 保存清洗后的 canonical poem schema | `data/processed/*.jsonl` + 版本号 | 便于脚本、实验、迁移、抽样审核 |
| 在线业务库 | 支撑用户、行为、收藏、推荐日志、内容画像 | PostgreSQL | 关系数据、行为日志、事务、一致性、可迁移性好 |
| 向量检索层 | 支撑语义召回、相似诗词、RAG/Agent 检索 | PostgreSQL + pgvector | 与业务表共库，MVP 不需要单独维护向量数据库 |
| 前端离线缓存 | PWA / 浏览器插件本地缓存诗词、用户状态 | IndexedDB；插件侧也可用 `chrome.storage` | 适合浏览器端结构化数据缓存与离线访问 |
| 实验与原型层 | 本地快速验证数据导入、搜索、推荐 | SQLite / DuckDB 可选 | 轻量、无需服务，适合 notebook/脚本实验 |

### 1.2 最核心的数据库决策

**Phase 1-2：先用 JSONL + Python 脚本验证数据 schema 与推荐闭环。** 这一步不要急着上 PostgreSQL，否则 schema 还没稳定就会产生迁移成本。

**Phase 3 开始：在线服务主库使用 PostgreSQL，并启用 pgvector。** 本项目需要同时处理诗词元数据、标签、用户行为、推荐日志、收藏、Push subscription、Agent run 记录和 embedding。PostgreSQL 能同时承载结构化关系、`jsonb` 扩展字段、全文检索、事务和向量扩展，适合一个人维护的 AI 全栈项目。

**不要在 MVP 阶段单独引入 Pinecone、Milvus、Weaviate、Elasticsearch。** 它们都能做某一类问题，但会增加运维和概念复杂度；等数据量和召回性能真的成为瓶颈后再拆。

---

## 2. 本项目对数据库的真实需求

### 2.1 内容数据需求

诗词内容不是单纯的 `title + author + content`。推荐系统需要更丰富的内容画像：

- 正文：标题、作者、朝代、体裁、词牌、正文、分句。
- 来源：原始数据源、许可、原始文件路径、导入批次。
- 质量：是否人工审核、是否有疑似错字、是否重复、是否适合推荐。
- 标签：主题、风格、情绪、场景、意象、体裁、难度、熟悉度。
- AI 字段：embedding、LLM 标注结果、推荐解释素材、Agent 审核状态。
- 展示字段：精选句、短摘要、适合壁纸/通知/新标签页的摘句。

### 2.2 用户与行为需求

推荐闭环需要保存的不只是收藏列表，还包括完整事件流：

- 用户初始问卷答案。
- 用户画像权重：偏好作者、主题、风格、难度、熟悉度、探索容忍度。
- 用户行为事件：曝光、点击、停留、喜欢、不喜欢、收藏、跳过、查看注释、生成壁纸、通知点击。
- 推荐日志：某次推荐为什么出现、分数是多少、召回来源是什么、排序位置是什么。
- 多端来源：PWA、Web Push、浏览器新标签页插件、未来 App。

### 2.3 调取方式需求

数据库必须支持这些调用方式：

1. **按 ID 取诗词详情**：详情页、收藏夹、历史记录。
2. **按标签/作者/体裁召回候选**：推荐系统第一阶段。
3. **按 embedding 相似度召回候选**：语义推荐、相似诗词、Agent 检索。
4. **按用户画像生成推荐 feed**：PWA 首页和插件新标签页。
5. **写入用户事件并更新画像**：行为闭环。
6. **记录推荐日志并离线评估**：面试展示和算法迭代。
7. **离线导出训练/评估数据**：推荐实验、Agent 标注质量评估。

---

## 3. 数据来源调研

### 3.1 首选来源：`chinese-poetry/chinese-poetry`

调研结论：这是 MVP 最适合的基础正文来源。

原因：

- 数据量足够大：仓库 README 称包含约 5.5 万首唐诗、26 万首宋诗、2.1 万首宋词，以及其他古典文集。
- 格式适合工程化处理：项目说明其通过 JSON 格式分发，便于开发者构建诗词类应用。
- 许可较友好：仓库标注 MIT license。
- 生态实践多：该仓库 README 列出了浏览器诗词网站、Android 离线全唐诗、诗词桌面、诗词小程序、MySQL DB 整合项目等案例，说明它常被用作诗词类项目的数据基础。

风险与处理：

- README 明确提到数据来源于互联网，采集过程没有完整记录；因此不能把它视为“绝对权威文本”。
- 不能直接信任所有断句、作者、标题和重复情况，需要抽样审核、去重和来源记录。
- 注释、翻译、赏析不能从商业网站直接复制；MVP 只能先做少量人工整理或 AI 辅助后人工审核。

建议用法：

- Phase 1 不拉取全量，只抽取 100-500 首 seed 数据。
- 优先选唐诗三百、宋词三百、诗经精选、苏轼/李白/杜甫/王维/李清照/辛弃疾等重点作者。
- 保留 `source_dataset`、`source_file`、`source_record_index`，保证每条诗词可追溯。

参考：`chinese-poetry/chinese-poetry` README 说明其规模、JSON 分发、MIT license 与案例展示。

### 3.2 可选来源：`chinese-poetry-npm`

适用场景：前端或 Node.js 侧快速消费诗词数据。

优点：

- 来源与 `chinese-poetry` 同生态。
- 适合以后浏览器插件或纯前端 demo 直接安装数据包。

限制：

- 本项目最终需要统一后端 schema，不应让前端直接依赖第三方包结构。
- 可以作为数据导入输入源，但导入后必须转换成自己的 canonical schema。

### 3.3 不建议作为主数据源：公开网站爬虫

原因：

- 版权和 ToS 风险更高。
- 注释、翻译、赏析多为现代整理内容，版权风险大于古诗正文。
- 数据清洗成本不可控。

可接受用法：

- 只作为人工核验参考。
- 不把爬取的现代注释/翻译直接入库上线。

### 3.4 AI 生成数据的定位

AI 适合生成或辅助生成：

- 标签、主题、风格、情绪、难度。
- 推荐解释候选。
- 白话翻译初稿。
- 用户偏好总结。

AI 不适合直接作为唯一事实来源：

- 作者、朝代、正文、关键注释必须可追溯。
- AI 输出必须保留 `generated_by`、`model`、`prompt_version`、`review_status`。

---

## 4. 数据结构设计

### 4.1 原始数据层：source manifest

建议新增：`data/raw/source_manifest.json`

```json
[
  {
    "source_id": "chinese_poetry_tang_300",
    "name": "chinese-poetry 唐诗数据子集",
    "homepage": "https://github.com/chinese-poetry/chinese-poetry",
    "license": "MIT",
    "retrieved_at": "2026-06-24",
    "raw_path": "data/raw/chinese-poetry/",
    "usage": "seed corpus for public-domain poem text; must be normalized before product use",
    "risk_notes": [
      "upstream says data comes from internet",
      "text correctness requires sampling audit",
      "annotations/translations are not imported from commercial sites"
    ]
  }
]
```

### 4.2 标准诗词 schema：canonical poem

建议新增：`docs/data-schema.md`，其中核心字段如下：

```json
{
  "poem_id": "poem_tang_li_bai_jing_ye_si",
  "title": "静夜思",
  "author": {
    "author_id": "author_li_bai",
    "name": "李白",
    "dynasty": "唐"
  },
  "dynasty": "唐",
  "genre": "诗",
  "form": "五言绝句",
  "cipai": null,
  "content": {
    "paragraphs": ["床前明月光，疑是地上霜。", "举头望明月，低头思故乡。"],
    "lines": ["床前明月光", "疑是地上霜", "举头望明月", "低头思故乡"]
  },
  "features": {
    "themes": ["思乡", "月夜"],
    "styles": ["自然", "含蓄", "清浅"],
    "imagery": ["明月", "霜"],
    "mood": ["孤独", "怀念"],
    "difficulty": 1,
    "familiarity": 5,
    "quality": 5,
    "suitable_contexts": ["夜晚", "思乡", "入门学习"]
  },
  "display": {
    "excerpt": "举头望明月，低头思故乡。",
    "short_reason_seed": "这是一首高度熟悉、语言浅近的思乡名篇。"
  },
  "source": {
    "source_id": "chinese_poetry",
    "source_file": "全唐诗/poet.tang.0.json",
    "source_record_index": 0,
    "license": "MIT"
  },
  "review": {
    "text_status": "sample_checked",
    "feature_status": "ai_generated_pending_review",
    "reviewer": null,
    "updated_at": "2026-06-24"
  }
}
```

设计原则：

- `poem_id` 必须稳定，不能用数据库自增 ID 作为跨端主键。
- 作者、朝代、体裁等高频过滤字段应结构化，不只放在 JSON 里。
- 标签、AI 标注、展示素材可在早期用 JSON 承载，稳定后再拆表。
- 正文要同时保留 `paragraphs` 和 `lines`，方便详情页、壁纸、通知和搜索。

### 4.3 PostgreSQL 在线表结构建议

#### `poems`

```sql
CREATE TABLE poems (
  id UUID PRIMARY KEY,
  poem_key TEXT UNIQUE NOT NULL,
  title TEXT NOT NULL,
  author_id UUID REFERENCES authors(id),
  dynasty TEXT,
  genre TEXT NOT NULL,
  form TEXT,
  cipai TEXT,
  paragraphs JSONB NOT NULL,
  lines JSONB NOT NULL,
  excerpt TEXT,
  source_id TEXT,
  source_file TEXT,
  source_record_index INTEGER,
  text_status TEXT NOT NULL DEFAULT 'unreviewed',
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

#### `poem_features`

```sql
CREATE TABLE poem_features (
  poem_id UUID PRIMARY KEY REFERENCES poems(id),
  themes JSONB NOT NULL DEFAULT '[]',
  styles JSONB NOT NULL DEFAULT '[]',
  imagery JSONB NOT NULL DEFAULT '[]',
  mood JSONB NOT NULL DEFAULT '[]',
  suitable_contexts JSONB NOT NULL DEFAULT '[]',
  difficulty SMALLINT,
  familiarity SMALLINT,
  quality SMALLINT,
  feature_status TEXT NOT NULL DEFAULT 'unreviewed',
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

#### `poem_embeddings`

```sql
CREATE TABLE poem_embeddings (
  poem_id UUID PRIMARY KEY REFERENCES poems(id),
  embedding_model TEXT NOT NULL,
  embedding vector(1536),
  embedded_text TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

> 维度 `1536` 只是示例，最终取决于 embedding 模型。文档和迁移脚本中必须把模型名、维度和生成文本版本绑定起来。

#### `user_events`

```sql
CREATE TABLE user_events (
  id UUID PRIMARY KEY,
  user_id UUID,
  anonymous_id TEXT,
  poem_id UUID REFERENCES poems(id),
  event_type TEXT NOT NULL,
  event_value DOUBLE PRECISION,
  source TEXT NOT NULL,
  metadata JSONB NOT NULL DEFAULT '{}',
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

#### `recommendation_logs`

```sql
CREATE TABLE recommendation_logs (
  id UUID PRIMARY KEY,
  request_id TEXT NOT NULL,
  user_id UUID,
  anonymous_id TEXT,
  poem_id UUID REFERENCES poems(id),
  rank_position INTEGER NOT NULL,
  final_score DOUBLE PRECISION NOT NULL,
  recall_sources JSONB NOT NULL DEFAULT '[]',
  score_breakdown JSONB NOT NULL DEFAULT '{}',
  explanation TEXT,
  surface TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

### 4.4 何时 JSONB，何时拆表

| 数据 | MVP 存法 | 长期存法 | 原因 |
|---|---|---|---|
| 诗词标题、作者、朝代、体裁 | 普通列 | 普通列 | 高频过滤、排序、展示 |
| 正文 lines/paragraphs | JSONB | JSONB 或子表 | 数组结构稳定，查询频率不复杂 |
| 标签 themes/styles | JSONB 数组 | 标签表 + 关系表可选 | MVP 灵活；规模增大后便于统计和治理 |
| 用户事件 metadata | JSONB | JSONB | 事件属性多变，适合半结构化 |
| 推荐分数 breakdown | JSONB | JSONB | 便于解释和调试，字段会经常变化 |
| embedding | vector | vector | 向量检索需要专门类型和索引 |

PostgreSQL 官方文档说明 `jsonb` 以分解后的二进制格式存储，处理时不需要每次重新解析，适合频繁处理的 JSON 数据；同时 `jsonb` 可以用 GIN 索引高效检索 key/value。因此，`jsonb` 适合作为 MVP 阶段承载标签、事件 metadata、推荐分数 breakdown 的扩展字段。

---

## 5. 存储方式与调取方式

### 5.1 后端主调取方式

推荐后端通过 Repository/Service 层隔离数据库：

```text
API Layer
  ↓
RecommendationService
  ↓
PoemRepository / UserProfileRepository / EventRepository
  ↓
PostgreSQL + pgvector
```

不要让前端直接拼 SQL，也不要把推荐逻辑写进前端。

### 5.2 推荐系统读取流程

一次推荐请求建议如下：

```text
GET /api/recommendations/feed?surface=newtab
  ↓
读取 user_profile
  ↓
读取最近 user_events / recommendation_logs
  ↓
多路召回：标签、作者、经典池、embedding 相似、探索池
  ↓
排序：用户匹配 + 质量 + 熟悉度 + 新颖度
  ↓
重排：多样性、去重、同作者限制、最近曝光降权
  ↓
写 recommendation_logs
  ↓
返回 poem card + explanation + request_id
```

### 5.3 行为写入流程

```text
POST /api/events
  ↓
写 user_events append-only log
  ↓
同步或异步更新 user_profile
  ↓
必要时触发下一次推荐缓存失效
```

建议行为日志 append-only，不要覆盖旧事件。这样后续能做离线评估和面试展示。

### 5.4 PWA / 插件本地缓存

前端本地缓存分两类：

| 数据 | PWA 推荐存储 | 插件推荐存储 | 说明 |
|---|---|---|---|
| 最近推荐卡片 | IndexedDB | IndexedDB 或 `chrome.storage.local` | 支持离线打开 |
| 用户轻量偏好 | IndexedDB | `chrome.storage.local` / `sync` | 插件可跨浏览器账号同步少量设置 |
| 全量诗词库 | 不建议全量缓存 | 不建议全量缓存 | 数据量会膨胀，且更新困难 |
| 最近 50-200 首诗词详情 | IndexedDB | IndexedDB | 提升打开速度 |

MDN 对 IndexedDB 的定位是浏览器端存储大量结构化数据，并通过索引支持高性能搜索；因此它适合 PWA 和插件缓存，而不是替代后端主库。

---

## 6. 数据库选型对比

### 6.1 PostgreSQL + pgvector

优点：

- 支持关系数据、事务、约束、JOIN，适合用户、行为、收藏和推荐日志。
- `jsonb` 能承载 AI 标注、事件 metadata、推荐分数 breakdown 等半结构化字段。
- pgvector 支持向量存储、精确/近似最近邻检索、多种距离度量，可以把 embedding 和业务数据放在同一个数据库里。
- 面试解释价值高：既能讲业务建模，也能讲语义召回和推荐日志评估。

缺点：

- 比 SQLite 更需要部署和迁移管理。
- 向量检索规模很大时，专用向量库可能更强。

结论：

> **推荐作为 Phase 3 以后的在线主库。**

### 6.2 SQLite

优点：

- 零服务，适合本地开发、数据清洗、实验和单机 demo。
- SQLite FTS5 支持全文检索，适合诗词标题/正文检索原型。
- 可以作为脚本处理的中间产物。

缺点：

- 多用户服务、并发写入、复杂权限、云部署和向量推荐都不如 PostgreSQL 合适。
- 不适合作为最终多端推荐产品的唯一在线主库。

结论：

> **适合作为 Phase 1-2 的本地实验数据库，不作为最终在线主库。**

### 6.3 MongoDB

优点：

- 文档模型灵活，适合半结构化内容。
- 诗词原始 JSON 可以较自然地存入。

缺点：

- 本项目有大量关系：用户-事件、用户-收藏、推荐日志、诗词-作者、诗词-标签。
- 推荐日志和行为分析经常需要 JOIN、聚合、时间窗口，PostgreSQL 更通用。
- 向量、事务和分析链路在个人项目中用 PostgreSQL 更容易形成统一叙事。

结论：

> **不作为首选。除非项目变成纯内容文档库，否则没必要引入。**

### 6.4 Elasticsearch / OpenSearch

优点：

- 全文搜索强，适合复杂检索、高亮、分词、相关性排序。

缺点：

- 运维复杂，MVP 数据量不需要。
- 本项目核心不是搜索引擎，而是推荐系统。

结论：

> **后期如果搜索成为核心功能再考虑，不进入 MVP。**

### 6.5 Pinecone / Milvus / Weaviate / Qdrant

优点：

- 专门做向量检索，扩展性和召回能力强。

缺点：

- 对个人 MVP 增加服务依赖和成本。
- 需要额外同步业务 ID、元数据过滤、权限和备份。
- 本项目初期诗词规模几十万以内，用 pgvector 足够验证推荐闭环。

结论：

> **不进入 MVP。等 pgvector 确实成为瓶颈再拆。**

### 6.6 Supabase

Supabase 不是一种数据库，而是托管 PostgreSQL + Auth + Storage + Edge Functions 等组合。

优点：

- 免费额度适合个人项目。
- PostgreSQL + pgvector 支持路径清晰。
- 以后如果需要登录、云同步、简单后台，开发效率高。

缺点：

- 会引入平台绑定。
- 如果主要目标是展示后端能力，完全依赖 BaaS 会削弱“我自己搭建后端”的表达。

结论：

> **可以作为部署选项，但本地开发和文档应按标准 PostgreSQL + FastAPI 设计。**

---

## 7. 类似项目实践观察

### 7.1 `chinese-poetry` 生态实践

`chinese-poetry` README 的案例展示很有价值：

- 浏览器诗词网站：说明 JSON 数据可以直接驱动 Web 展示。
- Android 离线全唐诗：说明诗词正文适合打包到本地离线库。
- 诗词桌面、诗词小程序：说明诗词内容适合强触达/轻交互产品形态。
- MySQL DB 整合 + Web 展示：说明有人把 JSON 转为关系数据库以支持检索和 Web 服务。

对本项目的启发：

- 原始 JSON 适合作为输入，不适合作为最终推荐系统的唯一存储。
- 离线展示型产品可以直接读 JSON，但个性化推荐需要用户行为库和推荐日志。
- 本项目相比已有案例的差异化不在“诗词大全”，而在“推荐闭环 + AI 内容理解 + 强触达”。

### 7.2 诗词生成项目实践

一些古诗生成项目会把 `chinese-poetry` JSON 转成训练文本，例如 `标题::作者::内容` 形式。这说明：

- 原始诗词 JSON 通常需要为不同任务转换格式。
- 本项目也应该保留“导出层”：既能导出推荐服务需要的结构化表，也能导出 embedding/Agent/evaluation 需要的 JSONL。

---

## 8. 推荐的目录与数据流

### 8.1 目录结构

建议 Phase 1 新增：

```text
data/
  raw/
    source_manifest.json
    chinese-poetry/              # 不一定提交全量，可用 README 指向获取方式
  samples/
    poems.sample.jsonl           # 20-100 首人工 seed
  processed/
    poems.v0.jsonl               # canonical poems
    authors.v0.jsonl
    import_report.v0.json

docs/
  data-schema.md
  database-research.md

scripts/
  data_import/
    normalize_poems.py
    validate_poems.py
    build_seed_dataset.py
```

### 8.2 数据流

```text
外部数据源 chinese-poetry JSON
  ↓
raw source manifest 记录来源、许可、获取时间
  ↓
normalize script 转成 canonical JSONL
  ↓
validate script 校验 schema、重复、必填字段、正文长度
  ↓
processed JSONL 进入推荐实验
  ↓
Phase 3 导入 PostgreSQL
  ↓
LLM/Agent 标注 features + embeddings
  ↓
推荐服务读取 poems / poem_features / poem_embeddings
  ↓
用户行为写入 events / recommendation_logs
```

---

## 9. 索引与性能规划

### 9.1 PostgreSQL 索引建议

```sql
CREATE INDEX idx_poems_author_id ON poems(author_id);
CREATE INDEX idx_poems_dynasty ON poems(dynasty);
CREATE INDEX idx_poems_genre ON poems(genre);
CREATE INDEX idx_poem_features_themes_gin ON poem_features USING GIN (themes);
CREATE INDEX idx_poem_features_styles_gin ON poem_features USING GIN (styles);
CREATE INDEX idx_user_events_user_created ON user_events(user_id, created_at DESC);
CREATE INDEX idx_user_events_anon_created ON user_events(anonymous_id, created_at DESC);
CREATE INDEX idx_recommendation_logs_request ON recommendation_logs(request_id);
```

向量索引：

```sql
CREATE INDEX idx_poem_embeddings_hnsw
ON poem_embeddings
USING hnsw (embedding vector_cosine_ops);
```

### 9.2 为什么推荐 HNSW

pgvector 文档说明 HNSW 的速度-召回权衡通常优于 IVFFlat，但构建更慢、内存占用更高。对于本项目，诗词 embedding 更新频率不高，读多写少，HNSW 适合作为语义召回索引。

### 9.3 全文搜索策略

MVP 可先不用 Elasticsearch：

- 后端 PostgreSQL 可用基础 `ILIKE` 或 PostgreSQL full text search 做简单搜索。
- 本地实验可用 SQLite FTS5 验证诗词正文检索。
- 真正复杂的中文分词、拼音搜索、注释搜索后期再单独规划。

---

## 10. 兼容后续步骤的关键约束

### 10.1 稳定 ID

`poem_id` / `poem_key` 必须从 Phase 1 就稳定，否则后续收藏、事件、推荐日志、embedding 都会失效。

建议格式：

```text
poem_{dynasty_slug}_{author_slug}_{title_slug}_{short_hash}
```

例如：

```text
poem_tang_li_bai_jing_ye_si_a1b2c3
```

### 10.2 数据版本

每次处理后的数据集要有版本：

```text
poems.v0.jsonl
poems.v1.jsonl
```

推荐日志中也要记录 `corpus_version`，否则离线评估无法复现。

### 10.3 AI 标注可追溯

所有 AI 标注字段必须记录：

```text
model
prompt_version
input_hash
generated_at
review_status
```

这样 Agent 开发岗位面试时可以讲清楚“可控生成”和“人工审核”。

### 10.4 原始数据与产品数据分离

不要直接修改 raw 数据；任何纠错都写入 processed 层或 `data_corrections` 表。这样能保留来源，也能解释为什么产品数据和上游不同。

---

## 11. 分阶段落地计划

### Phase 1：数据 MVP

产出：

- `docs/data-schema.md`
- `data/raw/source_manifest.json`
- `data/samples/poems.sample.jsonl`
- `scripts/data_import/validate_poems.py`
- `scripts/data_import/normalize_poems.py`

验收：

- 20-100 首诗词通过 schema 校验。
- 每首都有稳定 `poem_id`、来源、正文、基础标签。
- 能输出 import report：数量、重复、缺字段、标签覆盖率。

### Phase 2：推荐闭环实验

产出：

- 本地 JSONL 读入推荐脚本。
- 模拟用户画像与行为事件。
- 推荐前后变化报告。

验收：

- 用户喜欢某类诗后，该类标签权重上升。
- 不喜欢某类诗后，该类标签权重下降。
- 推荐结果仍保留熟悉/探索比例。

### Phase 3：PostgreSQL 在线库

产出：

- 数据库迁移 SQL / Alembic。
- 导入 processed JSONL 到 PostgreSQL。
- 基础 API：poem detail、recommendations、events、favorites。
- pgvector embedding 表可先留空，后续填充。

验收：

- 后端能从 PostgreSQL 返回推荐 feed。
- 用户事件能写入并更新用户画像。
- recommendation logs 能记录每次推荐原因。

### Phase 4：AI / Agent 数据增强

产出：

- 内容标注 Agent。
- embedding 生成脚本。
- 推荐解释生成脚本。
- 标注质量抽样报告。

验收：

- 至少 100 首诗有 AI 标签和 embedding。
- 相似诗词召回能工作。
- 推荐解释能引用用户偏好和诗词特征。

---

## 12. 最终建议

本项目的数据库方案应当服务于“推荐闭环”，而不是服务于“诗词大全”。最终建议如下：

1. **数据来源**：以 `chinese-poetry/chinese-poetry` 为基础正文来源，少量人工 seed 起步，保留来源与许可记录。
2. **数据结构**：建立自己的 canonical poem schema，不直接暴露上游 JSON 结构给业务层。
3. **存储方式**：raw/processed 文件层 + PostgreSQL 在线主库 + pgvector 语义召回 + IndexedDB/插件本地缓存。
4. **调取方式**：所有端都通过推荐 API 和事件 API 接入，不让 PWA、插件、未来 App 各自维护割裂逻辑。
5. **兼容性**：从 Phase 1 就保证稳定 ID、数据版本、来源追溯、AI 标注版本，避免后续推荐日志和 embedding 失效。
6. **不做的事**：MVP 不引入独立向量数据库、Elasticsearch 或 MongoDB，不直接爬取商业网站注释翻译，不把静态 JSON 当作最终数据库。

---

## 13. `chinese-poetry` 是否直接满足 features 需求？

简短结论：不能。`chinese-poetry/chinese-poetry` 适合作为 raw corpus 和正文底座，但它没有直接提供本项目推荐系统需要的主题、风格、情绪、难度、熟悉度、推荐解释、注释翻译、用户行为或 embedding 等完整 features。

更详细的字段覆盖、raw JSON 抽样、缺口分析和 Phase 1 修正方案见：[`docs/chinese-poetry-source-evaluation.md`](chinese-poetry-source-evaluation.md)。

---

## 14. 调研来源

- [`chinese-poetry/chinese-poetry`](https://github.com/chinese-poetry/chinese-poetry)：诗词正文主候选数据源；README 提供数据规模、JSON 分发、MIT license、生态案例信息。
- [`chinese-poetry/chinese-poetry-npm`](https://github.com/chinese-poetry/chinese-poetry-npm)：前端/Node.js 使用场景参考。
- [`pgvector/pgvector`](https://github.com/pgvector/pgvector)：PostgreSQL 向量检索扩展；支持 exact/approximate nearest neighbor、HNSW/IVFFlat 等。
- [PostgreSQL JSON Types](https://www.postgresql.org/docs/current/datatype-json.html)：`jsonb` 存储、处理效率和 GIN 索引参考。
- [SQLite FTS5](https://sqlite.org/fts5.html)：本地全文检索实验参考。
- [MDN IndexedDB API](https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API)：浏览器端结构化数据缓存参考。
