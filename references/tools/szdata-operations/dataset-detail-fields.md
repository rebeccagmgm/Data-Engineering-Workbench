# 数据集详情字段与联动

更新时间：2026-07-04。

本文记录数综 `/positionSwitch/config` 数据集详情弹窗里已验证的字段、选项、联动和适配器覆盖情况。`szdata` 是生产，只读；所有保存、预览、生成、删除、升级类验证都先走 `szdatatest`。

## 证据来源

- 截图：数据集详情弹窗，样本为 usageType=3「离线宽表配置」、不走指标体系、豁免场景5。
- 只读字典：`opencli szdatatest_detail dataset-config-dict --dict all -f json`；生产只读侧走 `opencli szdata_detail dataset-config-dict`。
- 只读详情：`opencli szdatatest dataset-config --id 1720 --debug-raw --field-preview 5 --sql-preview 120 -f json`。
- 走指标体系样本：`opencli szdatatest dataset-config --id 1714 --debug-raw --field-preview 20 --sql-preview 120 -f json`，读回 usageType=3、`isIndicatorSystem=true`、非空 `businessOwnershipCode`、`indicatorTargetCodeList`、`wideTableBusiCyc` 和 `wideTableConfigJson`。
- SQL 历史版本：`opencli szdatatest_detail dataset-sql-versions --id 1714`、`--version-no V1`、`--compare` 已验证；生产只读 `szdata dataset-sql-versions --id 20054` 已验证。
- 数据集模板：`opencli szdatatest_detail dataset-templates --size 1`、`--id 58 --sql-preview 120`、`--status-list` 已验证；生产只读 `szdata dataset-templates --size 1` 已验证。列表默认不输出完整 SQL/raw，模板 SQL 证据走 `--id` 详情。
- 走指标体系 SQL 探针：`opencli szdatatest_detail dataset-indicator-sql --id 1714 --sql-preview 180 --show-params -f json` 已验证 endpoint 需要 form 请求体；同一参数用 JSON 请求体会返回“用途不能为空”。样本 `1714` 因存量详情缺少非空 `wideTableConfigList`，只读复现返回空 SQL，这是当前可接受边界。生产样本 `20054` 缺少 `indicatorTargetCodeList` 时命令返回 `status=skipped`，不调用生成接口。
- 前端 bundle 窗口化核对：`tmp/portal-js-prod/dp.6b36573d.js`、`tmp/portal-js/dp.71e09ef9.js`，重点核对数据集详情模板、保存校验、历史版本和接口定义。
- 适配器源码：`C:\Users\13246\.opencli\shared\szdata-core\commands\dataset\*.js`。
- 已沉淀文档：`dataset-create.md`、`wide-table-management.md`、`dataset-configuration-profile.md`。

## 顶部基础字段

