# OpenCLI in this workspace

This note is the local orientation for agents working with OpenCLI from the Data Engineering Workbench. It exists to prevent a common mistake: treating this workspace as the adapter source tree.

## Source of truth

The live private OpenCLI adapters for the data platform are outside this workspace:

```text
C:\Users\13246\.opencli\clis\szdata
C:\Users\13246\.opencli\clis\szdatatest
```

This workspace contains skills, references, investigation notes, and temporary artifacts. Use it to understand rules and prior findings. Use the `.opencli\clis\...` directories to inspect or change adapter code.

## Site names and environments

| Site | Environment | Host | Default use |
|---|---|---|---|
| `szdata` | Production | `data.gf.com.cn` | Read-only investigation and production-state checks |
| `szdatatest` | Test | `datatest.gf.com.cn` | Validation of forms, saves, submits, previews, deletes, and generated artifacts |
| `szdata_detail` | Production detail site | `data.gf.com.cn` | Low-frequency diagnostics, audit, explanation, and historical readback |
| `szdatatest_detail` | Test detail site | `datatest.gf.com.cn` | Test-environment mirror of low-frequency diagnostics |

Production writes on `szdata` require prior passing validation in `szdatatest` and explicit user authorization.

Understand SZData CLI as task surfaces rather than a flat command list. The
global source of truth is [szdata-command-landscape.md](./szdata-command-landscape.md);
[szdata-cli-mindmap.md](./szdata-cli-mindmap.md) is only a visual index.
When auditing or optimizing these CLIs, follow
[szdata-agent-cli-audit.md](./szdata-agent-cli-audit.md). It is the SZData
specialization of generic CLI audit ideas and intentionally rejects broad
OpenCLI platform rewrites unless the user asks for that separately.

