# 写操作：新建 / 配置数据
父目录：[README.md](./README.md) · 路由：[demand-routing.md](./demand-routing.md)

| | |
|---|---|
| CLI | `dataset-config` / `dataset-create-columns` / `dataset-config-dict` / `dataset-create-current-user` / `dataset-create`（测试普SQL|
| 适配| 读已覆盖；✅ `szdatatest dataset-create` 可保存普SQL；✅ usage 3/5 普保存链路已硬阻断；测试环境宽表预览/生成已有专用命令；`dataset-update` 待建 |
| 沉淀程度 | 🔧 普SQL 可半自动；宽表配置只允许 dry-run/只读调查，预生成仍需测试环境继续逆向 |

## 何时
[demand-routing.md](./demand-routing.md)「何时创建数据集」与 **采集子任* 的区别：

| 维度 | 采集子任| 数据|
|---|---|---|
| 交付| 外部入湖采集工作| SQL 模型 / 宽表 / 对客数据产品配置 |
| 典型读命| `demand-subtask-list` | `widetable` `dataset-config` |
| 平台入口 | 霢子任| 数据/ 宽表配置 |

## 离线 Wiki 规范结论

本节来自本地离线 Wiki
- `E:\03_resource\wiki-down\大数据研发组\大数据研发组\3.数据基础\指标体系\指标弢发指引\1. 指标注册指引-207230695.md`
- `E:\03_resource\wiki-down\数据综合管理平台\数据综合管理平台 Home\2.原型与交互设计\2.2 原型方案\指标管理\数综生成持仓指标并与调度系统horae对接-190328358.md`
- `E:\03_resource\wiki-down\数据综合管理平台\数据综合管理平台 Home\2.原型与交互设计\2.2 原型方案\指标管理\数综生成组合指标并对接调度系统horae-193187520.md`
- `E:\03_resource\wiki-down\大数据研发组\大数据研发组\3.数据基础\指标体系\指标弢发指引\6.宽表配置-207230793.md`

### 基础指标数据
入口：`指标管理 数据集配新增`
适用范围
- **基础指标** 需要先配置数据集；衍生指标不走这一步，直接走指标字典和调度配置链路。基础持仓指标、基础组合指标都可走“配置数据集 -> 生成指标 -> 调度配置”。
关键规则
| | 规则 |
|---|---|
| 数据集名| 应与指标中文名保持一致，便于后续查询关联|
| SQL 变量 | 使用 `$` 格式；对接调度时当前主要支持日期变量，如 `${YYYY-MM-DD}`|
| 输出 | SQL 后点击“获取输出列”，再补充字段备注和中文名，最后保存 |
| SQL 别名 | 输出字段以后续别名展示，开发人员应在 SQL 中显式写 `as field_alias` |
| 持仓必需字段 | 至少包含 `hold_id`, `src_tbl`, `busi_date`, `busi_flag`, `trade_flag`, `std_flag`|
| 保存后动| 新数据集回到列表首行；再点生成指标，保存后进入调度配置|
| 已上线指标改 SQL | 先把指标变更到开发中”，再新增数据集导入SQL，并新建调度任务替换原调度|

组合指标指定 SQL 数据集时，时间条件也应使`${YYYY-MM-DD}`，例如：

```sql
select index_val, grp_type_code, grp_val, busi_date, tag_id
from tab
where busi_date = '${YYYY-MM-DD}'
```

调度侧常`sparkIndex`，前SQL 要跟指标类型、目标表和日期分区形式匹配
### 宽表场景不要混淆

宽表弢发不等同于新增一个普通数据集”离Wiki 的宽表配置更偏配置表和调度脚本：

| 配置任务 | 规则 |
|---|---|
| `dm_index_n.wt_template_wide_table_config` | `db_name`、`table_name` 霢与调度配置一致；表名不能与现有表重复|
| `dm_index_n.wt_template_sub_table_config` | 模型层来源填 SQL；组合指组合标签来源填固定日期参数示`busi_date between ':begin_date' and ':end_date'`|
| `dm_index_n.wt_template_wide_table_fields_config` | 字段顺序`num` 控制；分区字段必须排在普通字段之后|
| 调度任务 | 类型`runScript-2.0`，命令参数中 `-s` 库名、`-t` 表名霢与配置表丢致|