| 页面字段 | payload / adapter 字段 | 选项或来源 | 选择后变化 | 注意事项 |
|---|---|---|---|---|
| 数据集名称 | `name` / `--name` | 手填 | 保存后用于列表搜索、详情标题和后续宽表关联展示 | 必填。基础指标场景通常建议与指标中文名一致。 |
| 所属业务 | `businessOwnershipCode` / `--business-code` | `businessOwnership/listByKey.json`，候选行为 `{code,name}`，选择值为 `code` | 写入保存 payload；用于列表筛选和业务归属 | 已确认前端字段和值口径是 `businessOwnershipCode=code`；测试详情样本 `1714` 已读回非空 `businessOwnershipCode`。 |
| 数据集类型 | `dataSetType` | 当前测试字典只确认 `1 SQL语句`；前端仍保留 `2` 表/GUID 分支 | `1` 显示 SQL 编辑器并保存 `content`；`2` 显示库名/表名并通过表 GUID 获取输出列，保存时删除 `content` | `dataset-create` 仅支持 SQL 数据集；`szdata`/`szdatatest` 本轮按 `dataset-type 2 --size 1` 均未读到样本，表/GUID 保存分支未验证。 |
| 用途 | `usageType` / `--usage-type` | 1 持仓转换；2 离线指标生成；3 离线宽表配置；4 实时指标生成；5 实时宽表配置 | 决定是否出现宽表字段、实时数据引擎、保存按钮和后续路由 | 3/5 是宽表分支，普通 `dataset-create --save` 硬阻断；必须用专用宽表预览/生成链路。 |
| 技术负责人 | `techDirector[]` / `--tech-director-uid` | 页面默认当前登录人，可搜索用户 | 控制详情展示、权限判断、后续宽表编辑/调度权限 | 必填，保存 payload 是 userUuid 数组。 |
| 开发者 | `developer[]` / `--developer-uid` | 页面默认当前登录人，可搜索用户 | 控制详情展示、权限判断、后续宽表编辑/调度权限 | 必填，保存 payload 是 userUuid 数组。 |
| 数据集模板 | `templateId` / `--template-id` | `dataset-templates` / `/dataSetTemplate/list.json` | 选择模板会把模板 `sqlContent` 加载到 SQL 编辑器；模板详情会带负责人、状态、SQL 和引用它的数据集列表 | `dataset-create` 只透传 templateId；模板本身的新增/审批/删除不是 dataset save，本轮只开放只读查询。 |

## 用途联动

| usageType | 页面含义 | 主要联动 | 适配器边界 |
|---:|---|---|---|
| 1 | 持仓转换 | 普通 SQL 数据集；底部通常是「取消 / 确定」 | `szdatatest dataset-create --save` 已验证普通 SQL 保存；保存前必须重新获取输出列。 |
| 2 | 离线指标生成 | 指标生成链路；底部通常是「取消 / 确定」 | 按非宽表数据集处理；后续指标生成/调度不是本命令覆盖范围。 |
| 3 | 离线宽表配置 | 显示宽表用途、是否走指标体系、需求链接、豁免场景等；底部有「保存 / 保存并预览」 | 普通 save 被阻断；`wide-table-preview-test` 和 `wide-table-generate-test` 是测试环境专用链路。 |
| 4 | 实时指标生成 | 需要数据引擎，当前字典为 `1 StarRocks` | `dataset-create` 默认 realtime 用途未填时给 `dataEngine=1`。 |
| 5 | 实时宽表配置 | 兼具宽表分支和实时数据引擎；CreateWideTable type 为 `REAL_TIME` | 普通 save 被阻断；生产样本少，不要默认走“不走指标体系”。 |

## 宽表字段

| 页面字段 | payload / adapter 字段 | 选项或来源 | 选择后变化 | 注意事项 |
|---|---|---|---|---|
| 宽表用途 | `wideTableUsageTypes` / `--wide-table-usage-types` | `1 自助分析`；`2 其他` | 仅 usage 3/5 展示并写入；前端以逗号字符串保存 | 已确认默认常见值为 `2 其他`。现在 `dataset-config-dict --dict wideTableUsageType` 可单独查询。 |
| 是否走指标体系 | `indicatorSystemInfo.isIndicatorSystem` / `--indicator-system 1|0` | 开关，默认应为是 | 选是：通常不需要 `sceneType`；选否：必须选择豁免场景并写入 `indicatorSystemInfo` | 详情读取必须优先看 `indicatorSystemInfo.isIndicatorSystem`，不能只看顶层字段。 |
| 需求链接/jira | `indicatorSystemInfo.demandLink` / `--demand-link` | 手填 | 记录豁免或宽表需求来源 | 页面展示字段，当前未验证强必填。 |
| 豁免场景 | `indicatorSystemInfo.sceneType` / `--scene-type` | 场景 1-7 | 仅“不走指标体系”时必填；不同场景会要求附加字段 | 不要硬编码场景8；当前证据只有 1-7。 |

## 豁免场景

