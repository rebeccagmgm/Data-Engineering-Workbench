# My Permission readonly investigation

Date: 2026-07-05

Status: historical. The `my-permission-base`, `my-permission-function`, and
`my-permission-report` OpenCLI entries were removed from active `szdata`,
`szdatatest`, and `szdata_detail` routing on 2026-07-06 because they were weak
signals for the permission-and-subject diagnosis workflow.

Use this document only as background evidence for how the My Permission page was
previously explored. Do not choose `my-permission-*` for new agent workflows.

## Active Replacement

For current-login table access, use the task-oriented verdict command:

```powershell
opencli szdata table-permission-mine --table db.table -f json
```

`table-permission-mine` reads the My Permission data-permission page evidence
for one target table and returns a compact verdict card:

- `user`
- `table`
- `status`
- `matchedBy`
- `validity`
- `sourceTypes`
- `roles`
- `packages`

Status meanings:

- `PASS`: an active exact table grant or active whole-database grant was found.
- `EXPIRED`: matching rows exist, but none are currently effective.
- `NO`: the page readback returned no matching table/database grant.
- `UNKNOWN`: the command could not collect enough evidence.

`matchedBy=database` means the table is covered by a whole-database grant from
the My Permission page, even if the exact table row is absent or expired.

## Removed Entries

These commands are no longer active entries:

```text
my-permission-base
my-permission-function
my-permission-report
```

Reasons:

- `my-permission-base` only produced a current-account role/group/rule/entrust
  snapshot and did not answer whether any target table is readable.
- `my-permission-function` described menu/function visibility, not data access.
- `my-permission-report` described report/product visibility, not table access.

For role subjects, use `role-list`, `role-user-list`, and
`table-permission-role`. For scheduling subjects, use
`scheduling-topic-list-by-current-user`, `scheduling-topic-base-policy`, and
`table-permission-topic`.

## Historical Samples

Earlier production read-only samples showed:

- `table-permission-mine --table pdata_n.t03_otc_swap_comp_info` returned
  `PASS`, `matchedBy=table`, with role sources valid from 2026-03-27 /
  2026-04-20 to 2027-03-27 / 2027-04-20.
- `my-permission-function --keyword 数据地图 --size 3` returned menu rows under
  `数据查询 / 数据地图`.
- `my-permission-report --size 3` returned `totalAvailable=108`.

The latter two samples are retained only as historical page-shape evidence.
