# Wide Table Lifecycle Spec

This spec applies to `usageType=3` and `usageType=5` dataset configurations and
their downstream wide-table lifecycle commands.

## Meanings

- `usageType=3`: offline wide-table configuration.
- `usageType=5`: realtime wide-table configuration.
- `indicatorSystemInfo.isIndicatorSystem=true`: goes through the indicator
  system branch.
- `indicatorSystemInfo.isIndicatorSystem=false`: no-indicator-system branch;
  `sceneType` is required.

## Scene Types

The adapter currently treats `sceneType` values `1` through `7` as platform
rules learned from bundle/sample evidence. Do not invent stricter meanings than
the platform has verified. If a command requires a scene-specific field, name it
explicitly and verify with a real sample.

Known guardrails from the frontend form and sample readback:

- No-indicator-system usage `3`/`5` requires `sceneType`.
- Scene `2` requires `eventField`.
- Scene `3` requires `rectifierUuid` and `rectifierTime`; the frontend also
  checks rectifier remaining quota.
- Scene `4` requires `submittedTo`.
- Scene `7` requires `sceneDescription` and `expectedOfflineTime`.

## Command Boundary

Ordinary `dataset-create --save` must not write usage `3`/`5`. Dedicated
wide-table commands may do so only with explicit names and explicit write
confirmation.

Allowed active command pattern:

- `wide-table-preview-test`: test-only save and PreviewModal readback.
- `wide-table-generate-test`: test-only CreateWideTable generation/readback.

`wide-table-config-save-test` was a historical probe for config save/readback
and is archived. Do not expose it as a current command unless a new design
explicitly needs a standalone config-save lifecycle action.

Required properties for write-capable wide-table commands:

- Site is `szdatatest` unless production write authorization is explicit.
- Default is dry-run.
- Actual write requires an explicit `--execute` style flag.
- Actual write requires a confirmation phrase such as
  `--confirm-test-write YES_TEST_WRITE`.
- The command name must reveal the lifecycle action.
- No hidden calls to `applyUpgrade`, `deactivate`, `delete`, or
  `permitUpgrade`.

## Save And Preview

Save-and-preview is two actions:

1. Save dataset config through the dataset edit route.
2. Execute the PreviewModal `diySql` path and read the preview result.

Success is not an HTTP 200 from the save route. Success requires downstream
readback such as a preview log id, columns, and rows from the result endpoint.
Preview must not create a wide-table definition; verify with
`widetable-detail --data-set-config-id`.

## Generate Wide Table

Generating a wide table is a separate lifecycle action from saving dataset
config. Preconditions:

- Saved usage `3`/`5` dataSetConfigId exists.
- No existing generated wide-table UUID unless the command is explicitly an
  edit/upgrade command.
- Required fields such as demand, database name, Chinese table name, and English
  table name are present.
- `usageType=3` maps to offline generation.
- `usageType=5` maps to realtime generation.

Post-write readback must include:

- `widetable-detail --data-set-config-id <id>`.
- `widetable-detail --uuid <uuid>` when a UUID is returned.
- `widetable --eng <engTable>` or equivalent list lookup.
- `dataset-config --id <id>` to confirm preserved config fields/status.

## Production Boundary

`szdata` is production. Production writes require:

1. Passing `szdatatest` validation for the same action type.
2. User authorization naming the production action and target.
3. A command whose name and flags make the production write unmistakable.

Do not add hidden production write commands.
