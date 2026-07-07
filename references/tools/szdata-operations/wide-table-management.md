# 宽表管理逆向工程说明

父文档：[README.md](./README.md) / [szdata.md](../szdata.md)

更新时间026-07-04。本文记录数综平台宽表管理和数据`usageType=3/5` 宽表分支的已验证事实、CLI 用法、样本和风险边界。目标是让下agent 可以先读本文，再直接OpenCLI 接手调查
## 环境红线

- `szdata` = 生产 `data.gf.com.cn`。本次宽数据集链路交付只允许查询和只读核验；`szdata` namespace 内历史上存在其他生产写类 adapter，不能把“本次只读误解为“整namespace 无写能力”- `szdatatest` = 测试 `datatest.gf.com.cn`，任何保存预览生成升级下线删除等写动作必须先在这里验证- 本轮没有`szdata` 做任何写入，也没有为宽表/数据集链路开放生产写命令- 本轮没有对测试宽表做保存/生成/升级写入；原因是现有样本多为 `ONLINE` `WAITING_FOR_UPGRADE`，无效保存也可能触发版本或升级副作用。当前验证范围是安全只读链路：宽表列表数据集详情、生成宽表详情
## 本轮证据来源

前端 bundle
```text
tmp/portal-js/dp.71e09ef9.js
tmp/portal-js-prod/dp.6b36573d.js
```

重点模块和关键词
```text
wideTableList
CreateWideTable
wideTableGeneration
wideTableStatus
listWideTableDefinitionOptions
queryWideTableDataSetConfig
indicatorSystemInfo
isIndicatorSystem
sceneType
保存并预生成宽表
升级
```

Help 中心只做定向检索。以下关键词本轮通过 `opencli szdata_detail portal-help --keyword <kw> --size 20 -f json` 查询，均返回空数组：`宽表`、`宽表管理`、`宽表配置`、`生成宽表`、`宽表升级`、`数据集`、`数据集管理`、`保存并预览`、`指标体系`、`不走指标体系`、`实时宽表`、`离线宽表`。因此 Help 仅作为“未命中”证据，最终结论以前端 bundle、接口和样本为准。
## OpenCLI 命令

新增或补强的读命令：

```powershell
# 宽表列表，生产只opencli szdata widetable --keyword <kw> -f json
opencli szdata widetable --eng <wide_table_name> -f json

# 数据集配置详情，SQL、字段indicatorSystemInfo
opencli szdata dataset-config --id <id> --sql-preview 500 --field-preview 20 -f json
opencli szdatatest dataset-config --id <id> --sql-preview 500 --field-preview 20 -f json

# 生成宽表表单详情，读CreateWideTable 背后的真实接opencli szdata widetable-detail --data-set-config-id <id> -f json
opencli szdata widetable-detail --uuid <wideTableUuid> -f json
opencli szdatatest widetable-detail --data-set-config-id <id> -f json

# 枚举、状态权限场景解释，本地规则输出，不调用业务接口
opencli szdata_detail widetable-explain --section scene -f json
opencli szdata_detail widetable-explain --section action --keyword 升级 -f json
opencli szdatatest_detail widetable-explain --section status -f json
```

`dataset-config` 本轮修正点：

- `--usage-type` help 改为真实枚举：`1 持仓转换`、`2 离线指标生成`、`3 离线宽表配置`、`4 实时指标生成`、`5 实时宽表配置`- 详情模式优先`indicatorSystemInfo.isIndicatorSystem` 解析是否走指标体系，避免列表为是”详情误显示为否”- 详情模式增加 `sceneType`、`indicatorSystemInfoJson`、场景专属字段`fieldCount`、`fieldPreview`、`--debug-raw/--raw` 调试输出
写入 guard
```powershell
# 只读自检：确dataset-create usageType=3/5 + --save 会被本地 guard 阻断
opencli szdatatest dataset-create-guard-check -f json

# 实际阻断验收：该命令应失败，且失败发生在取字保存之前
opencli szdatatest dataset-create --name guard_check --usage-type 3 --save -f json
```

