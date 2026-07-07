# TableMetaData MCP 逻辑调研

更新时间：2026-07-07

## 结论

`TableMetaData` MCP 不是把 `data.gf.com.cn/portal/prod-api/...` 直接暴露出来，而是把一组 `openapi/metaservice/personaltoken/internal/metadataSearch/*` 接口包装成 MCP tools。

实际链路是：

```text
MCP Client
  -> mcp-api-inner.gf.com.cn/server/mcp/TableMetaData/sse
  -> TableMetaData MCP Server
  -> data.gf.com.cn/openapi/metaservice/personaltoken/internal/metadataSearch/*
  -> MCP tool result
```

因此前面两个判断要分开：

- MCP / openapi 链路能通：使用 MCP Authorization 进入 MCP server，再由 MCP server 透传/改写 `X-Personal-Token` 调 openapi。
- Portal 原生链路不一定通：同一个 Bearer 直打 `/portal/prod-api/...` 大多数返回 `NO_AUTH`。

## MCP 市场信息

来源：`gf-mcp detail TableMetaData --json`。

| 项 | 值 |
| --- | --- |
| appId | `TableMetaData` |
| 名称 | 表元数据 |
| orgId | `BDP_DATA_PORTAL` |
| serverVer | `16` |
| version | `V20260702132939` |
| updatedAt | `2026-07-02T05:29:39.226Z` |
| 连接方式 | SSE |
| MCP URL | `https://mcp-api-inner.gf.com.cn/server/mcp/TableMetaData/sse` / 市场示例为 `https://mcp-api.gf.com.cn/server/mcp/TableMetaData/sse` |
| MCP Auth | `Authorization: Bearer <mcp-token>` |
| 后端 Auth | `X-Personal-Token` |
| globalToolPlugins | `auth_upgrade`，会重写/透传 `X-Personal-Token` |

本地 Codex 配置使用环境变量承载敏感值：

- `CLAUDE_MCP_TABLEMETADATA_AUTHORIZATION`
- `CLAUDE_MCP_TABLEMETADATA_X_PERSONAL_TOKEN`

不要把这两个值写入仓库、命令行历史、日志或报告。

## Tool 到 openapi 映射

| MCP tool | 实际 openapi | 方法 | Header | Body |
| --- | --- | --- | --- | --- |
| `getGuid` | `/openapi/metaservice/personaltoken/internal/metadataSearch/listMetaTableInfo` | `POST` | `X-Personal-Token` | `{ "dbName": "string", "tableName": "string" }` |
| `getTableDDL` | `/openapi/metaservice/personaltoken/internal/metadataSearch/getTableDDL` | `POST` | `X-Personal-Token` | `{ "guid": "string" }` |
| `getTableDetailInfoByGuid` | `/openapi/metaservice/personaltoken/internal/metadataSearch/getTableByGuid` | `POST` | `X-Personal-Token` | `{ "guid": "string" }` |
| `getHoraeSqlByHoraeTaskId` | `/openapi/metaservice/personaltoken/internal/metadataSearch/getHoraeSqlByTaskId` | `POST` | `X-Personal-Token` | `{ "horaeTaskId": "string" }` |

完整 URL 前缀：

```text
https://data.gf.com.cn
```

## 本轮直连验证

验证方式：只使用本机环境变量中的 `X-Personal-Token`，不输出 token，不输出完整 DDL / SQL / GUID。

样例输入：

```json
{ "dbName": "dm_otc_n", "tableName": "md_stock_daily_market" }
```

| openapi | HTTP | code | 结果形态 |
| --- | --- | --- | --- |
| `/openapi/metaservice/personaltoken/internal/metadataSearch/listMetaTableInfo` | `200` | `0` | 返回 1 条记录，包含 `guid` / `cluster` / `systems` |
| `/openapi/metaservice/personaltoken/internal/metadataSearch/getTableDDL` | `200` | `0` | 返回 DDL 字符串 |
| `/openapi/metaservice/personaltoken/internal/metadataSearch/getTableByGuid` | `200` | `0` | 返回对象，包含 `guid,name,comment,qualifiedName,businessMetadata,technicalMetadata,columnCount,isPartitioned,numRows,totalSize` 等字段 |
| `/openapi/metaservice/personaltoken/internal/metadataSearch/getHoraeSqlByTaskId` | `200` | `0` | 返回 SQL 数组 |

对照验证：

| 方式 | 结果 |
| --- | --- |
| 只带 `X-Personal-Token` 调 openapi | 成功 |
| 只带 MCP `Authorization` 调 openapi | `401 Unauthorized` |
| 只带 Bearer 直打多数 `/portal/prod-api/...` | `NO_AUTH` |

这说明 `X-Personal-Token` 是 `TableMetaData` 后端 openapi 的关键认证头；MCP `Authorization` 只负责进入 MCP server。

## 为什么之前会看起来“都能打通”

因为成功链路不止一条：

| 链路 | 能说明什么 | 不能说明什么 |
| --- | --- | --- |
| `TableMetaData` MCP tool 成功 | MCP server 能调用它配置好的 openapi 后端 | 不能证明同一个 Bearer 可直连 Portal 原生 URL |
| `openapi/.../personaltoken/internal/...` + `X-Personal-Token` 成功 | personal token 可直连 openapi 后端 | 不能证明 `/portal/prod-api/...` 接受该 token |
| `opencli szdata` 成功 | 浏览器登录态 Cookie / `X-Token` 可读 Portal 页面/接口 | 不能证明 Bearer-only 可用 |
| `/portal/prod-api/...` Bearer-only 成功或失败 | 只说明 Portal 原生路径是否接受该 Bearer | 不能否定 MCP/openapi 链路 |

所以最终口径是：

```text
MCP tool 可用
  != openapi 可用
  != Portal prod-api Bearer-only 可用
  != 浏览器登录态可用
```

每条链路需要单独记录证据。

## 对 szdata / szdatatest 的影响

- `metadata` 类能力可以有两种来源：Portal 原生 `/portal/prod-api/metaservice/...`，以及 MCP 暴露的 `/openapi/metaservice/personaltoken/internal/...`。
- 当前 `szdata` 高准入口仍优先使用 Portal / 浏览器登录态，因为这与数综页面一致。
- 如果未来要新增 MCP/openapi 后备路径，命令名或输出必须明确标记认证模式，例如 `authMode=openapi_personal_token`，不能伪装成 Portal 原生读回。
- 调度详情 `getScheduleDetailTimeFormatted.json` 不属于本 `TableMetaData` MCP 的四个 tool；它仍应按 Portal 原生 schedule 接口单独验证。

## 安全备注

- 本轮没有保存任何 API key、Bearer token、cookie、`X-Token` 或 `X-Personal-Token`。
- 本机旧 Claude 配置中存在明文密钥形态的配置项；不在本文复述。建议后续轮换相关密钥，并统一迁到环境变量。
- 所有复跑脚本或命令都应从环境变量读密钥，输出只保留状态码、应用码、字段形态和计数。
