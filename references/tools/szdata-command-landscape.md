# SZData CLI 命令总账

更新时间：2026-07-06

这份文档是 `szdata` / `szdata_detail` / `szdatatest` / `szdatatest_detail` / `archive` 的全局命令地图。它不替代每个命令的 `--help`，只回答三件事：命令属于哪个任务域、什么时候选、不该拿它做什么。

## 总原则

- 高频生产只读主流程放 `szdata`。
- 测试验证、写前解析、测试写入链路放 `szdatatest`。
- 低频诊断、审计、解释、历史、日志、调度配置读回放 `szdata_detail`。
- 测试环境低频诊断镜像放 `szdatatest_detail`，命令清单必须与 `szdata_detail` 一致。
- `szdatatest` 与 `szdata` 重名的命令是测试环境主流程镜像，参数、默认输出和语义必须保持一致；不重叠的 `szdatatest` 命令表示仍处于测试验证期，不能当作生产稳定入口。
- 已替代、慢、容易误导、主体不清的旧入口放 `archive` 或直接拒绝。
- 同一任务族使用同一前缀，主体或维度放后缀，例如 `table-permission-mine/topic/role`。
- 主入口默认输出名片和结论摘要；长 SQL、DDL、日志、人员、字段、raw 证据必须走专项命令或显式参数。

## 入口边界

| 入口 | 定位 | 什么时候用 | 不该用它做什么 |
| --- | --- | --- | --- |
| `szdata` | 生产主工作流 | 找资产、核验表、查任务 SQL、读需求、读数据集/宽表、开发前置权限判断 | 默认不做生产写入；不放低频大对象诊断 |
| `szdata_detail` | 低频诊断解释面 | 字典、SQL 历史、模板、个人/统计视图、角色成员、调度策略、宽表日志/调度配置 | 不承载写入；不承载开发前置主判断 |
| `szdatatest` | 测试验证面 | 测试环境主流程镜像、字段解析、guard、宽表测试预览/生成/调度保存 | 不代表生产真实状态；独有命令表示仍在测试；测试写入也要显式 `--execute` 和确认 |
| `szdatatest_detail` | 测试低频诊断解释面 | 测试环境字典、SQL 历史、模板、角色成员、调度策略、宽表日志/调度配置 | 不承载测试生命周期写命令；清单必须对齐 `szdata_detail` |
| `archive` | 退役和风险命令 | 仅保留历史实现或排查资料 | 不作为 agent 可选入口 |

