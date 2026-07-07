# SZData Bearer 访问调研

更新时间：2026-07-07

## 范围

本次调研面向 `szdata` / `szdatatest` 相关的数综 Portal 底层接口，重点覆盖：

- `https://data.gf.com.cn/portal/metaservice` 相关的元数据、DDL、血缘、样例数据接口。
- 当前已确认的调度详情接口：`/portal/prod-api/developservice/schedule/getScheduleDetailTimeFormatted.json`。
- 调度主题权限、宽表调度、项目空间调度、Quartz 等 schedule 相关接口。

## 保密边界

- 不在本仓库、命令示例、日志或调研文档中保存任何 API key、Bearer token、cookie、`X-Token`。
- Bearer-only 校验脚本只从 `SZDATA_BEARER_TOKEN` 环境变量或隐藏输入读取 token。
- 写入、提交、删除、冻结、授权类接口只登记路径和用途，不发起调用。
- `tmp/` 下的校验结果是临时证据；写回文档前需要先检查是否包含敏感业务内容。

## 底层结论

1. `/portal/prod-api/developservice/schedule/getScheduleDetailTimeFormatted.json` 是当前调度详情底层入口，`schedule-detail` 和 `schedule-dependencies` 都基于这个 Portal 接口；上游依赖从返回体 `tasklink` 解析。
2. 当前活跃的调度详情实现不再走 MCP schedule 接口；`schedule-run-instances` / `schedule-run-logs` 没有验证到 direct Portal endpoint，不能用旧 MCP 结果冒充 Portal 适配器。
3. 现有 `szdata` OpenCLI 适配器主要复用登录态里的 Cookie / `X-Token`。这只能证明 Portal session 路径可用，不能证明单独的 `Authorization: Bearer ...` 可直接访问。
4. 本轮已使用本机已有密钥环境变量做一次 Bearer-only 安全复跑；token 未写入命令、文档、日志或结果文件。
5. 结论：Portal `/portal/prod-api/...` 下的 metaservice、schedule、wide-table、project-space、Quartz 大多数路径对该 Bearer 直连返回 `NO_AUTH`；`/govern/prod-api/metaservice/lineage/*` 两个血缘路径能到业务层，但样例参数返回业务错误；ranger external 路径返回 404，需另核路径。

## 更正说明

本轮早期判断曾把两类入口混在一起：一类是 MCP server 暴露的工具入口，另一类是 Data Portal 原生 `/portal/prod-api/...` 接口。这个混合口径会导致“API key 好像可以访问很多能力”的说法过宽。

用户指出当前 schedule 相关接口已经改为 `getScheduleDetailTimeFormatted.json` 后，重新核对 live adapter 底层实现和 Bearer-only 结果，最终口径修正为：

- MCP 工具可用，只能说明对应 MCP server 的 auth key 可访问 MCP 封装能力。
- Portal 原生接口可用，必须单独用原生 URL 校验，不能从 MCP 结果外推。
- 当前调度详情和调度上游依赖以 Portal 原生 `getScheduleDetailTimeFormatted.json` 为准；这一路径对本轮 Bearer-only 校验返回 `NO_AUTH`。
- 因此，早期“很多都能用 API key 访问”的判断只适用于 MCP server 入口，不能适用于本报告列出的 Portal 原生接口清单。

## 和 MCP API key 的区别

本报告里的 Bearer-only 校验只回答一个问题：把 token 放到 `Authorization: Bearer ...`，直接请求 `https://data.gf.com.cn/portal/prod-api/...` 或 `https://data.gf.com.cn/govern/prod-api/...`，是否会被 Portal/Govern 网关接受。

MCP 暴露的 API key 是另一层：

- MCP 客户端请求的是 `https://mcp-api-inner.gf.com.cn/server/mcp/<appId>/sse` 或 `/mcp`。
- 认证通常是 MCP server 自己的 `Authorization: Bearer <server-key>`，有些本地配置还会额外传 `X-Personal-Token`。
- MCP gateway / MCP server 再代表客户端去调用它封装好的后端能力；后端可能是某个 OpenAPI / 开放服务接口 / 内部服务接口 / 数据库服务，而不一定是 `data.gf.com.cn/portal/prod-api/...` 原生 URL。
- 因此 MCP 的调用链更像：`Client -> MCP gateway/server -> OpenAPI/内部后端 -> MCP tool result`。这个结果不能直接证明同一个 key 可以访问 Portal 原生 URL。
- `TableMetaData` 这类 MCP 的价值不只是返回表信息，也可以作为“实际 API 信息发现层”：它可能返回 API code、API 名称、实际请求路径、SQL 或上下游元信息。这个发现结果应作为端点来源证据，但还需要再分开验证调用入口和认证方式。
- 本机当前 `TableMetaData` MCP 配置使用 `CLAUDE_MCP_TABLEMETADATA_AUTHORIZATION` 作为 MCP `Authorization`，并额外使用 `CLAUDE_MCP_TABLEMETADATA_X_PERSONAL_TOKEN` 作为 `X-Personal-Token`；两者都不应写入文档或日志。

