# szdata 查看角色权限只读参考

> 面向后续 CLI / adapter / agent 的只读参考。本文只沉淀 2026-07-04 本轮观察结论；数量和页面行为均不写成永久事实。

## 页面与环境边界

- 页面：查看角色权限。
- 路由：`/permission/seeRolePermission/:id/:name?view=true`。
- 本轮目标角色：`股权衍生品部数据开发分析`。
- `roleId` / `roleUuid`：`1e1a8de8e209e211db3d9b559ea7be90`。
- 环境：`szdata` 生产环境 `data.gf.com.cn`。
- 操作边界：只读查看、被动 network 观察、bundle 定向搜索、help/wiki 定向搜索。
- 本次未执行保存、提交、修改、删除、授权、取消授权等权限写操作。

## 页面 UI 结论

本轮打开页面标题为“查看股权衍生品部数据开发分析在数据门户中的权限”，路由标题为“查看角色权限”。

该角色只显示“数据权限”页签；未显示“功能权限”“报表权限”。原因可由 `queryRoleTypePerm` 返回的本轮观察值解释：`functionCount=0`、`dataCount=266`、`productCount=0`。

数据权限页签筛选项：

- 集群。
- 库名。
- 表名。
- 业务管理部门。
- 操作按钮：`重置`、`搜索`。

数据权限表格列：

- 集群。
- 库名称。
- 表名称。
- 表中文名。
- 业务管理部门。
- 行权限。
- 列权限。
- 规则匹配。
- 授权方式。
- 相关IT需求。

只读表现：

- 页面 URL 带 `view=true`。
- 前端查看页组件传入 `only-see=true`、`show-save=false`。
- 数据权限表在 `only-see=true` 下移除 `operation` 列。
- 保存、提交、新增、删除、授权、取消授权等按钮未出现在本轮目标角色页面。
- 行权限、列权限包选择器以禁用方式展示。

注意：页面顶部导航来自当前登录用户的门户导航，不等于目标角色拥有的菜单权限；判断目标角色功能权限不能看顶部导航。

## URL 参数解释

路由定义形态为：

```text
/permission/seeRolePermission/:id/:name?view=true
```

- `id` 是目标角色的 `roleId` / `roleUuid`，用于查询角色详情和角色权限。
- 第二路径参数前端变量名叫 `name`，但跳转来源里既可能放角色名，也可能放 `Date.now()` 这样的时间戳/占位值。
- 页面最终展示的角色名以后端 `sysRole/detail` 返回的 `roleName` 为准，不应依赖第二路径参数。
- 查看模式页面标题是“查看...在数据门户中的权限”，子组件传 `only-see=true`、`show-save=false`。
- 设置/授权模式页面标题是“设置...在数据门户中的权限”，子组件传 `only-see=false`、`show-save=true`，会出现保存/提交类入口；CLI 只读实现不得走设置/授权路径。

## 只读接口清单

### `POST /permissionservice/sysRole/detail.json?id=<roleId>`

- 用途：读取角色基本信息。
- 关键参数：`id=<roleId>`，本轮为 `1e1a8de8e209e211db3d9b559ea7be90`。
- 关键响应字段：`uuid`、`roleName`、`remark`、`itDemand`、`creatorName`、`isSelfApplication`、`isSyncToBiUserGroup`、`isCanApplyDataPerm`、`createTime`、`updateTime`。
- 是否代表角色实际权限：不代表具体权限清单，只代表角色元信息和部分能力标志。

### `POST /permissionservice/sysRole/queryRoleTypePerm.json`

- 用途：读取角色三类权限计数，决定查看页显示哪些页签。
- 关键参数：`roleUuid`。
- 关键响应字段：`functionCount`、`dataCount`、`productCount`。
- 是否代表角色实际权限：可代表该角色在功能/数据/报表三类权限上的数量摘要，但不是明细。

### `POST /permissionservice/sysRolePerm/queryRoleDataPerm.json`

- 用途：读取角色数据权限明细，是数据权限判断主接口。
- 关键参数：`roleUuid`。
- 关键响应字段：`roleUuid`、`clusterUuid`、`permUuid`、`databaseName`、`databaseType`、`tableName`、`tableChnName`、`type`、`authMethod`、`ruleMatch`、`ownerName`、`rowPermDataPackages`、`columnPermDataPackages`、`itDemand`、`qualifiedName`。
- 是否代表角色实际权限：代表角色数据权限明细。本轮表格返回 84 行。
- 脱敏提醒：`qualifiedName` 可能携带内部数据源标识；默认摘要不输出。