`opencli szdatatest dataset-create --save` 现在`usageType=3/5` 硬阻断宽表配dry-run 仍可用于 payload 研究，但不能通过普数据集保存链路写入测试环境
补充：`dataset-config --save-sql` 只会SQL 导出到本地文件，不是平台写操作；但它仍会改本地文件系统，做纯只读审计时不要使用该参数
`widetable-detail` 读取接口
```text
POST /portal/prod-api/developservice/dataSetConfig/wideTableGeneration/detail
```

可用 `uuid` `id/dataSetConfigId` 查询，输`uuid`、`dataSetConfigId`、`dataSetId`、`type`、`status`、`isEnable`、`isRelatedDataSet`、`dbName`、`engTblName`、`chnTblName`、`horaeTaskId`、`demandList` 等字段这个命令用于确认下游生成宽表页面是否能读到数据，不是只`dataSetConfig/detail`
## 宽表列表页面

前端模块：`WideTableList`
列表接口
```text
POST /developservice/wideTable/list.json
```

筛项
| 筛项 | 请求字段/含义 |
|---|---|
| 宽表英文| `engTblName` |
| 宽表中文| `chnTblName` |
| 与我相关 | `relatedMe`，页面默认是 |
| 宽表库名 | `dbName` |
| 抢术负责人 | `techDirector` |
| 弢发| `developer` |
| 调度ID | `horaeTaskId` |
| 状| `status`，多选，来自 `wideTable/getWideTableStatus.json` |
| 实时类型 | `type`，来`wideTable/getWideTableTypeEnum.json` |
| 是否关联数据| `isRelatedDataSetConfig` |
| 新增日期 | `createTime` 范围 |
| 修改日期 | `updateTime` 范围 |
| 待下线处| `isWaitingOffline=true` |

顶部按钮
- `搜索`：调`wideTable/list.json`- `重置`：清空筛选- `新建`：进`CreateWideTable`- `复制调度任务ID`：复制当前中行任务号
表格核心列：

```text
uuid, chnTblName, engTblName, dbName, dataSetConfigId, dataSetConfigName,
dataSetId, horaeTaskId, status, type, isEnable, isRelatedDataSet,
techDirector, developer, demandList, createTime, updateTime
```

行操作：

| 操作 | 前端方法 | 写风|
|---|---|---|
| 编辑 | `toCreateWideTablePage(row)` | 写链路入|
| 调度配置 | `toDispatchConfigPage(row)` | 写链路入|
| 申请升级 | `applyForUpgrade(row)` | 写链路入口；必须`horaeTaskId` |
| 查看升级 | `viewUpgrade(row)` | 读为主，可进入审批对话框 |
| 运维审批 | `opsAudit(row)` | 写链路入|
| 下线 | `checkUpstreamDownstream(row, "disabled")` `wideTable/deactivate` | |
| 下线确认 | `OfflineConfirmDialog` / 依赖检查 | |
| 删除 | 依赖检查后 `wideTable/delete.json` | |
| 流转记录 | `wideTable/listActionLog` | |

依赖检查接口：

```text
POST /developservice/libraryTableDependency/checkDownstreamForBusiness.json
body: { busiType: 4, busiIdList: [wideTableUuid] }
```

状与可见操作白名单：

| 状| 可见操作白名|
|---|---|
| `DEVELOPING` | 编辑、调度配置申请升级流转记录删|
| `WAITING_FOR_UPGRADE` | 编辑、运维审批查看升级申请升级流转记录删|
| `ONLINE` | 下线、申请升级流转记录编辑下线确|
| `OFFLINE` | 编辑、申请升级流转记录删|
| `AUDITING` | 枚举存在；本轮前端行操作白名单未看到明确分支 |

权限门槛
- `superAdmin`：`userId === "00000000000000000000000000000000"`- 编辑：当前人为技术负责人/弢发或 `superAdmin`- 调度配置：`row.allowEditTask` 且当前人为技术负责人/弢发或 `superAdmin`- 申请升级：必须有 `horaeTaskId`，且当前人为抢术负责人/弢发或 `superAdmin`- 查看升级：技术负责人/弢发运维审批权限`viewUpgrade` 权限`superAdmin`- 运维审批：需`wideTableList.opsAudit`，且不是弢抢术负责人/创建人- 下线：需`wideTableList.offLine` `superAdmin`- 下线确认：`row.isShowConfirmOffline` 且当前人为技术负责人- 删除：`!row.isEnable` 且当前人为技术负责人/弢发或 `superAdmin`
## 数据usageType=3/5 分支