因此，“MCP 工具能查很多东西”和“Portal 原生接口能被同一个 Bearer 直连”不是同一个结论。当前这次测试说明：对原生 Portal 路径来说，大多数仍需要 Portal 登录态 Cookie / `X-Token`；对 MCP 路径来说，应按每个 MCP server 的连接配置使用对应 auth key。

后续如果要把“metadata MCP 拿到的实际 API”也分类，应扩成四列：

| 维度 | 要回答的问题 |
| --- | --- |
| MCP discovery | `TableMetaData` MCP 能不能查到实际 API path / apiCode / SQL / 元信息 |
| MCP auth | 对应 MCP server 的 auth key 能不能调用该 MCP tool |
| Portal native auth | 同一个或另一个 Bearer 能不能直连 `data.gf.com.cn/portal/prod-api/...` |
| Browser session auth | OpenCLI 复用 Cookie / `X-Token` 能不能读回同一结果 |

## Bearer-only 分类口径

| 分类 | 含义 |
| --- | --- |
| `AUTH_PASSED_BUSINESS_ERROR` | Bearer 没被鉴权挡住，请求已到业务接口；但样例参数或业务条件不完整，所以返回业务/参数错误，没有拿到有效数据。 |
| `NO_AUTH` | HTTP 401/403，或响应消息明确表示未登录、认证、鉴权、授权、权限、token 失败。 |
| `UNKNOWN` | 非 200 且不是明显鉴权失败，需要人工复核响应。 |
| `ERROR` | 网络、TLS、超时或脚本层异常。 |
| `NOT_TESTED_WRITE_PATH` | 状态变更接口，按安全边界跳过。 |
| `PENDING_SAFE_TOKEN_RUN` | 已列入清单，但本轮未用明文 token 运行 Bearer-only 校验。 |

## 只读 / 查询路径

