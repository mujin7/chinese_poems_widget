# 项目实施路线图与阶段产出

## 1. 这份文档解决什么问题

前面的文档已经回答了：

- 这个项目是什么。
- 为什么不是单纯壁纸、PWA 或插件。
- Planning 阶段还需要调研什么。
- 推荐系统、AI / Agent、强触达的大方向是什么。

这份文档进一步回答：

> **接下来应该按什么顺序做，每一步产出什么，以及每一步如何兼容后续步骤。**

核心原则是：

```text
先闭环，后体验；
先后端与数据，后复杂前端；
先可验证，后可扩展；
先本地/小规模，后云端/多端；
每一步都要给下一步留下接口和数据结构。
```

---

## 2. 总体路线

建议把项目分成 8 个阶段：

```text
Phase 0：项目骨架与工程规范
Phase 1：诗词数据 MVP
Phase 2：推荐系统最小闭环
Phase 3：后端 API 与数据库
Phase 4：Web MVP 用户界面
Phase 5：AI / Agent 内容增强
Phase 6：强触达能力
Phase 7：评估、展示与求职包装
```

每个阶段都要产出可检查的东西，避免只停留在想法。

---

## 3. 阶段设计总览

| 阶段 | 目标 | 核心产出 | 是否阻塞后续 |
|---|---|---|---|
| Phase 0 | 搭好工程骨架 | repo 结构、依赖、代码规范、基础 README | 是 |
| Phase 1 | 有可用诗词数据 | 小规模诗词 JSON/DB、schema、清洗脚本 | 是 |
| Phase 2 | 验证推荐会随行为变化 | 推荐脚本、用户画像、行为模拟、评估样例 | 是 |
| Phase 3 | 后端化推荐闭环 | FastAPI、PostgreSQL、事件 API、推荐 API | 是 |
| Phase 4 | 用户可以真实交互 | 问卷页、推荐页、详情页、反馈按钮 | 是 |
| Phase 5 | AI 增强内容理解 | 标签生成、推荐解释、Agent 运行记录 | 否，但加分 |
| Phase 6 | 主动触达用户 | Web Push、浏览器新标签页插件 | 否，但符合产品核心 |
| Phase 7 | 面试展示与验证 | demo、指标面板、案例、项目说明 | 是 |

---

## 4. Phase 0：项目骨架与工程规范

### 4.1 目标

把空仓库变成一个可以持续开发的工程项目。

### 4.2 为什么先做

如果没有工程骨架，后续每一步都会混乱：

- 数据脚本不知道放哪里。
- 推荐算法和后端代码混在一起。
- 前端、后端、Agent 没有边界。
- 面试展示时很难说明架构。

### 4.3 建议目录结构

```text
chinese_poems_widget/
├── README.md
├── docs/
│   ├── product-plan.md
│   ├── planning-research.md
│   ├── implementation-roadmap.md
│   └── github-codex-workflow.md
├── data/
│   ├── raw/
│   ├── processed/
│   └── samples/
├── scripts/
│   ├── data_import/
│   └── evaluation/
├── backend/
│   ├── app/
│   └── tests/
├── frontend/
│   ├── app/
│   └── tests/
├── extension/
│   └── newtab/
└── experiments/
    ├── recommendation/
    └── agent/
```

### 4.4 具体任务

- 创建工程目录。
- 选择语言与包管理工具。
- 添加基础 `.gitignore`。
- 添加 `docs/` 文档入口。
- 明确 Python / Node 版本。
- 决定是否使用 Docker。
- 决定后端是否从 FastAPI 开始。
- 决定前端是否从 Next.js 开始。

### 4.5 阶段产出

```text
1. 清晰的 repo 目录结构
2. README 更新为项目入口
3. docs/implementation-roadmap.md
4. backend / frontend / data / scripts 占位目录
5. 初始开发命令说明
```

### 4.6 和后续步骤的兼容性

