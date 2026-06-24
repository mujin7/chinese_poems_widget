# 个性化诗词推荐系统项目方案

## 1. 项目定位

本项目不是单纯的诗词壁纸生成器、PWA 网页或浏览器插件，而是一个以推荐系统为核心的个性化诗词内容产品。

项目目标是：

> 基于用户问卷、阅读行为、收藏、喜欢、不喜欢、跳过等反馈，持续学习用户偏好，并通过强触达入口向用户推荐兼具熟悉感与多样性的中国古代诗词。

项目面向的求职方向包括：

- 推荐算法
- AI 产品
- AI 全栈开发
- Agent 开发

因此，项目重点不应放在单一前端形态，而应放在：

- 推荐系统搭建
- 用户行为闭环
- 内容理解与 AI 标注
- 前后端连接
- 多端触达策略
- 产品指标与验证方法

---

## 2. 核心产品判断

### 2.1 不可妥协的核心点

本项目有两个最重要的产品原则：

1. **自动化推荐**
   - 系统必须根据用户行为持续更新推荐结果。
   - 用户的点击、收藏、喜欢、不喜欢、跳过、停留、查看注释等行为都应反馈到用户画像中。

2. **强触达**
   - 产品不能依赖用户每天主动打开某个网站。
   - 推荐内容需要通过通知、新标签页、组件、插件等形式主动出现在用户日常使用路径中。

### 2.2 为什么单纯壁纸轮换不可接受

静态壁纸包或提前生成 30 天壁纸的方案虽然可以做到“每天看见”，但缺少推荐闭环：

- 无法根据用户当天的行为调整明天的推荐。
- 用户很难对壁纸进行喜欢、不喜欢、收藏等反馈。
- 推荐系统无法持续学习用户偏好。

因此，壁纸只能作为推荐结果的一个衍生功能，而不是项目主形态。

正确关系应该是：

```text
推荐先发生
↓
用户看到推荐诗词
↓
用户行为反馈
↓
系统更新画像
↓
用户可以把当前推荐生成壁纸
```

而不是：

```text
预先生成一批壁纸
↓
系统静态轮换
```

---

## 3. 推荐产品形态

### 3.1 主产品：PWA Web App

PWA 作为主产品入口，承担完整产品体验：

- 初始问卷
- 今日推荐
- 推荐列表
- 诗词详情
- 注释和翻译
- 收藏夹
- 阅读历史
- 用户偏好
- 推荐解释
- Web Push 通知授权

PWA 的价值在于：

- 无需 App Store 上架。
- 可以在手机和电脑浏览器访问。
- 可以添加到主屏幕或桌面。
- 可以通过 Web Push 做每日推荐触达。
- 适合承载完整的产品和数据闭环。

### 3.2 强触达入口一：Web Push 通知

Web Push 用于每日主动触达用户。

示例：

```text
今日为你推荐
《定风波》苏轼
一蓑烟雨任平生
```

用户点击通知后进入诗词详情页，系统记录：

- 通知是否送达
- 通知是否点击
- 点击后是否阅读全文
- 是否收藏、喜欢或跳过

这些行为继续反馈到推荐系统。

### 3.3 强触达入口二：浏览器新标签页插件

浏览器插件用于电脑端高频触达。

用户每次打开新标签页时，都可以看到一首个性化推荐诗词。

插件页面可以提供：

- 今日推荐诗词
- 推荐理由
- 喜欢
- 不喜欢
- 收藏
- 换一首
- 查看全文
- 生成壁纸

插件的价值在于：

- 触达频率高。
- 用户行为反馈非常自然。
- 适合作为推荐系统的数据采集入口。
- 项目形态有差异化，适合面试展示。

### 3.4 辅助功能：壁纸生成

壁纸功能仍然可以保留，但作为推荐结果的衍生能力。

用户可以对当前推荐诗词执行：

- 生成手机壁纸
- 生成电脑壁纸
- 保存图片
- 分享图片

这些行为也可以作为强正反馈，例如：