用枚举：

| usageType | 含义 | 是否宽表分支 |
|---|---|---|
| 1 | 持仓转换 | |
| 2 | 离线指标生成 | |
| 3 | 离线宽表配置 | |
| 4 | 实时指标生成 | |
| 5 | 实时宽表配置 | |

`usageType=3/5` 不能按普SQL 数据集保存处理前端保存前会构造：

```js
form + {
  content,
  wideTableUsageTypes: form.wideTableUsageTypes.join(","),
  dataSetConfigFieldColumnList: exportTable.map(...)
}
```

然后`usageType=3/5` 额外塞入
```js
indicatorSystemInfo: {
  isIndicatorSystem,
  sceneType,
  eventField,
  rectifierUuid,
  rectifierTime,
  submittedTo,
  demandLink,
  expectedOfflineTime,
  sceneDescription,
  id,
  dataSetConfigId
}
```

保存接口
```text
POST /developservice/dataSetConfig/edit.json
```

保存后分流：

- 如果当前关联宽表状态是 `ONLINE` 或 `WAITING_FOR_UPGRADE`，非预览保存会继续读取 `wideTableGeneration/detail` 并进入调度升级路径。
- 如果点击 `保存并预览`，保存后会打开 `PreviewModal`，需要 `clusterUuid` 和 SQL；不能只用 `edit.json` 返回 200 判断成功。
- 如果还没有已启用/待升级宽表，普通保存后进入 `CreateWideTable`。

SQL/字段规则：

- SQL 为空不能获取输出列。
- usageType、dataSetType、实时用途的 dataEngine 必须完整。
- 修改 SQL 后必须重新 `获取输出列`，否则前端提示保存的仍是旧字段。
- 保存前会做 SQL 权限/语法检查，场景为 `CHECK_SCENE_TYPE.DATASET_MANAGE`。
- 输出字段必须与 SQL 字段一致。
- 分区字段必须排在字段列表最后。
- 字段备注 `fieldAlias` UTF-8 长度不能超过 100 bytes。
- usageType=3/5 的 `NUMBER` 字段必须包含 `dataPrecision` 和 `dataLength`。
## 不走指标体系

前端只确1 7，不要硬编码场景 8
| sceneType | 场景 | 额外必填字段 |
|---|---|---|
| 1 | 宽表数据全部是主数据、模型层的基本属| 无额外字|
| 2 | 明细数据、订单数| `eventField` |
| 3 | 紧需求，但开发流程长，可先不走指| `rectifierUuid`、`rectifierTime`；会`rectifierRemainingAmount.json` |
| 4 | 监管报类 | `submittedTo` |
| 5 | 指标跑数时间非日终或早于指标体系，指标时效不能满足要| 无额外字|
| 6 | 宽表扢涉及指标维度是四维及四维以上 | 无额外字|
| 7 | 临时活动场景 | `sceneDescription`、`expectedOfflineTime` |

共同规则
- `isIndicatorSystem=false` `usageType in [3,5]` 时，`sceneType` 必填- 页面还展`demandLink`，用于需Jira 链接- 场景 7 `expectedOfflineTime` 是预计下线时间；测试样本 `id=1678` 读到 `2026-02-08 00:00:00`
## CreateWideTable 生成宽表页面

前端模块：`CreateWideTable`
核心接口
```text
POST /developservice/dataSetConfig/wideTableGeneration/detail
POST /developservice/dataSetConfig/wideTableGeneration/edit
POST /developservice/dataSetConfig/queryWideTableDataSetConfig
POST /developservice/dataSetConfig/listWideTableDefinitionOptions
POST /developservice/wideTable/getUpgradeSchedulingConfig.json
POST /developservice/wideTable/applyUpgrade.json
POST /developservice/horaeUpgradeApply/getWideTableSql
```