实现说明：`szdata_detail` / `szdatatest_detail` 是普通 OpenCLI site wrapper，root `.js` 只绑定 surface 并引用共享 core 中对应环境的只读实现。低频/detail 命令不应再出现在 `opencli szdata --help` 或 `opencli szdatatest --help`。共享 core 在 `C:\Users\13246\.opencli\shared\szdata-core\commands\`，一致性审计脚本为 `audit-surfaces.mjs`。

## 6 个主任务域

| 任务域 | 用户问题 | 主入口 | 深化/低频入口 | 不推荐/归档 | 定位 |
| --- | --- | --- | --- | --- | --- |
| 1. 数据资产发现 | 我知道关键词/库表，怎么找到资产？ | `table` / `table-search` | `table-guid` / `table-detail` / `table-ddl` / `table-lineage` / `table-sample` | 旧名 `dms` / `guid` / `table-info` / `sample` / `lineage` | 找表、确认表、看结构/血缘/样例 |
| 2. 任务、需求、子任务 | 我知道任务号、需求或子任务，怎么读现状、拿 SQL 证据、授权后写子任务？ | `task-sql` / `demand-list` / `demand-detail` | `demand-subtask-list` / `demand-subtask-detail` / `demand-mine` / `demand-stats` | `etl-sql` | 读任务 SQL、需求详情、子任务现状；授权后创建/修改子任务 |
| 3. 权限与主体诊断 | 当前用户/主题/角色能不能读目标表？角色是什么、有哪些成员、有哪些可选主题？ | `table-permission-mine` / `table-permission-topic` / `table-permission-role` | `role-list` / `role-user-list` / `scheduling-topic-list-by-current-user` / `scheduling-topic-base-policy` | `current-user-data-permission` / `my-permission-base` / `my-permission-data` / `my-permission-function` / `my-permission-report` / `role-data-permission` / `role-summary` / `scheduling-topic-table-check` / `table-permission-check` | 主体是谁、能不能读表、主题基础策略是什么 |
| 4. 数据集读回与测试配置 | 数据集配置、SQL、字段、模板、字典怎么读？ | `dataset-config` | `dataset-config-dict` / `dataset-sql-versions` / `dataset-templates` / `dataset-indicator-sql` | - | 生产只读确认；测试环境承担字段解析和写前 guard |
| 5. 宽表管理 | 宽表、生成详情、状态、日志、调度配置怎么读？ | `widetable` / `widetable-detail` | `widetable-explain` / `widetable-action-log` / `widetable-schedule-config` / `widetable-schedule-detail` | 历史 config-save probe | 宽表状态、详情、调度配置、测试预览/生成/调度保存 |
| 6. 支撑入口 | 怎么登录、查帮助中心？ | `login` | `portal-help` | - | 只辅助会话和帮助检索，不代表业务验证成功 |

任务、需求、子任务的写入/辅助命令统一归入第 2 域：

| 命令 | 定位 | 什么时候选 | 边界 |
| --- | --- | --- | --- |
| `subtask-source-system-list` | 源系统候选 | 建采集子任务前，先找源系统 | 只读；不创建子任务 |
| `subtask-access-point-list` | 数据源候选 | 已知源系统，找 datasource/dbIdentifier | 只读；默认隐藏 host/port |
| `subtask-gather-create` | 新建采集子任务 | 明确授权后新建采集子任务 | 默认 dry-run；生产写入前必须读现状、测试验证、用户授权 |
| `subtask-gather-update` | 修改采集子任务 | 明确授权后修改采集子任务 | 不是读详情入口；先用 `demand-subtask-detail` |
| `subtask-modeling-create` | 新建建模子任务 | 明确授权后新建建模类子任务 | 默认 dry-run；不替代需求/子任务读回 |

## 数据资产发现

| 命令 | 默认字段/输出形态 | 什么时候选 | 不回答什么 |
| --- | --- | --- | --- |
| `table` | `identity` / `structure` / `ownership` / `tasks` / `lineage` / `sample` / `evidenceNote` | 已知 `db.table`，想快速确认表身份、结构摘要、负责人、任务、血缘预览 | 不返回完整 DDL、完整元数据、完整血缘 |
| `table-search` | `guid` / `name` / `comment` / `typeName` / `metadataType` / `qualifiedName` / `dbName` / `dataSource` | 只知道关键词、中文名、业务词 | 不做最终表核验 |
| `table-guid` | `guid` / `dbName` / `tableName` / `qualifiedName` / `comment` / `typeName` / `dataSource` / `resultLevel` | 已知 `db.table`，后续命令必须传 GUID | 通常不是用户问题的最终答案 |
| `table-detail` | 完整扁平元数据字段 | 已知 GUID，要完整归属、状态、来源任务、权限摘要等 | 不负责抽样数据或完整血缘行表 |
| `table-ddl` | `guid` / `qualifiedName` / `dbName` / `tableName` / `type` / `partition` / `ddl` | 明确要建表语句、字段类型、分区 | 不再拆冗余字段清单；DDL 本身就是证据 |
| `table-lineage` | `id` / `typeName` / `name` / `direction` / `apiCode` / `appId` / `usernames` / `status` | 明确要上下游依赖证据 | 不替代 `table` 的快速核验 |
| `table-sample` | 动态样例行字段，默认 10 行 | 明确要看少量样例 | 不作为资产发现主入口，不证明对账结果 |

选择规则：已知 `db.table` 先用 `table`；只知道词先 `table-search` 再 `table`；要 DDL、完整元数据、完整血缘、样例时才调用专项命令。

## 任务、需求、子任务

| 命令 | 默认字段/输出形态 | 什么时候选 | 不回答什么 |
| --- | --- | --- | --- |
| `task-sql` | `taskId` / `createSql` / `querySql` / `evidence_level` / `limitations` | 已知 Horae 任务号，要 SQL / ETL 证据 | 不证明任务实例运行成功，不证明数据正确 |
| `demand-list` | 需求列表名片 | 按关键词、状态、负责人找需求候选 | 不读完整需求内容 |
| `demand-detail` | 需求详情 | 已知需求 UUID，要读现状 | 不创建或推进需求 |
| `demand-subtask-list` | 子任务列表 | 已知需求 UUID，要看下面有哪些子任务 | 不读单个子任务完整字段 |
| `demand-subtask-detail` | 子任务详情 | 已知子任务 UUID，要读源表、数据源、状态等 | 不修改子任务 |
| `demand-mine` | 我的需求列表 | 低频个人视图 | 不作为需求检索主入口 |
| `demand-stats` | 状态统计、平均进度、接口人 TOP | 低频统计视图 | 不回答单个需求现状 |
| `subtask-gather-create` | dry-run / save / submit 输出 | 明确授权后新建采集子任务 | 不在未读现状时直接写 |
| `subtask-gather-update` | dry-run / save 输出 | 明确授权后修改采集子任务 | 不作为读详情入口 |
| `subtask-modeling-create` | dry-run / save / submit 输出 | 明确授权后新建建模类子任务 | 不替代需求/子任务读回 |

固定链路：`demand-detail` -> `demand-subtask-list` / `demand-subtask-detail` -> dry-run -> `szdatatest` 验证 -> 用户明确授权 -> 才考虑 `szdata` 生产写入。

## 权限与主体诊断

| 命令 | 默认输出 | 什么时候选 | 不该用它做什么 |
| --- | --- | --- | --- |
| `table-permission-mine` | `user` / `table` / `status` / `matchedBy` / `validity` / `sourceTypes` / `roles` / `packages` | 当前登录用户能不能读某表 | 不回答角色或调度主题 |
| `table-permission-topic` | `topicName` / `topicDesc` / `themeUser` / `table` / `conclusion` / `matchedBy` / `matched` / `source` / `validity` | 调度主题能不能读某表 | 不回答当前用户自身权限 |
| `table-permission-role` | `roleId` / `roleName` / `table` / `conclusion` / `matchedBy` / `matched` / `source` | 指定角色能不能读某表 | 不做无目标表的大盘输出 |
| `role-list` | `roleId` / `roleName` / `remark` / `itDemand` / `canApplyDataPerm` | 用角色名找 `roleId` | 不判断表权限 |
| `role-user-list` | `roleId` / `roleName` / `counts` / `rows` | 看某个角色有哪些人 | 不是 user -> roles 反查 |
| `scheduling-topic-list-by-current-user` | 当前用户可选调度主题 | 选择或确认主题 | 不判断主题能不能读表 |
| `scheduling-topic-base-policy` | 主题用户基础策略摘要 | 解释主题基础策略 | 最终表权限仍走 `table-permission-topic` |

归档/拒绝入口：`current-user-data-permission`、`my-permission-base`、`my-permission-data`、`my-permission-function`、`my-permission-report`、`role-data-permission`、`role-summary`、`scheduling-topic-table-check`、`table-permission-check`。

## 数据集读回与测试配置

| 命令 | 输出规则 | 什么时候选 | 不回答什么 |
| --- | --- | --- | --- |
| `dataset-config` | 默认过滤空值和 `"-"`；列表/详情都有边界；SQL 只在指定预览或保存本地时展开 | 读生产/测试数据集配置、用途、宽表挂接、字段摘要 | 不保存平台配置 |
| `dataset-config-dict` | 默认不返回 raw | 查 usageType、dataType、sceneType、businessOwnership 等字典 | 不解析 SQL 字段 |
| `dataset-sql-versions` | 列表只给版本号/时间；指定版本或 compare 才给 SQL 预览 | 查 SQL 历史或版本对比 | 不代表任务运行成功 |
| `dataset-templates` | 列表不吐完整 SQL/raw；指定 `--id` 才给 SQL 预览 | 查模板列表、模板详情 | 不作为普通数据集配置读回 |
| `dataset-indicator-sql` | SQL 预览有边界 | 指标体系宽表 SQL 参数探查 | 不自动完成完整指标选择流程 |
| `dataset-create-columns` | `szdatatest` 字段解析 | 写前解析 SQL/table 输出字段 | 不替代保存 |
| `dataset-create-guard-check` / `dataset-create` | `szdatatest` guard / dry-run / 显式测试保存 | 普通 SQL 数据集测试验证 | usage 3/5 普通保存硬阻断，宽表走专门命令 |

## 宽表管理

| 命令 | 输出规则 | 什么时候选 | 不回答什么 |
| --- | --- | --- | --- |
| `widetable` | 宽表名片列表 | 搜宽表、用 task-id 反查 UUID/dataSetConfigId | 不读完整调度配置 |
| `widetable-detail` | 宽表生成详情 | 已知 UUID 或 dataSetConfigId，要确认宽表定义 | 不证明任务实例成功 |
| `widetable-explain` | 本地规则解释 | 看状态、按钮、场景、环境边界 | 不访问平台保存接口 |
| `widetable-action-log` | 默认最多 20 行，`--raw` 才展开 raw | 看流转日志 | 不作为主入口，不默认 dump 全量日志 |
| `widetable-schedule-detail` | SQL 预览有边界 | 已知 Horae task-id，要读 DispatchTaskConfig | 不保存调度 |
| `widetable-schedule-config` | SQL 预览有边界 | 已知宽表 UUID，要读 local/upgrade 配置入口回显 | 不提交升级 |
| `wide-table-preview-test` / `wide-table-generate-test` / `wide-table-schedule-save-test` / `wide-table-schedule-validate` | `szdatatest`，默认 dry-run 或 read-only，写入要显式确认 | 宽表测试生命周期验证 | 不做生产写入 |

## 支撑入口

| 命令 | 什么时候选 | 边界 |
| --- | --- | --- |
| `login` | 会话过期、401、token 异常 | 只辅助登录，不代表业务验证成功 |
| `portal-help` | 查帮助中心内容 | 只读检索，不替代命令实测 |

## 本轮实测与收敛结果

| 命令 | 调整前实测 | 调整后实测 | 结论 |
| --- | ---: | ---: | --- |
| `dataset-config --size 2` | 约 3.0KB | 约 1.3KB | 默认过滤空值和 `"-"` |
| `dataset-sql-versions --id 17376` | 约 2.5KB | 约 1.2KB | 版本列表不再带空 SQL/raw 字段 |
| `dataset-config-dict --dict dataType` | 646B | 422B | 默认不输出 raw |
| `widetable-action-log --size 5` | 约 6.9KB 全量 | 约 0.9KB | 增加 `--size`，默认不输出 raw |
| `subtask-access-point-list --size 3` | 621B，含端口 | 489B，不含 host/port | 隐藏连接细节 |
| `table-permission-topic` | 456B | 335B | 来源/有效期压成短字段 |

本轮没有执行任何生产写入。