因此后续 CLI 不宜把新增指标数据集”和“宽表配置做成同丢个命令；应在霢求分析时先判断目标是指标数据集普SQL 数据集，还是宽表配置
### 是否走指标体=
默认原则：基于模型数据的逻辑加工应过指标体系完成；集市层默认也需要做指标，只有命中豁免场景才可择“不走指标体系
当前有文本证据的“无霢进行指标弢发豁免场景为 1~7
| 场景 | 内容 | 处理要求 |
|---|---|---|
| 1 | 宽表数据全部是主数据、模型层的基本属| 可不走指标体系|
| 2 | 明细数据、订单数| 可不走指标体系|
| 3 | 紧需求，但开发流程长，可先不走指| 霢登记整改时间；每5 个额度，循环额度|
| 4 | 监管报类 | 可不走指标体系|
| 5 | 指标跑数时间非日终或早于指标体系，指标时效不能满足要| 如下3 点中12 点晚上清算后马上加工|
| 6 | 宽表扢涉及指标维度是四维及四维以上 | 可不走指标体系|
| 7 | 临时活动场景 | 如首次发生短周期、治理沟通判定为单一场景，或定期发生但确认无可复用数据|

注意
- 用户口头提到“1~8”，但本次从 Wiki、生产前端 tooltip、生产帮助中心版本页均只找到 1~7 的文本证据；场景 8 暂不应硬编码。
- 场景 3 不是永久豁免，是临时绕行，后续治理会核查登记和整改。
- 前端 tooltip 文案写的是“仅满足以下场景的宽表开发可允许暂不走指标体系”，因此 `--indicator-system false` dry-run 必须要求选择/说明豁免场景。
- 帮助中心可用 `opencli szdata_detail portal-help --keyword <标题关键字>` 搜目录，`--uuid <uuid>` 读详情；它是补充证据，不适合全量扫版本页。

## 调查阶段（当前可用，只读）
```text
widetable --keyword <关键     找宽/ dataSetConfigId
dataset-config --id <id> --sql-preview <n> --field-preview <n>
                                SQL、字段发布配置；避免SQL / fieldList 爆上下文
dataset-config --id <id> --debug-raw
                                raw keys + indicatorSystemInfo 摘要；默认不输出 SQL 正文
table-lineage / table            上游表是否就demand-detail                    霢求是否指向数据集改```

**当前边界**：usage 3/5 不能通过普`dataset-create --save` 写入数据集配置；该路径已硬阻断测试环境已提供专用 dry-run/confirm 写命令验`保存并预览` `生成宽表`，生产写入仍不得执行，除非先`szdatatest` 验证结果并获得用户单独授权
## Portal 字段怎么
字段、下拉项、联动和按钮后续动作的集中说明见 [dataset-detail-fields.md](./dataset-detail-fields.md)。本节保留创保存链路的摘要
| 字段 | 规则/来源 | 获取方式 | 沉淀 |
|---|---|---|---|
| dataSetConfigId | 宽表搜索 | `widetable` | |
| 数据集名| 基础指标场景应与指标中文名一致；其他场景取需宽表语义| 霢求指标字典人工确| 📝 |
| 扢属业| 页面下拉 `businessOwnership/listByKey.json`；为 `{code,name}`，保存字`businessOwnershipCode` `code`；测试详情样本已读回非空| Portal API / `dataset-config-dict --dict businessOwnership` | 📝 |
| 数据集类| 当前页面默认/常见`SQL语句`，前端`dataSetType=1`；`dataSetType=2` 前端分支存在但本轮未读到样本 | Portal 字典 `getDataSetType.json` | 📝 |
| 用| 页面含持仓转捃69离实时宽表配置、离实时指标生成；读命令旧映射不完整 | Portal 字典 `getUsageType.json` | 📝 |
| 抢术负责人 / 弢发| 前端保存 UUID 数组；默认当前登录人 | 用户搜索接口 / 表单默认 | 📝 |
| SQL / 字段映射 | SQL 来自霢求或现有配置；输出列来自“获取输出列”后补备| `dataset-config` / 输出列解| 📝 |
| 输出字段备注 | 必填/强规则；可从 SQL 行尾 `--` 注释或需求字段中文名预填 | SQL 注释、需求文| 📝 |
| 是否走指标体| 默认是；选否必须命中豁免场景并记录说整改时间（场3）详情页读优先看 `indicatorSystemInfo.isIndicatorSystem`，再回顶层字段| Wiki/前端 tooltip/霢求材/ `dataset-config --debug-raw` | 📝 |
| 发布环境 / 版本 | 数据集保存本身未确认；调度阶段另配库主题 | Portal / Horae | 🔲 |
| 关联霢UUID | demand-detail | | |