2026-07-04 test-environment verification addendum:

- Historical config-save probe `opencli szdatatest wide-table-config-save-test` is archived and is not an active command.
- The archived probe cloned historical sample `1718` into test dataset config `1719`: usageType 3, no indicator system, sceneType 5, `wideTableUsageTypes=2`, 19 fields, SQL length 796.
- `opencli szdatatest wide-table-generate-test` is a dedicated test-only CreateWideTable command. It defaults to dry-run and requires the same confirmation string.
- Executing generation for dataSetConfig `1719` called `wideTableGeneration/edit` and read back UUID `93317f49d8d0d5b40e8f1c156995bff8`, status `DEVELOPING`, table `dm_dasa.codex_wt_probe_1719_20260704111925`.
- Read-back succeeded through `widetable-detail --data-set-config-id 1719`, `widetable-detail --uuid 93317f49d8d0d5b40e8f1c156995bff8`, `dataset-config --id 1719`, and `widetable --eng codex_wt_probe_1719_20260704111925`.
- `opencli szdatatest wide-table-preview-test` is a dedicated test-only 保存并预command. It defaults to dry-run and requires the same confirmation string.
- Executing preview created disposable dataSetConfig `1720` with minimal SQL `select 1 as codex_preview_probe`, then used the same PreviewModal `diySql` websocket flow and `/portalservice/userSql/queryExecuteHistoryLog.json` read-back. Result logId `37226341` returned one column `codex_preview_probe` and one row.
- `dataset-config --id 1720` read back usageType 3, no indicator system, sceneType 5, `wideTableUsageTypes=2`, SQL length 31, one NUMBER field. `widetable-detail --data-set-config-id 1720` returned an empty shell, so 保存并预did not generate a wide-table definition.
- This validates the test-only "save config, then preview" path and the "save config, then generate wide table" path for disposable samples. It does not validate upgrade, offline, delete, permit-upgrade, or any production write path.

表单字段
| 字段 | 规则 |
|---|---|
| `type` | 宽表实时类型，`REAL_TIME` `OFFLINE`；usageType=3 锁定离线，usageType=5 锁定实时 |
| `isRelatedDataSet` | 离线宽表是否基于数据集；已启用时禁用 |
| `reasonTypeList` | 离线且不基于数据集时必填，原因包spark 上限、SQL/字段过多、循环辑 |
| `demandList` | 关联霢求，必填 |
| `dataSetConfigId` | 基于数据集时必填 |
| `chnTblName` | 宽表中文|
| `dbName` | 宽表库名，默`dm_` 前缀 |
| `engTblName` | 宽表英文名；usageType=5 默认后缀 `_rt` |
| `techDirector/developer` | 不基于数据集时必|

保存生成宽表
- 从数据集管理跳转时，payload 使用 `{id: routeQuery.id, dataSetId, dataSetConfigId: routeQuery.id} + form`- 从宽表管理列表跳转时，payload 使用 `form + {id: form.dataSetConfigId, dataSetId: getDatasetId()}`- `demandList` 会被删除，改`demandUuidList`- 调用 `dataSetConfig/wideTableGeneration/edit`- 若已`horaeTaskId` 且只改需求，保存后不强制进入调度- 若已启用/待升级且改了表名/库名/中文名，会走 `forceUpdateDispatchInfo`，读取升级调度配置必要时`horaeUpgradeApply/getWideTableSql` 重新生成宽表 SQL，再 `wideTable/applyUpgrade.json`
## 样本核验

生产 `szdata` 只读样本
| id | usageType | 指标体系 | 场景 | 宽表 | 任务 | 读到的状|
|---|---:|---|---|---|---|---|
| 20159 | 3 | | 1 | `dm_om_test.index_org_trade_day_s` | 240068 | `DEVELOPING` |
| 20204 | 3 | | 6 | `asset_fund_share_recon_month` | 240448 | `DEVELOPING` |
| 20054 | 3 | | - | `wt_acct_open_referrer_trace_dtl` | 239302 | `DEVELOPING` |
| 20060 | 5 | | - | `ust_csdc_holder_info_rt` | 239350 | `DEVELOPING` |