| 场景 | 页面说明 | 附加字段 | adapter 校验 |
|---:|---|---|---|
| 1 | 宽表数据全部是主数据、模型层的基本属性 | 无额外字段 | 需要 `sceneType`。 |
| 2 | 明细数据、订单数据 | `eventField` | `dataset-create` dry-run/save payload 校验会要求 `eventField`。 |
| 3 | 紧急需求，但开发流程长，可先不走指标 | `rectifierUuid`、`rectifierTime`；前端还会查整改额度 | `dataset-create` 校验会要求整改人和整改时间。 |
| 4 | 监管报送类 | `submittedTo` | `dataset-create` 校验会要求 `submittedTo`。 |
| 5 | 指标跑数时间非日终或早于指标体系，时效性不能满足要求 | 无额外字段 | 测试样本 `1720` 已读回 sceneType=5。 |
| 6 | 宽表所涉及指标维度是四维及四维以上 | 无额外字段 | 需要 `sceneType`。 |
| 7 | 临时活动场景 | `sceneDescription`、`expectedOfflineTime` | `dataset-create` 校验会要求场景说明和预计下线时间。 |

## SQL 和输出字段区

| 页面/表格字段 | payload / adapter 字段 | 选项或来源 | 选择后变化 | 注意事项 |
|---|---|---|---|---|
| SQL 编辑器 | `content` / `--sql`、`--sql-file` | 手填或模板载入 | 修改 SQL 后必须重新「获取输出列」 | 不要用 `select *`；保存模式必须 fresh 解析输出列。 |
| 库名 | `databaseName` | `queryHiveDatabase.json` 远程搜索 | 仅 `dataSetType=2` 展示；驱动表名候选 | 本轮生产和测试 bounded list 查询均未找到 `dataSetType=2` 样本；adapter 只支持只读 GUID 输出列解析，不支持保存。 |
| 表名 | `tableName`、`tableGuid` | 库名下的表远程搜索 | 仅 `dataSetType=2` 展示；选中后写入表名和 GUID | 保存 `dataSetType=2` 时前端删除 `content`，字段来自 `getColumnByTableGuid.json`。 |
| 获取输出列 | `dataset-create-columns` | SQL 走 `positionSwitch/analysis/sql.json`；GUID 走 `getColumnByTableGuid.json` | 填充 `dataSetConfigFieldColumnList` | `--fields-file` 只能覆盖已解析行，不能替代输出列解析。 |
| 字段名 | `fieldName` | 输出列解析 | 字段列表主键 | 不能为空；需与 SQL 输出一致。 |
| 字段备注/中文名 | `fieldAlias` | 输出列注释、SQL 行尾 `--` 注释或人工补充 | 展示字段中文说明 | UTF-8 长度不能超过 100 bytes。 |
| 字段类型 | `fieldType` | `PARTITION_FIELD` 分区字段；`MODEL_FIELD` 模型字段；`COMBINED_LABEL` 组合标签；`COMBINATION` 组合；`INDEX` 指标；`DIM_INDEX` 维度指标 | 影响宽表字段语义和后续单元格控件；`INDEX`/`DIM_INDEX` 会出现指标/维度指标搜索，`INDEX`/`COMBINED_LABEL` 会出现标签/维度多选 | 分区字段必须放在末尾；切换字段类型会清空 `dimIndexId` 和 `dimTagList`。 |
| 数据类型 | `dataType` | `STRING` 字符；`NUMBER` 数值；`DATE` 日期；`DATETIME` 时间 | `NUMBER` 在宽表 3/5 下要求长度和精度 | 现在 `dataset-config-dict --dict dataType` 可单独查询。 |
| 长度 | `dataLength` | 字段表格手填或覆盖文件 | NUMBER 宽表校验项 | usage 3/5 的 NUMBER 不能为空。 |
| 精度 | `dataPrecision` | 字段表格手填或覆盖文件 | NUMBER 宽表校验项 | usage 3/5 的 NUMBER 不能为空。 |
| 指标/维度指标 | `dimIndexId` | `INDEX` 字段类型走 `dataSetConfig/indicator/queryByKeyword.json`；`DIM_INDEX` 走 `indicator/dimIndex/queryByKeyword` | 选中后写入指标或维度指标 ID；`INDEX` 还会触发标签候选加载 | 清空时同步清空 `dimTagList`。 |
| 标签/维度 | `dimTagList` | `INDEX`/`COMBINED_LABEL` 时展示；远程多选，选项以 `tagId/tagName` 或 `tagDimId/tagDimName` 回填 | 保存时转成 `{tagDimId, tagDimName}` 列表；影响指标/组合标签字段关系 | 现有 adapter 透传覆盖值；自动构造仍需要完整选择指标交互链路。 |