## 前端/API 证据

页面：`https://datatest.gf.com.cn/portal/#/positionSwitch/config`

已确认接口：

| 动作 | 接口 |
|---|---|
| 列表 | `POST /portal/prod-api/developservice/dataSetConfig/list.json` |
| 详情 | `POST /portal/prod-api/developservice/dataSetConfig/detail`；现有读适配器用 `detail.json` 也可|
| 保存新增/编辑 | `POST /portal/prod-api/developservice/dataSetConfig/edit.json` |
| 用字| `POST /portal/prod-api/developservice/dataSetConfig/getUsageType.json` |
| 数据集类型字| `POST /portal/prod-api/developservice/dataSetConfig/getDataSetType.json` |
| 扢属业务| `POST /portal/prod-api/developservice/dataSetConfig/businessOwnership/listByKey.json` |
| 字段类型字典 | `POST /portal/prod-api/developservice/dataSetConfig/getFieldType.json` |
| 数据引擎字典 | `POST /portal/prod-api/developservice/dataSetConfig/getDataEngineType.json` |
| 指标体系字段关系 | `POST /portal/prod-api/developservice/dataSetConfig/getFieldIndexInfo.json` |
| SQL 字段解析 | `POST /portal/prod-api/developservice/positionSwitch/analysis/sql.json` |
| 指标生成 SQL 校验 | `POST /portal/prod-api/developservice/dataSetConfig/indicatorGenerate/checkDataSetSql.json` |
| SQL 探索鉴权校验 | `POST /portal/prod-api/developservice/sqlExploration/checkSqlWithAuth.json` |
| 帮助中心目录/详情 | `POST /portal/prod-api/portalservice/sysHelp/tree.json` / `detail.json` |

前端保存 payload 关键结构（来`dp.*.js`）：

```text
form + {
  content: editor.getValue(),
  wideTableUsageTypes: form.wideTableUsageTypes.join(","),
  dataSetConfigFieldColumnList: exportTable.map(field => ({
    fieldName,
    fieldAlias,
    dataPrecision,
    dataLength,
    fieldType,
    dataType,
    dimTagList,
    dimIndexId
  }))
}
```

分支规则
- `dataSetType=1`（SQL 语句）保存时删除 `tableName/tableGuid/databaseName`- `dataSetType=2`（表/接口类）保存时删`content`；本`szdata`/`szdatatest` bounded list 都未读到样本，不弢放保存- 用为离线/实时宽表配置（前端判`[3,5].includes(usageType)`）时，会额外组装 `indicatorSystemInfo`- “获取输出列”后如果 SQL 被改动，前端会提醒必须重新获取输出列；CLI 也应做类似校验- 前端会解SQL 中的行尾 `--` 注释，尝试作为字段备注预填
## CLI 实现建议

不要丢次做丢个很大的 `dataset-create`。建议分三步
1. `dataset-create-columns`：输SQL / GUID，只调用输出列解析，返回字段名推断别名备注建议和缺失项2. `dataset-create --dry-run`：组`edit.json` payload，但不提交；校验必填、用途输出列、持仓必霢字段、日期变量3. `dataset-create --submit` / `dataset-update --submit`：明确授权后提交 `edit.json`
第一版建议只支持 `dataSetType=1` SQL 数据集，且默`--dry-run`
### 建议参数

| 参数 | 说明 |
|---|---|
| `--name` | 数据集名称基硢指标场景应等于指标中文名|
| `--sql-file` / `--sql` | SQL 来源，长 SQL 优先文件|
| `--usage-type` | 用，建议允许中文别名并内部解析字典|
| `--business-code` / `--business-keyword` | 扢属业务|
| `--tech-director` / `--developer` | 可，不填用页面默认当前人|
| `--fields-file` | 字段备注/类型补充，只能覆盖获取输出列”解析出的字段行；保存时不能替代解析结果|
| `--indicator-system` | 指标用时是否走指标体系，默认按页用规则|
| `--submit` | 真正提交；无此参数只 dry-run|

