# SZData SQL 诊断行为说明

更新日期：2026-07-07

状态：active/read-only

## 范围

本文记录以下命令的实测行为：

```powershell
opencli szdata sql-diagnosis --sql "<sql text>" -f json
```

在判断 `sql-diagnosis` 能证明什么之前，先读本文。它是 SQL 文本诊断/检查命令，不是 SQL 执行器，也不是当前登录用户表权限的事实来源。

## 来源路径

live adapter 实现：

```text
C:\Users\13246\.opencli\shared\szdata-core\commands\sql\sql-diagnosis.js
```

命令向以下接口提交表单：

```text
/portal/prod-api/developservice/sqlExploration/checkSqlWithAuth.json
```

关键表单字段：

```text
sceneType=DATASET_MANAGE
sqlList[0].sql=<sql text>
sqlList[0].sign=SQL
dataSourceId=<optional>
executionEngine=<optional>
```

adapter 没有 `save`、`submit`、`execute`、preview、websocket 或配置写入分支。它把 SQL 作为文本发给检查接口，并把返回的问题汇总成 `valid`、`issueCount`、`issues`。

## 它能证明什么

`sql-diagnosis` 目前可以证明：

- 当前浏览器登录态能访问 Data Portal SQL exploration 检查接口。
- 传入的 SQL 文本没有命中该接口当前返回的问题。
- 该接口可以返回部分规则问题，例如 `select *`。
- 该接口可以识别部分不存在的表引用。

它不能证明：

- SQL 已经执行。
- SQL 能返回结果集。
- 当前登录用户能读取所有引用表。
- 所有引用字段都存在。
- SQL 在执行引擎里语法一定合法。
- 它与 MCP `query.sql_diagnosis` 完全等价。

当前登录用户表权限请使用：

```powershell
opencli szdata table-permission-mine --table db.table -f json
```

已知表的有界样例数据请使用 `table-sample`。实际 SQL 预览执行只能走明确授权的 `szdatatest` 预览生命周期命令及其测试写入确认。

## 实测矩阵

以下结果来自 2026-07-07 的有界只读 `-f json` 调用。

| 探针形态 | 实测结果 | 解释 |
| --- | --- | --- |
| `select 1` | `valid=Y` | 常量 SQL 通过。 |
| `select count(1) from known_table` | `valid=Y` | 普通聚合探针通过。 |
| `select count(*) from known_table` | `valid=Y` | `count(*)` 不按 `select *` 处理。 |
| `select explicit_col from known_table limit 1` | 表存在时 `valid=Y` | 显式字段投影未被当前规则拦截。 |
| `select * from known_table` | `valid=N`；问题为 `select *` | 裸星号投影会被拦截。 |
| `select t.* from known_table t` | `valid=N`；问题为 `select *` | 别名星号投影也会被拦截。 |
| `select count(1) from missing_table` | `valid=N`；问题为表/字段不存在 | 该接口能识别部分不存在表引用。 |
| `select missing_col from known_table limit 1` | `valid=Y` | 字段存在性不是可靠检查项。 |
| 形如 `select from known_table` 的错误文本 | `valid=Y` | 不是严格语法解析/执行检查。 |
| 历史上把类似 DML 的文本作为检查字符串传入 | `valid=Y` | 不要在生产探针中重复；以后只用 SELECT-only 探针。 |

一个重要的表权限对照：

| 检查 | 表 | 结果 |
| --- | --- | --- |
| `table-permission-mine` | `pdata_n.t03_ord` | `status=NO` |
| `sql-diagnosis` + `select count(1)` | `pdata_n.t03_ord` | `valid=Y` |

因此，`sql-diagnosis` 不是当前登录用户表权限结论。

## 安全边界

客户端侧证据只能证明 OpenCLI 命令请求的是 `checkSqlWithAuth.json`。仅凭客户端代码，不能证明服务端实现绝对没有内部副作用。绝对证明需要服务端审计、Hive/Spark 执行日志，或平台 owner 确认。

后续生产侧调查必须遵守：

- 不要用 DDL、DML、DCL、`insert`、`overwrite`、`delete`、`update`、`merge`、`drop`、`truncate`、`alter` 或类似建表/写入的 SQL 文本做探针。
- 优先使用 SELECT-only 探针，例如 `select count(1) from db.table`。
- 只有在检查缺表诊断时，才使用明显不存在的表名。
- 把 `valid=Y` 理解为“该检查接口没有返回问题”，不要理解为执行成功或数据权限成功。
- 把 `valid=N` 理解为规则问题报告；需要阅读 `issues` 判断原因是 `select *`、缺表，还是其他规则。

## 实用路由

| 用户问题 | 使用 |
| --- | --- |
| 这段 SQL 文本是否命中 Data Portal SQL exploration 规则？ | `sql-diagnosis` |
| 当前登录用户能不能读 `db.table`？ | `table-permission-mine` |
| 表元数据是否存在？ | `table-search`、`table`、`table-detail` |
| 能否查看有界表样例？ | `table-sample` |
| 这段 SQL 能不能真实执行并返回行？ | `sql-diagnosis` 不能证明；需要明确授权的测试侧预览路径。 |

## 维护说明

- 本文需与 `C:\Users\13246\.opencli\shared\szdata-core\commands\sql\sql-diagnosis.js` 保持一致。
- 如果未来命令增加 MCP-backed 精确等价模式，应把模式切换与当前 direct Portal endpoint 分开记录。
- 如果服务 owner 确认接口服务端实现，应作为单独证据级别补充，不要从客户端代码倒推。
