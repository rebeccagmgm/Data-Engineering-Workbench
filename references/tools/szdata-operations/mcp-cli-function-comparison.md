# MCP / CLI 功能全集对比

更新日期：2026-07-07

## 范围

本文记录当前 `szdata` CLI 功能全集与三个 Data Portal MCP server 的功能覆盖关系：

- `https://data.gf.com.cn/mcp/metadata`
- `https://data.gf.com.cn/mcp/schedule`
- `https://data.gf.com.cn/mcp/sql_dignose`

保密边界：本文不保存任何 API key、Bearer token、cookie、`X-Token`、`X-Personal-Token` 实际值，不保存 GUID、完整 DDL、完整 SQL。

## 总结

当前 CLI 的功能全集比三个 MCP 暴露的 tool 更多，但 CLI 主要依赖 Portal 登录态 Cookie / `X-Token`。三个 MCP 是更窄的一组标准化工具，其中 metadata 已确认能进一步落成部分纯 `X-Personal-Token` direct openapi；schedule 和 sql_dignose 当前只证明 MCP 入口可用，未找到可绕过 MCP 的 `X-Personal-Token` 直连接口。

需要特别区分“功能面覆盖”和“输出形态等价”：当前 CLI 不是 MCP 输出的严格超集。CLI 覆盖了更多数综业务域，但在 schedule / sql_dignose 的若干工具上还没有完全复刻 MCP 返回内容，尤其是调度完整日志字段、SQL 诊断原始返回形态，以及 `schedule.get_task_run_states` 的后端参数/返回语义。

| 维度 | 当前 CLI | MCP metadata | MCP schedule | MCP sql_dignose |
| --- | --- | --- | --- | --- |
| 功能面 | 最大，但不是 MCP 输出严格超集 | 中等 | 中等 | 很小 |
| 认证 | Portal Cookie + `X-Token` | `X-Personal-Token` 进 MCP；部分可 direct openapi | `X-Personal-Token` 进 MCP | `X-Personal-Token` 进 MCP |
| 是否绕过 MCP | 是 | MCP 入口否；metadata openapi 可绕过 | 当前 CLI 绕过 MCP，但靠 Portal 登录态 | 当前 CLI 绕过 MCP，但只是部分替代 |
| 是否纯 `X-Personal-Token` direct API | 不是 | metadata 部分是 | 目前不是 | 目前不是 |
| 等价程度 | 业务域更广，但 MCP 部分输出未完全覆盖 | metadata 核心基本可对齐 | schedule 多数可读能力可部分对齐，日志/状态语义有缺口 | SQL 诊断不是精确等价 |

## MCP Tool 对 CLI 覆盖

| 功能 | MCP metadata | MCP schedule | MCP sql_dignose | 当前 CLI 对应 |
| --- | --- | --- | --- | --- |
| 表精确搜索 / `db.table` 查表 | `metadata.search_table` | - | - | `table`, `table-search`, `table-guid` |
| 表 DDL | `metadata.get_table_ddl` | - | - | `table-ddl` |
| ES / 综合元数据搜索 | `metadata.search_by_es` | - | - | `table-search`，部分覆盖 |
| Dify 问答式元数据助手 | `metadata.query_assistant_dify` | - | - | 暂无，不建议稳定 CLI 化 |
| GUID 查表详情 | `metadata.get_table_by_guid` | - | - | `table-detail` |
| 表血缘 | `metadata.get_table_lineage_info` | - | - | `table-lineage` |
| 调度任务详情 | - | `schedule.get_schedule_detail` | - | `schedule-detail` |
| 调度依赖 | - | `schedule.get_task_dependencies` | - | `schedule-mcp-dependencies` |
| 调度运行实例 | - | `schedule.get_task_run_instances` | - | `schedule-mcp-run-instances` |
| 调度运行状态 | - | `schedule.get_task_run_states` | - | `schedule-mcp-run-states` |
| 调度运行日志 | - | `schedule.get_task_run_logs` | - | `schedule-mcp-run-logs`，默认只输出日志可用性、长度和有界预览 |
| 负责人失败实例 | - | `schedule.get_owner_failed_instances` | - | `schedule-mcp-owner-failed-instances` |
| Horae 任务 SQL | - | `metadata.get_horae_sql_by_task_id` | - | `task-sql` |
| SQL 诊断 | - | - | `query.sql_diagnosis` | `sql-diagnosis`，部分覆盖，不是精确等价 |