## 下一步（实现顺序建议
1. 实现只读 `dataset-create-columns`，先验证 `positionSwitch/analysis/sql.json` 的请响应结构2. 实现 `dataset-create --dry-run`，不提交，只产出 payload 和校验结论3. 用测试环境手工构造一条最SQL 数据集，经过用户确认后再`--submit`4. 再拆 `dataset-update` 和指标生调度配置，避免一个命令承担全链路
## 与其它操
- **前置**：采集子任务完成 / 上游表存在（视场景）
- **易混*：[subtask-gather-create.md](./subtask-gather-create.md) 管采数，本文档管「模SQL 配置
## 待确认问
- [x] 普SQL 数据集新增保存路径已`szdatatest` 验证，记`id=1717`- [x] 用字典当前按 1-5 映射：持仓转捃69离线指标生成离线宽表配置实时指标生成实时宽表配置- [x] `dataset-config` detail `isIndicatorSystem` 映射已修正：优先 `indicatorSystemInfo.isIndicatorSystem`- [x] usage 3 历史回放记录 `id=1718` 已可读回；当adapter 已改为硬阻断 usage 3/5 的普`dataset-create --save`- [x] 2026-07-04: `sqlInfo.json` usage 3/5 宽表场景返回 dataset metadata 空壳，不适合作为“获取输出列”当adapter 已将 SQL 输出列解析统丢切到 `positionSwitch/analysis/sql.json`，并验证 usageType 3/5 `select 1 as codex_preview_probe` 可返回字段名- [ ] `edit.json` 编辑路径是否与新增完全共用字段；新增时哪些字段可省略- [x] 扢属业务择值按 `code` 保存`businessOwnershipCode`，展示为 `name`；测试详情样`1714` 已读回非`businessOwnershipCode`- [ ] `dataSetType=2` GUID 型数据集只有前端分支和输出列解析口径，本轮生测试列表未读到样本，保存链路未验证- [ ] 指标用的 `indicatorSystemInfo` 哪些字段为必填- [ ] 保存数据集本身是否触发审待办，还是只有后续指标生调度触发
## 案例
| 场景 | 读命令结| 平台动作 | 备注 |
|---|---|---|---|
| 普SQL 数据集测试保| `opencli szdatatest dataset-create --save` 返回 `id=1717`，详列表均可读回 | 仅测试环境保| `codex_test_dataset_20260704_01` 不要删除，作为验证证|
| 复刻生产 usage 3 宽表数据集配置（历史记录| 生产 `ETF成份股明细表-h20` `id=20149`、usage 3、不走指标体系场59 字段、分`src_id` 在最| 历史测试记录 `id=1718` 可读回；当前普`dataset-create --save` 已对 usage 3/5 硬阻| `codex_replay_ETF成份股明细表-h20_20260704` 不要删除；list/detail 可读回，`widetable-detail` 尚无生成详情 |
| 离线宽表不走指标体系 | `opencli szdata dataset-config --usage-type 3 --indicator-system-filter 0 --size 3 -f json` 返回 total=5054；样本为场景 1，分区字段在末尾 | 只读调查 | 生产只读，不能据此直接创修改 |
| 实时宽表不走指标体系 | `opencli szdatatest dataset-config --usage-type 5 --indicator-system-filter 0 --size 3 -f json` 返回 total=2；样本为场景 7，`dataEngine=1` | 测试环境只读验证 | 生产 usage 5 本轮只看到走指标体系样本 |
---

## 2026-07-04 verified: dataset UI and szdatatest adapter

Environment rules:
- `szdata` is production `data.gf.com.cn`; use it for query/read-only verification and understanding production state.
- `szdatatest` is test `datatest.gf.com.cn`; every form/save/delete/generate/submit/edit-config operation must be researched and verified here first.
- Any production write on `szdata` requires a passing `szdatatest` validation plus explicit user authorization.

