# MCP / OpenAPI 当前接口调研

更新时间：2026-07-07

## 范围

本报告只记录当前现状：当前 MCP 市场能查到什么、tool 配置里实际暴露了哪些 `openapi`、这些接口的用途和认证边界。不讨论旧 MCP 名称、历史快照或旧 CLI parity。

保密边界：本文不保存任何 API key、Bearer token、cookie、`X-Token`、`X-Personal-Token` 实际值，不保存 GUID、完整 DDL、完整 SQL。

## 当前结论

- 当前 MCP 市场列表总数：120 个 server。
- 抽取到 tool-level HTTP 配置：356 条。
- 其中 `/openapi/...` 路径：4 条。
- 当前 `/openapi/...` 全部来自 `TableMetaData` MCP。
- 当前按 `schedule`、`调度`、`sql_dignose`、`sql_diagnose`、`diagnosis`、`诊断`、`horae` 等关键词和 appId 复查，未发现数综调度或 SQL diagnosis MCP server。
- 当前 `诊断` 关键词只命中财富/基金类 MCP，不是数综 schedule 或 SQL diagnosis。
- 当前 356 条 tool HTTP 配置全文检索里，`schedule` / `调度` / `diagnosis` / `dignose` / `诊断` 均无命中；`sql` 只命中 `TableMetaData.getHoraeSqlByHoraeTaskId` 和一个非数综结算类 SQL 查询/脚本工具。
- 当前本机 Codex MCP 配置里可见的数综相关 MCP 只有 `TableMetaData`：URL 形态为 `https://<mcp-gateway>/server/mcp/TableMetaData/sse`，认证值通过环境变量名承载；未发现 `schedule`、`sql_dignose` 或 `sql_diagnose` 的现役 server 配置。
- 用户补充的 `https://data.gf.com.cn/mcp/metadata`、`/mcp/schedule`、`/mcp/sql_dignose` 三个直连 MCP URL 当前可用；它们不来自 MCP 市场公开 detail，但可用 `X-Personal-Token` 完成 MCP `initialize` / `tools/list`。
- 上述直连 MCP URL 只能证明 MCP server 和 MCP tools 可用；标准 MCP `tools/list` 没有暴露 tool-level `httpReq` 或后端 API path。
- 当前只证明 metadata 类 `/openapi/metaservice/personaltoken/internal/...` 可用 `X-Personal-Token` 直连；schedule / sql_dignose 的非 MCP 直连 API 仍未找到。
- `TableMetaData` openapi 后端使用 `X-Personal-Token`。
- 只带 MCP `Authorization` 直接访问这些 openapi 会返回 `401 Unauthorized`。
- Portal 原生 `/portal/prod-api/...` 和 MCP/openapi 不是同一条认证链；当前多数 Portal 原生路径 Bearer-only 为 `NO_AUTH`。

## 为什么 `TableMetaData` 能扒到 openapi

这一路线成功的关键不是“认证更容易”，而是“发现入口完整”。当前 `TableMetaData` 在 MCP 市场 detail 中提供了可枚举的 server/tool 元数据：

1. 有明确现役 `appId`：`TableMetaData`。
2. 有可连接的 MCP URL 形态：`https://<mcp-gateway>/server/mcp/TableMetaData/sse`。
3. 有 `mcpTools` 列表，能看到 tool 名、入参 schema 和用途说明。
4. 每个相关 tool 暴露了 `httpReq`，包括后端 path、method、body keys 和所需 header 名称。
5. `globalToolPlugins` 暴露了认证升级形态：MCP 入口认证进入 server，后端 openapi 由 `X-Personal-Token` 参与调用。

因此可走的证据链是：

```text
MCP market detail
  -> appId / MCP URL shape
  -> tool definitions
  -> tool-level httpReq
  -> /openapi/... backend paths
  -> bounded direct verification with environment variables
```

换句话说，`TableMetaData` 是先有“门牌”和“工具说明书”，再顺着 `httpReq` 找到 openapi。这里的 MCP `Authorization` 和后端 `X-Personal-Token` 是链路上的不同位置；直接访问 openapi 时不能把 MCP `Authorization` 当成 openapi token。

## 为什么 `schedule` / `sql_dignose` 当前扒不到

当前卡点不是“它们认证不同”或“同一 MCP Authorization 不可用”。如果这些能力仍由 MCP 承载，它们很可能也需要先进入对应 MCP server，再由 server 调后端能力。

当前真正缺失的是可发现的现役入口：

- MCP 市场公开列表里没有能定位到数综 schedule / SQL diagnosis 的 server。
- `gf-mcp detail schedule`、`gf-mcp detail sql_dignose`、`gf-mcp detail sql_diagnose` 当前返回空。
- 当前 356 条 tool-level HTTP 配置里没有 schedule / 调度 / diagnosis / dignose / 诊断相关后端配置。
- 本机当前 Codex MCP 配置也没有这些 server 名或 URL 形态。