### `POST /permissionservice/permFunction/list.json`

- 用途：读取全局功能/菜单权限目录。
- 关键参数：页面本轮未依赖目标角色参数来表达角色授权；它是目录读取。
- 关键响应字段：`permUuid`、`permName`、`permCode`、`permUrl`、`parentUuid`、`permType`、`openType`、`businessCode`、`sort`、`majorModuleId`。
- 是否代表角色实际权限：不代表目标角色拥有菜单权限。特别注意：这是全局功能目录，不能用它直接判断角色有无某菜单/按钮。

### `POST /developservice/cluster/list.json`

- 用途：读取数据权限筛选区的集群候选。
- 关键参数：本轮页面请求包含可选集群类型过滤和 `isShowNonHive=true` 类筛选。
- 关键响应字段：`uuid`、`name`、`clusterType`、`horaeClusterId`、`clusterIndex`、`canSelect`。
- 是否代表角色实际权限：不代表角色权限；只提供筛选/展示字典。

### `POST /developservice/database/queryDatabaseForRole.json`

- 用途：按集群读取角色相关数据库候选，用于库名筛选和权限展示辅助。
- 关键参数：`clusterUuid`，可带 `ownerUuidList`。
- 关键响应字段：`uuid`、`name`、`type`、`serverUuid`、`hasPerm`、`expire`、`owner`。
- 是否代表角色实际权限：可作为库候选和 `hasPerm` 辅助判断，但数据权限最终以 `queryRoleDataPerm` 明细为主。

### `POST /portalservice/dept/queryDeptByName.json`

- 用途：读取业务管理部门候选，用于筛选器。
- 关键参数：部门名称/关键词。
- 关键响应字段：`uuid`、`label`、`fullPath`、`leaf`。
- 是否代表角色实际权限：不代表角色权限；只提供部门字典。

## 目标角色权限摘要

本轮观察：

- `functionCount=0`。
- `productCount=0`。
- `dataCount=266`。
- `queryRoleDataPerm` 表格返回 84 行。

结论：该角色是数据权限型角色，不是菜单/功能/报表权限角色。不能把当前登录用户顶部导航当作该角色菜单权限。

按集群汇总：

- 观达（科学城）集群：77 行。
- StarRocks：2 行。
- StarRocks-UAT：2 行。
- TiDB-T1：1 行。
- TiDB-T2：1 行。
- TiDB-UAT：1 行。

按授权方式汇总：

- 按库动态更新：23 行。
- 按规则匹配更新：2 行。
- 按业务管理部门动态更新：1 行。
- 其他/静态表级：58 行。

按粒度汇总：

- 库级/整库：25 行。
- 表级：58 行。
- 其他/未指定库表：1 行。

主要库表范围：

- `bd_dm_otc` / `bd_dm_otc_uat`：在 StarRocks、TiDB 相关集群上有库级动态权限。
- `dpl`：在 StarRocks 与 StarRocks-UAT 上有规则匹配权限，规则样例为 `tit_titans%`。
- 观达（科学城）集群 Hive 库级权限样例：`dm_otc_n`、`dm_otc_test`、`odata_n_tit`、`odata_n_lss` 等。
- `pdata_n`：有表级权限，主题集中在 OTC 衍生品、期权/互换合约、持仓、估值、客户、组织/员工、TITANS 相关基础/附件等。
- 代表性表样例：`t03_otc_swap_comp_info`、`t03_otc_opt_comp_info`、`t01_otc_deri_cust`、`t98_otc_book_hold_sum`、`t00_tit_s3_attach_info`。

行/列权限包：

- 本轮 84 行中 `rowPermDataPackages` 和 `columnPermDataPackages` 均未返回包数据。
- 行/列权限包为空不代表没有表权限，只代表本轮未配置或未返回行/列权限包。

## 权限模型规律

功能/菜单/按钮权限字段：

- `permUuid`：权限节点 ID。
- `parentUuid`：父节点 ID，用于组成树。
- `permType`：权限类型，通常用于区分菜单、按钮等节点。
- `permCode`：权限编码。
- `permUrl`：功能路径或前端 URL。

数据权限字段：

- `clusterUuid`：集群 ID。
- `databaseName`：库名。
- `tableName`：表名；为空时通常表示库级/整库授权或动态授权条目。
- `authMethod`：授权方式。
- `ruleMatch`：规则匹配表达式，例如 `tit_titans%`。
- `rowPermDataPackages`：行权限包。
- `columnPermDataPackages`：列权限包。
- `ownerName`：业务管理部门名称。