## 走指标体系联动

仅 usageType 3/5 且「是否走指标体系」为是时，前端显示「选择指标」组件 `IndicatorGenerateSql`。该组件会影响 SQL 生成、字段关系和宽表配置，不等同于普通手写 SQL。

| 字段/事件 | payload 字段 | 选择后变化 | 注意事项 |
|---|---|---|---|
| 选择指标 | `indicatorTargetCodeList` | 改变可选指标、字段关系和生成 SQL 参数 | 前端通过 `pageWithNoBindIndicatorAndWideTableAndPosition.json`、`queryForWideTableByIndicatorId.json` 等接口取候选。 |
| 指标维度/字段关系 | `indicatorDimIndexList`、`dimTagList`、`dimIndexId` | 影响输出字段中「指标/维度指标/标签」关系 | 字段关系接口为 `getFieldIndexInfo.json`；当前 adapter 尚未自动填充。 |
| 宽表业务周期 | `wideTableBusiCyc` | 传给 SQL 生成配置和详情读回 | 存量详情会从 `wideTableBusiCyc` 读回并传给 `generateSql` 组件。 |
| 组合标签维度 | `combinationTagDimIdList` | 影响组合标签相关 SQL/字段配置 | 详情读回存在该字段；当前仅记录，不自动构造。 |
| 过滤无效客群 | `isFilterInvalidGroupType` | 影响宽表配置 JSON 和指标体系生成逻辑 | 存量详情中可出现该字段，adapter 只读输出在 raw/debug 中可见。 |
| 生成 SQL 配置列表 | `wideTableConfigList`、`wideTableConfigJson` | 保存/读回宽表相关配置 | 当前 `dataset-config` 会摘要展示 `wideTableConfigJson`；完整构造仍需专门逆向。 |

只读样本 `1714` 进一步确认：走指标体系时 `sceneType` 可以为空；`indicatorTargetCodeList` 可直接挂在顶层和 `wideTableConfigJson` 内；`wideTableBusiCyc=MONTH` 时配置内还会出现日期表达式 `${yyyyMM}`；`indicatorDimIndexList` 和字段行 `dimTagList/dimIndexId` 可以为空，不能把它们硬判为必填。

补充边界：`dataset-indicator-sql` 只作为低频走指标体系分支的只读探针。已确认 `getTempTableSql` 要用 form 方式提交，主要参数包括 `usageType`、`indicatorTargetCodeList`、`wideTableBusiCyc`、`wideTableConfigList`、`indicatorDimIndexList`、`combinationTagDimIdList`、`isFilterInvalidGroupType`。但从存量详情读回的 `wideTableConfigJson` 不一定包含可直接生成 SQL 的 `wideTableConfigList`；如果 `indicatorTargetCodeList` 为空，命令直接返回 `status=skipped`。所以当前不把自动构造“选择指标”完整 payload 作为 adapter 必备能力。

## 按钮和后续动作

