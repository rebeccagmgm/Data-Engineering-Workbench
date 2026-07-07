# szdata

`szdata` is the production OpenCLI entrypoint for Data Portal read-only work on `data.gf.com.cn`. The live adapter source is not this workbench repository:

```text
C:\Users\13246\.opencli\clis\szdata
C:\Users\13246\.opencli\clis\szdatatest
```

This repository stores durable rules, command maps, and investigation reports. When command behavior changes, update this file, [szdata-command-landscape.md](./szdata-command-landscape.md), the relevant operation note, and the live adapter `COMMANDS.md`.

## Environment Boundary

- `szdata`: production read-only confirmations and high-frequency workflow commands.
- `szdatatest`: test-environment mirrors, guard checks, field parsing, and explicit test write probes.
- `szdata_detail`: production low-frequency diagnostics, audit views, explanations, history, logs, and large detail surfaces.
- `szdatatest_detail`: test low-frequency diagnostic mirror of `szdata_detail`.
- Production writes require a passing `szdatatest` validation and explicit user authorization for the exact action.

## Read First

| Goal | Read |
| --- | --- |
| Choose the right command | [szdata-command-landscape.md](./szdata-command-landscape.md) |
| Audit or optimize SZData CLI | [szdata-agent-cli-audit.md](./szdata-agent-cli-audit.md) |
| Edit live OpenCLI adapters | [opencli.md](./opencli.md) and live adapter `COMMANDS.md` |
| Dataset, wide-table, subtask, or schedule operation details | [szdata-operations/README.md](./szdata-operations/README.md) |
| MCP-to-CLI coverage and schedule MCP wrappers | [szdata-operations/mcp-cli-coverage-report.md](./szdata-operations/mcp-cli-coverage-report.md) |
| Four-surface consistency audit | `node C:\Users\13246\.opencli\shared\szdata-core\audit-surfaces.mjs --plain` |

## Common Routes

| User question | Preferred command | Notes |
| --- | --- | --- |
| Known `db.table`, what is this table? | `opencli szdata table --db <db> --table <table> -f json` | Use `table-ddl` for full DDL, `table-lineage` for lineage. |
| Keyword, Chinese name, or business term only | `opencli szdata table-search --keyword <keyword> -f json` | Then verify candidates with `table` or `table-detail`. |
| Known GUID, need metadata/DDL/lineage/sample | `table-detail` / `table-ddl` / `table-lineage` / `table-sample` | Keep sample rows bounded. |
| Known Horae task id, need SQL evidence | `opencli szdata task-sql --task-id <id> -f json` | Does not prove runtime success or data correctness. |
| Known Horae task id, need schedule config | `schedule-detail` | Direct Data Portal `prod-api`; use MCP commands below for runtime/dependency parity. |
| Need schedule upstream/downstream dependencies | `schedule-mcp-dependencies` | MCP-backed wrapper for `schedule.get_task_dependencies`; requires `SZDATA_X_PERSONAL_TOKEN`. |
| Known task id and date range, need run instances/states | `schedule-mcp-run-instances` / `schedule-mcp-run-states` | MCP-backed wrappers for schedule runtime state. |
| Need owner/date failed-instance worklist | `schedule-mcp-owner-failed-instances` | MCP-backed wrapper for owner failed instances. |
| Need runtime logs for one task/date | `schedule-mcp-run-logs` | MCP-backed wrapper; full log bodies are hidden by default, use bounded `--log-preview` for snippets. |
| 需要 SQL 文本诊断 | `sql-diagnosis` | Direct Data Portal SQL exploration 检查；见 [sql-diagnosis-behavior.md](./szdata-operations/sql-diagnosis-behavior.md)。它不是 SQL 执行，也不是当前登录用户表权限结论。 |
| Need demand or subtask readback | `demand-list` / `demand-detail`; detail-only subtask commands in `szdata_detail` | Read current state before any write planning. |
| Can the current login user read a table? | `table-permission-mine --table db.table -f json` | For scheduling topic or role, use `table-permission-topic` / `table-permission-role`. |
| Dataset config readback | `dataset-config --id <id> -f json` | SQL bodies remain bounded unless preview/save flags are explicit. |
| Wide-table readback | `widetable` / `widetable-detail` | Logs and schedule config explanations stay in `szdata_detail`. |
| Gather/model subtask candidate lookup | `subtask-source-system-list` -> `subtask-access-point-list` | Candidate lookup is read-only; write commands default to dry-run. |

## Naming Rules

- Table assets use `table-*`.
- Table permissions use `table-permission-*`, with the subject at the suffix: `mine`, `topic`, or `role`.
- Schedule task diagnostics use `schedule-*`; explicit MCP-backed schedule wrappers use `schedule-mcp-*`.
- Runtime schedule parity commands in `szdata` are explicit MCP wrappers because the user approved this route for the schedule subset.
- Dataset commands use `dataset-*`; test parsing and write guards stay in `szdatatest`.
- Wide-table commands use `widetable-*` for readback and `wide-table-*-test` for explicit test-environment lifecycle probes.
- Subtask commands use `subtask-*`; production write paths must be clearly named and authorized.

## Output Rules

- Main commands default to compact cards and bounded previews.
- Long SQL, DDL, logs, person lists, field lists, and raw payloads require a dedicated command or explicit flag.
- Avoid returning infrastructure details such as connection hosts, ports, tokens, cookies, or data-source internals.
- A command appearing in `--help` proves registration only; behavior must be verified with bounded `-f json` smoke tests and readback.

## Not Proven By These Commands

- A task instance actually produced correct business data.
- A sample row represents full reconciliation truth.
- Demand, dataset, or wide-table configuration status equals downstream job success.
- A missing search result proves the table does not exist.
- `schedule-mcp-run-logs` does not print full runtime-log bodies by default; it reports availability, character counts, and bounded previews only.

## Topic Docs

- [opencli.md](./opencli.md): adapter location, command discovery, editing, and verification rules.
- [szdata-command-landscape.md](./szdata-command-landscape.md): global command ownership ledger.
- [szdata-detail.md](./szdata-detail.md): `szdata_detail` boundary.
- [szdata-operations/README.md](./szdata-operations/README.md): operation-specific index.
- [szdata-operations/mcp-cli-coverage-report.md](./szdata-operations/mcp-cli-coverage-report.md): direct-endpoint coverage review for the MCP inventory.
- [szdata-operations/sql-diagnosis-behavior.md](./szdata-operations/sql-diagnosis-behavior.md): `sql-diagnosis` 行为、实测规则边界和安全说明。
- [szdata-operations/dataset-create.md](./szdata-operations/dataset-create.md): ordinary SQL dataset test creation and guard flow.
- [szdata-operations/wide-table-management.md](./szdata-operations/wide-table-management.md): wide-table readback, preview, generation, and schedule configuration.
- [szdata-operations/role-permission-readonly.md](./szdata-operations/role-permission-readonly.md): role and permission read-only diagnostics.