所以“从 MCP 市场扒”这条路线在它们身上断在发现层，而不是断在认证层。没有现役 `appId`、MCP URL、tool 定义或 `httpReq` 元数据，就不知道该连哪个 server、调用哪个 tool、按什么 schema 传参、后端 path 是什么；认证材料即便同类，也没有可落点的调用对象。

要继续深挖，只能换当前证据来源：现役 appId、MCP URL 形态、本地 MCP 配置、服务端工具配置、网关目录，或实际调用日志。旧会话、旧 MCP 名称、旧 CLI parity 只能作为历史线索，不能当作当前现状证据。

## 用户补充 MCP URL 后的直连探测

用户提供了当前可用的 Data Portal MCP URL 形态：

```json
{
  "data-portals-metadata": "https://data.gf.com.cn/mcp/metadata",
  "data-portals-schedule": "https://data.gf.com.cn/mcp/schedule",
  "data-portals-dignose": "https://data.gf.com.cn/mcp/sql_dignose"
}
```

本轮只从本机环境变量读取 `X-Personal-Token`，未输出或保存 token 值。MCP 协议探测结果如下：

| MCP URL | initialize | serverName | tools/list |
| --- | --- | --- | --- |
| `/mcp/metadata` | HTTP 200 | `mcpservice-metadata` | 6 个 tools |
| `/mcp/schedule` | HTTP 200 | `mcpservice-schedule` | 7 个 tools |
| `/mcp/sql_dignose` | HTTP 200 | `mcpservice-sql_dignose` | 1 个 tool |

可见 tool 清单：

| MCP server | Tool | Input keys |
| --- | --- | --- |
| metadata | `metadata.search_table` | `clusterId`, `dataSourceId`, `dbName`, `tableName` |
| metadata | `metadata.get_table_ddl` | `guid` |
| metadata | `metadata.search_by_es` | `assetName`, `content`, `businessSystemKeywords`, `upstreamSystemKeywords`, `dbNames`, `dbTypes`, `pageNo`, `pageSize` |
| metadata | `metadata.query_assistant_dify` | `question` |
| metadata | `metadata.get_table_by_guid` | `guid` |
| metadata | `metadata.get_table_lineage_info` | `guid`, `status` |
| schedule | `schedule.get_task_dependencies` | `taskId`, `scope` |
| schedule | `schedule.get_task_run_instances` | `taskId`, `beginDate`, `endDate`, `pageNum`, `pageSize` |
| schedule | `schedule.get_task_run_states` | `taskId`, `dateFrom`, `dateTo` |
| schedule | `schedule.get_task_run_logs` | `taskId`, `dataDate` |
| schedule | `schedule.get_owner_failed_instances` | `ownerId`, `dataDate`, `pageNum`, `pageSize` |
| schedule | `metadata.get_horae_sql_by_task_id` | `horaeTaskId` |
| schedule | `schedule.get_schedule_detail` | `schedulingId` |
| sql_dignose | `query.sql_diagnosis` | `sql`, `databaseName`, `clusterUuid`, `executionEngine`, `sign` |

安全调用探测：

| MCP server | Tool | Sample shape | Result |
| --- | --- | --- | --- |
| schedule | `schedule.get_schedule_detail` | invalid task id only | MCP tool reached downstream and returned a not-found business error |
| sql_dignose | `query.sql_diagnosis` | `select 1` only | MCP tool returned valid SQL diagnosis shape |

这说明：用户补充的 URL 可以作为 MCP 工具入口使用，且 `X-Personal-Token` 能让 MCP server 执行 tool。但标准 `tools/list` 和这两个安全 `tools/call` 结果没有暴露 `/openapi/...`、`/portal/prod-api/...` 或其他后端直连 path。

## 非 MCP + X-Personal-Token 直连探测

目标是验证能否绕过 MCP，直接用 `X-Personal-Token` 调后端 API。当前结果：