判断规则：

- 判断功能权限不能只看 `permFunction/list.json`，该接口是全局目录。
- 判断目标角色功能权限，应查角色实际功能权限明细或角色功能树选中状态；本轮目标角色 `functionCount=0`，无功能权限页签可展开。
- 判断数据权限以 `queryRoleDataPerm` 为主。

## 面向数据集开发前置权限检查的 CLI 实现规格

目标不是做授权。给 agent 的开发前置主路径优先回答两个问题：

- 当前登录用户是否有目标 `db.table` 权限：用 `table-permission-mine --table db.table`。
- 调度主题是否能访问目标表：用 `table-permission-topic --topic <topic> --table db.table`。

如果用户明确问“某个角色是否覆盖这张表”，使用同一任务族的 `table-permission-role --role-id <roleId> --table db.table`。

已实现 CLI（`szdata` / `szdatatest` 均为只读）：

- `role-list`：读取/搜索角色列表，用中文角色名找 `roleId`。
- `role-user-list`：读取某个角色下的用户列表；这是 `role -> users`，不是任意用户反查角色。
- `table-permission-mine`：当前登录用户指定 `db.table` 权限检查，是开发前置用户侧主入口。
- `table-permission-role`：指定角色对目标 `db.table` 的表权限检查，是角色维度的表权限入口。

已归档/改名命令：`current-user-data-permission`、`role-data-permission`、`role-summary`、`table-permission-check`、`role-user-group-list`、`role-function-permission`、`table-data-package-check`、`sql-permission-package-check`。旧实现已移至 `C:/Users/13246/.opencli/archive/clis/` 或收敛到新命令名，不再放在 `clis/<site>/archive/` 下，避免 OpenCLI registry 发现层误加载退役模块。

### `role-user-list`

输入：

- `--role-id <roleId>`。
- `--role-name <roleName>`：可用中文角色名解析 `roleId`。
- 可选：`--keyword`、`--page`、`--size`。

调用：

- `/permissionservice/sysRole/queryUserInfo.json`。

默认输出：

- `roleId`、`roleName`。
- `totalAvailable`、`totalObserved`。
- `counts`：接口返回的有效、无效、过期数量摘要。
- `rows`：只输出 `userName`、`mainDeptName`、`startTime`、`endTime`、`empStatCd`。

默认不输出：

- 手机、邮箱、账号、工号、`userUuid`、cookie、token、内部 IP/端口或 raw JSON。

边界：

- 该命令只能确认“某个角色下有哪些用户”。
- 不能把它解释成“某个用户有哪些角色”；后者需要另一个明确的只读反向接口证据。

### `table-permission-role`

输入：

- `--role-id <roleId>`。
- `--role-name <roleName>`：可用中文角色名解析 `roleId`。
- `--table <db.table>` 或 `--tables <db.table,db.table>`。
- 可选：`--cluster`、`--detail`、`--format json|text`。

默认输出：

- 单表默认输出 `roleId`、`roleName`、`table`、`conclusion`、`matchedBy`、`matched`、`source`。
- `conclusion` 为 `PASS` / `MAYBE` / `NO` / `UNKNOWN`。
- `source` 只保留角色数据权限行里的紧凑证据，例如集群、库、表、授权方式、规则。
- 加 `--detail` 时才输出 `results`、`databaseCoverage`、分组摘要和截断后的 `rows`。

`scope` 口径：

- `database`：库级授权配置，例如“按库动态更新”。
- `explicit-table`：显式表级授权配置，`sampleTables` 只给代表性表名，`hasMoreTables=true` 表示还有更多表级配置。
- `rule`：规则匹配配置，例如 `ruleMatch=tit_titans%`；`recordCount` 表示匹配规则在不同集群/环境下的配置行数。
- `other`：当前规则无法稳定归入上述三类的只读证据。

详细证据：

- 加 `--detail` 时才输出 `summaryByCluster`、`databasePermissions`、`clusterSchemaRules` 和截断后的 `rows`。
- `rows` 中 `clusterUuid` 与 `clusterName` 分开；`clusterName` 是可读集群名，避免把 UUID 当集群名展示。
- 默认不输出 `summaryByDatabase`、`summaryByAuthMethod`、`summaryByScope` 这类计数字典；需要统计矩阵时加 `--detail`。

默认不输出：

