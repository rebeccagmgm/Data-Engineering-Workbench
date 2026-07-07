# SZData CLI 视觉索引

更新时间：2026-07-06

这份文档只帮助快速建立空间感，不是命令规则源。规则源和命令归属以 [szdata-command-landscape.md](./szdata-command-landscape.md) 为准；日常选择路径看 [szdata.md](./szdata.md)。

## 入口关系

```mermaid
flowchart LR
  Q["用户问题"] --> A["判断任务域"]
  A --> S["szdata<br/>生产高频主流程"]
  A --> D["szdata_detail<br/>低频诊断/审计/解释"]
  A --> T["szdatatest<br/>测试验证/写前 guard/测试写入"]
  A --> TD["szdatatest_detail<br/>测试低频诊断镜像"]
  A --> R["archive<br/>退役/误导/慢命令"]

  S --> S1["资产发现<br/>table / table-search"]
  S --> S2["任务需求子任务<br/>task-sql / demand-* / subtask-*"]
  S --> S3["表权限<br/>table-permission-mine/topic/role"]
  S --> S4["数据集/宽表主读<br/>dataset-config / widetable / widetable-detail"]

  D --> D1["字典/模板/SQL 历史"]
  D --> D2["角色成员/我的权限快照"]
  D --> D3["调度主题策略"]
  D --> D4["宽表日志/调度配置/规则解释"]

  T --> T1["dataset-create-columns / dataset-create-current-user"]
  T --> T2["dataset-create guard/dry-run/test save"]
  T --> T3["wide-table-*-test"]

  TD --> D1
  TD --> D3
  TD --> D4

  R --> R1["current-user-data-permission 等旧入口"]
```

## 6 个主任务域

| 任务域 | 先看哪个文档 | 主入口 |
| --- | --- | --- |
| 数据资产发现 | [szdata-command-landscape.md](./szdata-command-landscape.md#数据资产发现) | `table` / `table-search` |
| 任务、需求、子任务 | [szdata-command-landscape.md](./szdata-command-landscape.md#任务需求子任务) | `task-sql` / `demand-list` / `demand-detail` / `subtask-*` |
| 权限与主体诊断 | [szdata-command-landscape.md](./szdata-command-landscape.md#权限与主体诊断) | `table-permission-mine` / `table-permission-topic` / `table-permission-role` |
| 数据集读回与测试配置 | [szdata-command-landscape.md](./szdata-command-landscape.md#数据集读回与测试配置) | `dataset-config` |
| 宽表管理 | [szdata-command-landscape.md](./szdata-command-landscape.md#宽表管理) | `widetable` / `widetable-detail` |
| 支撑入口 | [szdata-command-landscape.md](./szdata-command-landscape.md#支撑入口) | `login` / `szdata_detail portal-help` / `szdatatest_detail portal-help` |

## 权限快速判断

```mermaid
flowchart TD
  P["用户问：有没有权限？"] --> B{"主体是谁？"}
  B -->|当前登录用户| M["table-permission-mine --table db.table"]
  B -->|调度主题| T["table-permission-topic --topic TOPIC --table db.table"]
  B -->|角色| R["table-permission-role --role-id ROLE_ID --table db.table"]
  B -->|没说清| C["先追问主体，不猜"]

  M --> V["读 status / matchedBy / validity"]
  T --> V2["读 conclusion / matchedBy / source / validity"]
  R --> V3["读 conclusion / matchedBy / source"]
```

旧入口 `current-user-data-permission`、`my-permission-base`、`my-permission-data`、`my-permission-function`、`my-permission-report`、`role-data-permission`、`role-summary`、`scheduling-topic-table-check`、`table-permission-check` 不再作为 agent 工作流入口。

## 子任务路由

```mermaid
flowchart TD
  D["已知需求"] --> R["demand-detail"]
  R --> L["demand-subtask-list"]
  L --> G{"要写哪类子任务？"}
  G -->|采集新增| GC["subtask-gather-create"]
  G -->|采集修改| GU["demand-subtask-detail -> subtask-gather-update"]
  G -->|建模类新增| MC["subtask-modeling-create"]
  GC --> V["dry-run -> szdatatest 验证 -> 用户授权 -> 回读"]
  GU --> V
  MC --> V
```

## 文档优先级

1. 全局归属和选择规则：[szdata-command-landscape.md](./szdata-command-landscape.md)
2. 日常入口指南：[szdata.md](./szdata.md)
3. 低频 detail router：[szdata-detail.md](./szdata-detail.md)
4. 写操作和复杂流程：[szdata-operations/README.md](./szdata-operations/README.md)
5. live adapter 本地地图：`C:\Users\13246\.opencli\clis\szdata\COMMANDS.md` 和 `C:\Users\13246\.opencli\clis\szdatatest\COMMANDS.md`
6. 四入口一致性审计：`node C:\Users\13246\.opencli\shared\szdata-core\audit-surfaces.mjs --plain`