```text
生成壁纸 = 用户对这首诗有较强兴趣
```

---

## 4. PWA 与浏览器插件的关系

PWA 和浏览器新标签页插件是两套不同的触达方案，但应该共用同一个推荐系统和后端能力。

### 4.1 二者定位

```text
PWA：主站、移动端入口、详情页、收藏、偏好管理、Web Push
浏览器插件：桌面端高频触达、新标签页推荐、快速反馈
```

### 4.2 可以共用的部分

- 诗词数据库
- 用户画像
- 推荐算法
- 用户行为事件模型
- 收藏系统
- 推荐日志
- 后端 API
- AI 标注结果
- 推荐解释服务

### 4.3 不完全共用的部分

PWA 特有：

- Web App Manifest
- Service Worker
- Push API
- Notification API
- 添加到主屏幕

浏览器插件特有：

- Manifest V3
- `chrome_url_overrides`
- `chrome.storage`
- background service worker
- extension options page

---

## 5. 面向求职目标的项目重点

### 5.1 推荐算法岗位

应重点展示：

- 内容画像
- 用户画像
- 冷启动
- 召回
- 排序
- 重排
- 多样性控制
- 熟悉度控制
- 用户行为反馈
- 推荐解释
- 离线评估

项目讲法：

> 我搭建了一个中文诗词个性化推荐系统。系统通过初始问卷解决用户冷启动问题，并结合用户浏览、收藏、喜欢、不喜欢、跳过等行为持续更新用户画像。推荐链路采用基于标签和语义向量的多路召回，再通过个性化匹配分、熟悉度分、质量分和多样性约束进行排序与重排，解决古诗词推荐中“熟悉感”和“探索性”的平衡问题。

### 5.2 AI 产品岗位

应重点展示：

- 用户场景洞察
- 为什么需要强触达
- 为什么问卷冷启动
- 为什么需要推荐解释
- 如何设计反馈闭环
- 如何定义成功指标
- 如何设计 MVP
- 如何迭代

项目讲法：

> 我设计了一个面向诗词内容消费的 AI 推荐产品。产品不是让用户主动搜索诗词，而是通过 PWA 推送和新标签页插件在日常场景中主动触达用户。产品使用问卷进行冷启动，并根据用户反馈不断调整推荐，使用户在熟悉名篇和探索冷门佳作之间获得平衡体验。

### 5.3 AI 全栈开发岗位

应重点展示：

- 前后端连接
- API 设计
- 数据库设计
- 推荐服务
- 用户行为事件管道
- Web Push
- 浏览器插件接入
- LLM 内容标注
- embedding 检索
- 部署与监控

项目讲法：

> 我实现了一个包含前端触达、后端 API、推荐服务、用户行为事件管道和 LLM 内容标注流程的全栈 AI 推荐项目。前端包括 PWA 和 Chrome 新标签页插件，后端负责用户事件采集、画像更新、推荐生成和 Web Push 通知，AI 模块用于诗词标签、难度、主题、推荐解释等内容增强。

### 5.4 Agent 开发岗位

应重点展示：

- Agent 工作流
- 工具调用
- 内容处理自动化
- 用户偏好总结
- 推荐解释生成
- 质量评估
- 人工审核流

项目讲法：

> 我设计了多个面向诗词推荐系统的 Agent，包括内容标注 Agent、翻译注释 Agent、用户偏好总结 Agent、推荐解释 Agent 和评估 Agent。它们通过工具调用完成诗词清洗、标签生成、推荐理由生成和结果质量检查，形成可控的人机协作内容生产流程。

---

## 6. 推荐系统设计

### 6.1 内容画像

每首诗词需要结构化画像。

示例：

```json
{
  "poem_id": "song_sushi_dingfengbo",
  "title": "定风波",
  "author": "苏轼",
  "dynasty": "宋",
  "type": "词",
  "cipai": "定风波",
  "themes": ["人生", "旷达", "风雨", "自我安顿"],
  "styles": ["豪放", "豁达", "哲理"],
  "difficulty": 3,
  "familiarity": 5,
  "quality": 5,
  "length": "medium",
  "embedding": []
}
```