- cookie、token。
- 内部 IP、端口、网关细节。
- 全量 raw JSON。
- `qualifiedName` 等可能含内部数据源标识的字段。

## 归档旧入口

以下旧入口不再作为 agent 工作流入口，也不应从新对话里直接选择：

- `current-user-data-permission`
- `role-summary`
- `role-user-group-list`
- `role-function-permission`
- `table-permission-check`
- `table-data-package-check`
- `sql-permission-package-check`

替代路径固定为三类：

- 当前登录用户是否能读表：`table-permission-mine --table db.table`。
- 调度主题是否能读表：`table-permission-topic --topic <topic> --table db.table`。
- 指定角色是否覆盖表：`table-permission-role --role-id <roleId> --table db.table`。

角色本身和成员关系只用 `role-list` / `role-user-list`。不要再使用“角色画像”型总览命令把角色详情、成员、计数和表覆盖混在一起。

## CLI 用法与示例

这些命令用于“数据集开发前置源表权限检查”，只读调用
`/permissionservice/sysRolePerm/queryRoleDataPerm.json`。默认角色为
`股权衍生品部数据开发分析`：

```powershell
opencli szdata_detail role-list --keyword "股权衍生品" --size 20 -f json
opencli szdata_detail role-user-list --role-name "股权衍生品部数据开发分析" -f json
opencli szdata_detail role-user-list --role-id 1e1a8de8e209e211db3d9b559ea7be90 --keyword "甘敏" -f json
opencli szdata table-permission-role --role-id 1e1a8de8e209e211db3d9b559ea7be90 --table pdata_n.t03_otc_swap_comp_info -f json
opencli szdata table-permission-role --role-name "股权衍生品部数据开发分析" --table pdata_n.t03_otc_swap_comp_info --detail -f json
opencli szdata table-permission-mine --table pdata_n.t03_otc_swap_comp_info -f json
opencli szdata table-permission-topic --topic DM_OTC_N --table pdata_n.t03_otc_swap_comp_info -f json

```

测试环境命令名相同，仅 site 改为 `szdatatest`：

```powershell
opencli szdatatest table-permission-role --help
opencli szdatatest_detail role-user-list --help
opencli szdatatest table-permission-mine --help
opencli szdatatest table-permission-topic --help
```

输出边界：
- `role-user-list` 只输出角色成员摘要，不输出手机号、邮箱、账号、工号、`userUuid` 或 raw JSON；它是 `role -> users`，不是 `user -> roles`。
- `table-permission-role` 单表默认输出紧凑结论；加 `--detail` 才输出 `databaseCoverage`、分组摘要和截断后的 `rows`。`recordCount` 是权限配置记录数，不是物理表数量；不会 dump `qualifiedName`、cookie、token、内部 IP/端口或 raw JSON。
- `rowPermDataPackages` / `columnPermDataPackages` 不输出详情，只转成 `hasRowPerm` / `hasColumnPerm` / 包数量。

开发前置边界：
- 当前用户表权限以 `table-permission-mine --table db.table` 为主。
- 调度主题表权限以 `table-permission-topic --topic <topic> --table db.table` 为主。
- 角色表权限以 `table-permission-role --role-id <roleId> --table db.table` 为主，但只有用户明确要求角色维度时使用。

## Evidence

- 日期：2026-07-04。
- 来源：页面只读打开、network 被动观察、bundle 定向搜索、help/wiki 定向搜索。
- 环境：`szdata` 生产。
- 安全边界：不贴 cookie、token、内部 IP、端口、网关细节。
- 数量口径：`functionCount=0`、`dataCount=266`、`productCount=0`、`queryRoleDataPerm` 返回 84 行，均为本轮观察值，不写成永久事实。
- 操作边界：本轮没有做任何权限修改。

## 2026-07-06 audit addendum

Production `szdata` smoke sample:

```powershell
opencli szdata table-permission-role --role-id 1e1a8de8e209e211db3d9b559ea7be90 --table dm_otc_n.md_stock_daily_market -f json
```

Observed compact verdict fields: `roleId`, `roleName`, `table`, `conclusion`,
`matchedBy`, `matched`, `source`. The sample returned `conclusion=PASS`,
`matchedBy=database`, and `matched=dm_otc_n`.

Role-dimension table checks remain part of the `table-permission-*` family, but
agents should only choose `table-permission-role` when the user explicitly asks
about a role. Current-login user checks use `table-permission-mine`; scheduling
topic checks use `table-permission-topic`.
