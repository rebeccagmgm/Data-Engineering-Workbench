# MCP To SZData CLI Coverage Report

Date: 2026-07-07

Scope: compare the live MCP inventory for Data Portal metadata, schedule, and SQL diagnosis against the local `szdata` / `szdata_detail` CLI surfaces. This report focuses on current active CLI routing after the schedule MCP wrapper decision.

## Ground Rule

For the schedule runtime subset, the user explicitly approved direct MCP-backed CLI wrappers. These are named with the `schedule-mcp-*` prefix so they are not confused with direct Portal endpoints.

## Live MCP Inventory Observed

| MCP server | Tool | Current CLI status |
| --- | --- | --- |
| `metadata` | `metadata.search_table` | Covered by `szdata table-search` / `table-guid` |
| `metadata` | `metadata.get_table_ddl` | Covered by `szdata table-ddl` |
| `metadata` | `metadata.search_by_es` | Covered/partial by `szdata table-search`; filter parity should be checked per use case |
| `metadata` | `metadata.query_assistant_dify` | Not CLIized; not currently recommended as deterministic CLI surface |
| `metadata` | `metadata.get_table_by_guid` | Covered by `szdata table-detail` |
| `metadata` | `metadata.get_table_lineage_info` | Covered by `szdata table-lineage` |
| `schedule` | `schedule.get_schedule_detail` | Covered by `szdata schedule-detail` |
| `schedule` | `schedule.get_task_dependencies` | Covered by `szdata schedule-mcp-dependencies` |
| `schedule` | `schedule.get_task_run_instances` | Covered by `szdata schedule-mcp-run-instances` |
| `schedule` | `schedule.get_task_run_states` | Covered by `szdata schedule-mcp-run-states`; datetime shape has live smoke coverage |
| `schedule` | `schedule.get_task_run_logs` | Covered by `szdata schedule-mcp-run-logs`; full log bodies hidden by default |
| `schedule` | `schedule.get_owner_failed_instances` | Covered by `szdata schedule-mcp-owner-failed-instances` |
| `schedule` | `metadata.get_horae_sql_by_task_id` | Covered by `szdata task-sql` |
| `sql_dignose` | `query.sql_diagnosis` | Still partial via `szdata sql-diagnosis`; no MCP-backed SQL command added in this round |

## Active Schedule Commands

| Command | Backend class | Evidence level |
| --- | --- | --- |
| `schedule-detail` | Direct Data Portal `prod-api` | `portal_schedule_detail` |
| `schedule-mcp-dependencies` | Data Portal MCP | `mcp_schedule_get_task_dependencies` |
| `schedule-mcp-run-instances` | Data Portal MCP | `mcp_schedule_get_task_run_instances` |
| `schedule-mcp-run-states` | Data Portal MCP | `mcp_schedule_get_task_run_states` |
| `schedule-mcp-run-logs` | Data Portal MCP | `mcp_schedule_get_task_run_logs` |
| `schedule-mcp-owner-failed-instances` | Data Portal MCP | `mcp_schedule_get_owner_failed_instances` |

## Retired Active Commands

The following root wrappers were removed from active `szdata` command discovery and archived under the live OpenCLI archive because they were partial direct probes, not MCP-complete CLI surfaces:

- `schedule-dependencies`
- `schedule-run-instances`
- `schedule-run-states`
- `schedule-run-logs`
- `schedule-owner-failed-instances`

Their shared implementation files may remain as historical direct Portal probes, but they are no longer the recommended active command surface.

## Direct Endpoint Evidence

| Evidence path | Request shape verified | Prior support | Current status |
| --- | --- | --- | --- |
| `/portal/prod-api/developservice/projectSpace/workNode/schedule/listTaskInstance` | Form URL encoded | Prior `schedule-run-instances`, `schedule-run-states`, and instance-existence side of `schedule-run-logs` | Retired from active CLI in favor of explicit MCP wrappers |
| `/portal/prod-api/developservice/horaeFailedTask/page.json` | Form URL encoded | Prior `schedule-owner-failed-instances` | Retired from active CLI in favor of explicit MCP wrapper |
| `/portal/prod-api/developservice/sqlExploration/checkSqlWithAuth.json` | Form URL encoded with `sceneType` and indexed `sqlList` fields | `sql-diagnosis` | Still active; SQL diagnosis MCP wrapper was not added in this schedule-focused round |

No production writes were executed during this evaluation.

## Decisions

- Use explicit `schedule-mcp-*` command names for schedule MCP-backed functionality.
- Keep `schedule-detail` and `task-sql` active because they are established direct/metadata workflows and were not part of the retired runtime set.
- Remove the partial direct runtime wrappers from active `szdata` discovery to avoid misleading command selection.
- Keep full log bodies hidden by default; expose counts and bounded previews only.

## Follow-Up

1. Decide separately whether SQL diagnosis also needs a dedicated `sql-mcp-diagnosis` command.
2. If the retired direct probes are still useful as low-frequency diagnostics, reintroduce them under explicit `*-direct-*` or detail-surface names rather than the old MCP-like names.
