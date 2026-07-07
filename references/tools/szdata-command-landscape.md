# SZData CLI Command Landscape

Updated: 2026-07-07

This is the global command ledger for `szdata`, `szdata_detail`, `szdatatest`, `szdatatest_detail`, and archived surfaces. It does not replace per-command `--help`; it answers where a command belongs, when to choose it, and what it must not be used to prove.

## Principles

- High-frequency production read-only workflows belong in `szdata`.
- Test validation, field parsing, guards, and explicit test write probes belong in `szdatatest`.
- Low-frequency diagnostics, audit, explanations, history, logs, and large detail surfaces belong in `szdata_detail`.
- `szdatatest_detail` mirrors `szdata_detail` for test low-frequency diagnostics.
- `szdatatest` commands with the same name as `szdata` commands must preserve argument shape, default output, and semantics.
- Retired, slow, risky, or misleading commands belong in `archive` or are rejected as agent entrypoints.
- Main commands default to compact summaries; long SQL, DDL, logs, person lists, field lists, and raw evidence require dedicated commands or explicit flags.

## Surface Boundaries

| Surface | Role | Use it for | Do not use it for |
| --- | --- | --- | --- |
| `szdata` | Production main workflow | Asset discovery, table verification, task SQL, schedule readback, demand readback, dataset/wide-table readback, pre-development permission checks | Default production writes, low-frequency large diagnostics |
| `szdata_detail` | Production diagnostic/detail surface | Dictionaries, SQL history, templates, personal views, role members, scheduling policy, wide-table logs/config detail | Writes or primary pre-development decisions |
| `szdatatest` | Test validation surface | Test mirrors, field parsing, guards, explicit test lifecycle probes | Production truth or unstated writes |
| `szdatatest_detail` | Test diagnostic/detail mirror | Test dictionaries, SQL history, templates, role members, scheduling policy, wide-table logs/config detail | Test lifecycle writes |
| `archive` | Retired/risky history | Historical source for old implementations | Agent-selected active workflows |