测试 `szdatatest` 只读样本
| id | usageType | 指标体系 | 场景 | 宽表 | 任务 | 读到的状|
|---|---:|---|---|---|---|---|
| 1716 | 3 | | 1 | `dm_dasa.dasdsad` | 34403 | `WAITING_FOR_UPGRADE` |
| 1714 | 3 | | - | `wt_ecom_fin_lvl_expense_detail` | 34306 | `WAITING_FOR_UPGRADE` |
| 1678 | 5 | | 7 | `xqz_test0202_rt` | 33379 | `ONLINE` |
| 1664 | 5 | | - | `zxp_sr_view_test` | 33147 | `WAITING_FOR_UPGRADE` |

样本结论
- `dataset-config` 列表能按 `usageType` `isIndicatorSystem` 过滤- `dataset-config --id` 默认SQL 长度、字段预览和 `indicatorSystemInfo`；SQL 正文霢要显`--sql-preview <n>` `--save-sql`- `widetable-detail --data-set-config-id` 能读 CreateWideTable 下游详情，确认页面可以拿到宽UUID、库名表名需求任务号- adapter 会把详情中的走指标体系样本误显示为否”，原因是详情里指标体系字段主要`indicatorSystemInfo`；本轮已修正
## 下一agent 操作路径

只读调查
```powershell
opencli szdata widetable --keyword <关键 -f json
opencli szdata dataset-config --id <dataSetConfigId> --sql-preview 500 --field-preview 20 -f json
opencli szdata widetable-detail --data-set-config-id <dataSetConfigId> -f json
opencli szdata_detail widetable-explain --section status -f json
```

不走指标体系样本分析
```powershell
opencli szdata dataset-config --usage-type 3 --indicator-system-filter 0 --size 5 -f json
opencli szdata dataset-config --usage-type 5 --indicator-system-filter 0 --size 5 -f json
opencli szdatatest dataset-config --usage-type 3 --indicator-system-filter 0 --size 5 -f json
opencli szdatatest dataset-config --usage-type 5 --indicator-system-filter 0 --size 5 -f json
```

写链路前置门禁：

1. 先用 `szdatatest` 找一个用户明确允许修改的测试样本或新建样本2. 先抓浏览器真实请求，确认 `dataSetConfig/edit.json`、`wideTableGeneration/edit`、预览接口和调度/升级接口 payload3. dry-run 输出 payload，确`indicatorSystemInfo`、字段精度分区字段需求库表名、任务号4. 只在 `szdatatest` 执行保存/预览/生成5. 保存后必须用 `dataset-config --id` `widetable-detail --data-set-config-id` 复查，下游页面能读到才算验证通过6. 生产 `szdata` 写入仍需用户单独明确授权
## 未验证和风险

- 已在 `szdatatest` 用专用命令执usageType=3 保存`保存并预览`：测试配`1720`，PreviewModal 同源 websocket 预览 logId `37226341` 1 行结果普`dataset-create --save` 仍然硬阻usageType=3/5- `opencli szdatatest dataset-create --save` 已对 usageType=3/5 加硬阻断；后续需要专用宽表写命令时，必须另设明确授权语义并先在测试环境验证预生成链路- 已在 `szdatatest` 用专用命令执`wideTableGeneration/edit`：测试配`1719` 生成 UUID `93317f49d8d0d5b40e8f1c156995bff8`，状`DEVELOPING`。仍未执`applyUpgrade`、`deactivate`、`delete`、`permitUpgrade`- `AUDITING` 状枚举存在，但本轮未在行操作白名单中看到明确分支，需要遇到实际样本再核验- `wideTableUsageTypes` 当前字典已确`1 自助分析`、`2 其他`；默认常见为 `[2]`。择自助分析的后Doris/自助分析链路仍未做写验证- 预览链路已用测试集群验证websocket 执行结果；后续若换真实业SQL，仍霢单独评估 SQL 权限、运行成本和结果行数- 测试样本多处`ONLINE`/`WAITING_FOR_UPGRADE`，对其执行无变化保存”也可能产生版本、更新时间或升级副作用；不要未经授权拿现有测试样本做写验证## 2026-07-04 addendum: wide-table list, action log, and schedule detail