内容画像来源：

- 开源诗词数据
- 人工规则
- LLM 标注
- embedding
- 用户反馈修正

### 6.2 用户画像

用户画像记录用户偏好。

示例：

```json
{
  "user_id": "anonymous_123",
  "level": "intermediate",
  "preferred_authors": {
    "苏轼": 0.82,
    "王维": 0.67
  },
  "preferred_themes": {
    "山水": 0.71,
    "人生": 0.88,
    "送别": 0.24
  },
  "preferred_styles": {
    "旷达": 0.8,
    "清新": 0.7,
    "沉郁": 0.3
  },
  "difficulty_preference": 3,
  "familiarity_preference": 0.6,
  "exploration_tolerance": 0.35
}
```

### 6.3 行为权重

不同行为对应不同反馈强度。

```text
收藏：+8
喜欢：+5
生成壁纸：+4
分享：+5
查看全文：+3
复制诗句：+3
通知点击：+3
查看注释：+2
停留时间长：+2
通知忽略：-1
快速跳过：-2
不喜欢：-6
```

### 6.4 推荐链路

推荐链路分为四步：

```text
召回
↓
排序
↓
重排
↓
解释
```

#### 6.4.1 召回

多路召回：

- 标签召回
- 作者召回
- 主题召回
- 相似 embedding 召回
- 热门经典召回
- 探索召回
- 收藏相似召回

#### 6.4.2 排序

基础打分公式：

```text
score =
0.30 * user_tag_match
+ 0.20 * author_match
+ 0.15 * semantic_similarity
+ 0.15 * quality_score
+ 0.10 * familiarity_match
+ 0.05 * context_match
+ 0.05 * novelty_score
```

#### 6.4.3 重排

重排约束：

- 同一作者不能连续太多。
- 同一主题不能过度集中。
- 熟悉内容与探索内容保持比例。
- 最近曝光过的诗词降权。
- 用户明确不喜欢的标签降权。

#### 6.4.4 解释

推荐解释示例：

```text
因为你最近收藏了王维的山水诗，也多次喜欢清新闲适风格，所以今天推荐这首《山居秋暝》。
```

---

## 7. AI 与 Agent 模块

### 7.1 内容标注 Agent

任务：

- 输入诗词正文。
- 输出主题标签、风格标签、难度、适合场景。

示例输出：

```json
{
  "themes": ["山水", "闲适", "秋日"],
  "styles": ["清新", "宁静", "自然"],
  "difficulty": 2,
  "suitable_context": ["夜晚", "秋天", "放松"]
}
```

### 7.2 翻译注释 Agent

任务：

- 生成白话翻译。
- 提取关键词注释。
- 降低古文理解门槛。

注意事项：

- 需要人工审核。
- 不能直接复制版权网站内容。
- AI 辅助内容需要标注来源和质量状态。

### 7.3 用户偏好总结 Agent

任务：

- 根据用户行为总结偏好。
- 给推荐系统提供可读的偏好摘要。

示例：

```text
用户偏好宋词、旷达风格、人生感悟主题，对边塞和咏史类内容兴趣较低。最近收藏行为显示其对苏轼和辛弃疾作品兴趣增强。
```

### 7.4 推荐解释 Agent

任务：

- 将推荐系统的分数和原因转成自然语言解释。
- 降低用户对冷门推荐的陌生感。

### 7.5 评估 Agent

任务：

- 检查推荐结果是否过于重复。
- 检查解释是否符合诗词内容。
- 检查标签是否明显错误。
- 检查翻译是否有事实问题。

---

## 8. 数据库设计

### 8.1 核心表

建议包含：

```text
poems
authors
poem_annotations
poem_translations
poem_features
users
user_profiles
user_events
favorites
recommendation_logs
push_subscriptions
agent_runs
```

### 8.2 用户行为表