Shared implementation lives under `C:\Users\13246\.opencli\shared\szdata-core\commands\`. Run the consistency audit with:

```text
node C:\Users\13246\.opencli\shared\szdata-core\audit-surfaces.mjs --plain
```

## Task Domains

| Domain | User question | Main entrypoints | Detail/low-frequency | Avoid/archive | Boundary |
| --- | --- | --- | --- | --- | --- |
| 1. Data asset discovery | I know a keyword, GUID, or `db.table`; how do I find or verify the asset? | `table`, `table-search`, `table-guid`, `table-detail`, `table-ddl`, `table-lineage`, `table-sample`, `indicator`, `tagdim` | - | Old aliases such as `dms`, `guid`, `table-info`, `sample`, `lineage` | Find tables, verify structure, DDL, lineage, and bounded sample evidence. |
| 2. Task, demand, and schedule | I know a task id, demand, or subtask; how do I read current state, SQL, schedule config, dependencies, run states, or failed instances? | `task-sql`, `schedule-detail`, `schedule-mcp-dependencies`, `schedule-mcp-run-instances`, `schedule-mcp-run-states`, `schedule-mcp-owner-failed-instances`, `schedule-mcp-run-logs`, `demand-list`, `demand-detail` | `demand-subtask-list`, `demand-subtask-detail`, `demand-mine`, `demand-stats` | `etl-sql`; retired partial direct schedule runtime wrappers | Schedule runtime parity uses explicit MCP wrappers; full log bodies remain bounded by default. |
| 3. Permission and subject diagnostics | Can the current user/topic/role read a target table? Who is in a role? Which topics are available? | `table-permission-mine`, `table-permission-topic`, `table-permission-role` | `role-list`, `role-user-list`, `scheduling-topic-list-by-current-user`, `scheduling-topic-base-policy` | `current-user-data-permission`, `my-permission-*`, `role-data-permission`, `role-summary`, `scheduling-topic-table-check`, `table-permission-check` | Final table-permission answers use `table-permission-*`; role/topic commands explain subjects and policies. |
| 4. Dataset readback and test config | How do I read dataset config, SQL versions, templates, dictionaries, or parse fields before a write? | `dataset-config` | `dataset-config-dict`, `dataset-sql-versions`, `dataset-templates`, `dataset-indicator-sql` | - | Production readback stays compact; test parsing and guards stay in `szdatatest`. |
| 5. Wide-table management | How do I read wide-table status, generated detail, logs, or schedule config? | `widetable`, `widetable-detail` | `widetable-explain`, `widetable-action-log`, `widetable-schedule-config`, `widetable-schedule-detail` | Historical config-save probes | Test preview/generate/schedule-save probes use explicit `wide-table-*-test` names. |
| 6. Subtask write support | How do I find source systems or access points before gather/modeling subtask work? | `subtask-source-system-list`, `subtask-access-point-list`, `subtask-gather-create`, `subtask-gather-update`, `subtask-modeling-create` | - | Old `create-subtask`, `update-subtask`, `create-model-subtask`, `list-source-systems`, `list-access-points` | Write commands default to dry-run and require readback, test validation, and user authorization. |
| 7. Support | How do I log in, search help, or run a bounded SQL check? | `login`, `sql-diagnosis` | `portal-help` | - | `sql-diagnosis` is a direct Data Portal risk/auth check, not exact MCP table-existence diagnosis parity. |

## Data Asset Discovery

| Command | Default output | Choose when | Does not answer |
| --- | --- | --- | --- |
| `table` | Compact identity, structure, ownership, tasks, lineage, sample note | Known `db.table`; need a quick asset card | Full DDL, full metadata tree, full lineage |
| `table-search` | Candidate table metadata | Keyword, Chinese name, or business term only | Final table verification |
| `table-guid` | GUID and identity bridge | Known `db.table`; next command requires GUID | Full answer to a business question |
| `table-detail` | Flattened metadata detail | Known GUID; need ownership/status/source-task/permission summary | Sample rows or full lineage rows |
| `table-ddl` | DDL and structural evidence | Need create-table statement, field types, partition evidence | Business-level validation |
| `table-lineage` | Upstream/downstream lineage rows | Need lineage evidence | Quick table card |
| `table-sample` | Bounded sample rows | Need a few rows for inspection | Reconciliation truth or full dataset proof |

## Task, Demand, And Schedule

| Command | Default output | Choose when | Does not answer |
| --- | --- | --- | --- |
| `task-sql` | Task SQL evidence and limitations | Known Horae task id; need create/query SQL | Runtime success or data correctness |
| `schedule-detail` | Schedule task card, cycle, owner summary, SQL preview | Known task id; need Data Portal schedule config | Runtime instances or full logs |
| `schedule-mcp-dependencies` | Upstream/downstream dependency shape from MCP | Need schedule dependency parity | Direct Portal-only dependency proof |
| `schedule-mcp-run-instances` | Runtime instances from MCP | Need run instance parity over a date range | Business-data correctness |
| `schedule-mcp-run-states` | Runtime states from MCP | Need state history by task/date range | Business-data correctness |
| `schedule-mcp-owner-failed-instances` | Owner/date failed-instance worklist from MCP | Need failed worklist by owner and data date | Full downstream remediation state |
| `schedule-mcp-run-logs` | Runtime log metadata/counts/bounded previews from MCP | Need log availability and bounded log evidence | Printing complete log bodies by default |
| `demand-list` | Demand candidates | Search demands by keyword/status/owner | Full demand content |
| `demand-detail` | Demand detail | Known demand UUID; need current state | Create or advance a demand |
| `demand-subtask-list` | Subtask list | Known demand UUID; need subtasks | Full single-subtask fields |
| `demand-subtask-detail` | Subtask detail | Known subtask UUID; need source/data-source/status detail | Modify a subtask |
| `demand-mine` | Personal demand view | Low-frequency personal view | Demand search main entrypoint |
| `demand-stats` | Status statistics and top owners | Low-frequency stats view | Single-demand truth |

## Permission And Subject Diagnostics

| Command | Default output | Choose when | Do not use it for |
| --- | --- | --- | --- |
| `table-permission-mine` | User, table, status, matched source, validity | Current login user vs target table | Role or topic explanation |
| `table-permission-topic` | Topic, table, conclusion, matched source | Scheduling topic vs target table | Current user permission |
| `table-permission-role` | Role, table, conclusion, matched source | Role vs target table | Broad role inventory |
| `role-list` | Role candidates | Need role id by role name | Table-permission verdict |
| `role-user-list` | Role members | Need members of one role | Reverse user-to-role lookup |
| `scheduling-topic-list-by-current-user` | Available scheduling topics | Need selectable topics | Topic table-permission verdict |
| `scheduling-topic-base-policy` | Topic user base policy summary | Need policy explanation | Final table-permission verdict |

## Dataset And Wide Table

| Command | Output rule | Choose when | Boundary |
| --- | --- | --- | --- |
| `dataset-config` | Filters empty values and `"-"` by default; SQL only by explicit preview/save flags | Read production/test dataset config | Does not save config |
| `dataset-config-dict` | No raw by default | Check dictionaries such as usageType, dataType, sceneType | Does not parse SQL fields |
| `dataset-sql-versions` | Version list first; SQL preview only when requested | Check SQL history/version diff | Does not prove task success |
| `dataset-templates` | Template list first; SQL preview by id | Check dataset templates | Not ordinary config readback |
| `dataset-indicator-sql` | Bounded SQL preview | Indicator-system wide-table SQL parameter investigation | Does not complete the full indicator selection flow |
| `dataset-create-columns` | Test field parser | Parse SQL/table output fields before save | Does not save |
| `dataset-create-guard-check` / `dataset-create` | Test guard/dry-run/explicit save | Validate ordinary SQL dataset creation in test | Blocks hidden usage 3/5 wide-table lifecycle writes |
| `widetable` | Wide-table cards | Search wide tables or reverse lookup by task id | Does not read full schedule config |
| `widetable-detail` | Generated wide-table detail | Known UUID/dataSetConfigId | Does not prove runtime success |
| `widetable-action-log` | Bounded logs, raw only on request | Inspect flow logs | Not main entrypoint |
| `widetable-schedule-detail` | Bounded SQL preview | Known Horae task id; read DispatchTaskConfig | Does not save schedule |
| `widetable-schedule-config` | Bounded SQL preview | Known wide-table UUID; read local/upgrade config echo | Does not submit upgrade |
| `wide-table-preview-test` / `wide-table-generate-test` / `wide-table-schedule-save-test` / `wide-table-schedule-validate` | `szdatatest`, explicit dry-run/read-only/execute semantics | Test wide-table lifecycle behavior | No production writes |

## Support

| Command | Choose when | Boundary |
| --- | --- | --- |
| `login` | Session expired, 401, token/session abnormal | Session helper only |
| `portal-help` | Search Help Center content | Read-only help search, not command verification |
| `sql-diagnosis` | Need direct Data Portal SQL risk/auth check | Partial MCP parity; missing-table diagnosis was not reproduced by the verified direct endpoint |

## Current Evidence Notes

- The 2026-07-07 MCP coverage review is recorded in [szdata-operations/mcp-cli-coverage-report.md](./szdata-operations/mcp-cli-coverage-report.md).
- `schedule-mcp-*` commands are explicit MCP-backed wrappers approved for schedule runtime parity.
- The prior partial direct wrappers (`schedule-dependencies`, `schedule-run-instances`, `schedule-run-states`, `schedule-owner-failed-instances`, `schedule-run-logs`) were removed from active `szdata` discovery and archived on 2026-07-07.
- `sql-diagnosis` is intentionally marked partial because the verified direct SQL exploration endpoint does not match MCP table-existence behavior.
