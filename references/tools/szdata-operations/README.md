# szdata-operations

Updated: 2026-07-07

This directory holds operation-specific SZData procedures, read-only investigations, and durable evidence notes. The global command map remains [../szdata-command-landscape.md](../szdata-command-landscape.md), and day-to-day routing starts from [../szdata.md](../szdata.md).

## Scope

- Write-operation design, dry-run, test validation, production authorization boundaries.
- Dataset, wide-table, gather subtask, modeling subtask, scheduling, and permission workflows.
- Read-only endpoint evidence and command parity reports.
- Historical investigation reports are background only; they do not override the active command map.

Do not maintain a second full command list here. If command ownership changes, update the global ledger first and then update only the affected operation note.

## Read Order

| Scenario | First read | Then read |
| --- | --- | --- |
| Unsure which command to use | [../szdata-command-landscape.md](../szdata-command-landscape.md) | [../szdata.md](../szdata.md) |
| Auditing or optimizing SZData CLI | [../szdata-agent-cli-audit.md](../szdata-agent-cli-audit.md) | [../opencli.md](../opencli.md), live adapter `COMMANDS.md` |
| Editing OpenCLI adapters | [../opencli.md](../opencli.md) | live adapter `COMMANDS.md` |
| Dataset save or field parsing | [specs/dataset-save-flow.md](./specs/dataset-save-flow.md) | [dataset-create.md](./dataset-create.md), [dataset-detail-fields.md](./dataset-detail-fields.md) |
| Wide-table preview/generate/schedule save | [specs/wide-table-lifecycle.md](./specs/wide-table-lifecycle.md) | [wide-table-management.md](./wide-table-management.md) |
| Demand and subtask read/write planning | [demand-routing.md](./demand-routing.md) | [subtask-gather-create.md](./subtask-gather-create.md), [subtask-gather-update.md](./subtask-gather-update.md) |
| Permission diagnostics | [../szdata-command-landscape.md](../szdata-command-landscape.md) | [role-permission-readonly.md](./role-permission-readonly.md), [scheduling-permission-readonly.md](./scheduling-permission-readonly.md) |
| MCP feature coverage and schedule wrappers | [mcp-cli-coverage-report.md](./mcp-cli-coverage-report.md) | live adapter `COMMANDS.md` |
| SQL 诊断行为 | [sql-diagnosis-behavior.md](./sql-diagnosis-behavior.md) | [mcp-cli-coverage-report.md](./mcp-cli-coverage-report.md) |

## Document Index

| Document | Purpose | Status |
| --- | --- | --- |
| [mcp-cli-coverage-report.md](./mcp-cli-coverage-report.md) | Live MCP inventory vs direct Data Portal CLI coverage, including partial gaps | active |
| [sql-diagnosis-behavior.md](./sql-diagnosis-behavior.md) | Direct Portal `sql-diagnosis` 行为、实测规则边界和安全说明 | active/read-only |
| [demand-routing.md](./demand-routing.md) | Decide whether a demand needs gather subtask, modeling subtask, dataset work, or read-only investigation | active |
| [subtask-gather-create.md](./subtask-gather-create.md) | New gather subtask flow | active |
| [subtask-gather-update.md](./subtask-gather-update.md) | Gather subtask update flow | active |
| [dataset-create.md](./dataset-create.md) | Ordinary SQL dataset test creation, field parsing, guard, and save boundary | active |
| [dataset-detail-fields.md](./dataset-detail-fields.md) | Dataset detail fields, options, linkages, and button behavior | active |
| [dataset-configuration-profile.md](./dataset-configuration-profile.md) | Existing dataset configuration profile and usageType/sceneType summary | active/read-only |
| [wide-table-management.md](./wide-table-management.md) | Wide-table list, detail, preview, generation, schedule config, and status rules | active |
| [role-permission-readonly.md](./role-permission-readonly.md) | Role/member/table-permission read-only diagnostics | active |
| [scheduling-permission-readonly.md](./scheduling-permission-readonly.md) | Scheduling topic, topic user base policy, and topic table-permission evidence | active |
| [bearer-access-survey.md](./bearer-access-survey.md) | Bearer-only direct-access classification for selected paths | active/read-only |
| [mcp-cli-function-comparison.md](./mcp-cli-function-comparison.md) | Current full-function comparison across `szdata` CLI and Data Portal metadata/schedule/sql_dignose MCP servers | active/read-only |
| [my-permission-readonly.md](./my-permission-readonly.md) | Historical My Permission snapshot; `my-permission-*` active entrypoints were removed | historical |
| [permissionservice-readonly-survey.md](./permissionservice-readonly-survey.md) | Historical `/permissionservice` survey | historical |
| [_template.md](./_template.md) | Template for new operation notes | template |