Test adapter status:
- `opencli szdatatest_detail dataset-config-dict`: read test dictionaries. Supports `usageType`, `dataSetType`, `fieldType`, `dataType`, `wideTableUsageType`, `dataEngineType`, `sceneType`, `businessOwnership`, `all`.
- `opencli szdata_detail dataset-config-dict`: read production dictionaries with the same read-only coverage; use only for production-state confirmation.
- `dataset-config-dict` also separates `dataType` and `wideTableUsageType` from the field-type dictionary so agents can query those options directly.
- `opencli szdatatest_detail dataset-sql-versions` / `opencli szdata_detail dataset-sql-versions`: read SQL version list, historical SQL by version number, and current-vs-previous SQL compare. Verified with test `id=1714` and production `id=20054`.
- `opencli szdatatest_detail dataset-templates` / `opencli szdata_detail dataset-templates`: read dataset template list/detail/status. List mode is compact and does not dump template SQL/raw; pass `--id <templateId>` for detail and bounded SQL preview. Template SQL source field is `sqlContent`; referencing dataset lists are detail evidence, not default list output.
- `opencli szdatatest_detail dataset-indicator-sql` / `opencli szdata_detail dataset-indicator-sql`: read-only probe for indicator-system `getTempTableSql` parameters. Defaults to form body because JSON was verified to fail with “用途不能为空 Returns `status=skipped` when stored detail lacks `indicatorTargetCodeList`; it is not a full replacement for the live "选择指标" interaction when `wideTableConfigList` is empty in stored detail.
- `opencli szdatatest dataset-create-columns`: read output columns. SQL parsing now mirrors the UI "获取输出 path through `/developservice/positionSwitch/analysis/sql.json` for usage 1-5; GUID mode still uses `/developservice/dataSetConfig/getColumnByTableGuid.json`.
- `opencli szdatatest dataset-create-current-user`: read current login user through `/portalservice/login/info.json?majorModuleIds=1-2`; used to mirror the UI default tech director/developer.
- `opencli szdatatest dataset-create`: test-environment payload builder. Default is dry-run. `--save` writes only non-wide-table ordinary dataset paths to `szdatatest`; usage 3/5 is hard-blocked. Save mode requires successful `dataset-create-columns` output parsing first; `--fields-json`/`--fields-file` can only override parsed rows and cannot replace "获取输出. No production create command is open.
- For usage 3/5, `dataset-create` supports `--wide-table-usage-types`, `--indicator-system 0|1`, `--scene-type`, and related `indicatorSystemInfo` fields for dry-run payload research only. `--save` is hard-blocked for usage 3/5 and does not run 保存并预/ 生成宽表.
- `opencli szdatatest dataset-create-guard-check`: read-only self-check. It must report usage 3/5 + save as blocked and ordinary usage 1 save as allowed.

Verified guard self-check:
```powershell
opencli szdatatest dataset-create-guard-check -f json
```

Actual negative check, expected to fail before SQL parsing/output-column fetch/save:
```powershell
opencli szdatatest dataset-create --name guard_check --usage-type 3 --save -f json
```

Verified dry-run:
```powershell
opencli szdatatest dataset-create `
  --name codex_dryrun_test `
  --usage-type 1 `
  --sql "select grp_id, grp_name, busi_date from dm_index_n.grp_def where busi_date='2026-07-03'" `
  -f json
```

Result: `status=ready`; current login user is filled into `techDirector/developer`; output columns are `grp_id`, `grp_name`, `busi_date`; `busi_date` is marked `PARTITION_FIELD`.

Verified blocked dry-run:
```powershell
opencli szdatatest dataset-create `
  --name codex_bad_star `
  --usage-type 1 `
  --sql "select * from dm_index_n.grp_def where busi_date='2026-07-03'" `
  -f json
```

Result: `status=errors`; output field name is empty. Rule: do not use `select *` in dataset SQL. List fields explicitly before saving.

List page logic:
- Entry: `/positionSwitch/config`, menu "指标管理 / 数据/ 数据集管.
- `搜索`: query `dataSetConfig/list.json`.
- `重置`: clear filters.
- `高级搜索/收起`: toggles advanced filters. Newer design includes dataset name, usage, related-to-me, indicator object, task id, wide-table name, dataset type, business ownership, create/update dates, tech director, developer, template usage/name, and indicator-system flag.
- `新增`: opens `DataSets.show("add")`; tech director and developer default to the current login user.
- `数据集模板`: enters template management, not dataset save.
- Row `编辑`: owner/admin only; calls `DataSets.show("edit", id)`. Usage 2 can be blocked if the related indicator is auditing deletion/deleted.
- Row `删除`: owner/admin only; blocks when `unitHoraeTaskId`, `tradeHoraeTaskId`, or `generateHoraeTaskId` exists; otherwise confirms and calls `dataSetConfig/delete`.
- Row `持仓转换`: usage 1 only; routes to `/positionSwitch/add?id=<dataSetId>`.
- Row `关联指标`: usage 2/4 only; routes to `CreateIndicator`.
- Row `生成宽表`: usage 3/5 only; routes to `CreateWideTable`.

Add/edit dialog:
- Required base fields: dataset name, usage, tech director, developer.
- Business ownership comes from `businessOwnership/listByKey.json`.
- Dataset type is currently confirmed as `1 SQL语句` in test.
- Usage dict in test: `1 持仓转换`, `2 离线指标生成`, `3 离线宽表配置`, `4 实时指标生成`, `5 实时宽表配置`.
- Data engine is required for realtime indicator generation; confirmed dict value: `1 star_rocks`.
- Dataset template change loads template SQL into the editor.