## 实际试用记录（MCP + CLI，替换前）

本节记录 2026-07-07 对用户关注的 schedule / SQL 相关能力做的实际调用。MCP 侧使用用户提供的 `/mcp/schedule`、`/mcp/sql_dignose` 入口和环境变量中的 `X-Personal-Token`；CLI 侧使用当前 `opencli szdata` 生产只读命令。输出只保留状态、数量、字段形态和缺口，不保存 token、GUID、完整 SQL、DDL 或完整日志正文。

注意：本节是替换前的实测记录。后续已新增 active `schedule-mcp-*` 命令，并将旧 partial direct schedule runtime wrappers 从 active `szdata` 入口移出。

| 功能 | MCP 实测 | CLI 实测 | 当前判断 |
| --- | --- | --- | --- |
| 调度任务详情 | `schedule.get_schedule_detail` 返回任务详情对象，包含任务标识、名称、状态、周期、负责人等字段形态 | `schedule-detail --sql-preview 0 -f json` 成功，能返回任务卡片；本次关闭 SQL 预览 | 两边都可用，CLI 已覆盖主要详情读取 |
| 调度依赖 | `schedule.get_task_dependencies` 返回上游/下游依赖字段形态 | `schedule-dependencies -f json` 成功，样例任务解析到上游依赖数量 | 两边都可用；CLI 当前主要以 Portal `tasklink` 解析上游为主 |
| 调度运行实例 | `schedule.get_task_run_instances` 返回实例数组，样例窗口返回 2 条实例字段 | `schedule-run-instances -f json` 成功，样例窗口返回 2 条实例摘要 | 两边都可用；CLI 输出更克制，不带日志地址等敏感/低价值字段 |
| 调度运行状态 | `schedule.get_task_run_states` 使用日期参数时后端返回反序列化错误 | `schedule-run-states -f json` 成功，由实例列表派生状态 | CLI 当前更稳定，但这不证明与 MCP 后端完全等价；MCP 可能需要不同日期参数形态 |
| 调度运行日志 | `schedule.get_task_run_logs` 返回日志对象字段形态，包含坏日志/完整日志内容字段，但本文不保存正文 | `schedule-run-logs -f json` 成功确认实例与状态；样例返回 `logAvailable=N` | 这是最大缺口：MCP 能拿到完整日志字段，CLI 当前只是实例/状态级确认 |
| 负责人失败实例 | `schedule.get_owner_failed_instances` 用无效负责人和未来日期安全探测，返回空数组 | `schedule-owner-failed-instances -f json` 同样返回空数组 | 调用路径可用；真实负责人场景仍需按授权做只读验证 |
| Horae 任务 SQL | `metadata.get_horae_sql_by_task_id` 返回 SQL 数组字段形态，本文不保存 SQL 正文 | `task-sql -f json` 成功，能返回 SQL 字段；本文不保存 SQL 正文 | 两边都可取 SQL；CLI 已覆盖，但输出使用时必须继续限制 SQL 展示 |
| SQL 诊断 | `query.sql_diagnosis` 对安全样例 SQL 返回诊断对象，含 `valid` / `errors` 字段形态 | `sql-diagnosis --sql 'select 1' -f json` 成功，返回有效、问题数为 0，并明确其证据级别 | 两边都可用；CLI 是 Portal 诊断接口的部分替代，不是已证明的 MCP 精确等价 |

## 2026-07-07 后续改造

用户确认 schedule 这部分可以直接 MCP-backed CLI 化。因此 active `szdata` 入口改为新增 `schedule-mcp-*` 命令，旧的 partial direct runtime wrappers 不再作为 active 入口暴露。

| 原 partial direct 命令 | 新 active MCP 命令 | 说明 |
| --- | --- | --- |
| `schedule-dependencies` | `schedule-mcp-dependencies` | 覆盖 MCP 上游/下游依赖形态 |
| `schedule-run-instances` | `schedule-mcp-run-instances` | 直接封装 MCP 运行实例 |
| `schedule-run-states` | `schedule-mcp-run-states` | 直接封装 MCP 运行状态；已用日期时间参数做 live smoke |
| `schedule-run-logs` | `schedule-mcp-run-logs` | 直接封装 MCP 日志字段；默认不输出完整日志正文 |
| `schedule-owner-failed-instances` | `schedule-mcp-owner-failed-instances` | 直接封装 MCP 负责人失败实例 |