| No | 路径 | 用途 | Bearer-only 状态 |
| --- | --- | --- | --- |
| 1 | `/portal/prod-api/metaservice/metadataSearch/searchByEs` | 数据地图搜索 | `NO_AUTH` |
| 2 | `/portal/prod-api/metaservice/metadataSearch/getTableByGuid` | 表详情 | `NO_AUTH` |
| 3 | `/portal/prod-api/metaservice/metadataSearch/getTableDDL` | 表 DDL | `NO_AUTH` |
| 4 | `/portal/prod-api/metaservice/metadataSearch/getHoraeSqlByTaskId` | Horae 任务 SQL | `NO_AUTH` |
| 5 | `/portal/prod-api/metaservice/metaTableSampleData/hive` | Hive 样例数据 | `NO_AUTH` |
| 6 | `/govern/prod-api/metaservice/lineage/getLineageInfo.json` | 表血缘 | `AUTH_PASSED_BUSINESS_ERROR` |
| 7 | `/govern/prod-api/metaservice/lineage/getGuidByApiCode.json` | API code 转 GUID | `AUTH_PASSED_BUSINESS_ERROR` |
| 8 | `/portal/prod-api/metaservice/businessSystem/queryReviewed.json` | 已审核业务系统候选 | `NO_AUTH` |
| 9 | `/portal/prod-api/developservice/schedule/getScheduleDetailTimeFormatted.json` | 调度任务详情 / DispatchTaskConfig 详情 | `NO_AUTH` |
| 10 | `/portal/prod-api/developservice/schedule/getScheduleDetailTimeFormatted.json` | 调度上游依赖，读取返回体 `tasklink` | `NO_AUTH` |
| 11 | `/portal/prod-api/developservice/schedule/getScheduleTopicList.json` | 调度主题字典 | `NO_AUTH` |
| 12 | `/portal/prod-api/developservice/schedule/getScheduleTopicListByUser.json` | 当前用户可选调度主题 | `NO_AUTH` |
| 13 | `/portal/prod-api/developservice/schedule/getScheduleTopicUser.json` | 调度主题对应主题用户 | `NO_AUTH` |
| 14 | `/portal/prod-api/external/execservice/ranger/getUserPoliciesByServiceNameAndUser` | 主题用户基础库表策略 | `UNKNOWN` |
| 15 | `/portal/prod-api/developservice/schedule/getTaskLabelList.json` | 任务标签字典 | `NO_AUTH` |
| 16 | `/portal/prod-api/developservice/schedule/getScheduleTypeList.json` | 任务类型字典 | `NO_AUTH` |
| 17 | `/portal/prod-api/behaviourservice/scheduleThemeApply/page` | 调度主题权限申请列表 | `NO_AUTH` |
| 18 | `/portal/prod-api/behaviourservice/scheduleThemeApply/{applyNo}` | 调度主题权限申请详情 | `NO_AUTH` |
| 19 | `/portal/prod-api/behaviourservice/scheduleThemeApplyRecord/applyRecord` | 调度主题权限申请流转记录 | `NO_AUTH` |
| 20 | `/portal/prod-api/behaviourservice/scheduleThemeApply/isOa` | OA 相关判断 | `NO_AUTH` |
| 21 | `/portal/prod-api/developservice/wideTable/list` | 宽表列表 | `NO_AUTH` |
| 22 | `/portal/prod-api/developservice/dataSetConfig/wideTableGeneration/detail` | 宽表生成详情 | `NO_AUTH` |
| 23 | `/portal/prod-api/developservice/wideTable/getLocalSchedulingConfig.json` | 宽表本地调度配置回显 | `NO_AUTH` |
| 24 | `/portal/prod-api/developservice/wideTable/getUpgradeSchedulingConfig.json` | 宽表升级调度配置回显 | `NO_AUTH` |
| 25 | `/portal/prod-api/developservice/horaeUpgradeApply/getWideTableSql` | 生成宽表调度 SQL | `NO_AUTH` |
| 26 | `/portal/prod-api/developservice/wideTable/getIndicatorTaskIdList.json` | 宽表上游任务 link | `NO_AUTH` |
| 27 | `/portal/prod-api/developservice/wideTable/listActionLog` | 宽表操作日志 | `NO_AUTH` |
| 28 | `/portal/prod-api/developservice/projectSpace/workNode/schedule/listTaskInstance` | 项目空间调度任务实例列表 | `NO_AUTH` |
| 29 | `/portal/prod-api/developservice/projectSpace/workNode/schedule/getTaskConfigRunResult` | 调度配置运行结果 | `NO_AUTH` |
| 30 | `/portal/prod-api/developservice/projectSpace/workNode/schedule/getTask` | 项目空间调度任务配置 | `NO_AUTH` |
| 31 | `/portal/prod-api/developservice/projectSpace/workNode/schedule/getTaskVersionList.json` | 调度任务版本列表 | `NO_AUTH` |
| 32 | `/portal/prod-api/developservice/projectSpace/workNode/schedule/getVersionCompareInfo.json` | 调度任务版本对比 | `NO_AUTH` |
| 33 | `/portal/prod-api/developservice/schedule/waitOfflineTaskPage.json` | 待下线调度任务列表 | `NO_AUTH` |
| 34 | `/portal/prod-api/developservice/schedule/fetchWaitOfflineTaskChangeLog.json` | 待下线任务变更日志 | `NO_AUTH` |
| 35 | `/portal/prod-api/developservice/schedule/getDateAfterNBusinessDays.json` | N 个工作日后的日期 | `NO_AUTH` |
| 36 | `/portal/prod-api/developservice/horaeFailedTask/page.json` | Horae 失败任务列表 | `NO_AUTH` |
| 37 | `/portal/prod-api/graphservice/taskLoopDetection/getAllLinkByStartAndEnd.json` | 任务链路 / 环检测 | `NO_AUTH` |
| 38 | `/portal/prod-api/quartzservice/sysTask` | Quartz 任务 | `NO_AUTH` |
| 39 | `/portal/prod-api/quartzservice/sysTaskLog` | Quartz 任务日志 | `NO_AUTH` |

## 写入 / 状态变更路径

