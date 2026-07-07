# SZData Agent CLI 审计规范

更新时间：2026-07-06

这份规范把通用 CLI 审计方法压缩成 SZData 专用执行标准。它用于审计、改造或复核 `szdata`、`szdata_detail`、`szdatatest`、`szdatatest_detail`，目标是让新开的 agent 窗口不用猜命令、猜环境、猜输出。

## 适用范围

只审计和改造这四类 CLI 面：

| CLI | 定位 | 不做什么 |
| --- | --- | --- |
| `szdata` | 生产高频主流程和只读确认 | 不默认承载低频解释；不做未经授权的生产写入 |
| `szdata_detail` | 低频诊断、审计、解释、历史、日志、调度配置回读 | 不承载写入；不作为高频默认入口 |
| `szdatatest` | 测试验证、字段解析、guard、测试写入和生命周期探针 | 不代表生产事实；不隐藏写动作 |
| `szdatatest_detail` | 测试环境低频诊断镜像 | 不承载测试写入；命令清单必须对齐 `szdata_detail` |

这不是通用 OpenCLI 框架治理任务。不要因为本规范去重建 manifest、doctor、profile、browser primitive、统一 JSON envelope 或发布体系，除非用户另行明确要求。

## 必读顺序

1. `AGENTS.md`
2. `references/tools/opencli.md`
3. `references/tools/szdata-command-landscape.md`
4. `references/tools/szdata.md`
5. `references/tools/szdata-operations/README.md`
6. live adapter `COMMANDS.md`

live adapter 源码不在本工作区：

```text
C:\Users\13246\.opencli\clis\szdata
C:\Users\13246\.opencli\clis\szdatatest
C:\Users\13246\.opencli\clis\szdata_detail
C:\Users\13246\.opencli\clis\szdatatest_detail
C:\Users\13246\.opencli\shared\szdata-core
```

## 审计步骤

### 1. 项目地图

先确认当前对象属于哪个面：

- `szdata` root command 是否是高频生产只读入口。
- `szdata_detail` command 是否是低频诊断、解释、历史、日志、统计或审计。
- `szdatatest` command 是否是测试主流程镜像、字段解析、guard 或显式测试写入。
- `szdatatest_detail` command 是否是测试环境低频诊断镜像。
- `archive` 是否只保留退役、误导、风险或历史实现。

不要把 workspace 的 `references/`、`tmp/`、`_archive/` 当 live adapter 源码。

### 2. 命令总账

以 [szdata-command-landscape.md](./szdata-command-landscape.md) 为唯一全局总账，检查每个命令：

| 检查项 | 通过标准 |
| --- | --- |
| 任务域 | 只属于一个主任务域；不能让 agent 猜 |
| 命名 | 同类命令同前缀，主体/维度放后缀 |
| 主入口 | 高频问题优先放 `szdata` |
| detail | 低频解释、日志、历史、统计放 `szdata_detail` |
| test | 测试写入、写前验证、生命周期探针放 `szdatatest` |
| test detail | 测试环境低频解释、日志、历史、统计放 `szdatatest_detail`，清单对齐 `szdata_detail` |
| archive | 重复、慢、误导、历史兼容旧名移出活动入口 |

旧混乱入口不做兼容保留。若用户已明确要求收敛，旧名应归档或拒绝，并在文档写替代命令。

### 3. 输出契约

审计输出时优先问：agent 是否能用最少 token 拿到关键结论？

默认输出规则：

- 主入口默认给结论摘要或名片，不 dump 大对象树。
- SQL、DDL、日志、人员列表、字段列表、raw JSON 默认必须有边界。
- 需要完整证据时使用专项命令或显式参数，例如 `--detail`、`--raw`、`--size`、`--sql-preview`、`--field-preview`、`--save-sql`。
- 默认删除无业务意义字段，例如空值、`"-"`、内部 endpoint、host、port、cookie、token、连接信息。
- `-f json` 输出应稳定、字段名清楚、可脚本读取；不要为了统一格式强行改成 `{ok,data,meta}` envelope。
- 错误和 warning 可以保留，但不能污染可解析主结果。

专项证据命令可以更长，但必须命名清楚，且 help/doc 明确说明它是证据命令，不是默认发现入口。

### 4. Agent 可选性

每个命令必须在文档或 help 中能回答三件事：

1. 它回答什么问题。
2. 它不回答什么问题。
3. 下一步该用哪个命令。

如果两个命令名字相近，必须说明职责差异。例如 `table` 和 `table-detail`、`table-lineage` 和 `table.lineage` 预览、`role-list` 和 `table-permission-role`。

### 5. 环境和安全

- `szdata` 是生产，默认只读。
- `szdatatest` 是测试，任何写入/保存/提交/预览/生成/调度保存都必须先在这里验证。
- 生产写入需要用户明确授权具体目标和动作。
- 写命令必须默认 dry-run；实际写入必须有显式 `--execute` 和确认参数。
- 不输出 cookie、token、internal host/port、JDBC/HDFS/网关细节、浏览器 profile secret。
- 不把运行时数据库权限、平台目录权限、调度主题权限混成一个结论。

### 6. 真实验证

不能只看 `--help` 或源码推断。审计结论必须至少包含：

- 命令是否在活动入口出现。
- 小样本 `-f json` 实测字段。
- 输出是否有界。
- 是否命中正确环境。
- 代表性 `node --check`。

Chrome-backed OpenCLI 命令不要并行跑；按序执行，避免浏览器 bridge 争用。

### 7. 文档一致性

任何命令行为或归属变化，都要同步：

- [szdata-command-landscape.md](./szdata-command-landscape.md)
- [szdata.md](./szdata.md)
- [szdata-detail.md](./szdata-detail.md)（涉及 `szdata_detail` 时）
- [szdata-operations/README.md](./szdata-operations/README.md)（涉及复杂流程时）
- live adapter `COMMANDS.md`
- 相关专题文档或 skill

专题文档只保留领域细节，不维护第二套全局命令清单。

## 验收清单

一次审计或改造完成前，至少检查：

- `szdata-command-landscape.md` 能解释所有 active 命令归属。
- `szdata` / `szdata_detail` / `szdatatest` / `szdatatest_detail` 边界一致。
- `node C:\Users\13246\.opencli\shared\szdata-core\audit-surfaces.mjs --plain` 输出 `mismatch=0`。
- 旧混乱入口不会作为 agent 可选入口出现。
- 默认输出没有明显大 SQL、大 raw、大人员列表、大日志。
- help、COMMANDS、workspace docs 不互相打架。
- 改过的 JS 通过 `node --check`。
- 至少一个代表性 smoke test 通过。
- 中文文档和命令说明无乱码标记。