- `data/` 为 Phase 1 数据清洗保留位置。
- `scripts/` 为导入、评估、批处理保留位置。
- `backend/` 为 Phase 3 API 服务保留位置。
- `frontend/` 为 Phase 4 Web MVP 保留位置。
- `extension/` 为 Phase 6 新标签页插件保留位置。
- `experiments/` 为推荐和 Agent 实验保留位置。

---

## 5. Phase 1：诗词数据 MVP

### 5.1 目标

先得到一批质量可控、字段稳定、能支持推荐的诗词数据。

### 5.2 为什么先做数据

推荐系统的输入是内容。如果数据字段混乱，后续推荐、AI 标注、详情页和搜索都会返工。

### 5.3 数据规模建议

MVP 不需要全量诗词。

建议第一批：

```text
100-300 首：用于快速开发和调试
500-1000 首：用于第一版推荐体验
```

### 5.4 数据字段 schema

第一版至少包含：

```json
{
  "id": "tang_wangwei_shanjvqiuming",
  "title": "山居秋暝",
  "author": "王维",
  "dynasty": "唐",
  "type": "律诗",
  "content": [
    "空山新雨后，天气晚来秋。",
    "明月松间照，清泉石上流。"
  ],
  "tags": ["山水", "秋天", "清新", "闲适"],
  "difficulty": 2,
  "familiarity": 5,
  "quality": 5,
  "source": "manual_seed"
}
```

### 5.5 具体任务

- 选定第一批诗词来源。
- 定义 `poem.schema.json`。
- 写入 20 首人工 seed 数据。
- 编写导入脚本。
- 编写数据校验脚本。
- 检查字段完整性。
- 标准化作者、朝代、体裁、标签。
- 建立数据质量问题列表。

### 5.6 阶段产出

```text
1. data/samples/poems.sample.json
2. data/processed/poems.mvp.json
3. docs/data-schema.md
4. scripts/data_import/validate_poems.py
5. 数据质量报告
```

### 5.7 验收标准

- 每首诗有稳定唯一 ID。
- 每首诗有标题、作者、朝代、正文。
- 80% 以上诗词有基础标签。
- 数据校验脚本能发现缺字段、重复 ID、空正文。

### 5.8 和后续步骤的兼容性

- 稳定 ID 会被用户行为、收藏、推荐日志引用，不能随意变化。
- 标签字段会被 Phase 2 推荐算法使用。
- `difficulty`、`familiarity` 会影响推荐排序。
- `source` 字段为版权追踪和数据质量审计服务。

---

## 6. Phase 2：推荐系统最小闭环

### 6.1 目标

不急着做前端，先证明推荐结果会根据用户行为变化。

### 6.2 为什么这一阶段很关键

这是项目最核心的求职价值：

```text
用户画像
内容画像
行为反馈
推荐变化
```

只要这个闭环跑通，产品就不只是一个展示页。

### 6.3 最小推荐闭环

```text
输入：用户问卷答案
↓
生成：初始用户画像
↓
推荐：返回 Top N 诗词
↓
反馈：用户喜欢/不喜欢/收藏/跳过
↓
更新：用户画像权重变化
↓
再推荐：下一批结果发生变化
```

### 6.4 具体任务

- 定义用户画像结构。
- 定义行为事件结构。
- 实现标签匹配打分。
- 实现作者偏好打分。
- 实现熟悉度/探索度控制。
- 实现最近曝光去重。
- 实现简单多样性重排。
- 写一个命令行模拟脚本。

### 6.5 推荐模块接口

建议先实现成纯 Python 模块：

```python
def build_initial_profile(onboarding_answers):
    ...


def recommend(profile, poems, recent_events, limit=10):
    ...


def update_profile(profile, event, poem):
    ...
```

### 6.6 阶段产出

```text
1. backend/app/recommendation/
2. scripts/evaluation/simulate_user_feedback.py
3. docs/recommendation-design.md
4. 示例用户画像 JSON
5. 示例推荐结果 JSON
6. 行为反馈前后对比报告
```

### 6.7 验收标准