```sql
CREATE TABLE user_events (
  id TEXT PRIMARY KEY,
  user_id TEXT,
  anonymous_id TEXT,
  poem_id TEXT,
  event_type TEXT,
  event_value REAL,
  source TEXT,
  metadata JSON,
  created_at TIMESTAMP
);
```

### 8.3 推荐日志表

```sql
CREATE TABLE recommendation_logs (
  id TEXT PRIMARY KEY,
  user_id TEXT,
  poem_id TEXT,
  rank_position INTEGER,
  score REAL,
  recall_source TEXT,
  explanation TEXT,
  source TEXT,
  created_at TIMESTAMP
);
```

推荐日志表很重要，因为它可以支持后续评估：

- 展示了什么
- 用户点了什么
- 为什么推荐
- 排名是多少
- 后续反馈如何

---

## 9. API 设计

### 9.1 推荐 API

```http
GET /api/recommendations/today
GET /api/recommendations/feed
POST /api/recommendations/refresh
```

### 9.2 行为 API

```http
POST /api/events
```

请求示例：

```json
{
  "poem_id": "xxx",
  "event_type": "like",
  "source": "extension",
  "metadata": {}
}
```

### 9.3 用户画像 API

```http
GET /api/profile
PATCH /api/profile
POST /api/profile/onboarding
```

### 9.4 收藏 API

```http
GET /api/favorites
POST /api/favorites
DELETE /api/favorites/:poem_id
```

### 9.5 推送 API

```http
POST /api/push/subscribe
POST /api/push/unsubscribe
POST /api/push/send-daily
```

### 9.6 Agent API

```http
POST /api/agents/tag-poem
POST /api/agents/explain-recommendation
POST /api/agents/summarize-user-profile
POST /api/agents/evaluate-recommendations
```

---

## 10. 推荐技术栈

### 10.1 前端

```text
Next.js / React
TypeScript
Tailwind CSS
PWA support
Service Worker
Web Push
```

### 10.2 浏览器插件

```text
Chrome Extension Manifest V3
React / TypeScript
chrome_url_overrides
chrome.storage
background service worker
```

### 10.3 后端

```text
FastAPI / Python
PostgreSQL
SQLAlchemy / Prisma
Redis 可选
Docker
```

### 10.4 推荐与 AI

```text
Python
pandas / numpy
scikit-learn
embedding model
pgvector
LLM structured output
Agent workflow
```

### 10.5 部署

```text
Frontend: Vercel / Cloudflare Pages
Backend: Render / Railway / Fly.io / Cloudflare Workers
Database: Supabase PostgreSQL / Neon / Railway PostgreSQL
```

### 10.6 技术栈选择理由

由于求职方向是推荐算法、AI 产品、AI 全栈和 Agent 开发，后端与推荐模块建议优先使用 Python。

原因：

- Python 更适合推荐算法实验。
- Python 生态适合 AI、embedding、Agent workflow。
- FastAPI 能清晰展示前后端 API 连接。
- PostgreSQL + pgvector 可以展示结构化数据和向量检索结合。

---

## 11. MVP 开发路线

### 阶段 1：推荐闭环

目标：证明系统可以根据用户行为持续改变推荐结果。

功能：

- 诗词数据
- 初始问卷
- 用户画像
- 推荐 feed
- 喜欢 / 不喜欢 / 收藏 / 跳过
- 行为采集
- 推荐日志
- 推荐解释

### 阶段 2：PWA 主站

目标：完成完整产品体验。

功能：

- 推荐首页
- 诗词详情
- 注释和翻译
- 收藏夹
- 阅读历史
- 偏好设置
- 添加到主屏幕

### 阶段 3：强触达

目标：证明产品不是等用户主动打开，而是主动触达。

功能：

- Web Push
- 每日推荐通知
- 通知点击回传
- 浏览器新标签页插件

### 阶段 4：AI 增强

目标：证明 AI 参与内容理解和推荐解释。

功能：

- LLM 自动标签
- embedding 相似召回
- 推荐理由生成
- 用户偏好总结
- 内容质量评估

### 阶段 5：项目展示

目标：让项目适合面试展示。