| Target | Result | Meaning |
| --- | --- | --- |
| `/openapi/metaservice/personaltoken/internal/metadataSearch/listMetaTableInfo` | HTTP 200 / code 0 | metadata openapi 直连成立 |
| `/portal/prod-api/developservice/schedule/getScheduleDetailTimeFormatted.json` | HTTP 401 | Portal 原生 schedule path 不接受仅 `X-Personal-Token` |
| `/portal/prod-api/developservice/projectSpace/workNode/schedule/listTaskInstance` | HTTP 401 | Portal 原生 run-instance path 不接受仅 `X-Personal-Token` |
| `/portal/prod-api/developservice/horaeFailedTask/page.json` | HTTP 401 | Portal 原生 failed-task path 不接受仅 `X-Personal-Token` |
| `/portal/prod-api/developservice/sqlExploration/checkSqlWithAuth.json` | HTTP 401 | Portal 原生 SQL exploration path 不接受仅 `X-Personal-Token` |
| guessed `/openapi/developservice/personaltoken/internal/...` schedule/sql paths | HTTP 401, not opened for personal-token access | 不能靠简单路径替换得到可用直连 API |
| random `/openapi/developservice/personaltoken/internal/...` path | same personal-token-not-open result | `developservice` 命名空间存在，但具体接口未按该 guessed path 开放 |
| random unknown openapi service | HTTP 404 | 用作对照，说明不是所有 openapi path 都返回同一错误 |

因此当前 CLI 改造判断是：

- metadata 能走非 MCP 的 `/openapi/metaservice/personaltoken/internal/...` + `X-Personal-Token`。
- schedule / sql_dignose 目前只能证明 MCP 入口可用，不能证明存在可直连的 `X-Personal-Token` 后端 API。
- 现有 `szdata` direct Portal CLI 路线是浏览器登录态 Cookie / `X-Token`，不是 `X-Personal-Token`。
- 如果 CLI 必须“不走 MCP，只走 direct API + X-Personal-Token”，还需要拿到服务端实际后端 path，或让服务方把 schedule/sql_dignose 对应接口开放成 personaltoken openapi。

## MCP 调用链

当前 `TableMetaData` MCP 的实际链路是：

```text
MCP Client
  -> MCP gateway/server
  -> data.gf.com.cn/openapi/metaservice/personaltoken/internal/metadataSearch/*
  -> MCP tool result
```

这说明 MCP server key 只负责进入 MCP server；后端 openapi 另走 `X-Personal-Token`。

## 当前 openapi 清单

完整前缀：

```text
https://data.gf.com.cn
```

1. `/openapi/metaservice/personaltoken/internal/metadataSearch/listMetaTableInfo`
   用途：按库名、表名查元数据表记录，返回表元数据候选项和 GUID。
   方法：`POST`
   Body：`{ "dbName": "string", "tableName": "string" }`
   认证：`X-Personal-Token`
   本轮验证：HTTP 200 / code 0。

2. `/openapi/metaservice/personaltoken/internal/metadataSearch/getTableDDL`
   用途：按 GUID 查询表 DDL。
   方法：`POST`
   Body：`{ "guid": "string" }`
   认证：`X-Personal-Token`
   本轮验证：HTTP 200 / code 0。

3. `/openapi/metaservice/personaltoken/internal/metadataSearch/getTableByGuid`
   用途：按 GUID 查询表详情，包括表名、注释、分类分级、业务元数据、技术元数据、字段规模、分区、行数、大小等。
   方法：`POST`
   Body：`{ "guid": "string" }`
   认证：`X-Personal-Token`
   本轮验证：HTTP 200 / code 0。

4. `/openapi/metaservice/personaltoken/internal/metadataSearch/getHoraeSqlByTaskId`
   用途：按 Horae 任务 ID 查询任务 SQL。
   方法：`POST`
   Body：`{ "horaeTaskId": "string" }`
   认证：`X-Personal-Token`
   本轮验证：HTTP 200 / code 0。

## 当前 MCP Tool 映射

| MCP server | Tool | 实际路径 | 用途 |
| --- | --- | --- | --- |
| `TableMetaData` | `getGuid` | `/openapi/metaservice/personaltoken/internal/metadataSearch/listMetaTableInfo` | 按库名、表名查 GUID 和表元数据候选项 |
| `TableMetaData` | `getTableDDL` | `/openapi/metaservice/personaltoken/internal/metadataSearch/getTableDDL` | 按 GUID 查 DDL |
| `TableMetaData` | `getTableDetailInfoByGuid` | `/openapi/metaservice/personaltoken/internal/metadataSearch/getTableByGuid` | 按 GUID 查表详情 |
| `TableMetaData` | `getHoraeSqlByHoraeTaskId` | `/openapi/metaservice/personaltoken/internal/metadataSearch/getHoraeSqlByTaskId` | 按 Horae 任务 ID 查 SQL |

## 当前认证分类

| 入口 | 认证方式 | 当前结果 | 说明 |
| --- | --- | --- | --- |
| MCP server | MCP `Authorization` | 可进入 MCP server | 只证明 MCP 入口可用 |
| `TableMetaData` openapi | `X-Personal-Token` | 可直连，HTTP 200 / code 0 | 当前实际可用 openapi 后端 |
| `TableMetaData` openapi | 仅 MCP `Authorization` | `401 Unauthorized` | MCP key 不能直接当 openapi token |
| 多数 `/portal/prod-api/...` | Bearer-only | `NO_AUTH` | Portal 原生路径通常仍需浏览器登录态 Cookie / `X-Token` |
| 少数 `/govern/prod-api/...` lineage 路径 | Bearer-only | 到业务层但样例参数业务错误 | 只能说明认证层未直接拦截，不代表已拿到有效数据 |