| No | 路径 | 用途 | Bearer-only 状态 |
| --- | --- | --- | --- |
| 40 | `/portal/prod-api/developservice/wideTable/saveOrUpdateLocalSchedule.json` | 保存宽表调度配置 | `NOT_TESTED_WRITE_PATH` |
| 41 | `/portal/prod-api/developservice/horaeUpgradeApply/commitUpgradeApply.json` | 宽表升级提交 | `NOT_TESTED_WRITE_PATH` |
| 42 | `/portal/prod-api/developservice/wideTable/applyUpgrade.json` | 宽表申请升级 | `NOT_TESTED_WRITE_PATH` |
| 43 | `/portal/prod-api/developservice/schedule/waitOfflineTaskSubmit.json` | 待下线任务提交 | `NOT_TESTED_WRITE_PATH` |
| 44 | `/portal/prod-api/developservice/projectSpace/workNode/schedule/freezeTask.json` | 冻结调度任务 | `NOT_TESTED_WRITE_PATH` |
| 45 | `/portal/prod-api/developservice/projectSpace/workNode/schedule/submitOffline.json` | 提交调度下线 | `NOT_TESTED_WRITE_PATH` |
| 46 | `/portal/prod-api/developservice/projectSpace/workNode/schedule/updateConfigRunResult.json` | 更新配置运行结果 | `NOT_TESTED_WRITE_PATH` |
| 47 | `/portal/prod-api/behaviourservice/scheduleThemeApply/batchAdd` | 新增 / 批量新增调度主题权限申请 | `NOT_TESTED_WRITE_PATH` |
| 48 | `/portal/prod-api/behaviourservice/scheduleThemeApply/verify` | 校验调度主题权限申请 | `NOT_TESTED_WRITE_PATH` |
| 49 | `/portal/prod-api/behaviourservice/scheduleThemeApply/update` | 更新 / 审核 / 授权调度主题权限申请 | `NOT_TESTED_WRITE_PATH` |
| 50 | `/portal/prod-api/behaviourservice/scheduleThemeApply/edit` | 编辑调度主题权限申请 | `NOT_TESTED_WRITE_PATH` |
| 51 | `/portal/prod-api/behaviourservice/scheduleThemeApply/updateModeling` | 更新关联建模 | `NOT_TESTED_WRITE_PATH` |
| 52 | `/portal/prod-api/behaviourservice/scheduleThemeRule/create` | 创建调度主题规则 | `NOT_TESTED_WRITE_PATH` |
| 53 | `/portal/prod-api/behaviourservice/scheduleThemeRule/update` | 更新调度主题规则 | `NOT_TESTED_WRITE_PATH` |
| 54 | `/portal/prod-api/behaviourservice/scheduleThemeRule/delete` | 删除调度主题规则 | `NOT_TESTED_WRITE_PATH` |

## 安全复跑方法

推荐直接运行脚本，让脚本隐藏提示输入 Bearer token：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/check-szdata-bearer-access.ps1 -OutputPath tmp/szdata-bearer-access-result.json
```

只查看清单、验证脚本语法，不输入 token：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/check-szdata-bearer-access.ps1 -ListOnly
```

脚本输出 JSON 字段：

| 字段 | 含义 |
| --- | --- |
| `no` | 本文路径编号 |
| `path` | 请求路径 |
| `use` | 用途 |
| `method` | HTTP 方法 |
| `bearerAccess` | Bearer-only 分类 |
| `httpStatus` | HTTP 状态码 |
| `appCode` | 响应 JSON 中的 `code`，如果有 |
| `message` | 响应消息或截断后的错误信息 |

## 本轮验证记录

- 已运行 `scripts/check-szdata-bearer-access.ps1 -ListOnly`，确认脚本可解析并列出 54 个路径。
- 已通过本机已有密钥环境变量运行一次 Bearer-only 校验，结果汇总：`NO_AUTH` 36 个、`AUTH_PASSED_BUSINESS_ERROR` 2 个、`UNKNOWN` 1 个、`NOT_TESTED_WRITE_PATH` 15 个。
- 原始分类结果保存到 `tmp/szdata-bearer-access-result.json`；该文件只含路径、状态码、应用码和截断消息，不含 token。
- 已扫描本调研文档、脚本和 `CHANGELOG.md`，未发现常见中文 mojibake 标记。
- 已核对本机 MCP 配置：`TableMetaData` MCP 走 `mcp-api-inner.gf.com.cn`，使用独立 MCP `Authorization` 和 `X-Personal-Token` 环境变量；这与 Portal 原生 URL Bearer-only 校验分属两套入口。

## 证据来源

- `C:\Users\13246\.opencli\shared\szdata-core\commands\scheduling\schedule-command-utils.js`
- `C:\Users\13246\.opencli\shared\szdata-core\commands\scheduling\schedule-detail.js`
- `C:\Users\13246\.opencli\shared\szdata-core\commands\scheduling\schedule-dependencies.js`
- `C:\Users\13246\.opencli\shared\szdata-core\commands\widetable\widetable-schedule-detail.js`
- `C:\Users\13246\.opencli\shared\szdata-core\portal-shared.mjs`
- `references/tools/szdata.md`
- `references/tools/szdata-command-landscape.md`