SQL toolbar:
- `?`: help.
- fullscreen icon: fullscreen the editor container.
- collapse/expand icon: change SQL area height.
- `丢键复制`: copy SQL; warns if SQL is empty.
- `获取输出列`: validates SQL/usage, parses SQL output columns, and populates the output table. For wide-table usage 3/5 it also fetches indicator-system field relations.

Output column rules:
- Field names come from SQL parsing; Chinese name/remark should be completed before save.
- Field types include partition field, model field, combined label, combination, indicator, dimension indicator.
- Data types include string, number, date, datetime.
- Partition fields must be at the end.
- Field alias/remark must be <= 100 UTF-8 bytes.
- NUMBER fields in wide-table usage 3/5 require `dataLength` and `dataPrecision`.

Save buttons:
- Usage 1/2/4: footer is `取消` + `确定`.
- Usage 3/5: footer is `取消` + `保存` + `保存并预览`; preview requires a cluster.
- Save validates SQL auth/syntax, refreshed output columns, alias length, partition order, and wide-table numeric precision.

Version/history buttons:
- `查看历史`: calls `getSqlVersionInfoList` and `getSqlByVersionNo`.
- `与上丢版本对比`: shown only on latest version when at least two versions exist; calls `getSqlVersionCompareInfo` and opens a version-diff tab.
- Switching history while current SQL is dirty prompts whether to save.
- Historical versions hide/disable compare/output-column actions.

Wide-table branch:
- Usage 3/5 defaults `wideTableUsageTypes=[2]` ("其他").
- `是否走指标体系` should default true. Only exemption scenarios 1-7 are confirmed by Wiki/frontend dict; do not hard-code scenario 8.
- Usage 3/5 builds `indicatorSystemInfo` and then continues into preview/create-wide-table/upgrade flow based on wide-table status.
- `dataset-create --save` is hard-blocked for usage 3/5. Use `wide-table-preview-test` and `wide-table-generate-test` for the dedicated `szdatatest` preview/create-wide-table validation paths; both require explicit `--execute --confirm-test-write YES_TEST_WRITE`.
- Dedicated 宽表管理 reverse-engineering, status/action permissions, `CreateWideTable`, and `widetable-detail` usage are now in [wide-table-management.md](./wide-table-management.md).

Core endpoints confirmed from test/prod frontend bundle:
- `dataSetConfig/list.json`
- `dataSetConfig/detail`
- `dataSetConfig/edit.json`
- `dataSetConfig/delete`
- `dataSetConfig/getUsageType.json`
- `dataSetConfig/getDataSetType.json`
- `dataSetConfig/getFieldType.json`
- `dataSetConfig/getDataEngineType.json`
- `dataSetConfig/getSceneType.json`
- `dataSetConfig/businessOwnership/listByKey.json`
- `dataSetConfig/getColumnByTableGuid.json`
- `dataSetConfig/sqlInfo.json`
- `positionSwitch/analysis/sql.json`
- `dataSetConfig/getFieldIndexInfo.json`
- `dataSetConfig/getSqlVersionInfoList`
- `dataSetConfig/getSqlByVersionNo`
- `dataSetConfig/getSqlVersionCompareInfo`
- `dataSetConfig/indicatorGenerate/*`
- `dataSetConfig/wideTableGeneration/*`

Portal help keywords `数据集`, `数据集配置`, `宽表配置`, and `指标生成` returned empty arrays in this round. Local Wiki exports and frontend bundles are the main evidence.

### 2026-07-04 szdatatest save verification

User authorized a test-environment save on 2026-07-04. No production write was performed.

Command:
```powershell
opencli szdatatest dataset-create `
  --name codex_test_dataset_20260704_01 `
  --usage-type 1 `
  --sql "select grp_id, grp_name, busi_date from dm_index_n.grp_def where busi_date='2026-07-03'" `
  --fields-file "E:\02_area\agent-env\Data-Engineering-Workbench\tmp\codex-test-dataset-fields.json" `
  --save `
  -f json
```

Result:
- Save returned `status=saved`, `id=1717`.
- Read-back detail succeeded: `opencli szdatatest dataset-config --id 1717 -f json`.
- Read-back list succeeded: `opencli szdatatest dataset-config --keyword codex_test_dataset_20260704_01 --size 10 -f json`.
- Detail showed SQL content and field list: `分组ID(grp_id); 分组名称(grp_name); 业务日期(busi_date)`.
- `dataSetId=47350c1d4e9bf3dac8d4f82d4bc2fc85`.