- 用户喜欢“山水”后，山水相关诗词权重上升。
- 用户不喜欢“边塞”后，边塞相关诗词推荐下降。
- 同一作者不会连续刷屏。
- 推荐结果中同时包含熟悉内容和探索内容。
- 每次推荐能输出推荐理由字段。

### 6.8 和后续步骤的兼容性

- 推荐模块要写成后端可调用的 service，而不是只写在脚本里。
- 用户画像和行为事件 schema 要和 Phase 3 数据库一致。
- 推荐结果要包含 `score`、`reason`、`recall_source`，方便后续做日志和评估。

---

## 7. Phase 3：后端 API 与数据库

### 7.1 目标

把推荐闭环从脚本升级为可被前端、插件、Web Push 调用的后端服务。

### 7.2 为什么现在做后端

前端、插件、Web Push 都需要统一的服务端能力：

- 获取诗词详情
- 提交用户行为
- 获取推荐结果
- 保存收藏
- 更新用户画像
- 保存推荐日志

### 7.3 建议技术栈

```text
FastAPI
PostgreSQL
SQLAlchemy / SQLModel
Alembic
Pydantic
pytest
```

后续需要语义召回时再加入：

```text
pgvector
embedding batch job
```

### 7.4 核心 API

```text
GET  /health
GET  /poems/{poem_id}
GET  /recommendations/feed
GET  /recommendations/today
POST /events
GET  /profile
POST /onboarding
POST /favorites
DELETE /favorites/{poem_id}
```

### 7.5 核心数据库表

```text
poems
poem_features
users
user_profiles
user_events
favorites
recommendation_logs
```

### 7.6 具体任务

- 初始化 FastAPI 项目。
- 建立数据库连接。
- 设计 ORM model。
- 添加 migration。
- 导入 Phase 1 诗词数据。
- 暴露诗词详情 API。
- 暴露推荐 API。
- 暴露行为事件 API。
- 行为事件触发用户画像更新。
- 推荐结果写入推荐日志。

### 7.7 阶段产出

```text
1. backend/app/main.py
2. backend/app/models/
3. backend/app/api/
4. backend/app/services/recommendation_service.py
5. backend/app/services/profile_service.py
6. backend/alembic migrations
7. docs/api-design.md
8. docs/database-schema.md
9. API smoke test
```

### 7.8 验收标准

- `GET /health` 正常返回。
- 可以导入诗词数据。
- 可以提交问卷并生成用户画像。
- 可以获取推荐 feed。
- 可以提交 like/dislike/favorite/skip。
- 用户反馈后再次请求推荐，结果发生变化。
- 推荐日志可追踪每次推荐的结果和分数。

### 7.9 和后续步骤的兼容性

- Web 前端只调用 API，不直接操作推荐逻辑。
- Chrome 插件后续也调用同一套 API。
- Web Push 的每日推荐也调用同一套 recommendation service。
- Agent 生成的标签写入 `poem_features`，不破坏原始 `poems` 表。

---

## 8. Phase 4：Web MVP 用户界面

### 8.1 目标

让真实用户可以完成问卷、看到推荐、进行反馈。

### 8.2 为什么先做 Web MVP

Web MVP 是最简单的产品验证入口：

- 不需要 App Store。
- 不需要浏览器插件审核。
- 方便分享给朋友测试。
- 方便收集反馈。

### 8.3 页面范围

MVP 只需要：

```text
1. 首页 / 项目介绍
2. 初始问卷页
3. 推荐 Feed 页
4. 诗词详情页
5. 收藏页
6. 简单偏好页
```

### 8.4 具体任务

- 初始化前端项目。
- 建立 API client。
- 实现问卷表单。
- 实现推荐卡片。
- 实现喜欢、不喜欢、收藏、跳过按钮。
- 实现诗词详情页。
- 实现收藏列表。
- 显示“为什么推荐”。
- 增加基础加载和错误状态。

### 8.5 阶段产出