## 当前扒不到的目标

按当前市场和已抽取 tool 配置，下面两个目标没有可扒的现役 MCP 暴露面：

1. `schedule`
   当前 `gf-mcp list` 关键词 `schedule` / `调度` 返回 0，`gf-mcp detail schedule` 返回空列表，356 条 tool HTTP 配置中也没有 `schedule` / `调度` 命中。

2. `sql_dignose` / `sql_diagnose`
   当前 `gf-mcp detail sql_dignose` 和 `gf-mcp detail sql_diagnose` 都返回空列表；关键词 `sql` 返回 0；关键词 `诊断` 只命中非数综财富/基金类 MCP；tool 配置全文里没有 `diagnose` / `diagnosis` / `dignose` / `诊断` 命中。`sql` 相关只看到 `TableMetaData.getHoraeSqlByHoraeTaskId` 和一个非数综结算类 SQL 查询/脚本工具，其中 `TableMetaData` 的用途是按 Horae 任务 ID 查 SQL，不是 SQL diagnosis。

所以现状判断是：这两个如果还存在，就不在当前 MCP 市场公开列表、当前 tool `httpReq` 配置和当前本机 MCP 配置里；需要拿到现役 appId、MCP URL 形态、本地 MCP 配置或实际调用日志，才能继续往下扒。

## 当前 Portal 原生路径补充

这些不是 MCP 市场扒出的 openapi，只是当前 `szdata` 本地适配器和 Bearer-only 调研中确认过的 Portal 原生路径。它们和上面的 `openapi` 不是同一个认证入口。

1. `/portal/prod-api/developservice/schedule/getScheduleDetailTimeFormatted.json`
   用途：调度任务详情；也用于解析 `tasklink` 上游依赖。
   当前认证判断：浏览器登录态可用；Bearer-only 为 `NO_AUTH`。

2. `/portal/prod-api/developservice/projectSpace/workNode/schedule/listTaskInstance`
   用途：调度任务实例列表；可派生运行状态。
   当前认证判断：浏览器登录态可用；Bearer-only 为 `NO_AUTH`。

3. `/portal/prod-api/developservice/horaeFailedTask/page.json`
   用途：Horae 失败任务工作列表。
   当前认证判断：浏览器登录态可用；Bearer-only 为 `NO_AUTH`。

4. `/portal/prod-api/developservice/sqlExploration/checkSqlWithAuth.json`
   用途：SQL 探索风险/权限检查。
   当前认证判断：浏览器登录态可用；Bearer-only 为 `NO_AUTH`。

5. `/portal/prod-api/metaservice/metadataSearch/searchByEs`
   用途：Portal 原生数据地图搜索。
   当前认证判断：浏览器登录态可用；Bearer-only 为 `NO_AUTH`。

6. `/portal/prod-api/metaservice/metadataSearch/getTableByGuid`
   用途：Portal 原生表详情。
   当前认证判断：浏览器登录态可用；Bearer-only 为 `NO_AUTH`。

7. `/portal/prod-api/metaservice/metadataSearch/getTableDDL`
   用途：Portal 原生表 DDL。
   当前认证判断：浏览器登录态可用；Bearer-only 为 `NO_AUTH`。

8. `/portal/prod-api/metaservice/metadataSearch/getHoraeSqlByTaskId`
   用途：Portal 原生任务 SQL。
   当前认证判断：浏览器登录态可用；Bearer-only 为 `NO_AUTH`。

## `AUTH_PASSED_BUSINESS_ERROR` 含义

`AUTH_PASSED_BUSINESS_ERROR` 的意思是：请求没有被认证网关直接拦截，已经到达业务接口；但样例参数不完整、不匹配或业务条件不满足，所以返回参数/业务错误。

它不能等同于“接口可用”，只能说明“认证层未直接挡住”。要确认可用，还要用正确参数拿到有效业务数据。

## 后续建议

如果继续扒当前 `openapi`，优先从当前 MCP market 的 `httpReq`、`globalToolPlugins`、OpenAPI 网关目录或服务端配置源继续找；不要把 Portal bundle 里出现的 `/portal/prod-api/...` 误归为 MCP/openapi。

本轮临时抽取结果保存在：

- `tmp/mcp-openapi-recon/mcp-httpreq-inventory.json`
- `tmp/mcp-openapi-recon/openapi-inventory.json`

这两个文件不包含 token，但包含内部服务路径和 tool 配置，外发或长期沉淀前需要再做敏感信息复核。