This addendum records the current verified behavior from local Wiki notes, frontend bundle slices, the provided screenshots, and live adapter readback. Production `szdata` checks in this section were read-only. Test `szdatatest` checks were also read-only.

### Wide-table list

The wide-table management list calls:

```text
POST /developservice/wideTable/list.json
```

Safe read commands:

```powershell
opencli szdata widetable --keyword <name> -f json
opencli szdata widetable --eng <engTblName> -f json
opencli szdata widetable --task-id <horaeTaskId> -f json
opencli szdatatest widetable --task-id <horaeTaskId> -f json
```

The list row is the handoff point for later UI flows. Important fields are `uuid`, `dataSetConfigId`, `dataSetConfigName`, `dataSetId`, `chnTblName`, `engTblName`, `dbName`, `horaeTaskId`, `status`, `type`, `isEnable`, `isRelatedDataSet`, `techDirector`, `developer`, and `demandList`.

### Edit A Specific Wide Table

The row action `编辑` opens `CreateWideTable`; it is not the ordinary dataset SQL edit dialog. The route carries `id=dataSetConfigId`, `uuid=wideTableUuid`, `name=dataSetConfigName`, `dataSetId`, `horaeTaskId`, and `usageType = REAL_TIME ? 5 : 3`.

Read detail endpoint:

```text
POST /developservice/dataSetConfig/wideTableGeneration/detail
```

Safe read commands:

```powershell
opencli szdata widetable-detail --data-set-config-id <id> -f json
opencli szdata widetable-detail --uuid <wideTableUuid> -f json
opencli szdatatest widetable-detail --data-set-config-id <id> -f json
```

Save/generate endpoint remains a write path:

```text
POST /developservice/dataSetConfig/wideTableGeneration/edit
```

Do not execute that endpoint in production. Test generation is covered only by `opencli szdatatest wide-table-generate-test`, which defaults to dry-run and requires `--execute --confirm-test-write YES_TEST_WRITE`.

### Click Task ID / Configure Schedule

Clicking `horaeTaskId` in the wide-table list opens `DispatchTaskConfig`. The ordinary task-ID detail branch calls:

```text
POST /developservice/schedule/getScheduleDetailTimeFormatted.json
body: { schedulingId: <horaeTaskId> }
```

Safe read commands:

```powershell
opencli szdata_detail widetable-schedule-detail --task-id <horaeTaskId> --wide-table-uuid <uuid> --sql-preview 120 -f json
opencli szdatatest_detail widetable-schedule-detail --task-id <horaeTaskId> --wide-table-uuid <uuid> --sql-preview 120 -f json
```

The command reads DispatchTaskConfig state and summarizes task name, task type, topic, cycle, target database/table, insert mode, and SQL snippets. It does not save schedule configuration and does not prove a task instance ran successfully.

The row action `调度配置` is a different entry from simply clicking the task id. When `allowEdit=true`, the frontend first reads:

```text
POST /developservice/wideTable/getLocalSchedulingConfig.json
body: { wideTableUuid: <uuid> }
```

Safe read command:

```powershell
opencli szdata_detail widetable-schedule-config --uuid <wideTableUuid> --mode local --sql-preview 120 -f json
opencli szdatatest_detail widetable-schedule-config --uuid <wideTableUuid> --mode local --sql-preview 120 -f json
```

If the user later saves from this page, the write endpoint is:

```text
POST /developservice/wideTable/saveOrUpdateLocalSchedule.json
```

That save endpoint remains unvalidated and is not opened by the read command.

Verified read-only samples:

```powershell
opencli szdata_detail widetable-schedule-detail --task-id 239995 --wide-table-uuid d1635793ca55332a3854308be6c2d0c1 --sql-preview 60 -f json
opencli szdatatest_detail widetable-schedule-detail --task-id 34403 --wide-table-uuid 9a9366b09957526aa53721b849e1e158 --sql-preview 60 -f json
```

Generated-but-not-scheduled sample:

