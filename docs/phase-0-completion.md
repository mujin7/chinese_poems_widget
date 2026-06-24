# Phase 0 完成说明

## 1. Phase 0 目标

Phase 0 的目标是把空仓库变成一个可以持续开发的工程项目，为 Phase 1 数据建设、Phase 2 推荐闭环、Phase 3 后端 API、Phase 4 Web MVP、Phase 6 插件和强触达能力预留清晰边界。

## 2. 已完成内容

### 2.1 工程目录

已创建：

```text
data/raw
data/processed
data/samples
scripts/data_import
scripts/evaluation
backend/app
backend/tests
frontend/app
frontend/tests
extension/newtab
experiments/recommendation
experiments/agent
```

### 2.2 基础版本与工具约定

已添加：

```text
.python-version
.node-version
pyproject.toml
package.json
.editorconfig
```

### 2.3 验证脚本

已添加：

```text
scripts/verify_structure.py
```

用途：验证 Phase 0 必需目录与文件是否存在。

### 2.4 目录说明文档

每个主要目录都添加了 README，说明该目录的用途、近期计划和后续兼容性。

## 3. 关键设计决策

### 3.1 先建骨架，不初始化完整框架

Phase 0 没有直接创建 FastAPI、Next.js 或 Chrome Extension 运行时代码。

原因：

- 当前还没有稳定数据 schema。
- 推荐闭环尚未实现。
- 过早初始化框架会增加无效依赖和迁移成本。

### 3.2 保留后续兼容性

- `backend/app/` 后续承载 FastAPI 服务。
- `frontend/app/` 后续承载 Web MVP。
- `extension/newtab/` 后续承载浏览器新标签页插件。
- `experiments/recommendation/` 后续承载推荐算法实验。
- `experiments/agent/` 后续承载 AI / Agent 实验。
- `data/` 与 `scripts/` 为 Phase 1 数据工程预留。

## 4. Phase 0 验收方式

运行：

```bash
python scripts/verify_structure.py
```

预期输出：

```text
Phase 0 structure check passed: 25 required paths found.
```

## 5. 下一步

进入 Phase 1：诗词数据 MVP。

建议下一步产出：

```text
docs/data-schema.md
data/samples/poems.sample.json
scripts/data_import/validate_poems.py
```

目标是先建立 20 首人工 seed 诗词数据，并能用脚本校验数据格式。
