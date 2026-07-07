# Dataset Save Flow Spec

This spec applies to `szdatatest` OpenCLI dataset add/edit/save work for the
Data Engineering Workbench. `szdata` is production and remains read-only unless
the user gives explicit production-write authorization after a passing
`szdatatest` validation.

## Scope

- Dataset management page: `/positionSwitch/config`.
- OpenCLI adapter source: `C:\Users\13246\.opencli\clis\szdatatest`.
- Ordinary dataset command: `opencli szdatatest dataset-create`.
- Output-column command: `opencli szdatatest dataset-create-columns`.

## UI Contract

Adding or editing a SQL dataset follows this UI order:

1. Fill the dataset base fields.
2. Enter SQL.
3. Click `获取输出列`.
4. Review or complete the output field rows.
5. Save, or save and preview when that button exists for the selected usage.

The CLI must preserve this contract. It must not save a SQL dataset by sending
SQL plus hand-authored fields while skipping output-column parsing.

## Output Columns

- SQL output-column parsing must use the same effective route as the UI
  `获取输出列` action.
- Current verified route: `/developservice/positionSwitch/analysis/sql.json`.
- `dataSetConfig/sqlInfo.json` is not the output-column parser for usage
  `3`/`5`; it can return a dataset metadata shell with no fields.
- `dataset-create-columns --sql` and `dataset-create-columns --sql-file` must return parsed
  field names before any save-capable command may write.
- `--fields-json` and `--fields-file` are override sources only. They may fill
  aliases, field type, data type, length, precision, tags, or dimension fields
  for already-parsed rows. They must not replace a failed or empty
  `获取输出列` result in save mode.

## Usage Types

| usageType | Meaning | Ordinary `dataset-create --save` |
|---|---|---|
| `1` | 持仓转换 / ordinary SQL dataset path | Allowed in `szdatatest` after output-column parsing and validation |
| `2` | 离线指标生成 | Treat as non-wide-table dataset save unless a later spec narrows it |
| `3` | 离线宽表配置 | Blocked in ordinary `dataset-create --save`; use dedicated wide-table command |
| `4` | 实时指标生成 | Treat as non-wide-table dataset save with `dataEngine` validation |
| `5` | 实时宽表配置 | Blocked in ordinary `dataset-create --save`; use dedicated wide-table command |

The `3`/`5` restriction is not a platform claim that wide-table configs cannot
be saved. It is a CLI safety boundary: ordinary `dataset-create --save` must
not hide a wide-table lifecycle write. Dedicated wide-table commands may save
`3`/`5` when they are explicit, test-only by default, and guarded.

## Save Preconditions

Before any platform save in `szdatatest`:

- SQL source is exactly one of `--sql` or `--sql-file`.
- Output-column parsing returned at least one field.
- No parsed row has an empty `fieldName`.
- Required base fields are present: name, usageType, tech director, developer.
- Partition fields such as `busi_date`, `busi_mon`, and `busi_year` remain at
  the end when marked `PARTITION_FIELD`.
- Field alias byte length does not exceed the platform limit.
- Realtime usage `4`/`5` has `dataEngine`.
- Wide-table usage `3`/`5` includes `indicatorSystemInfo` in dry-run payloads,
  but ordinary `dataset-create --save` still refuses to write them.

## Verification

Use bounded, non-production checks:

```powershell
node --check C:\Users\13246\.opencli\shared\szdata-core\commands\dataset\shared.js
node --check C:\Users\13246\.opencli\shared\szdata-core\commands\dataset\dataset-create-columns.js
node --check C:\Users\13246\.opencli\shared\szdata-core\commands\dataset\dataset-create.js
opencli szdatatest dataset-create-columns --sql "select 1 as codex_preview_probe" --usage-type 3 -f json
opencli szdatatest dataset-create-guard-check -f json
```

Run actual `--save` only when the user authorizes a concrete `szdatatest`
sample/action. Never run a production `szdata` write from this spec alone.
