# szdata

`szdata` 是数综生产环境 `data.gf.com.cn` 的 OpenCLI 主工作流入口。适配器源码不在本工作区，live 目录是：

```text
C:\Users\13246\.opencli\clis\szdata
C:\Users\13246\.opencli\clis\szdatatest
```

本工作区只保存规则、文档和调查证据。改命令行为时同步维护 [szdata-command-landscape.md](./szdata-command-landscape.md) 和 live adapter 的 `COMMANDS.md`。

## 环境边界

- `szdata`：生产只读确认和高频主流程。
- `szdatatest`：测试读回、字段解析、guard、测试写入生命周期验证。
- `szdata_detail`：生产低频诊断、审计、解释、历史、日志、调度配置读回。
- `szdatatest_detail`：测试环境低频诊断镜像，命令清单对齐 `szdata_detail`。
- 生产写入必须先有 `szdatatest` 验证，再拿到用户明确授权。
- `szdatatest` 与 `szdata` 重名的命令必须保持参数、默认输出和语义一致；`szdatatest_detail` 与 `szdata_detail` 命令清单必须一致；`szdatatest` 独有命令表示仍在测试验证期，不代表生产稳定入口。

## 先读哪里

| 目的 | 先读 |
| --- | --- |
| 不知道该用哪个命令 | [szdata-command-landscape.md](./szdata-command-landscape.md) |
| 审计或优化 CLI | [szdata-agent-cli-audit.md](./szdata-agent-cli-audit.md) |
| 看 OpenCLI adapter 位置和编辑规则 | [opencli.md](./opencli.md) |
| 写操作、数据集、宽表、子任务专题 | [szdata-operations/README.md](./szdata-operations/README.md) |
| 低频 wrapper 边界 | [szdata-detail.md](./szdata-detail.md) |
| 四入口一致性审计 | `node C:\Users\13246\.opencli\shared\szdata-core\audit-surfaces.mjs --plain` |

## 常用选择路径

| 用户问题 | 优先命令 | 下一步 |
| --- | --- | --- |
| 已知 `db.table`，想确认这表是什么 | `opencli szdata table --db <db> --table <table> -f json` | 完整 DDL 用 `table-ddl`，完整血缘用 `table-lineage` |
| 只知道关键词、中文名、业务词 | `opencli szdata table-search --keyword <keyword> -f json` | 对候选 `db.table` 再用 `table` |
| 已知 GUID，要元数据/DDL/血缘/样例 | `table-detail` / `table-ddl` / `table-lineage` / `table-sample` | 不要把 `table-sample` 当资产发现入口 |
| 已知 Horae 任务号，要 SQL 证据 | `opencli szdata task-sql --task-id <id> -f json` | 宽表任务继续看 `widetable --task-id` / `widetable-schedule-detail` |
| 已知需求或子任务，要读现状 | `demand-list` / `demand-detail` / `demand-subtask-list` / `demand-subtask-detail` | 写操作前必须先读现状 |
| 当前登录用户能不能读表 | `table-permission-mine --table db.table -f json` | 需要来源明细再看 detail 类命令 |
| 调度主题能不能读表 | `table-permission-topic --topic TOPIC --table db.table -f json` | 解释主题基础策略用 `szdata_detail scheduling-topic-base-policy` |
| 角色能不能读表 | `table-permission-role --role-id ROLE_ID --table db.table -f json` | 角色名找 ID 用 `szdata_detail role-list` |
| 看数据集配置 | `dataset-config --id <id> -f json` 或带筛选列表 | SQL 历史用 `dataset-sql-versions`，模板/字典走 `szdata_detail` |
| 看宽表 | `widetable` / `widetable-detail` | 日志、调度配置、规则解释走 `szdata_detail` |
| 建采集/建模子任务前找候选 | `subtask-source-system-list` -> `subtask-access-point-list` | 写入命令必须 dry-run、测试验证、用户授权 |

## 命名规则

- 表资产统一 `table-*`。
- 表权限统一 `table-permission-*`，主体放后缀：`mine` / `topic` / `role`。
- 角色命令 `role-*` 只回答角色和成员，不回答表权限。
- `my-permission-*` 已从活动入口移除；不要用它回答表权限或主体诊断。
- 调度主题 `scheduling-topic-*` 只回答主题选择和基础策略，不回答最终表权限。
- 数据集 `dataset-*` 只读配置、字典、模板、SQL 历史；测试解析和写前 guard 放 `szdatatest`。
- 宽表 `widetable-*` 读回和解释；`wide-table-*-test` 明确表示测试写入链路。
- 子任务统一 `subtask-*`：`subtask-gather-*` 是采集子任务，`subtask-modeling-*` 是建模类子任务，辅助列表用 `subtask-*-list`。

## 输出规则

- 主入口默认返回摘要，不返回大对象树。
- 诊断命令默认给结论和预览；长来源用 `--detail`，raw 用 `--raw`。
- SQL、DDL、日志、人员列表、字段列表默认有边界。
- 不返回无业务意义字段，例如空值、`limitations: "-"`、默认隐藏 raw、连接 host/port。

## 归档和拒绝入口

这些不是 agent 可选入口：

```text
current-user-data-permission
my-permission-base
my-permission-data
my-permission-function
my-permission-report
role-data-permission
role-summary
scheduling-topic-table-check
table-permission-check
demand-subtasks
create-subtask
update-subtask
create-model-subtask
list-source-systems
list-access-points
```

对应替代：

- 当前用户表权限：`table-permission-mine`
- 调度主题表权限：`table-permission-topic`
- 角色表权限：`table-permission-role`
- 需求下子任务列表：`demand-subtask-list`
- 采集子任务写入：`subtask-gather-create` / `subtask-gather-update`
- 建模类子任务写入：`subtask-modeling-create`
- 子任务候选辅助：`subtask-source-system-list` / `subtask-access-point-list`
- 表资产旧名：`dms` / `guid` / `table-info` / `sample` / `lineage` 已收敛到 `table-search` / `table-guid` / `table-detail` / `table-sample` / `table-lineage`

## 不能证明什么

- 任务实例实际运行成功。
- 指定业务日期数据正确。
- 样例数据代表全量对账结果。
- 数据集、宽表、需求状态等于生产作业成功。
- 查不到表就代表表不存在。

## 专题文档

- [opencli.md](./opencli.md)：OpenCLI 适配器位置、命令发现、编辑和验证规范。
- [szdata-command-landscape.md](./szdata-command-landscape.md)：全局任务域和命令归属总账。
- [szdata-detail.md](./szdata-detail.md)：`szdata_detail` router 边界。
- [szdata-operations/README.md](./szdata-operations/README.md)：写操作和复杂流程索引。
- [szdata-operations/dataset-create.md](./szdata-operations/dataset-create.md)：普通 SQL 数据集测试创建和 guard。
- [szdata-operations/wide-table-management.md](./szdata-operations/wide-table-management.md)：宽表读回、测试预览、生成、调度配置。
- [szdata-operations/role-permission-readonly.md](./szdata-operations/role-permission-readonly.md)：角色/权限只读诊断参考。
