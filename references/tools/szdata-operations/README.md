# szdata-operations

更新时间：2026-07-06

本目录只放数综平台的专题流程和复杂操作细节。全局命令归属、默认入口、归档入口以 [../szdata-command-landscape.md](../szdata-command-landscape.md) 为准；日常路由看 [../szdata.md](../szdata.md)。

## 本目录定位

- 写操作设计、dry-run、测试验证、生产授权边界。
- 数据集、宽表、采集/建模类子任务等复杂流程。
- 权限、调度主题等只读诊断的底层接口和证据解释。
- 历史调查报告只作背景，不作 active 命令地图。

不要在本目录维护第二份全局命令清单。命令归属变化先改总账，再改专题文档。

## 必读顺序

| 场景 | 先读 | 再读 |
| --- | --- | --- |
| 不确定该用哪个命令 | [../szdata-command-landscape.md](../szdata-command-landscape.md) | [../szdata.md](../szdata.md) |
| 审计或优化 SZData CLI | [../szdata-agent-cli-audit.md](../szdata-agent-cli-audit.md) | [../opencli.md](../opencli.md), live adapter `COMMANDS.md` |
| 要改 OpenCLI adapter | [../opencli.md](../opencli.md) | live adapter `COMMANDS.md` |
| 数据集创建/保存/字段解析 | [specs/dataset-save-flow.md](./specs/dataset-save-flow.md) | [dataset-create.md](./dataset-create.md), [dataset-detail-fields.md](./dataset-detail-fields.md) |
| 宽表预览/生成/调度保存 | [specs/wide-table-lifecycle.md](./specs/wide-table-lifecycle.md) | [wide-table-management.md](./wide-table-management.md) |
| 需求和子任务读写 | [demand-routing.md](./demand-routing.md) | [subtask-gather-create.md](./subtask-gather-create.md), [subtask-gather-update.md](./subtask-gather-update.md) |
| 权限诊断 | [../szdata-command-landscape.md](../szdata-command-landscape.md#权限与主体诊断) | [role-permission-readonly.md](./role-permission-readonly.md), [scheduling-permission-readonly.md](./scheduling-permission-readonly.md) |

## 文档索引

| 文档 | 定位 | 状态 |
| --- | --- | --- |
| [demand-routing.md](./demand-routing.md) | 需求分析后该建采集子任务、建模类子任务、数据集，还是只读调查 | active |
| [subtask-gather-create.md](./subtask-gather-create.md) | 新建采集子任务流程 | active |
| [subtask-gather-update.md](./subtask-gather-update.md) | 修改采集子任务流程 | active |
| [dataset-create.md](./dataset-create.md) | 普通 SQL 数据集测试创建、字段解析、guard 和保存边界 | active |
| [dataset-detail-fields.md](./dataset-detail-fields.md) | 数据集详情字段、选项、联动和按钮行为 | active |
| [dataset-configuration-profile.md](./dataset-configuration-profile.md) | 存量数据集配置画像和 usageType/sceneType 归纳 | active/read-only |
| [wide-table-management.md](./wide-table-management.md) | 宽表列表、详情、预览、生成、调度配置、状态规则 | active |
| [role-permission-readonly.md](./role-permission-readonly.md) | 角色、成员、角色对表权限只读诊断证据 | active |
| [my-permission-readonly.md](./my-permission-readonly.md) | 历史 My Permission 快照调查；`my-permission-*` 活动入口已移除 | historical |
| [scheduling-permission-readonly.md](./scheduling-permission-readonly.md) | 调度主题、主题用户基础策略、主题对表权限证据 | active |
| [permissionservice-readonly-survey.md](./permissionservice-readonly-survey.md) | `/permissionservice` 历史探索报告 | historical |
| [_template.md](./_template.md) | 新增专题文档模板 | template |

## Active 命令边界

| 领域 | 高频入口 | 低频/detail | 测试/写前验证 |
| --- | --- | --- | --- |
| 数据集 | `szdata dataset-config` | `szdata_detail` / `szdatatest_detail` 的 `dataset-config-dict` / `dataset-sql-versions` / `dataset-templates` / `dataset-indicator-sql` | `szdatatest dataset-create-columns` / `dataset-create-current-user` / `dataset-create` / `dataset-create-guard-check` |
| 宽表 | `szdata widetable` / `widetable-detail` | `szdata_detail` / `szdatatest_detail` 的 `widetable-explain` / `widetable-action-log` / `widetable-schedule-config` / `widetable-schedule-detail` | `szdatatest wide-table-preview-test` / `wide-table-generate-test` / `wide-table-schedule-save-test` / `wide-table-schedule-validate` |
| 需求/子任务 | `szdata task-sql` / `demand-list` / `demand-detail` | `szdata_detail` / `szdatatest_detail` 的 `demand-subtask-list` / `demand-subtask-detail` / `demand-mine` / `demand-stats` | `subtask-gather-create` / `subtask-gather-update` / `subtask-modeling-create` 必须先 dry-run；测试环境优先验证 |
| 子任务辅助 | `subtask-source-system-list` / `subtask-access-point-list` | - | 只读候选，不暴露连接细节 |
| 权限 | `szdata table-permission-mine/topic/role` | `role-list` / `role-user-list` / `scheduling-topic-*` | 需要时在 `szdatatest` 做同类只读检查 |

## Hard Boundaries

- 本目录规则不授权任何生产写入。
- `szdata` 生产写入必须先有 `szdatatest` 验证和用户明确授权。
- `szdatatest` 与 `szdata` 重名的命令是测试环境主流程镜像，必须保持参数、默认输出和语义一致。
- `szdatatest_detail` 与 `szdata_detail` 是低频诊断镜像，命令清单必须一致。
- `szdatatest` 独有命令表示仍在测试验证期，只能用于测试读回、guard、字段解析或显式测试写入，不能当作生产稳定入口。
- 普通 `dataset-create --save` 不允许隐藏 usage 3/5 宽表生命周期写入。
- 宽表测试写入必须使用命名清楚的 `wide-table-*-test` 命令，并显式 `--execute` 和确认参数。
- `dataset-create-columns` 是 SQL/table 输出字段解析入口；手写 fields 文件不能替代解析成功。
- `subtask-access-point-list` 默认不输出 host/port 等连接细节。
- 旧权限入口、`my-permission-*` 和旧子任务入口不作为 agent 工作流入口。

## 写操作通用流程

1. 读现状：先用需求、子任务、数据集或宽表 readback 命令确认当前状态。
2. dry-run：构造 payload，不写平台。
3. 测试验证：涉及表单、保存、提交、预览、生成、调度保存时先走 `szdatatest`。
4. 用户授权：生产写入必须由用户明确说清目标和动作。
5. 生产执行：只执行已授权的具体动作。
6. 回读验证：成功标准是下游页面或 follow-up readback 能读到结果，不只是 API 200。

## 维护规则

- 新增专题文档时，从 [_template.md](./_template.md) 开始。
- 任意命令归属变化先更新 [../szdata-command-landscape.md](../szdata-command-landscape.md)，再更新本目录专题。
- 历史调查可以保留，但必须标明 historical，不得覆盖 active command map。