Adapter improvement from this verification:
- `dataset-create` now supports `--fields-file` to avoid Windows shell JSON quoting issues with `--fields-json`.
- `dataset-config` usage/scene display maps were corrected to current dataset config dictionaries: usage 1-5 and scene 1-7.

### 2026-07-04 read adapter hardening and samples

Adapter changes:
- `dataset-config --field-preview <n>` limits detail `fieldList`; default is 20, `0` means full output.
- `dataset-config --debug-raw` emits raw keys and an `indicatorSystemInfo` summary while omitting full SQL by default. Combine with `--sql-preview <n>` only when a short SQL excerpt is useful.
- Detail `isIndicatorSystem` now resolves from `indicatorSystemInfo.isIndicatorSystem` first. This fixed the case where list showed `是` but detail showed `否` because the detail payload lacked top-level `isIndicatorSystem`.
- `szdata` and `szdatatest` `dataset-config` were both checked with `node --check`.

Representative read-only commands verified:
```powershell
opencli szdata dataset-config --usage-type 3 --indicator-system-filter 0 --size 3 -f json
opencli szdata dataset-config --usage-type 3 --indicator-system-filter 1 --size 3 -f json
opencli szdatatest dataset-config --usage-type 5 --indicator-system-filter 0 --size 3 -f json
opencli szdata dataset-config --id 20054 --debug-raw --field-preview 3 -f json
opencli szdata dataset-config --id 20159 --field-preview 3 --sql-preview 80 -f json
opencli szdatatest dataset-config --id 1678 --debug-raw --field-preview 3 -f json
```

Sample findings:
- Production usage 1 持仓转换: total=30. Sample detail `id=16820` had 7 output fields and long SQL; no indicator-system branch.
- Production usage 2 离线指标生成: total=9107. Sample detail `id=20201` had 7 output fields and no indicator-system branch.
- Production usage 3 离线宽表配置:
  - `indicator-system-filter 0`: total=5054. Sample details `20159`, `20206`, `20181` all used scene 1; `busi_date` was the last `PARTITION_FIELD`; field counts were 144, 45, and 48.
  - `indicator-system-filter 1`: total=5140. Sample details `20054`, `20205`, `20195` had `indicatorSystemInfo.isIndicatorSystem=true`; scene fields were empty because no exemption scene is needed.
- Production usage 4 实时指标生成: total=12. Sample detail `id=19927` had `dataEngine=1` (`star_rocks`) and 7 output fields.
- Production usage 5 实时宽表配置: total=3; sampled rows were all 走指标体 Sample detail `id=20060` had `dataEngine=1`, `wideTableUsageTypes=2`, and `indicatorSystemInfo.isIndicatorSystem=true`.
- Test usage 5 不走指标体系: total=2. Sample details `1678` and `1427` used `sceneType=7`, `dataEngine=1`, `wideTableUsageTypes=[2]`; `1678` had `sceneDescription=测试下线场景-实时宽表`.

Targeted Portal help search:
- Searched exactly these keywords once: `数据集管理`, `宽表`, `宽表配置`, `生成宽表`, `保存并预览`, `指标体系`, `不走指标体系`, `场景1`, `场景7`, `实时宽表`, `离线宽表`.
- All returned empty arrays in this round. Do not repeatedly scan the whole help site; current evidence remains frontend bundle + local Wiki + read-only config samples.

### 2026-07-04 usage 3 historical save record: ETF成份股明细表-h20

This section is historical evidence only. Current `opencli szdatatest dataset-create --save` hard-blocks usage 3/5, so do not repeat this ordinary save path for wide-table configs.

User requested replaying production `ETF成份股明细表-h20` into test to verify a non-ordinary dataset type. Production was read-only.

Production source:
```powershell
opencli szdata dataset-config --keyword "ETF成份股明细表-h20" --size 10 -f json
opencli szdata dataset-config --id 20149 --debug-raw --field-preview 20 --save-sql tmp\prod_etf_h20.sql -f json
```

