# 写操作：修改采集子任务
父目录：[README.md](./README.md) · 新建：[subtask-gather-create.md](./subtask-gather-create.md)

| | |
| --- | --- |
| CLI | `opencli szdata subtask-gather-update` |
| 读现状 | `opencli szdata_detail demand-subtask-detail` |
| 适配器 | `subtask-gather-update.js` |
| API | `POST developservice/demandSubtask/update.json` |
| 默认行为 | dry-run，不写平台 |

## 为什么单独命名
| 维度 | `subtask-gather-create` | `subtask-gather-update` |
| --- | --- | --- |
| API | `save.json` | `update.json` |
| 锚点 | `--demand-uuid` | `--uuid` |
| 语义 | 从零新建 | detail 后合并补丁 |
| 必填 | 父需求 | 子任务 UUID + 至少一项变更 |

不要把 create/update 合成一个命令，这样容易让 agent 误把“新建”写成“修改”，或在修改时漏传现有 uuid/state/sort。
## 推荐流程

```text
demand-subtask-detail --uuid <SUBTASK_UUID>
  -> 读现状
subtask-gather-update ...
  -> dry-run 预览补丁
subtask-gather-update ... --save
  -> 用户明确授权后保存
demand-subtask-detail --uuid <SUBTASK_UUID>
  -> 回读验证
```

## 常见改法

改单张表备注
```powershell
opencli szdata subtask-gather-update `
  --uuid <SUBTASK_UUID> `
  --source-table HS_USER.ETFCODE `
  --remark "补采字段 cash_ratio_mode,basket_bonus" `
  -f json
```

重写多表及备注：

```powershell
opencli szdata subtask-gather-update `
  --uuid <SUBTASK_UUID> `
  --source-system 零售柜台内存清算系统 `
  --gather-lines "HS_USER.ETFCODE, 备注1
HS_ASSET.ETFCOMPONENT, 备注2" `
  -f json
```

改期望完成日期：

```powershell
opencli szdata subtask-gather-update `
  --uuid <SUBTASK_UUID> `
  --expected-time 2026-08-15 `
  -f json
```

霢要保存时再追`--save`，且必须先得到用户授权
## 字段补丁

| 字段 | CLI | 说明 |
| --- | --- | --- |
| 子任UUID | `--uuid` | 必填 |
| 采集备注 | `--remark` + `--source-table` | 多表时一次只改一张，或用 `--gather-lines` |
| 源库表列| `--gather-lines` / `--gather-info` | 按库表名匹配保留 gather uuid |
| 源系数据| `--source-system` / `--data-source-id` | 可单独改或随 gather 丢起改 |
| 期望完成日期 | `--expected-time` | 可|
| 优先任务| `--priority` / `--task-name` | 可|

更新时会自动带上 detail 里的 `uuid`、`number`、`state`、`subtaskGatherConfig.uuid`、各`gatherInfo.uuid/sort`。已HIVE 表名taskId 不应被清空
## 回读验证

```powershell
opencli szdata_detail demand-subtask-detail --uuid <SUBTASK_UUID> -f json
```

成功标准是详情中目标源表、备注期望完成时间等字段符合预期
