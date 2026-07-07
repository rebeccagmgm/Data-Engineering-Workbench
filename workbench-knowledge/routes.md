# Knowledge Routes

本文件定义 Case 收尾时，`distilled/` 里的候选应该去哪里。

## 路由表

| 候选类型 | 判断标准 | 去向 |
| --- | --- | --- |
| Case 现场记录 | 只解释本次需求发生了什么 | 留在 Case |
| 原始材料索引 | 来源、摘要、候选问题、待验证点 | `00-原始需求背景/source-index.md` |
| 平台读回证据 | Horae、Flow、szdata、DSP、数据库读回 | Case `evidence/` 或 `trust-pack/` |
| 当前可信结论 | 本 Case 下一步行动所依赖的判断 | `case.md` |
| 卡片模板 | 下次能复用的任务卡、阻塞卡、证据卡格式 | `workbench-knowledge/card-templates/` |
| 工作流模式 | 多个卡片和证据门禁组成的常见推进套路 | `workbench-knowledge/workflow-patterns/` |
| 能力契约 | 业务能力和工具实现的稳定映射 | `workbench-knowledge/capability-contracts/` |
| 未审核经验 | 有复用潜力，但还没被下个 Case 验证 | `workbench-knowledge/promotion-inbox/` |
| 稳定业务知识 | 表、字段、系统、口径、业务概念 | `agent-kb/股衍/` 或 `agent-kb/数据开发/` |
| 稳定工程方法 | Case 工作法、经验编译、评估门禁 | `agent-kb/工程方法/` 或 `agent-kb/知识库设计/` |
| 工具缺口 | 高频人工动作、CLI 输出不适合 Agent、缺读回能力 | Workbench 先记录，成熟后进入 OpenCLI 源码 |
| 全局规则 | 生产写入边界、读回验证门禁 | Workbench docs / `AGENTS.md` / Skill |

## 晋升检查

进入正式知识库或 Skill 前，至少回答：

- 来源 Case 是哪个？
- 它解决了什么重复问题？
- 它适用于哪些场景？
- 它不适用于哪些场景？
- 下次 Case 如何验证它真的有用？

## 降级检查

候选应降级或留在历史案例中，如果：

- 只适用于一个需求。
- 没有读回证据支撑。
- 依赖过时平台状态。
- 和 `agent-kb` 现有正式知识冲突但未修订。
- 下次 Case 命中后没有减少工作量。
