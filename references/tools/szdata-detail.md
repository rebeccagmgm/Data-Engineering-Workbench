# szdata_detail / szdatatest_detail

Date: 2026-07-06

`szdata_detail` is the production diagnostics, audit, and explanation surface
for SZData CLI. `szdatatest_detail` is the same low-frequency diagnostics
surface for the test environment. Both expose normal flat OpenCLI wrapper files
under `C:\Users\13246\.opencli\clis\<surface>\` and import selected
low-frequency read-only implementations from shared core without exposing them
as `szdata` / `szdatatest` public commands.

Use `opencli szdata_detail --help` and `opencli szdatatest_detail --help` for
command lists. These detail commands should not appear in `opencli szdata
--help` or `opencli szdatatest --help`.

Use [szdata-command-landscape.md](./szdata-command-landscape.md) as the global command ledger.

## Wrapper Shape

`szdata_detail` and `szdatatest_detail` are normal OpenCLI site adapter folders
whose root command files are thin wrappers. The previous external router and
direct-call compatibility scripts have been removed.

```text
C:\Users\13246\.opencli\clis\szdata_detail\*.js
C:\Users\13246\.opencli\clis\szdatatest_detail\*.js
C:\Users\13246\.opencli\shared\szdata-core\commands\<domain>\...
C:\Users\13246\.opencli\shared\szdata-core\audit-surfaces.mjs
```

List active detail commands:

```powershell
opencli szdata_detail --help
opencli szdata_detail <command> --help
opencli szdatatest_detail --help
opencli szdatatest_detail <command> --help
```

The detail surfaces no longer rely on `opencli external` registration or
`C:\Users\13246\.opencli\bin` direct-call scripts.

## When To Use

Use `szdata_detail` for low-frequency diagnostics, audit evidence, history, logs, rules, dictionaries, template readback, SQL history, role members, and wide-table schedule/config readback.

Use `szdata` for high-frequency production workflow: data discovery, table card, task SQL, demand detail, dataset config, wide-table card/detail, and table-permission prechecks.

Use `szdatatest_detail` for the same low-frequency diagnostics against `datatest.gf.com.cn`.

Use `szdatatest` for test validation, field parsing, guard checks, preview/generate/schedule-save test lifecycle actions, and any write rehearsal.

## Rejected Names

The router rejects archived or renamed commands such as:

- `current-user-data-permission`
- `my-permission-base`
- `my-permission-data`
- `my-permission-function`
- `my-permission-report`
- `role-data-permission`
- `role-summary`
- `scheduling-topic-table-check`
- `table-permission-check`

Use the task-oriented replacements:

- Current login user table access: `opencli szdata table-permission-mine --table db.table -f json`
- Scheduling topic table access: `opencli szdata table-permission-topic --topic TOPIC --table db.table -f json`
- Role table access: `opencli szdata table-permission-role --role-id ROLE_ID --table db.table -f json`

`szdata_detail` and `szdatatest_detail` must not add hidden save, submit, delete, apply, approve, revoke, preview, generate, or schedule-save flows.
