# Planning 阶段补充调研与决策清单

## 1. 这份文档解决什么问题

`docs/product-plan.md` 已经回答了“这个产品是什么”和“推荐系统大方向怎么设计”。但在真正开始实现之前，planning 阶段还需要继续补齐：

- 用户与场景验证
- 数据源与版权策略
- 推荐系统技术路线
- AI / Agent 介入边界
- 前后端与数据架构
- PWA / Web Push / 浏览器插件的接入成本
- 指标、实验与评估
- 隐私、合规与风险
- MVP 范围与求职展示路线

这份文档的目标是把这些“还应该 plan 什么”全部整理成可执行的调研结论和待办清单。

---

## 2. 当前已经确定的核心结论

### 2.1 项目主语不是前端形态

本项目不应该被定义成：

```text
诗词网站
诗词壁纸生成器
PWA 小应用
浏览器插件
```

而应该被定义成：

> **个性化中文诗词推荐系统。**

PWA、Web Push、浏览器新标签页插件、壁纸生成都只是推荐系统的触达入口或展示出口。

### 2.2 两个不可妥协的产品原则

1. **自动化推荐**
   - 推荐结果必须能随着用户行为变化。
   - 用户的点击、收藏、喜欢、不喜欢、跳过、停留、查看详情等行为都要进入推荐闭环。

2. **强触达**
   - 产品不能依赖用户每天主动打开网站。
   - 推荐内容需要进入用户日常路径，例如通知、新标签页、插件、组件等。

### 2.3 求职展示目标决定了技术重心

因为目标岗位偏向：

- 推荐算法
- AI 产品
- AI 全栈开发
- Agent 开发

所以规划重点应该放在：

- 推荐系统链路
- 用户行为事件系统
- 内容理解与标签体系
- AI / Agent 工作流
- 可解释推荐
- 评估与实验设计
- 前后端、后端、数据库、任务调度的完整连接

而不是只展示页面 UI。

---

## 3. Planning 阶段还应该补齐的 12 件事

## 3.1 用户研究计划

### 为什么要 plan

诗词推荐不是刚需工具，用户为什么愿意长期使用并不天然成立。必须验证：

- 用户是否愿意被每日诗词触达。
- 用户是否愿意通过喜欢、不喜欢、收藏来训练推荐。
- 用户更喜欢“经典名篇”还是“冷门佳作”。
- 用户是否需要全文、注释、翻译、赏析。
- 用户对通知、新标签页、插件的接受度。

### 需要调研的问题

访谈 5-10 个潜在用户：

```text
1. 你平时会主动读古诗词吗？频率如何？
2. 你会为了诗词单独打开一个网站或 App 吗？
3. 你愿意每天收到一首诗的推荐通知吗？
4. 你愿意把浏览器新标签页换成每日诗词推荐吗？
5. 你更想看到熟悉名篇，还是不常见但很美的诗词？
6. 你会使用喜欢、不喜欢、收藏来调整推荐吗？
7. 你读诗词时最需要什么辅助：翻译、注释、赏析、背景、朗读、推荐理由？
8. 你会不会觉得通知打扰？什么频率可接受？
9. 你会把一首喜欢的诗生成壁纸吗？
10. 什么情况下你会持续使用这个产品一周以上？
```

### 产出物

- 用户访谈记录
- 用户分群
- 核心使用场景
- 反需求清单
- MVP 功能优先级

---

## 3.2 用户分群与核心场景

### 建议先定义 4 类用户

| 用户类型 | 特征 | 需要什么 | 推荐策略 |
|---|---|---|---|
| 入门用户 | 古诗词基础弱，只记得教材名篇 | 易懂、翻译、注释、熟悉感 | 经典优先，难度低，解释多 |
| 文艺用户 | 喜欢诗词氛围和审美表达 | 句子美、风格准、场景感 | 强调情绪、季节、风格匹配 |
| 学习用户 | 想系统学习诗词 | 全文、背景、作者、注释 | 按主题/作者/体裁递进 |
| 深度用户 | 熟悉大量名篇，希望发现新作品 | 多样性、冷门佳作、细颗粒标签 | 增加探索比例和语义相似召回 |

### MVP 先服务谁

建议 MVP 先服务：

```text
文艺用户 + 普通爱好者
```

原因：

- 他们对诗词审美有兴趣。
- 不要求极高学术准确性。
- 更容易接受“推荐 + 强触达”。
- 更可能收藏、分享、生成壁纸。

---

## 3.3 数据源与版权策略

