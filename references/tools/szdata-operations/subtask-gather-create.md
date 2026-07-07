# 写操作：新建采集子任
父目录：[README.md](./README.md) · 路由：[demand-routing.md](./demand-routing.md)

| | |
| --- | --- |
| CLI | `opencli szdata subtask-gather-create` |
| 适配| `subtask-gather-create.js` |
| 定位 | 明确授权后，新建“外部源系统采数入湖”类子任|
| 默认行为 | dry-run，不写平|

## 仢么时候用

先看 [demand-routing.md](./demand-routing.md)。典型场景是父需求已经明确，工作内容是从源系源库表采集数据，并且霢要在数综霢求下登记采集子任务
不要用它做：

- 查需求现状用 `demand-detail`- 查子任务现状。用 `demand-subtask-list` / `demand-subtask-detail`- 建模类子任务。用 `subtask-modeling-create`- 数据集或宽表配置。看数据宽表专题
## 推荐流程

```text
demand-detail / demand-subtask-list
  -> 确认父需求查subtask-source-system-list --keyword ...
  -> 搜源系统候subtask-access-point-list --source-system ...
  -> 可，查数据源候subtask-gather-create ...
  -> dry-run
subtask-gather-create ... --save / --submit
  -> 仅在用户明确授权后执demand-subtask-list / demand-subtask-detail
  -> 回读验证
```

## 常用命令

```powershell
opencli szdata subtask-source-system-list --keyword 柜台 --size 10 -f json
opencli szdata subtask-access-point-list --source-system 万得 --keyword wind --size 10 -f json
```

单表 dry-run
```powershell
opencli szdata subtask-gather-create `
  --demand-uuid <UUID> `
  --source-system 万得 `
  --source-table wind.my_table `
  --remark "新增 20:00 批次采集" `
  -f json
```

多表 dry-run
```powershell
opencli szdata subtask-gather-create `
  --demand-uuid <UUID> `
  --source-system 零售柜台内存清算系统 `
  --gather-lines "HS_USER.ETFCODE, 新增 20:00 批次
HS_ASSET.ETFCOMPONENT, 新增 20:00 批次" `
  -f json
```

## 参数规则

| 参数 | 规则 |
| --- | --- |
| `--demand-uuid` | 必填，父霢UUID |
| `--source-system` | 必填，建议先`subtask-source-system-list` 选定 |
| `--source-table` | 单表模式使用 |
| `--gather-lines` | 多表模式使用，每`库表, 备注` |
| `--gather-info` | 多表 JSON 模式，每项包`originalTable` `remark` |
| `--remark` | 单表备注；多表不要用同一备注批量覆盖 |
| `--data-source-id` | 可，来自 `subtask-access-point-list` |
| `--expected-time` | 可，通常来自父需求截止日|

`--source-table` / `--gather-lines` / `--gather-info` 三一
## 备注规范

采集备注是普通文本框，不是结构化字段。建议写清：

- 仢么时间采：批次时点频率- 采什么：字段、范围全增量- 特殊说明：厂商口径补采原因与现有批次关系
创建时不要写 HIVE 目标表名Horae 任务 ID；这些常由采集负责人弢发完成后回填
## 回读验证

保存或提交后，用
```powershell
opencli szdata_detail demand-subtask-list --demand-uuid <UUID> -f json
opencli szdata_detail demand-subtask-detail --uuid <SUBTASK_UUID> -f json
```

成功标准是子任务能被列表和详情读回，不是接口返回 200