## Active Command Boundaries

| Domain | High-frequency entrypoints | Low-frequency/detail | Test or write-precheck |
| --- | --- | --- | --- |
| Dataset | `szdata dataset-config` | `szdata_detail` / `szdatatest_detail`: `dataset-config-dict`, `dataset-sql-versions`, `dataset-templates`, `dataset-indicator-sql` | `szdatatest dataset-create-columns`, `dataset-create-current-user`, `dataset-create`, `dataset-create-guard-check` |
| Wide table | `szdata widetable`, `widetable-detail` | `widetable-explain`, `widetable-action-log`, `widetable-schedule-config`, `widetable-schedule-detail` | `szdatatest wide-table-preview-test`, `wide-table-generate-test`, `wide-table-schedule-save-test`, `wide-table-schedule-validate` |
| Task, demand, schedule | `task-sql`, `schedule-detail`, `schedule-mcp-dependencies`, `schedule-mcp-run-instances`, `schedule-mcp-run-states`, `schedule-mcp-owner-failed-instances`, `schedule-mcp-run-logs`, `demand-list`, `demand-detail` | `demand-subtask-list`, `demand-subtask-detail`, `demand-mine`, `demand-stats` | `subtask-gather-create`, `subtask-gather-update`, `subtask-modeling-create` must start with dry-run and test validation |
| SQL 支持 | `sql-diagnosis` | [sql-diagnosis-behavior.md](./sql-diagnosis-behavior.md) | 不是写入路径；不是 MCP SQL diagnosis 精确等价；不是表权限结论 |
| Subtask candidates | `subtask-source-system-list`, `subtask-access-point-list` | - | Read-only candidates; default output hides connection details |
| Permission | `table-permission-mine`, `table-permission-topic`, `table-permission-role` | `role-list`, `role-user-list`, `scheduling-topic-*` | Same read-only checks may be mirrored in `szdatatest` when needed |

## Hard Boundaries

- These notes do not authorize any production write.
- Production writes on `szdata` require `szdatatest` validation plus explicit user authorization.
- `szdatatest` mirrors must keep argument shape, default output, and semantics aligned with the `szdata` command they mirror.
- `szdatatest_detail` mirrors must keep command inventory aligned with `szdata_detail`.
- `subtask-access-point-list` must not expose connection host/port details by default.
- Retired `my-permission-*` and old subtask aliases are not active agent entrypoints.
- Schedule runtime/log parity commands in `szdata` now use explicit `schedule-mcp-*` names because the user authorized MCP-backed wrappers for this subset.

## Generic Write Flow

1. Read current state through demand, subtask, dataset, or wide-table readback.
2. Build a dry-run payload without saving platform state.
3. Validate form/save/submit/preview/generate/schedule-save behavior in `szdatatest`.
4. Get explicit user authorization for the exact production action.
5. Execute only the authorized production action.
6. Verify by downstream page or follow-up readback, not just HTTP 200.

## Maintenance Rules

- Start new operation docs from [_template.md](./_template.md).
- Update [../szdata-command-landscape.md](../szdata-command-landscape.md) before local operation notes when command ownership changes.
- Mark historical investigations as historical; do not let them override the active command map.
- Keep secrets, cookies, tokens, connection details, and raw logs out of durable docs.