```text
1. frontend/app/
2. 问卷页面
3. 推荐页面
4. 详情页面
5. 收藏页面
6. API client
7. 基础 UI 组件
8. 可录屏 demo
```

### 8.6 验收标准

- 用户能完成问卷。
- 用户能看到推荐列表。
- 用户能打开诗词详情。
- 用户能点击喜欢、不喜欢、收藏、跳过。
- 用户反馈后推荐能变化。
- 页面能展示推荐理由。

### 8.7 和后续步骤的兼容性

- UI 组件要尽量可被插件复用。
- 推荐行为统一走 `POST /events`。
- 不要把推荐算法写在前端。
- 前端只负责展示、交互和行为上报。

---

## 9. Phase 5：AI / Agent 内容增强

### 9.1 目标

用 AI 提升内容理解、推荐解释和项目技术含金量。

### 9.2 不要一开始就做 AI 的原因

如果没有前面的数据和推荐闭环，AI 会变成装饰：

```text
看起来高级，但无法证明产品更好。
```

所以 AI 应该在推荐闭环跑通后加入。

### 9.3 Agent 模块

```text
内容标注 Agent：生成主题、风格、情绪、场景、难度
推荐解释 Agent：基于用户画像和推荐分数生成解释
用户偏好总结 Agent：总结用户近期偏好变化
评估 Agent：检查推荐列表是否重复、解释是否不一致
```

### 9.4 具体任务

- 定义 Agent 输入输出 schema。
- 为 50 首诗生成 AI 标签。
- 人工抽样检查标签质量。
- 将 AI 标签写入 `poem_features`。
- 为推荐结果生成解释。
- 记录 Agent 运行日志。
- 建立失败重试和缓存策略。

### 9.5 阶段产出

```text
1. backend/app/agents/
2. docs/ai-agent-design.md
3. agent_runs 表
4. 50 首诗词 AI 标签样例
5. 推荐解释样例
6. Agent 质量检查报告
```

### 9.6 验收标准

- AI 输出符合结构化 schema。
- 生成的标签能被推荐系统使用。
- 推荐解释不编造用户行为。
- Agent 运行结果可追踪。
- 同一首诗重复运行不会浪费成本。

### 9.7 和后续步骤的兼容性

- AI 生成字段必须和人工字段分开，保留 `generated_by`、`review_status`。
- Agent 不能直接覆盖人工审核内容。
- 推荐解释要能降级为模板，不依赖每次实时调用 LLM。

---

## 10. Phase 6：强触达能力

### 10.1 目标

验证产品不是等用户主动打开，而是能主动进入用户日常路径。

### 10.2 分两步做

```text
Phase 6A：Web Push
Phase 6B：浏览器新标签页插件
```

### 10.3 Phase 6A：Web Push

#### 任务

- PWA manifest。
- Service Worker。
- 通知权限申请。
- 保存 push subscription。
- 每日推荐定时任务。
- 通知点击打开诗词详情。
- 记录 notification_sent 和 notification_clicked。

#### 产出

```text
1. Web Push demo
2. push_subscriptions 表
3. 定时发送脚本
4. 通知点击行为日志
5. docs/push-design.md
```

#### 兼容性

- 通知推荐必须调用 Phase 3 的 recommendation service。
- 通知点击必须写入统一的 `user_events`。
- 不要为 Web Push 单独写一套推荐逻辑。

### 10.4 Phase 6B：浏览器新标签页插件

#### 任务

- 初始化 extension 目录。
- 配置 Manifest V3。
- 实现 newtab 页面。
- 展示今日推荐。
- 支持喜欢、不喜欢、收藏、跳过。
- 与后端 API 同步行为。

#### 产出

```text
1. extension/newtab/
2. manifest.json
3. 新标签页推荐页面
4. 插件本地调试说明
5. docs/extension-design.md
```

#### 兼容性

- 插件端复用 Web MVP 的展示组件或数据结构。
- 插件行为仍统一走 `POST /events`。
- 插件推荐仍统一走 `/recommendations/today` 或 `/recommendations/feed`。

