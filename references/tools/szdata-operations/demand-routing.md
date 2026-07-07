# 需求分析到数综动作路由

父目录：[README.md](./README.md)

本文回答：读完需求、做完调查后，什么时候只读，什么时候需要在数综里创建或修改平台记录。

## 总体决策

```text
需求/工单输入
  ├─ 只需要查清表、SQL、血缘、现状
  │    -> 只读命令：table / table-search / task-sql / demand-detail / dataset-config / widetable
  ├─ 需要登记“从外部系统采数入湖”
  │    -> 采集子任务：subtask-gather-create / subtask-gather-update
  ├─ 需要登记“建模类子任务”
  │    -> 建模类子任务：subtask-modeling-create
  └─ 需要配置 SQL 数据集或宽表
       -> 数据集/宽表流程：dataset-create / wide-table-*-test
```

生产写入固定前置：读现状 -> dry-run -> `szdatatest` 验证 -> 用户明确授权 -> `szdata` 执行 -> 回读验证。

## 什么时候建采集子任务

倾向创建：

| 信号 | 说明 |
| --- | --- |
| 需求描述含“采集、接入、入湖、外部文件、接口源表” | 典型外部数据源进入 BDP |
| `demand-detail` 显示采集交付或 outputGather 相关信息 | 以平台字段为准 |
| 已有父需求 UUID，子任务列表里没有对应源表项 | 先用 `demand-subtask-list` 查重 |
| 用户明确要求“在数综建采集子任务” | 直接 dry-run，别先猜 payload |

倾向不创建：

| 信号 | 处理 |
| --- | --- |
| 只是查表现状、对账、排障 | 走 `table` / `task-sql` / `table-lineage` |
| 是宽表或 SQL 模型改造，不涉及新源系统接入 | 走 `dataset-config` / `widetable` / 数据集专题 |
| 父需求已关闭或验收，只是事后分析 | 先问用户是否仍需写平台记录 |
| 源系统、源表、批次口径都不清楚 | 先补齐调查，再 dry-run |

## 什么时候建建模类子任务

倾向创建 `subtask-modeling-create`：

| 信号 | 说明 |
| --- | --- |
| 工作内容是模型表、贴源模型、ODS/模型层加工 | 建模类子任务，不叫 `model` 命令族，统一用 `modeling` |
| 需求要求登记开发工作，但不是外部采集接入 | 先确认父需求和已有子任务 |
| 用户明确说“建模子任务/开发子任务” | 先 dry-run，不直接保存 |

不要把它用于：

- 普通资产发现。
- 查 SQL 证据。
- 数据集或宽表配置保存。

## 写前必须收集的信息

| 信息 | 常用来源 | 用于 |
| --- | --- | --- |
| 父需求 UUID | `demand-list` / 用户提供 | 所有子任务写入锚点 |
| 需求标题、截止日期 | `demand-detail` | taskName、expectedTime |
| 已有子任务列表 | `demand-subtask-list` | 避免重复创建 |
| 单个子任务详情 | `demand-subtask-detail` | 修改前读现状 |
| 源系统名称 | 需求正文 / `subtask-source-system-list` | `subtask-gather-create --source-system` |
| 数据源候选 | `subtask-access-point-list` | 可选 dataSourceId/dbIdentifier |
| 源库表 | 需求正文 / 厂商文档 / 表核验 | `--source-table` 或 `--gather-lines` |
| 批次/口径/备注 | 需求正文 | `--remark` 或每行备注 |

## 读命令与写命令的分工

| 问题 | 命令 |
| --- | --- |
| 需求在哪里、状态是什么 | `demand-list` / `demand-detail` |
| 需求下有哪些子任务 | `demand-subtask-list` |
| 子任务当前源表、数据源、状态是什么 | `demand-subtask-detail` |
| 源系统候选是什么 | `subtask-source-system-list` |
| 源系统下有哪些数据源 | `subtask-access-point-list` |
| 新建采集子任务 | `subtask-gather-create` |
| 修改采集子任务 | `subtask-gather-update` |
| 新建建模类子任务 | `subtask-modeling-create` |

## 仍需谨慎的点

- 子任务写入是生产写入，不因为有 CLI 就自动授权。
- `--save` / `--submit` 前必须确认父需求和目标子任务。
- 多源表采集不要把一段总备注批量套给所有表；每张表要有自己的备注。
- 回读验证以 `demand-subtask-list` / `demand-subtask-detail` 能读到结果为准，不以 API 200 为准。