内容：

- 推荐效果 demo
- 用户画像变化可视化
- 推荐日志分析
- 行为反馈前后对比
- Agent 工作流展示
- 技术架构图
- 产品指标设计

---

## 12. 验证方案

### 12.1 技术可行性验证

#### 验证 PWA Web Push

最小验证：

```text
创建 PWA demo
添加到主屏幕
请求通知权限
服务端发送 push
点击通知打开诗词详情页
记录 notification_click 事件
```

成功标准：

```text
通知能到达
点击能打开指定诗词
点击行为能写入 user_events
```

#### 验证浏览器插件

最小验证：

```text
创建 Chrome Extension
覆盖新标签页
展示推荐诗词
点击喜欢 / 不喜欢
写入 chrome.storage 或后端
下一次打开新标签页推荐变化
```

成功标准：

```text
新标签页能显示推荐
行为能记录
推荐能根据行为改变
```

#### 验证推荐系统

最小验证：

```text
先不做复杂 UI
用脚本模拟 20 个用户
每个用户有不同问卷和行为
跑推荐算法
观察推荐结果是否随行为变化
```

成功标准：

```text
喜欢山水的用户逐渐收到更多山水诗
不喜欢边塞的用户边塞推荐下降
高熟悉偏好的用户更多收到经典名篇
探索比例仍保留一定冷门佳作
```

### 12.2 产品价值验证

#### 验证强触达价值

访谈问题：

```text
你会主动打开一个诗词网站吗？
你愿意每天收到一首诗的通知吗？
你愿意把新标签页换成每日诗词吗？
你希望推荐更经典还是更冷门？
你会点击喜欢/不喜欢来让系统更懂你吗？
```

成功标准：

```text
超过一半用户不愿主动打开网站
但愿意接受通知或新标签页这种轻触达
用户能理解个性化推荐的价值
```

#### 验证熟悉感与多样性平衡

测试方式：

```text
A：全是教材名篇
B：全是冷门诗词
C：经典 + 个性化 + 探索混合
```

询问用户：

```text
哪个更愿意继续刷？
哪个更像懂你？
哪个更适合每天推荐？
```

成功标准：

```text
大部分用户选择 C
```

### 12.3 求职价值验证

验证方式：

```text
准备四个版本的项目介绍：
1. 推荐算法版
2. AI 产品版
3. AI 全栈版
4. Agent 开发版

分别给相关方向从业者或面试官视角的人看，询问：
- 是否和岗位相关？
- 哪里最有亮点？
- 哪里不像真实项目？
- 是否有面试追问空间？
```

成功标准：

```text
对方能围绕推荐链路、行为闭环、AI 标注、Agent workflow 提出深入问题，
而不是只评价页面好不好看。
```

---

## 13. 项目最终表达

推荐最终将项目表述为：

> 一个个性化诗词推荐系统，通过问卷冷启动、用户行为反馈、内容语义理解和多端强触达，为用户持续推荐兼具熟悉感与多样性的中国古代诗词。系统包含 PWA 主站、Web Push 通知、浏览器新标签页插件、推荐服务、用户画像服务、LLM 内容标注与推荐解释 Agent。

项目关键词：

```text
个性化推荐
用户画像
内容画像
冷启动
行为反馈
多路召回
排序与重排
多样性控制
可解释推荐
Web Push
Chrome Extension
LLM 标注
Agent workflow
AI 全栈
产品验证
```

---

## 14. 最终结论

本项目不应定位为单纯的诗词展示、壁纸生成、PWA 或浏览器插件项目。

更准确的定位是：

> **以推荐系统为核心，以 AI 内容理解为增强，以 PWA 和浏览器插件为触达入口的个性化诗词推荐产品。**

对求职目标而言，最重要的展示顺序是：

```text
1. 推荐系统是否完整
2. 用户行为是否形成闭环
3. AI 是否参与内容理解和解释
4. 产品是否有强触达和真实使用场景
5. 前后端是否连接清晰
6. 项目是否能被验证和迭代
```