```powershell
opencli szdatatest widetable-detail --uuid 93317f49d8d0d5b40e8f1c156995bff8 -f json
opencli szdatatest_detail widetable-schedule-config --uuid 93317f49d8d0d5b40e8f1c156995bff8 --mode local --sql-preview 80 -f json
```

This test wide table was generated and is `DEVELOPING`, but it has no `horaeTaskId`; local schedule config readback returned an empty shell. Therefore `生成宽表` does not by itself prove a schedule task exists or that DispatchTaskConfig has populated schedule fields.

### After Generate Wide Table

`生成宽表` and `配置调度` are separate lifecycle actions:

1. A saved usageType `3` or `5` dataset config enters `CreateWideTable`.
2. `wideTableGeneration/edit` creates or updates the wide-table definition.
3. Read back with `widetable-detail --data-set-config-id`, `widetable-detail --uuid`, and `widetable --eng`.
4. If no `horaeTaskId` exists yet, schedule readback may be an empty shell; the schedule has not been configured yet.
5. Schedule configuration is handled through `DispatchTaskConfig`; read existing task state with `widetable-schedule-detail` or entry config with `widetable-schedule-config`.

Saving schedule configuration is still a write path and is not opened by these read commands.

### Apply Upgrade

The row action `申请升级` first navigates to `DispatchTaskConfig` with `isCommit=true`; it is not a direct list-page POST. Later submit may call write endpoints such as:

Before submit, the frontend reads upgrade schedule config:

```text
POST /developservice/wideTable/getUpgradeSchedulingConfig.json
body: { wideTableUuid: <uuid> }
```

Safe read command:

```powershell
opencli szdata_detail widetable-schedule-config --uuid <wideTableUuid> --mode upgrade --sql-preview 120 -f json
opencli szdatatest_detail widetable-schedule-config --uuid <wideTableUuid> --mode upgrade --sql-preview 120 -f json
```

```text
POST /developservice/wideTable/applyUpgrade.json
POST /developservice/horaeUpgradeApply/commitUpgradeApply.json
```

Those write paths were not executed here and must not be hidden behind explain/detail commands.

### Action Log

The row action `流转记录` calls:

```text
POST /developservice/wideTable/listActionLog
body: { uuid: <wideTableUuid> }
```

Safe read commands:

```powershell
opencli szdata_detail widetable-action-log --uuid <wideTableUuid> --size 20 -f json
opencli szdatatest_detail widetable-action-log --uuid <wideTableUuid> --size 20 -f json
```

Verified read-only samples:

```powershell
opencli szdata_detail widetable-action-log --uuid d1635793ca55332a3854308be6c2d0c1 --size 20 -f json
opencli szdatatest_detail widetable-action-log --uuid 9a9366b09957526aa53721b849e1e158 --size 20 -f json
```

The command defaults to bounded rows and hides raw payloads; increase `--size`
only when the investigation needs more history.

The production sample showed these actions: 新建, 调度配置, 申请升级, 编辑, 修改数据 运维审批, 编辑. The test sample showed: 新建, 修改数据 编辑, 调度配置, 申请升级.

### Safety Boundary

- `widetable`, `widetable-detail`, `widetable-action-log`, `widetable-schedule-detail`, and `widetable-explain` are read-only.
- `widetable-schedule-config` is read-only; it reads the schedule config used by `调度配置` or `申请升级` entry modes.
- `widetable-explain` is a local explanation command; it does not call save, preview, generate, upgrade, offline, or delete endpoints.
- `wide-table-preview-test` and `wide-table-generate-test` are test-only write-path commands and default to dry-run.
- `applyUpgrade`, `commitUpgradeApply`, `deactivate`, `delete`, `permitUpgrade`, and schedule save remain unvalidated write paths.
- Any future CLI for schedule save or upgrade submit must be a distinct command, default to dry-run, be validated in `szdatatest`, and require explicit user authorization for the exact action.
## 2026-07-04 addendum: test schedule save

`opencli szdatatest wide-table-schedule-save-test` is the dedicated test-only command for first-time schedule configuration after a wide-table definition has been generated.

Boundary:

