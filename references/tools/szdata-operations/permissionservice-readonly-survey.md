# permissionservice 只读探察报告

> Current status, 2026-07-06: this is a historical survey, not the active command map. The active command map is maintained in [../szdata-command-landscape.md](../szdata-command-landscape.md), with daily routing summarized in [../szdata.md](../szdata.md).

## 结论

`/permissionservice` 是一组权限域服务，不是单一“角色权限接口”。它覆盖角色、用户组、功能权限、数据权限、权限申请、权限回收、报表/产品权限、规则匹配、脱敏和风险规则等能力。

对 agent 开发前置检查，当前只保留三条表权限主路径：

| 问题 | 主命令 | 输出重点 |
| --- | --- | --- |
| 当前登录用户是否能读某张表？ | `table-permission-mine --table db.table` | `PASS` / `EXPIRED` / `NO` / `UNKNOWN`、命中来源、权限有效期 |
| 某个调度主题是否能读某张表？ | `table-permission-topic --topic TOPIC --table db.table` | `PASS` / `EXPIRED` / `NO` / `UNKNOWN`、命中来源、权限有效期 |
| 某个角色是否能读某张表？ | `table-permission-role --role-id ROLE_ID --table db.table` | `PASS` / `EXPIRED` / `NO` / `UNKNOWN`、命中来源、权限有效期 |

角色相关命令保留为诊断/审计/解释面：

| 命令 | 定位 |
| --- | --- |
| `szdata_detail role-list` | 通过中文角色名或关键词定位 `roleId` |
| `szdata_detail role-user-list` | 查询 `role -> users` 成员关系 |
| `table-permission-role` | 检查某个角色是否覆盖指定 `db.table`，角色维度归入表权限家族 |

`my-permission-base`、`my-permission-function`、`my-permission-report` 已从活动入口移除。它们只能说明当前账号工作台快照，不能回答某表是否可读，默认保留会让 agent 误用。

## 安全边界

本调查只允许只读行为：

- 读取现有 OpenCLI `--help`、本地适配器源码和已登记文档。
- 调用已实现且声明 `access=read` 的 OpenCLI 命令做小样本验证。
- 不保存、不提交、不审批、不授权、不回收、不清缓存、不上传附件、不写入风险规则。
- 不输出 cookie、token、内部 IP/端口、数据库连接串、HDFS 路径等基础设施细节。

`szdata` 是生产环境，只用于只读查询、调查和生产状态确认。任何保存、提交、生成、预览、删除、编辑配置等动作必须先在 `szdatatest` 验证，并且需要用户明确授权。

## Endpoint 分层

适合保留为只读命令的 endpoint 应满足：

- 能回答稳定用户任务，而不是暴露平台内部菜单。
- 默认输出可以被 agent 一眼读懂，不 dump 全量 raw JSON。
- 结果是证据、来源、有效期、覆盖范围或下一步动作提示。
- 不触发授权、回收、保存、提交、审批、生成、上传或缓存刷新。

当前建议分层：

| 层级 | 代表能力 | 处理方式 |
| --- | --- | --- |
| 开发前置 | 当前用户表权限、调度主题表权限 | 主动入口，保持简洁结论 |
| 诊断解释 | 角色搜索、角色成员、主题基础策略、当前用户可选主题 | 放在 `szdata_detail`，只读，默认摘要，`--detail` 才展开 |
| 历史/归档 | 角色画像大杂烩、SQL/表权限包装检查、低价值 endpoint 探察 | 不主动暴露 |
| 禁止默认开放 | 保存、提交、授权、回收、审批、上传、缓存刷新 | 不做生产只读命令 |

## 维护提醒

后续新增权限类命令时，先问五个问题：

1. 用户是在完成开发前置主工作流，还是解释已有状态？
2. 输入对象是业务主对象（如 `db.table` / 调度主题），还是诊断对象（如 `roleId` / 规则 / 申请单）？
3. 输出是可执行结论和下一步动作，还是证据、来源、历史和规则解释？
4. 是否涉及写入或生命周期动作？
5. 是否过慢、已替代、推断链太长或容易误导？

能回答开发前置主问题的命令进入 `szdata` 主入口；只能解释来源的命令进入诊断面；过慢、已替代或容易误导的命令归档。