`szdata` is the high-frequency production workflow surface. `szdata_detail` is
the low-frequency production diagnostics, audit, explanation, and historical
readback surface. `szdatatest_detail` mirrors that detail surface against the
test environment. All four surfaces are visible as normal
`~/.opencli/clis/<surface>/*.js` OpenCLI wrappers. The wrappers stay thin and
import real implementations from
`C:\Users\13246\.opencli\shared\szdata-core\commands\`. See
[szdata-detail.md](./szdata-detail.md).

## Discovery commands

Use the registry instead of guessing command names:

```powershell
opencli list -f json
opencli szdata --help
opencli szdata <command> --help
opencli szdatatest --help
opencli szdatatest <command> --help
opencli szdata_detail --help
opencli szdata_detail <command> --help
opencli szdatatest_detail --help
opencli szdatatest_detail <command> --help
```

For agent work, prefer explicit JSON:

```powershell
opencli szdata dataset-config --usage-type 3 --size 3 -f json
```

Keep output bounded with command-specific flags such as `--size`, `--sql-preview`, `--field-preview`, or keyword filters.

## Adapter layout

Common files in each site directory:

```text
_shared.js              shared HTTP/session helpers
<command>.js            one OpenCLI command per file
*.js                    thin root wrappers that import shared command modules
COMMANDS.md             local command map for the private adapter
```

Command implementations and shared code that must not be scanned as a site
adapter live under
`C:\Users\13246\.opencli\shared\szdata-core\`.

For `szdata` / `szdatatest`, commands normally execute `fetch` inside the logged-in browser session using Portal cookies/token. This is not DOM automation unless a command explicitly says so.

The current OpenCLI private adapter loader scans only the flat
`~/.opencli/clis/<site>/*.js` command directory. For larger adapters such as
`szdata`, `szdatatest`, `szdata_detail`, and `szdatatest_detail`, keep command
entry files flat and thin: root files should only import `command` from
`shared/szdata-core/commands/<domain>/<command-name>.js`, bind the proper
environment with `materializeCommand(...)`, then call `cli(command)`. Put
domain behavior in `shared/szdata-core/commands/`, keep
only `_shared.js` as the cross-command transport/helper re-export, and maintain
`COMMANDS.md` as the local command map. Do not move command entry files into
subdirectories unless the loader has been changed and validated.

## Command placement and naming

- Put high-frequency production workflow commands in `szdata`.
- Put low-frequency diagnostics, audit, explanation, and historical readback in `szdata_detail`.
- Put test validation, write probes, preview/generate lifecycle checks, and pre-production write validation in `szdatatest`.
- Put test-environment low-frequency diagnostics in `szdatatest_detail`; its command list must match `szdata_detail`.
- Put retired, slow, risky, or misleading commands in `archive`.
- Name commands by task family: keep the same prefix for the same question type, and put the subject/dimension at the suffix. Example: `table-permission-mine`, `table-permission-topic`, and `table-permission-role` are one table-permission family with current-user, scheduling-topic, and role dimensions.

## Search rules

When investigating adapter code, search the live adapter directories first:

```powershell
rg "dataSetConfig" C:\Users\13246\.opencli\clis\szdata C:\Users\13246\.opencli\clis\szdatatest
rg --files C:\Users\13246\.opencli\clis\szdata
rg --files C:\Users\13246\.opencli\clis\szdatatest
```

Avoid broad searches over workspace `tmp/`, `_archive/`, browser-state files, and old trace outputs unless the task is explicitly about history. Historical traces can suggest leads, but they are not current adapter code.

## Editing checklist

1. Identify the exact live adapter file under `C:\Users\13246\.opencli\clis\<site>\`.
2. Read the nearby shared helper files before copying patterns.
3. Keep transport/session helpers separate from command parsing and presentation.
4. Preserve existing command arguments where possible; add new flags instead of changing semantics.
5. Default risky commands to dry-run.
6. Do not expose cookies, tokens, internal IPs, ports, gateway details, or full raw payloads in docs or final answers.
7. Use `apply_patch` for manual edits.
8. Run syntax checks on changed JavaScript:

```powershell
node --check C:\Users\13246\.opencli\clis\szdata\<file>.js
node --check C:\Users\13246\.opencli\clis\szdatatest\<file>.js
```

9. Run a small bounded smoke test:

```powershell
opencli szdata <command> --help
opencli szdata <command> --size 1 -f json
```

For write-capable commands, smoke-test dry-run first. Run test writes only in `szdatatest` and only when the user has authorized the specific sample/action.

## Current szdata/szdatatest conventions

- `szdata` is allowed for high-frequency read-only commands such as metadata lookup, demand lookup, dataset config, wide-table card/detail, and table-permission prechecks.
- Permission commands such as `table-permission-mine` and `table-permission-role` are read-only high-frequency prechecks. For agent development prechecks, prefer `table-permission-mine --table db.table` for current-login user table access; use `table-permission-role --role-id ROLE_ID --table db.table` only when the user explicitly asks about a role as the permission subject. `role-list` and `role-user-list` are detail-only commands under `szdata_detail`. The old `current-user-data-permission`, `my-permission-base`, `my-permission-data`, `my-permission-function`, `my-permission-report`, `role-data-permission`, `role-summary`, and `table-permission-check` entries were archived or renamed.
- Scheduling topic permission commands: `table-permission-topic` is the `szdata` high-frequency verdict command; `scheduling-topic-list-by-current-user` and `scheduling-topic-base-policy` are detail-only commands under `szdata_detail`. For a single table, `table-permission-topic` defaults to `conclusion=PASS/EXPIRED/NO/UNKNOWN`, matched source, and validity; base Hive/Ranger policy evidence (`BASE_PASS`) and application-grant evidence (`APPLY_PASS`) are detail evidence, not the primary conclusion.
- 2026-07-06 naming rule: development precheck commands are named by the question an agent asks: `table-permission-mine` answers "can the current login user read this table?", `table-permission-topic` answers "can this scheduling topic read this table?", and `table-permission-role` answers "can this role read this table?".
- `szdatatest` is the only place where dataset or wide-table save/preview/generate workflows may be validated.
- `szdatatest` commands that overlap with `szdata` must preserve arguments, default output, and semantics. `szdatatest_detail` must preserve the `szdata_detail` command list.
- Run `node C:\Users\13246\.opencli\shared\szdata-core\audit-surfaces.mjs --plain` after changing command placement.
- Dataset and wide-table detail commands should support bounded output, for example `--sql-preview` and `--field-preview`.
- Debug/raw flags must be read-only and should omit giant SQL by default.
- Detail fields may differ from list fields. For dataset wide-table records, `isIndicatorSystem` should be read from `indicatorSystemInfo.isIndicatorSystem` first, then the top-level field as fallback.

## Chrome / OpenCLI contention

Treat OpenCLI as the primary business-system channel. Many internal adapters use the same Chrome profile and Codex Chrome Extension/native-host path as direct Chrome browser control, so direct Chrome control and OpenCLI can contend for the same tab/session bridge.

Current local profile split:

- OpenCLI Browser Bridge: `opencli-business` is the default OpenCLI profile (`opencli profile list` should show it as `default`). Keep production business adapters such as `szdata` on this profile.
- Direct Codex Chrome control: use the separate Chrome profile named `用户1` when UI reconnaissance is necessary. Do not select the Default business profile for direct Chrome control unless the user explicitly needs that exact logged-in UI state.

Operational rules:

- Do not run direct Chrome-control work and `opencli <site> ...` commands at the same time for the same internal system.
- Do not parallelize multiple Chrome-backed OpenCLI commands when they need the logged-in browser session; run them sequentially.
- Prefer OpenCLI adapters for read-only business evidence when an adapter exists. Use direct Chrome control only for UI state that the adapter cannot read.
- If direct Chrome control is used, release it before running OpenCLI again: call `browser.tabs.finalize({ keep: [] })`, then dispose the browser client if the runtime exposes `agent.browsers.dispose()`.
- If `Detached while handling command`, `Pre-navigation ... failed`, or tab enumeration hangs occur, treat it first as Chrome extension/session contention rather than a business API failure.
- Recovery sequence: stop/directly dispose Codex Chrome control, verify `opencli profile list`, then retry one OpenCLI command sequentially. Open a fresh Chrome window in the selected profile only if the bridge is disconnected.

Codex Chrome selection pattern for this workspace:

```js
if (globalThis.agent?.browsers == null) {
  const { setupBrowserRuntime } = await import("C:/Users/13246/.codex/plugins/cache/openai-bundled/chrome/26.623.101652/scripts/browser-client.mjs");
  await setupBrowserRuntime({ globals: globalThis });
}

const chromeProfiles = await agent.browsers.list();
const codexChrome = chromeProfiles.find((browser) => browser.metadata?.profileName === "用户1");
if (!codexChrome) throw new Error("Codex Chrome profile 用户1 is not connected.");
globalThis.browser = await agent.browsers.get(codexChrome.id);
```

Before switching back to OpenCLI:

```js
await browser.tabs.finalize({ keep: [] });
if (agent.browsers.dispose) await agent.browsers.dispose();
```

Evidence from 2026-07-06:

- OpenCLI profile `wnezfmrw` was renamed to `opencli-business` and set as the default.
- Codex Chrome detected two extension backends: Default (`您的 Chrome`) and the separate profile `用户1`; selecting `用户1` by browser id returned only that profile's tabs.
- `browser.tabs.finalize({ keep: [] })` alone was not sufficient before returning to OpenCLI; the next `opencli szdata task-sql --task-id 238523 -f json` failed with `Detached while handling command`.
- After `agent.browsers.dispose()`, the same `opencli szdata task-sql --task-id 238523 -f json` succeeded and returned the expected fields: `taskId`, `createSql`, `querySql`, `evidence_level`, `limitations`.

## Related docs

Read these before platform-specific work:

```text
references/tools/szdata.md
references/tools/szdata-operations/README.md
references/tools/szdata-operations/dataset-create.md
references/tools/szdata-operations/wide-table-management.md
```
