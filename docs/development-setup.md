# 开发环境与工程约定

## 1. Phase 0 技术选择

当前阶段只做工程骨架，不引入完整运行时依赖。

已明确的基础版本：

- Python：3.12
- Node.js：22

计划中的技术方向：

- 后端：FastAPI + Python
- 数据库：PostgreSQL，MVP 可先用 SQLite
- 向量检索：pgvector，等进入语义召回阶段再接入
- 前端：Next.js / React / TypeScript，等进入 Web MVP 阶段再初始化
- 插件：Chrome Extension Manifest V3，等进入强触达阶段再初始化

## 2. 为什么 Phase 0 不直接初始化所有框架

原因：

1. 当前还没有数据 schema 和推荐闭环，不应被框架细节牵制。
2. 后端、前端、插件的技术栈虽然有方向，但还需要根据 Phase 1/2 的实际需求确认。
3. 先建立目录边界和验证脚本，可以降低后续迁移成本。

## 3. 当前可运行命令

```bash
python scripts/verify_structure.py
```

或通过 npm script：

```bash
npm run verify:structure
```

这两个命令用于验证 Phase 0 必需目录和文件是否存在。

## 4. 代码与文档约定

- 所有规划文档放在 `docs/`。
- 原始数据放在 `data/raw/`。
- 清洗后的可消费数据放在 `data/processed/`。
- 小规模开发样例放在 `data/samples/`。
- 数据导入脚本放在 `scripts/data_import/`。
- 推荐评估脚本放在 `scripts/evaluation/`。
- 后端代码放在 `backend/app/`。
- 后端测试放在 `backend/tests/`。
- Web 前端放在 `frontend/app/`。
- 前端测试放在 `frontend/tests/`。
- 浏览器插件放在 `extension/newtab/`。
- 推荐和 Agent 实验放在 `experiments/`。

## 5. 下一阶段进入条件

进入 Phase 1 前，应该满足：

- Phase 0 目录结构存在。
- `python scripts/verify_structure.py` 通过。
- README 能引导读者找到项目文档。
- 数据、脚本、后端、前端、插件、实验目录边界清晰。