## CLI 额外功能

下面这些是当前 CLI 已覆盖、但三个 MCP server 没有暴露为 tool 的功能。

| 功能域 | 当前 CLI 功能 | MCP 三件套状态 |
| --- | --- | --- |
| 表样例数据 | `table-sample` | 未暴露 |
| 指标搜索 | `indicator` | 未暴露 |
| 标签维度搜索 | `tagdim` | 未暴露 |
| 需求列表/详情 | `demand-list`, `demand-detail` | 未暴露 |
| 需求子任务详情 | `demand-subtask-list`, `demand-subtask-detail` in `szdata_detail` | 未暴露 |
| 我的需求/需求统计 | `demand-mine`, `demand-stats` in `szdata_detail` | 未暴露 |
| 当前用户表权限 | `table-permission-mine` | 未暴露 |
| 调度主题表权限 | `table-permission-topic` | 未暴露 |
| 角色表权限 | `table-permission-role` | 未暴露 |
| 角色/成员查询 | `role-list`, `role-user-list` in `szdata_detail` | 未暴露 |
| 调度主题/基础策略 | `scheduling-topic-list-by-current-user`, `scheduling-topic-base-policy` in `szdata_detail` | 未暴露 |
| 数据集配置 | `dataset-config` | 未暴露 |
| 数据集字典/SQL 版本/模板 | `dataset-config-dict`, `dataset-sql-versions`, `dataset-templates`, `dataset-indicator-sql` | 未暴露 |
| 测试环境数据集创建校验 | `dataset-create-columns`, `dataset-create-guard-check`, `dataset-create` in `szdatatest` | 未暴露 |
| 宽表查询/详情 | `widetable`, `widetable-detail` | 未暴露 |
| 宽表解释/日志/调度配置 | `widetable-explain`, `widetable-action-log`, `widetable-schedule-config`, `widetable-schedule-detail` | 未暴露 |
| 宽表测试生命周期 | `wide-table-preview-test`, `wide-table-generate-test`, `wide-table-schedule-save-test`, `wide-table-schedule-validate` | 未暴露 |
| 采集/建模子任务候选 | `subtask-source-system-list`, `subtask-access-point-list` | 未暴露 |
| 采集/建模子任务写路径 | `subtask-gather-create`, `subtask-gather-update`, `subtask-modeling-create` | 未暴露，且 CLI 需要授权/测试优先 |
| 登录/帮助 | `login`, `portal-help` | 未暴露 |

## 关键判断

1. 当前 CLI 发现面最大，因为它来自 Data Portal 页面、Portal 原生 `prod-api`、OpenCLI live adapter 和历史验证路径。
2. “CLI 功能面更广”不等于“CLI 是 MCP 输出超集”。当前 CLI 对 schedule / sql_dignose 仍有若干输出形态缺口，最明确的是完整运行日志和 SQL 诊断精确等价。
3. 三个 MCP server 暴露的是较窄的标准化工具集，适合做能力清单和行为参考，但不是数综全部功能。
4. `X-Personal-Token` 不是通用非 MCP API token：metadata direct openapi 可用，schedule / sql_dignose 当前没有找到可用 direct personaltoken API。
5. 当前 CLI 绕过 MCP 的方式是 Portal 登录态 Cookie / `X-Token`，不是纯 `X-Personal-Token`。
6. 如果后续目标是“全部功能都纯 direct API + X-Personal-Token”，需要服务端 route 元数据、网关目录、实际调用日志，或服务方将 schedule / sql_dignose 相关接口开放为 personaltoken openapi。

## 相关文档

- [mcp-openapi-survey.md](./mcp-openapi-survey.md)：当前 MCP / OpenAPI / `X-Personal-Token` 探测。
- [mcp-cli-coverage-report.md](./mcp-cli-coverage-report.md)：MCP tool 到 `szdata` CLI 的覆盖与缺口。
- [../szdata-command-landscape.md](../szdata-command-landscape.md)：`szdata` / `szdata_detail` / `szdatatest` / `szdatatest_detail` 全局命令归属。