| 按钮/动作 | 触发 | 成功判定 | 适配器 |
|---|---|---|---|
| 确定 | usage 1/2/4 普通保存 | `edit.json` 保存后 `dataset-config --id` 和列表可读回 | `dataset-create --save` 仅在 `szdatatest`，且不支持 3/5。 |
| 保存 | usage 3/5 保存配置 | 不能只看 HTTP 200；需读回 dataset config，并按状态继续宽表链路 | 普通命令硬阻断；历史探针已归档。 |
| 保存并预览 | usage 3/5 保存后打开 PreviewModal | 需要预览 logId、列、行读回；不生成宽表定义 | `wide-table-preview-test` 已验证测试样本。 |
| 生成宽表 | usage 3/5 后续 CreateWideTable | `widetable-detail --data-set-config-id` / `--uuid` 和 `widetable --eng` 能读回 | `wide-table-generate-test` 已验证测试样本。 |
| 查看历史 | 编辑/详情模式 SQL 区右上角版本下拉 | `getSqlVersionInfoList` 读版本列表，`getSqlByVersionNo` 读历史 SQL；adapter 命令为 `dataset-sql-versions` | 切换历史 SQL 后会影响编辑器展示；修改当前 SQL 后前端提示重新获取输出列。 |
| 与上一版本对比 | 最新版本且至少两个版本时显示 | `getSqlVersionCompareInfo` 返回 `currentSql/lastSql`；adapter 用 `dataset-sql-versions --compare` | 只读对比动作；不是保存。 |
| 编辑/删除/升级/下线 | 存量记录或宽表列表动作 | 必须看下游状态/依赖/权限 | 升级、下线、删除仍未验证，不开放生产写。 |

## 当前知识遗漏

| 项 | 现状 | 建议 |
|---|---|---|
| 指标体系字段关系自动构造 | 已读到走指标体系样本 `1714`，确认 `indicatorTargetCodeList`、`wideTableBusiCyc`、`isFilterInvalidGroupType`、`wideTableConfigJson` 的读回形态；`dataset-indicator-sql` 已确认 `getTempTableSql` 走 form 请求，JSON 会触发“用途不能为空”；字段级控件联动已定位到 `dimIndexId` 和 `dimTagList` | 当前场景低频，暂不追完整 live 选择链路。若后续要自动构造走指标体系 payload，再抓页面“选择指标”交互时 `IndicatorGenerateSql -> getConfigList -> getTempTableSql` 的完整非空 `wideTableConfigList`。 |
| 表/GUID 型数据集 | 前端保留 `dataSetType=2` 库名/表名分支，但当前测试字典只确认 `SQL语句`；`szdata`/`szdatatest` bounded list 均未读到样本 | 不要保存；若后续字典开放，应先只读抓库表搜索和 `getColumnByTableGuid.json` 回包。 |
| 编辑存量数据集 | `edit.json` 可能与新增共用，但哪些字段可省略未完全确认 | 不要直接做生产/存量编辑；先在 `szdatatest` 建 disposable 样本验证。 |
| 审批/待办触发 | 保存数据集本身是否触发审批/待办仍未确认 | 后续遇到业务场景时查流程中心/QC/Horae 下游读回。 |

## 快速命令

```powershell
opencli szdatatest_detail dataset-config-dict --dict all -f json
opencli szdatatest_detail dataset-config-dict --dict wideTableUsageType -f json
opencli szdatatest_detail dataset-config-dict --dict dataType -f json
opencli szdatatest_detail dataset-config-dict --dict businessOwnership --keyword DMS -f json
opencli szdata_detail dataset-config-dict --dict dataType -f json
opencli szdatatest dataset-config --id 1720 --debug-raw --field-preview 5 --sql-preview 120 -f json
opencli szdatatest_detail dataset-sql-versions --id 1714 -f json
opencli szdatatest_detail dataset-sql-versions --id 1714 --version-no V1 --sql-preview 120 -f json
opencli szdatatest_detail dataset-sql-versions --id 1714 --compare --sql-preview 120 -f json
opencli szdatatest_detail dataset-templates --size 1 -f json
opencli szdatatest_detail dataset-templates --id 58 --sql-preview 120 -f json
opencli szdatatest_detail dataset-templates --status-list -f json
opencli szdatatest_detail dataset-indicator-sql --id 1714 --sql-preview 180 --show-params -f json
opencli szdatatest dataset-create-guard-check -f json
opencli szdatatest_detail widetable-explain --section scene -f json
```