---

## 11. Phase 7：评估、展示与求职包装

### 11.1 目标

把项目变成可以面试讲清楚、演示出来、被追问也站得住的作品。

### 11.2 为什么必须单独做

很多项目失败不是因为没写代码，而是：

- 没有 demo。
- 没有指标。
- 没有架构图。
- 没有前后对比。
- 讲不清技术取舍。
- 讲不清和岗位的关系。

### 11.3 具体任务

- 做一组固定 demo 用户。
- 展示用户反馈前后的推荐变化。
- 展示用户画像权重变化。
- 展示推荐日志。
- 展示 AI 标注前后推荐效果差异。
- 画系统架构图。
- 写面试讲解稿。
- 写项目复盘。

### 11.4 阶段产出

```text
1. docs/demo-script.md
2. docs/interview-story.md
3. docs/system-architecture.md
4. docs/evaluation-report.md
5. 推荐效果截图或录屏
6. 架构图
7. 项目复盘文档
```

### 11.5 验收标准

- 3 分钟能讲清楚项目。
- 10 分钟能讲清楚推荐链路。
- 能展示一次完整用户行为闭环。
- 能解释为什么选择 PWA / Push / 插件。
- 能解释 AI / Agent 在系统里的真实价值。
- 能说清楚下一步如何扩展。

---

## 12. 推荐的最小可交付版本

如果只做一个最小但完整的版本，建议范围是：

```text
数据：100 首诗词
后端：FastAPI + SQLite/PostgreSQL
推荐：标签匹配 + 行为权重 + 多样性重排
前端：问卷 + 推荐 + 详情 + 反馈
AI：先不做或只做标签样例
触达：先不做 Push 和插件
展示：能录屏演示用户反馈后推荐变化
```

这个版本的价值是：

```text
它已经证明了推荐闭环。
```

之后所有东西都是增强：

```text
更多数据
更好推荐
AI 标注
Web Push
插件
向量召回
指标面板
```

---

## 13. 每一步都要避免的返工点

### 13.1 不要让 poem_id 不稳定

`poem_id` 一旦被收藏、行为日志、推荐日志引用，就不能随便改。

### 13.2 不要把推荐逻辑写死在前端

推荐逻辑应该在后端 service 或独立模块里，前端只展示。

### 13.3 不要让 AI 生成内容覆盖人工内容

需要区分：

```text
manual_tags
ai_tags
generated_by
review_status
```

### 13.4 不要先做复杂 UI

先证明闭环，再做视觉。

### 13.5 不要过早做账号系统

MVP 先用匿名用户 ID，避免被登录、密码、OAuth、隐私流程拖慢。

### 13.6 不要过早做全量数据

先做好 100 首，再扩到 500 首、1000 首。

---

## 14. 推荐近期任务清单

如果现在马上继续做，建议按这个顺序：

### Task 1：创建工程目录

```text
data/
scripts/
backend/
frontend/
extension/
experiments/
```

产出：空目录和 README 说明。

### Task 2：写 20 首 seed 诗词数据

```text
data/samples/poems.sample.json
```

产出：可被推荐脚本读取的最小数据。

### Task 3：写数据 schema 和校验脚本

```text
docs/data-schema.md
scripts/data_import/validate_poems.py
```

产出：保证后续数据不会乱。

### Task 4：写推荐模拟脚本

```text
scripts/evaluation/simulate_user_feedback.py
```

产出：命令行看到推荐随行为变化。

### Task 5：再启动后端

```text
backend/app/main.py
```

产出：`GET /health` 和基础推荐 API。

---

## 15. 当前最推荐的下一步

当前最应该做的不是继续扩写规划，而是进入：

> **Phase 0：项目骨架与工程规范。**

建议下一次提交直接创建：

```text
data/
scripts/
backend/
frontend/
extension/
experiments/
```

并配套写：

```text
docs/data-schema.md
```

然后进入第一批 seed 数据建设。

这样项目会从“规划文档”正式进入“可执行工程”。