### 调研结论

开源数据源可以作为 MVP 的正文基础，但需要认真处理：

- 数据许可
- 数据质量
- 错字、断句、重复
- 注释、翻译、赏析的版权
- AI 生成解释的准确性与标注

### 可选数据源

| 数据源 | 适合用途 | 风险 |
|---|---|---|
| `chinese-poetry/chinese-poetry` | 大规模诗词正文、作者、朝代、JSON 数据 | 数据来自互联网，需要清洗与抽样审核 |
| 自建精选数据 | MVP 高质量内容 | 人工成本高 |
| AI 辅助标注 | 标签、难度、推荐理由、初版翻译 | 需要人工校验 |
| 公版文本 | 正文低版权风险 | 元数据和解释仍需整理 |

`chinese-poetry` 仓库说明其包含大量唐诗、宋诗、宋词等 JSON 数据，并采用 MIT license；这适合作为 MVP 数据起点，但仍需要我们建立清洗、去重、抽样校验和内容质量评分流程。参考：[`chinese-poetry/chinese-poetry`](https://github.com/chinese-poetry/chinese-poetry)。

### 数据策略建议

MVP 不要一开始追求“全”。建议：

```text
第一批：500-1000 首
重点：唐诗三百首、宋词三百首、诗经精选、苏轼/李白/杜甫/王维/李清照/辛弃疾等重点作者
要求：正文准确、元数据完整、标签可用
```

### 必须建立的数据处理流程

```text
原始数据导入
↓
字段标准化
↓
去重
↓
繁简/异体字策略
↓
断句校验
↓
作者朝代校验
↓
AI 初步打标签
↓
人工抽样审核
↓
生成推荐特征表
```

---

## 3.4 内容标签体系与内容画像

### 为什么要 plan

推荐系统的质量很大程度取决于内容画像。如果诗词标签粗糙，推荐就会单调或不准。

### 建议标签分层

```text
主题标签：山水、田园、送别、思乡、爱情、边塞、怀古、人生、节日、咏物
风格标签：豪放、婉约、清新、沉郁、旷达、悲凉、闲适、浪漫、典雅
情绪标签：孤独、安定、振奋、惆怅、释然、怀念、平和
场景标签：清晨、夜晚、雨天、春天、秋天、考试、工作、旅行、睡前
体裁标签：五绝、七绝、律诗、词、古体诗、诗经、楚辞
难度标签：入门、普通、进阶、高难
熟悉度标签：教材常见、大众名篇、经典但不常见、冷门佳作
```

### 内容画像字段

```json
{
  "poem_id": "song_sushi_dingfengbo",
  "title": "定风波",
  "author": "苏轼",
  "dynasty": "宋",
  "type": "词",
  "themes": ["人生", "旷达", "风雨"],
  "styles": ["豪放", "豁达"],
  "emotions": ["释然", "坚定"],
  "scenes": ["雨天", "低谷", "自我安顿"],
  "difficulty": 3,
  "familiarity": 5,
  "quality": 5,
  "embedding_text": "标题、作者、正文、标签、译文摘要组合后的文本"
}
```

---

## 3.5 推荐系统路线

### 调研结论

推荐系统不是一开始就要训练复杂模型。对 MVP 来说，更适合：

```text
规则 + 标签画像 + 行为权重 + 语义向量召回 + 多样性重排
```

这条路线比纯 LLM 推荐更稳定，也更容易解释。

推荐系统实践资料通常强调从数据、候选召回、排序、评估、实验等环节逐步搭建。Microsoft / Linux Foundation AI & Data 的 Recommenders 项目提供了推荐系统原型、实验和最佳实践示例，可作为工程参考：[`recommenders-team/recommenders`](https://github.com/recommenders-team/recommenders)。

### MVP 推荐链路

```text
1. 冷启动问卷生成初始用户画像
2. 标签召回：按主题、作者、体裁、风格召回候选
3. 语义召回：用 embedding 找相似诗词
4. 热门经典召回：保证熟悉感
5. 探索召回：引入少量冷门佳作
6. 排序：计算用户兴趣匹配分
7. 重排：控制作者、主题、体裁重复
8. 推荐解释：告诉用户为什么推荐
9. 行为反馈：更新用户画像
```

### 行为权重建议

| 行为 | 权重 | 说明 |
|---|---:|---|
| 收藏 | +8 | 强正反馈 |
| 喜欢 | +5 | 明确正反馈 |
| 查看全文 | +3 | 中等正反馈 |
| 查看注释/翻译 | +2 | 学习兴趣 |
| 长停留 | +2 | 隐式兴趣 |
| 复制诗句 | +3 | 内容有价值 |
| 生成壁纸 | +4 | 强审美偏好 |
| 通知点击 | +3 | 触达有效 |
| 快速跳过 | -2 | 弱负反馈 |
| 不喜欢 | -6 | 明确负反馈 |
| 通知长期忽略 | -1 | 触达疲劳 |

---

## 3.6 向量检索与 embedding 方案

### 为什么需要 embedding

标签只能表达人工定义的维度，embedding 可以补充：

- 语义相似
- 情绪相似
- 意境相似
- 主题近似但标签不同的诗词

OpenAI 文档将 embedding 描述为浮点数向量，向量距离可以衡量文本相关性；这适合用于相似诗词召回、用户兴趣向量、语义检索。参考：[OpenAI Embeddings Guide](https://developers.openai.com/api/docs/guides/embeddings)。

### 存储方案

建议使用 PostgreSQL + pgvector。

pgvector 是 PostgreSQL 的开源向量相似搜索扩展，支持精确/近似最近邻、L2、内积、cosine 等距离，并可以与普通业务数据存在同一个 PostgreSQL 数据库里。参考：[`pgvector/pgvector`](https://github.com/pgvector/pgvector)。

### MVP embedding 文本

不要只 embed 原诗正文，可以组合：

```text
标题 + 作者 + 朝代 + 正文 + 主题标签 + 风格标签 + 白话摘要
```

原因：

- 古诗正文很短，语义可能含蓄。
- 标签和摘要能帮助模型捕捉现代语义。
- 推荐解释也更容易生成。

---

## 3.7 数据库与后端架构

### 推荐后端技术

面向 AI / 推荐 / Agent 岗位展示，后端建议优先：

```text
FastAPI + PostgreSQL + pgvector
```

FastAPI 官方文档定位为基于 Python type hints 的现代高性能 Web API 框架，适合快速搭建推荐 API、事件采集 API、Agent API。参考：[FastAPI 官方文档](https://fastapi.tiangolo.com/)。

PostgreSQL 适合承载结构化业务数据；如果需要存储灵活标签和元数据，PostgreSQL 官方文档说明 `jsonb` 支持索引，GIN indexes 可用于高效搜索大量 JSONB 文档中的 key 或 key/value。参考：[PostgreSQL JSON Types](https://www.postgresql.org/docs/current/datatype-json.html)。

### 建议服务拆分

MVP 可以先单体，逻辑上拆模块：

```text
api/
  users
  poems
  events
  recommendations
  favorites
  push
  agents

services/
  recommendation_service
  profile_service
  event_service
  content_feature_service
  agent_service
```

### 关键表

```text
poems
poem_features
poem_embeddings
users
user_profiles
user_events
favorites
recommendation_logs
push_subscriptions
agent_runs
experiments
```

### 必须提前 plan 的数据问题

- 是否匿名用户优先？建议是。
- 是否需要登录？MVP 不需要。
- 行为事件是否可追溯？需要。
- 推荐结果是否记录日志？需要。
- 是否记录每次推荐的 score 和 recall_source？需要。

推荐日志非常关键，因为它支持后续评估：

```text
系统推荐了什么
为什么推荐
用户有没有点击
用户后续是否喜欢
哪个召回源有效
```

---

## 3.8 PWA、Web Push 与浏览器插件接入

### PWA + Web Push

Apple 官方文档说明，iOS 16.4 或更高版本的 Home Screen web apps 可以使用 Web Push；Safari 16 for macOS 13 或更高也支持相关能力。参考：[Apple Web Push 文档](https://developer.apple.com/documentation/usernotifications/sending-web-push-notifications-in-web-apps-and-browsers)。

WebKit 也说明，iOS / iPadOS 16.4 起，添加到主屏幕的 Web App 支持 Web Push。参考：[WebKit: Web Push for Web Apps on iOS and iPadOS](https://webkit.org/blog/13878/web-push-for-web-apps-on-ios-and-ipados/)。

### 对本项目的意义

PWA + Web Push 适合作为：

```text
移动端轻量触达
每日推荐通知
点击通知进入详情页
通知点击行为进入推荐系统
```

### 浏览器新标签页插件

Chrome 扩展官方文档说明，扩展可通过 Chrome Extension APIs 构建，并且 Manifest V3 是当前扩展平台版本。参考：[Chrome Extensions API Reference](https://developer.chrome.com/docs/extensions/reference/api) 与 [Manifest V3](https://developer.chrome.com/docs/extensions/develop/migrate/what-is-mv3)。

MDN 对 `chrome_url_overrides` 的说明中，新标签页可通过 `newtab` 指向自定义 HTML 页面；这说明浏览器插件可以承载“每次打开新标签页展示推荐诗词”的产品形态。参考：[MDN chrome_url_overrides](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/manifest.json/chrome_url_overrides)。

### 接入优先级

建议：

```text
P0：Web App 推荐闭环
P1：Web Push
P2：Chrome 新标签页插件
```

原因：

- Web App 是主产品和后端 API 验证入口。
- Web Push 验证强触达。
- 插件验证桌面端高频触达。

---

## 3.9 AI / Agent 模块规划

### 原则

AI 不应该只是“聊天窗口”。AI 应该参与推荐系统核心环节：

```text
内容理解
标签生成
难度判断
推荐解释
用户偏好总结
结果质量评估
```

### 建议 Agent 列表

| Agent | 输入 | 输出 | 风险控制 |
|---|---|---|---|
| 内容标注 Agent | 诗词正文、作者、朝代 | 主题、风格、情绪、场景、难度 | 抽样人工审核 |
| 翻译注释 Agent | 原文 | 白话翻译、关键词注释 | 标注 AI 辅助，避免版权复制 |
| 推荐解释 Agent | 推荐分数、用户画像、诗词画像 | 自然语言推荐理由 | 不编造用户行为 |
| 用户偏好总结 Agent | 用户行为日志 | 偏好总结 | 只基于真实事件 |
| 评估 Agent | 推荐列表、标签、解释 | 重复度、错误、解释一致性检查 | 结合规则检查 |

### 必须 plan 的 AI 评估

- 标签是否准确？
- 难度是否稳定？
- 推荐解释是否真实对应用户行为？
- 翻译是否有明显误解？
- 是否生成了不存在的典故？

---

## 3.10 指标体系与实验设计

### 产品指标

| 指标 | 含义 |
|---|---|
| onboarding completion rate | 问卷完成率 |
| notification click-through rate | 通知点击率 |
| newtab interaction rate | 新标签页互动率 |
| poems viewed per session | 每次访问阅读首数 |
| like rate | 喜欢率 |
| favorite rate | 收藏率 |
| dislike rate | 不喜欢率 |
| detail open rate | 详情打开率 |
| next-day return | 次日回访 |
| 7-day retention | 7 日留存 |

### 推荐指标

| 指标 | 含义 |
|---|---|
| CTR | 推荐点击率 |
| like/favorite after impression | 曝光后的喜欢/收藏率 |
| skip rate | 跳过率 |
| diversity | 推荐多样性 |
| novelty | 新颖度 |
| familiarity balance | 熟悉/探索比例 |
| coverage | 内容覆盖率 |
| repeat rate | 重复推荐率 |
| explanation helpfulness | 推荐解释有用性 |

### MVP 实验

最重要的实验不是复杂 A/B，而是验证推荐闭环：

```text
同一用户连续反馈 10 次后，推荐结果是否明显变化？
喜欢山水后，山水/田园/清新相关诗词是否增加？
不喜欢边塞后，边塞诗是否降低但没有完全消失？
收藏苏轼后，苏轼和相似风格作者是否合理增加？
```

---

## 3.11 隐私与合规规划

### MVP 隐私策略

建议一开始采用：

```text
匿名用户 ID
不要求登录
本地存储 + 最小必要服务端数据
用户可清除数据
明确说明记录哪些行为
```

### 需要记录的数据

```text
问卷答案
喜欢/不喜欢/收藏
阅读历史
通知点击
推荐日志
匿名设备或浏览器标识
```

### 不建议 MVP 记录的数据

```text
真实姓名
手机号
精确地理位置
通讯录
敏感身份信息
```

### 必须 plan 的文档

- Privacy Policy 草案
- 数据字段说明
- 用户数据删除机制
- AI 生成内容说明
- 数据源与许可证说明

---

## 3.12 成本、部署与运维计划

### MVP 低成本部署

建议：

```text
前端：Vercel / Cloudflare Pages
后端：Render / Fly.io / Railway / Cloudflare Workers / 自建 VPS
数据库：Supabase Postgres / Neon / Railway Postgres
定时任务：GitHub Actions / Vercel Cron / Cloudflare Cron Triggers
```

### 成本风险

- embedding 生成成本
- LLM 标注成本
- Web Push 后端与数据库成本
- 图片生成和存储成本
- 大规模访问后的带宽成本

### 控制策略

```text
先只处理 500-1000 首诗词
离线批量生成 embedding
Agent 标注结果缓存
推荐解释优先模板化，少量调用 LLM
不做账号系统，降低复杂度
```

---

## 4. 建议新增的规划文档清单

后续可以逐步拆出以下文档：

```text
docs/user-research-plan.md          用户访谈与调研计划
docs/data-source-plan.md            数据源、清洗、版权策略
docs/recommendation-design.md       推荐系统详细设计
docs/ai-agent-design.md             AI / Agent 工作流设计
docs/system-architecture.md         前后端与部署架构
docs/metrics-and-experiments.md     指标与实验设计
docs/privacy-plan.md                隐私与数据合规计划
docs/mvp-scope.md                   MVP 范围与里程碑
```

当前阶段先用本文件统一收口，等实现开始后再拆分。

---

## 5. 推荐的下一步执行顺序

### Step 1：补数据计划

产出：

```text
诗词数据源列表
第一批 500 首选择标准
字段 schema
数据清洗脚本计划
版权说明
```

### Step 2：补推荐系统详细设计

产出：

```text
用户画像字段
内容画像字段
行为事件 schema
召回/排序/重排算法
推荐日志格式
离线评估脚本计划
```

### Step 3：做一个后端优先的最小闭环

不急着做漂亮 UI，先做：

```text
FastAPI
PostgreSQL
poems 表
user_events 表
recommendations API
profile update service
```

### Step 4：做一个非常简单的 Web 页面

只验证闭环：

```text
问卷
推荐一首
喜欢/不喜欢/收藏/跳过
下一首推荐变化
```

### Step 5：再接强触达

```text
Web Push
Chrome 新标签页插件
```

### Step 6：加入 AI / Agent

```text
内容标签生成
推荐解释
用户偏好总结
评估 Agent
```

---

## 6. 当前阶段的最终判断

Planning 阶段还应该 plan 的不是“再想更多功能”，而是把项目从一个想法变成可实现、可验证、可面试讲述的系统。

最重要的补充规划是：

1. 用户研究与核心场景
2. 数据源与版权策略
3. 内容标签与画像体系
4. 推荐链路与行为反馈
5. embedding 与向量检索
6. 后端、数据库、API 架构
7. PWA / Web Push / 插件触达方案
8. AI / Agent 工作流
9. 指标、实验与评估
10. 隐私、成本、部署与风险

如果这些规划都完成，本项目就不再只是“想做一个诗词产品”，而是一个完整的：

> **个性化内容推荐系统 + AI 内容理解系统 + 多端触达产品 + 可展示的求职项目。**

---

## 7. 本文调研来源

- [`chinese-poetry/chinese-poetry`](https://github.com/chinese-poetry/chinese-poetry)：中文古诗词 JSON 数据源与 MIT license 信息。
- [`recommenders-team/recommenders`](https://github.com/recommenders-team/recommenders)：推荐系统原型、实验与最佳实践参考。
- [OpenAI Embeddings Guide](https://developers.openai.com/api/docs/guides/embeddings)：embedding 与文本相关性基础说明。
- [`pgvector/pgvector`](https://github.com/pgvector/pgvector)：PostgreSQL 向量相似搜索扩展。
- [FastAPI 官方文档](https://fastapi.tiangolo.com/)：Python API 服务框架。
- [PostgreSQL JSON Types](https://www.postgresql.org/docs/current/datatype-json.html)：JSONB 与索引能力。
- [Apple Web Push 文档](https://developer.apple.com/documentation/usernotifications/sending-web-push-notifications-in-web-apps-and-browsers)：Safari / iOS Home Screen Web App 的 Web Push 能力。
- [WebKit Web Push for Web Apps on iOS and iPadOS](https://webkit.org/blog/13878/web-push-for-web-apps-on-ios-and-ipados/)：iOS / iPadOS 16.4 起对 Home Screen Web App Web Push 的支持说明。
- [Chrome Extensions API Reference](https://developer.chrome.com/docs/extensions/reference/api)：Chrome Extension API。
- [Chrome Manifest V3](https://developer.chrome.com/docs/extensions/develop/migrate/what-is-mv3)：Chrome 扩展平台 Manifest V3。
- [MDN chrome_url_overrides](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/manifest.json/chrome_url_overrides)：浏览器扩展覆盖新标签页能力。