Source facts:
- Production `id=20149`, usage 3 `离线宽表配置`.
- `isIndicatorSystem=否`, `sceneType=5`, `wideTableUsageTypes=[2]`.
- SQL length 796; field count 19.
- Last field `src_id` is `PARTITION_FIELD`.
- Historical note: `sqlInfo.json` in `szdatatest` returned empty dataset metadata for this SQL, so the earlier replay used production detail fields as `--fields-file`. Current save logic treats that only as historical evidence; real save mode must have fresh parsed output columns from `positionSwitch/analysis/sql.json`.

Test replay:
```powershell
opencli szdatatest dataset-create `
  --name "codex_replay_ETF成份股明细表-h20_20260704" `
  --usage-type 3 `
  --indicator-system 0 `
  --scene-type 5 `
  --wide-table-usage-types 2 `
  --sql-file tmp\prod_etf_h20.sql `
  --fields-file tmp\prod_etf_h20_fields.json `
  --save `
  -f json
```

Result:
- Historical save returned `status=saved`, `id=1718`; current adapter now blocks this path for usage 3/5.
- Read-back detail succeeded: `opencli szdatatest dataset-config --id 1718 --debug-raw --field-preview 25 --sql-preview 120 -f json`.
- Read-back list succeeded: `opencli szdatatest dataset-config --keyword "codex_replay_ETF成份股明细表-h20_20260704" --size 10 -f json`.
- Detail preserved usage 3, no indicator-system, scene 5, `wideTableUsageTypes=2`, 19 fields, SQL length 796, and partition `src_id`.
- `opencli szdatatest widetable-detail --data-set-config-id 1718 -f json` returned an empty shell, meaning generated wide-table detail/preview has not been created yet.
- Do not delete test record `id=1718`; it is verification evidence.

### 2026-07-04 dedicated wide-table config save and generation test

This section supersedes the older "generated wide-table detail has not been created yet" statement for the cloned test sample only. The ordinary `dataset-create --save` path remains hard-blocked for usage 3/5.

Commands added under `szdatatest` only:
- `wide-table-preview-test`: saves a disposable usageType 3/5 dataset config, then executes the Portal PreviewModal `diySql` websocket preview and reads `/portalservice/userSql/queryExecuteHistoryLog.json`. Default dry-run; write/execute requires `--execute --confirm-test-write YES_TEST_WRITE`.
- `wide-table-generate-test`: calls `dataSetConfig/wideTableGeneration/edit` for a saved usageType 3/5 dataset config. Default dry-run; write requires `--execute --confirm-test-write YES_TEST_WRITE`.

Historical note: `wide-table-config-save-test` was used once as a config-save probe and is now archived, not exposed as an active command.

Verified chain:
```powershell
opencli szdatatest wide-table-preview-test --source-id 1718 --execute --confirm-test-write YES_TEST_WRITE -f json
opencli szdatatest wide-table-generate-test --data-set-config-id 1719 --execute --confirm-test-write YES_TEST_WRITE -f json
opencli szdatatest widetable-detail --data-set-config-id 1719 -f json
opencli szdatatest widetable-detail --uuid 93317f49d8d0d5b40e8f1c156995bff8 -f json
opencli szdatatest widetable --eng codex_wt_probe_1719_20260704111925 -f json
opencli szdatatest dataset-config --id 1720 --debug-raw --field-preview 5 --sql-preview 100 -f json
```

Result:
- Test dataset config `id=1719`, name `codex_widetable_save_probe_1718_20260704111551`.
- Generated wide-table UUID `93317f49d8d0d5b40e8f1c156995bff8`.
- Generated wide table `dm_dasa.codex_wt_probe_1719_20260704111925`, status `DEVELOPING`, isEnable `false`, demand `4477`.
- `dataset-config --id 1719` showed `wideTableStatus=DEVELOPING` and preserved usageType 3, no indicator system, sceneType 5, `wideTableUsageTypes=2`, 19 fields, SQL length 796.
- `widetable --eng codex_wt_probe_1719_20260704111925` returned exactly one row.
- Preview test dataset config `id=1720`, name `codex_widetable_preview_probe_1718_20260704113008`.
- Preview used minimal SQL `select 1 as codex_preview_probe`; result logId `37226341`, one column, one row.
- `dataset-config --id 1720` preserved usageType 3, no indicator system, sceneType 5, `wideTableUsageTypes=2`, one NUMBER field, SQL length 31.
- `widetable-detail --data-set-config-id 1720` returned an empty shell, confirming 保存并预did not create a generated wide-table definition.

Still not covered:
- `wideTable/applyUpgrade.json`, `deactivate`, `delete`, `permitUpgrade`, or any task dispatch mutation.
- Production `szdata` writes.