- Site is `szdatatest` only.
- Default is dry-run.
- Actual write requires `--execute --confirm-test-write YES_TEST_WRITE`.
- The command refuses to overwrite an existing `horaeTaskId`.
- The command refuses non-`DEVELOPING` wide tables.
- It calls `wideTable/saveOrUpdateLocalSchedule.json` only; it does not call preview, generate, applyUpgrade, deactivate, delete, or permitUpgrade.
- Production `szdata` schedule save is still not opened.

Verified test record:

```powershell
opencli szdatatest wide-table-schedule-save-test --uuid 93317f49d8d0d5b40e8f1c156995bff8 -f json
opencli szdatatest wide-table-schedule-save-test --uuid 93317f49d8d0d5b40e8f1c156995bff8 --execute --confirm-test-write YES_TEST_WRITE -f json
opencli szdatatest widetable-detail --uuid 93317f49d8d0d5b40e8f1c156995bff8 -f json
opencli szdatatest_detail widetable-schedule-detail --task-id 34450 --wide-table-uuid 93317f49d8d0d5b40e8f1c156995bff8 --sql-preview 80 -f json
opencli szdatatest_detail widetable-schedule-config --uuid 93317f49d8d0d5b40e8f1c156995bff8 --mode local --sql-preview 80 -f json
opencli szdatatest_detail widetable-action-log --uuid 93317f49d8d0d5b40e8f1c156995bff8 --size 20 -f json
```

Readback result: table `dm_dasa.codex_wt_probe_1719_20260704111925`, dataSetConfig `1719`, wideTable UUID `93317f49d8d0d5b40e8f1c156995bff8`, task ID `34450`, status `DEVELOPING`, topic `BD_TEST`, cluster `3`, daily cycle `D`, save mode `overwrite`. The action log added `调度配置` at `2026-07-04 22:36:07`.

## 2026-07-04 addendum: DispatchTaskConfig full-point validation

`opencli szdatatest wide-table-schedule-validate` is a read-only validator for the wide-table schedule configuration page. It is not a save command. It reads wide-table detail, local schedule config, schedule detail, and frontend option dictionaries, then reports:

- `currentValues`: compact schedule readback, including owner, topic, self-depend, task type, priority, cycle, retry settings, db/table, insert mode, engine/source, concurrency, partition file count, SQL and pre-SQL presence.
- `optionSummary`: exact dictionary matching for self-depend, cycle unit, priority, task label, task type, and topic.
- `fieldSummary`: required missing points, optional empty points, and mounted-hidden extension points.
- `fieldChecklist`: the full known DispatchTaskConfig point list, including visible fields and hidden/mounted extension fields.

Verified command:

```powershell
opencli szdatatest wide-table-schedule-validate --uuid 93317f49d8d0d5b40e8f1c156995bff8 -f json
```

For `dm_dasa.codex_wt_probe_1719_20260704111925`, required missing points were empty. Optional empty points were `tasklink`, `task_desc`, `targetTableFields`, `finishSql`, `minThreshold`, `failAfterAlarm`, and `countSql`. Mounted-hidden points observed from the live DOM were script parameters, minimum threshold, fail-after-alarm, and row-count SQL; only script parameters had a value in the schedule ext readback.

Live Chrome DOM reconciliation:

- Before a fresh reload, the page could show required-field errors for self-depend, priority, cycle, and task label even though schedule readback already contained values. This is a stale first-time component state, not proof that the saved task payload is invalid.
- After refreshing/reopening the same DispatchTaskConfig route, the page showed no validation errors and populated the visible form points through `horaeTaskId=34450`.
- Therefore schedule validation must combine OpenCLI/API readback with a fresh live UI check when the visible page state matters. Do not rely only on red-box errors, and do not rely only on HTTP/API readback.

Visible fields confirmed after refresh: task name, topic, owner, self-depend, task type, priority, cluster, cycle, date/time, daily data type/parameter, advance-init, step, task label, rerun, run attempts, timeout warnings, dependency, description, db/table, insert mode, insert fields, write concurrency, partition file count, engine, Kyuubi source, Spark config, SQL, pre-SQL, and post-SQL.
