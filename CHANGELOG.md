# Changelog

## 2026-07-07 - case dashboard generator v0

### Changed
- Added a local read-only case-dashboard-generator script that derives dashboard state from cases/* source files.
- Added unittest coverage for the Jinshida replay sample to verify attention lanes, Top Risks before Top Actions, and local-only HTML output markers.
- Added a Superpowers implementation plan for the dashboard generator.
- Generated a disposable local dashboard at tmp/case-dashboard/index.html; this output remains ignored and is not a source of truth.
- This round adds local generator code, tests, and documentation only; it does not execute platform writes, add a server, create an editable UI, or store credentials.

### Files
- scripts/case_dashboard_generator.py
- tests/test_case_dashboard_generator.py
- docs/superpowers/plans/2026-07-07-case-dashboard-generator.md
- tmp/case-dashboard/index.html (generated, ignored)
- CHANGELOG.md

### Decisions
- Keep the first dashboard as static generated HTML instead of a React/Vite application.
- Keep cases/ Markdown/YAML files as the only durable source of truth.
- Use PyYAML plus Python unittest to avoid adding a frontend build stack for V0.
- Surface failed verification and trust risks before action prompts.

### Open Questions
- Which additional 1-2 Cases should join the first two-week dashboard trial.
- Whether claim_scope.truth_environment should be backfilled into existing sample claims before broadening trust-gap checks.
- Whether later versions should add a JSON cache beside the HTML output.

### Next
- Open the generated HTML locally during daily work and decide whether it exposes the next action faster than reading raw Case files.
- Add more Case samples before expanding UI surface area.
- Revisit the Dashboard kill criteria after the first trial period.

## 2026-07-07 - schedule mcp wrapper commands

### Changed
- Added explicit MCP-backed schedule commands in the live OpenCLI adapter: `schedule-mcp-dependencies`, `schedule-mcp-run-instances`, `schedule-mcp-run-states`, `schedule-mcp-run-logs`, and `schedule-mcp-owner-failed-instances`.
- Added a shared MCP JSON-RPC helper for `szdata` schedule MCP calls, reading personal-token credentials only from environment variables.
- Archived the previous partial direct schedule runtime wrappers from active `szdata` discovery: `schedule-dependencies`, `schedule-run-instances`, `schedule-run-states`, `schedule-run-logs`, and `schedule-owner-failed-instances`.
- Updated the MCP parity design, implementation plan, live adapter command map, and workspace routing docs to use the explicit `schedule-mcp-*` command names.
- Verified all five new schedule MCP commands with bounded live smokes; `schedule-mcp-run-logs` was run with `--log-preview 0` and did not print log bodies.
- This round changes live adapter behavior and documentation only; it does not execute production writes or store credentials, GUIDs, full DDL, full SQL, or full log content.

### Files
- `C:\Users\13246\.opencli\shared\szdata-core\commands\mcp\mcp-client.js`
- `C:\Users\13246\.opencli\shared\szdata-core\commands\scheduling\schedule-mcp-*.js`
- `C:\Users\13246\.opencli\shared\szdata-core\test\mcp-client.test.mjs`
- `C:\Users\13246\.opencli\shared\szdata-core\test\schedule-commands.test.mjs`
- `C:\Users\13246\.opencli\clis\szdata\schedule-mcp-*.js`
- `C:\Users\13246\.opencli\clis\szdata\COMMANDS.md`
- `docs/superpowers/specs/2026-07-07-szdata-mcp-parity-cli-design.md`
- `docs/superpowers/plans/2026-07-07-szdata-schedule-mcp-commands.md`
- `references/tools/szdata.md`
- `references/tools/szdata-command-landscape.md`
- `references/tools/szdata-operations/README.md`
- `references/tools/szdata-operations/mcp-cli-function-comparison.md`
- `references/tools/szdata-operations/mcp-cli-coverage-report.md`
- `CHANGELOG.md`

### Decisions
- Use new command names instead of overloading old partial direct commands.
- Keep full runtime log bodies out of default output; expose counts and bounded previews.
- Leave SQL diagnosis MCP wrapping for a separate decision.

### Open Questions
- Whether the retired direct schedule probes should later return under explicit `*-direct-*` or detail-surface names.

### Next
- Keep docs and command maps aligned if SQL diagnosis receives a separate MCP-backed wrapper.

## 2026-07-07 - SQL 诊断行为说明

### Changed
- 新增专门的 `sql-diagnosis` 行为说明，记录 direct Portal endpoint、请求形态、实测规则边界和安全约束。
- 记录 `sql-diagnosis` 通过 `checkSqlWithAuth.json` 检查 SQL 文本；它不是 SQL 执行，不是当前登录用户表权限证明，也不是 MCP `query.sql_diagnosis` 精确等价。
- 将说明文档加入 SZData operations 索引、主 SZData 路由表和 Data Engineering Investigation skill 入口。
- 本轮只更新文档；不修改 runtime adapter，不执行生产写入，不保存凭证、原始 token、完整 SQL 正文或执行日志。

### Files
- `references/tools/szdata-operations/sql-diagnosis-behavior.md`
- `references/tools/szdata-operations/README.md`
- `references/tools/szdata.md`
- `skills/data-engineering-investigation/SKILL.md`
- `CHANGELOG.md`

### Decisions
- 将内容保存为 operation reference，而不是新建 skill；因为它是命令级证据和路由说明，不是通用可复用流程。
- 明确安全边界：客户端证据只能证明 OpenCLI 命令请求的是检查接口；若要绝对证明服务端无副作用，需要平台/服务端日志或 owner 确认。
- 在持久说明中禁止使用 DDL/DML/DCL 形态的生产探针；后续检查使用 SELECT-only 探针。

### Open Questions
- 服务 owner 是否能确认 `checkSqlWithAuth.json` 的服务端实现。
- 未来 MCP-backed parity mode 是否应在显式 source/mode flag 后暴露更完整的原始诊断字段。

### Next
- 解读 `sql-diagnosis` 的 `valid=Y` 或 `valid=N` 前，先查阅该说明。
- 如果 adapter 行为变化，同步更新该说明和 live adapter 命令文档。

## 2026-07-07 - szdata mcp parity cli design

### Changed
- Added a draft design for extending selected `szdata` CLI commands with explicit MCP parity mode while preserving direct Portal mode as the default.
- Scoped phase one to `schedule-run-logs`, `schedule-dependencies`, and `sql-diagnosis`.
- Recorded security and output boundaries for MCP mode: environment-variable token only, no secret values in output, and no full SQL or full log bodies by default.
- This round updates design documentation only; it does not change runtime adapters, execute production writes, or store credentials, GUIDs, full DDL, full SQL, or full log content.

### Files
- `docs/superpowers/specs/2026-07-07-szdata-mcp-parity-cli-design.md`
- `CHANGELOG.md`

### Decisions
- Use explicit `--source mcp` instead of changing existing commands to MCP-backed behavior by default.
- Treat direct Portal evidence and MCP exact/shape-compatible parity as separate output levels.

### Open Questions
- Whether `schedule-run-states` should join phase two after its MCP date/time argument shape is verified.
- Whether MCP mode should later support explicit redacted raw output for debugging.

### Next
- After user review, create the TDD implementation plan and modify the live OpenCLI shared core.

## 2026-07-07 - mcp and cli actual smoke record

### Changed
- Added a bounded actual-use record comparing Data Portal schedule/sql_dignose MCP `tools/call` results with current `opencli szdata` read-only command results.
- Recorded that schedule detail, dependencies, run instances, owner failed instances, Horae SQL, and SQL diagnosis are callable on both surfaces in safe sample probes.
- Recorded two important gaps: MCP schedule run-state call failed with the tested date shape while CLI derived states succeeded, and MCP run logs expose full log-content fields while current CLI only confirms instance/status availability.
- Clarified that the current CLI has a broader business function surface, but is not a strict superset of MCP output shapes.
- This round updates documentation only; it does not change runtime adapters, execute production writes, or store credentials, GUIDs, full DDL, full SQL, or full log content.

### Files
- `references/tools/szdata-operations/mcp-cli-function-comparison.md`
- `CHANGELOG.md`

### Decisions
- Treat actual MCP/CLI sample calls as smoke evidence, not full semantic parity proof.
- Treat "broader CLI function surface" and "complete MCP output parity" as separate claims.
- Keep raw SQL and log bodies out of the repository even when a command or tool can return them.

### Open Questions
- Whether `schedule.get_task_run_states` expects a different date/time shape than the tested CLI-style date range.
- Whether a non-MCP direct endpoint can be found for full schedule runtime logs.

### Next
- Use this smoke table as the current entrypoint for deciding which schedule/sql_dignose features are CLI-ready and which still need endpoint reconnaissance.

## 2026-07-07 - mcp cli function comparison note

### Changed
- Added a standalone analysis note comparing the full current `szdata` CLI function surface with Data Portal metadata, schedule, and sql_dignose MCP tools.
- Recorded that the CLI function surface is broader than the three MCP servers, while pure `X-Personal-Token` direct API coverage is currently narrower than MCP coverage.
- Added the new note to the `szdata-operations` document index.
- This round updates documentation only; it does not change runtime adapters, execute production writes, or store credentials, GUIDs, full DDL, or full SQL.

### Files
- `references/tools/szdata-operations/mcp-cli-function-comparison.md`
- `references/tools/szdata-operations/README.md`
- `CHANGELOG.md`

### Decisions
- Keep the comparison as a dedicated analysis note instead of expanding the openapi survey further.
- Treat `szdata` CLI, MCP tool coverage, and pure `X-Personal-Token` direct API coverage as three distinct layers.

### Open Questions
- Whether service-side route metadata can later close the schedule/sql_dignose direct personaltoken API gap.

### Next
- Use this note as the compact entrypoint when deciding whether a feature should be implemented via current CLI, MCP, or future direct personaltoken API.

## 2026-07-07 - data portal mcp direct-url probe

### Changed
- Probed the user-provided Data Portal MCP URLs for metadata, schedule, and sql_dignose using `X-Personal-Token` from environment variables only.
- Recorded that `/mcp/metadata`, `/mcp/schedule`, and `/mcp/sql_dignose` currently initialize successfully and expose MCP tool inventories.
- Recorded that standard MCP `tools/list` and safe sample `tools/call` responses do not expose backend `httpReq` or direct API paths.
- Recorded direct `X-Personal-Token` API probes: metadata `/openapi/metaservice/personaltoken/internal/...` succeeds, while Portal-native schedule/sql paths and guessed developservice personaltoken paths do not provide a usable non-MCP direct API.
- This round updates documentation only; it does not change runtime adapters, execute production writes, or store credentials, GUIDs, full DDL, or full SQL.

### Files
- `references/tools/szdata-operations/mcp-openapi-survey.md`
- `CHANGELOG.md`

### Decisions
- Treat the user-provided `/mcp/...` URLs as current MCP entrypoints, separate from MCP market discovery.
- Do not treat an MCP URL plus `X-Personal-Token` as proof of a direct non-MCP backend API.
- For CLI work, keep metadata as direct personaltoken openapi-capable, but keep schedule/sql_dignose direct `X-Personal-Token` backend status as unproven.

### Open Questions
- What exact backend path does `mcpservice-schedule` call for each schedule tool?
- What exact backend path does `mcpservice-sql_dignose` call for `query.sql_diagnosis`?
- Whether service owners can expose those backend paths through `/openapi/.../personaltoken/internal/...` for non-MCP CLI use.

### Next
- If direct `X-Personal-Token` CLI parity is required, obtain service-side route metadata, gateway catalog entries, or call logs for schedule/sql_dignose.
- Keep using environment variables for token checks and keep output limited to server/tool/path-shape evidence.

## 2026-07-07 - mcp openapi discovery boundary clarification

### Changed
- Clarified why `TableMetaData` can be traced from MCP market metadata to `/openapi/...`: the current market detail exposes appId, MCP URL shape, tool definitions, and tool-level `httpReq`.
- Clarified that current `schedule` and `sql_dignose` / `sql_diagnose` investigation is blocked at discovery, not at MCP authentication.
- Recorded the current local MCP configuration check at a redacted shape level: only `TableMetaData` is visible for this SZData-related path, with credential values carried by environment-variable names.
- This round updates documentation only; it does not change runtime adapters, execute production writes, or store credentials, GUIDs, full DDL, or full SQL.

### Files
- `references/tools/szdata-operations/mcp-openapi-survey.md`
- `CHANGELOG.md`

### Decisions
- Treat MCP registration/detail metadata as the decisive discovery layer for market-based openapi extraction.
- Do not describe missing `schedule` / `sql_dignose` surfaces as an authentication mismatch; describe them as missing current appId, MCP URL shape, tool definitions, and `httpReq` metadata.
- Keep historical MCP names and old parity notes out of current-state conclusions except as stale leads.

### Open Questions
- Whether a service-side registry, gateway catalog, or real call log can provide the current appId or MCP URL shape for schedule / SQL diagnosis if those MCP tools still exist.
- Whether any private, non-market MCP server exists for these capabilities outside the current Codex MCP configuration.

### Next
- If deeper discovery is needed, use only current config, current server metadata, or actual call logs, and keep all credential values redacted.
- Keep `mcp-openapi-survey.md` current-state-only unless an explicit historical comparison is requested.

## 2026-07-07 - szdata MCP coverage CLIization

### Changed
- Documented the live MCP-to-SZData CLI coverage review and the direct-endpoint parity decisions for metadata, schedule, and SQL diagnosis tools.
- Rewrote the corrupted SZData routing docs into clean UTF-8 so future agents can read the current command ownership and limitations.
- Recorded that five new production read-only `szdata` commands were added in the live OpenCLI adapter source outside this repository: `schedule-run-instances`, `schedule-run-states`, `schedule-owner-failed-instances`, `schedule-run-logs`, and `sql-diagnosis`.
- Marked `schedule-run-logs` as a current direct-endpoint gap rather than full runtime-log parity, and marked `sql-diagnosis` as partial direct parity rather than exact MCP `query.sql_diagnosis` equivalence.
- This round documents read-only adapter behavior and does not execute production writes.

### Files
- `references/tools/szdata.md`
- `references/tools/szdata-command-landscape.md`
- `references/tools/szdata-operations/README.md`
- `references/tools/szdata-operations/mcp-cli-coverage-report.md`
- `CHANGELOG.md`

### Decisions
- Treat CLIization for this workstream as direct Data Portal/platform endpoints, with MCP used only as an inventory and behavior oracle.
- Keep the requested schedule runtime commands in `szdata`, not `szdata_detail`.
- Do not CLIize `metadata.query_assistant_dify` unless a concrete deterministic workflow needs it.

### Open Questions
- Exact runtime-log parity still needs a verified non-MCP log endpoint.
- Exact SQL table-existence diagnosis parity still needs the direct backend behind MCP `query.sql_diagnosis`, or explicit approval for an MCP-backed fallback command.
- `metadata.search_by_es` filter/scoring parity should be checked before claiming full uncommon-search coverage.

### Next
- Use the new commands for bounded production read-only checks and keep their limitations visible in user-facing output.
- If full log or exact SQL diagnosis parity becomes necessary, run endpoint reconnaissance before changing the commands.

## 2026-07-07 - szdata bearer access survey

### Changed
- Added a durable Bearer-only access survey for SZData metaservice, schedule, wide-table schedule, project-space schedule, Quartz, and schedule-theme paths.
- Added a safe PowerShell checker that reads Bearer credentials only from `SZDATA_BEARER_TOKEN` or hidden prompt input.
- Recorded the current schedule detail path as `/portal/prod-api/developservice/schedule/getScheduleDetailTimeFormatted.json` and marked old MCP schedule assumptions as not current evidence.
- Ran one Bearer-only classification through an existing local secret environment variable without printing or storing the token.
- Renamed the ambiguous reachable-but-parameter-error status to `AUTH_PASSED_BUSINESS_ERROR`.
- Clarified that MCP server auth keys and direct Portal Bearer-only access are separate authentication paths.
- Added an explicit correction note distinguishing the early MCP-based assumption from the verified Portal-native endpoint result.
- Clarified that `TableMetaData` MCP may discover actual API metadata, but discovery evidence and direct Portal authentication evidence must be recorded separately.
- Clarified the MCP proxy chain as client to MCP gateway/server to OpenAPI or internal backend to tool result.
- Added a dedicated `TableMetaData` MCP logic investigation, including MCP tool to openapi mapping and safe direct-verification results.
- Added a current-state-only MCP / OpenAPI survey: current MCP market has 120 servers and 356 tool HTTP configs, but only four `/openapi/...` tools, all under `TableMetaData`.
- Clarified that current `schedule` and `sql_dignose` / `sql_diagnose` MCP surfaces are not visible through current market keyword/detail lookup or extracted tool HTTP configs.
- This round updates documentation and a read-only/safe probe script only; it does not change adapter runtime behavior and does not execute production writes.

### Files
- `references/tools/szdata-operations/bearer-access-survey.md`
- `references/tools/szdata-operations/tablemetadata-mcp-logic.md`
- `references/tools/szdata-operations/mcp-openapi-survey.md`
- `scripts/check-szdata-bearer-access.ps1`
- `CHANGELOG.md`

### Decisions
- Keep the survey under `references/tools/szdata-operations/` because it is an SZData platform operation and auth-boundary investigation.
- Keep the actual Bearer token out of repository files, command examples, logs, and summaries.
- Skip all state-changing paths in the checker and classify them as `NOT_TESTED_WRITE_PATH`.
- Treat successful OpenCLI browser/session access as separate evidence from Bearer-only direct access.
- Keep the MCP / OpenAPI survey focused on current market evidence only, without old MCP name parity mapping.

### Open Questions
- If another Bearer token must be classified, rerun the checker through hidden prompt input or a secure environment variable.
- Some bundle-discovered endpoints may need exact payload refinement before interpreting non-auth business errors.
- Additional current openapi discovery should come from current MCP `httpReq`, tool plugins, gateway catalog, or service-side configuration sources.

### Next
- Rerun the checker with hidden token input if the target token changes.
- Review `tmp/szdata-bearer-access-result.json` for sensitive content before promoting stable classifications back into the survey.
- Keep future updates to the MCP / OpenAPI survey current-state-only unless explicitly asked to compare historical MCP names.

## 2026-07-07 - agent change recording and push confirmation policy

### Changed
- Added explicit Agent rules requiring `CHANGELOG.md` updates for every material repository change.
- Added explicit Agent rules requiring user confirmation before any remote push.
- Clarified that edit or commit approval is not push approval.
- This round updates documentation and process contract only; it does not enter implementation.

### Files
- `AGENTS.md`
- `CHANGELOG.md`

### Decisions
- Keep the rule in root `AGENTS.md` because it is the first repository-level instruction file for future agents.
- Require pre-push summaries to include branch, commit id, changed files, verification performed, and changelog status.
- Require current-turn confirmation for each push, rather than relying on prior approval.

### Open Questions
- Whether to add a local pre-push hook later to mechanically block pushes without confirmation notes.
- Whether to add a reviewer checklist or CI rule for changelog coverage.

### Next
- Commit this rule change locally.
- Wait for user confirmation before pushing the commit to GitHub.

## 2026-07-07 - public repository bootstrap

### Changed
- Initialized the Data Engineering Workbench as a git-backed public documentation repository.
- Added public-facing repository entrypoints and security boundary notes.
- Added ignore rules for local runtime state, browser state, traces, archives, backups, caches, environment files, and scratch probes.
- Added line-ending normalization for text files.
- Published existing workbench references, case example material, dashboard design notes, skills, and workbench knowledge layer docs.
- Rewrote selected corrupted entrypoint docs into clean, agent-readable English.
- This round updated documentation, contracts, case examples, and repository structure only; it did not implement runtime application code.

### Files
- `.gitattributes`
- `.gitignore`
- `AGENTS.md`
- `CONTEXT.md`
- `README.md`
- `SECURITY.md`
- `.agents/skills/szdata-spec-first/SKILL.md`
- `skills/data-engineering-investigation/SKILL.md`
- `cases/CASE-20260611-jinshida-market-push/`
- `docs/dashboard-acceptance-checklist.md`
- `docs/dashboard-ui-spec.md`
- `docs/dashboard-view-model.md`
- `references/research/`
- `references/tools/`
- `workbench-knowledge/`

### Decisions
- Keep the repository public so cloud agents can read it directly.
- Keep local runtime state and raw transient artifacts out of git.
- Treat this repository as durable workbench documentation, not live adapter source.
- Keep production-oriented workflows read-only by default and require test-environment validation before state-changing operations.
- Prefer concise public entrypoints over copying local cache, browser state, or trace dumps.

### Open Questions
- Some historical Markdown files may still contain older wording or encoding issues outside the cleaned entrypoints.
- Public-safe abstraction depth may need tightening if future material contains more direct business data.
- The repository does not yet include automated linting for changelog coverage or secret scanning.

### Next
- Add a changelog gate so every future material change updates `CHANGELOG.md`.
- Review older reference files incrementally for encoding quality and public readability.
- Add lightweight checks for ignored runtime state and high-confidence secret patterns before future pushes.

## 2026-07-07 - changelog maintenance policy

### Changed
- Added root `CHANGELOG.md` as the required change record for future human and agent review.
- Added repository guidance that every document, schema, contract, Case example, or directory-structure change must update `CHANGELOG.md`.
- Added `CHANGELOG.md` to the main reader entrypoints.
- This round updates documentation and process contract only; it does not enter implementation.

### Files
- `CHANGELOG.md`
- `AGENTS.md`
- `README.md`

### Decisions
- Changelog entries must be concise and record only real changes.
- Every entry must include date, phase, changed summary, files, decisions, open questions, and next steps.
- Sensitive internal details, real accounts, cookies, tokens, and production connection details must not be recorded.
- Reviewer should treat missing changelog updates for obvious file changes as an incomplete delivery.

### Open Questions
- Whether to add an automated changelog coverage check later.
- Whether to split future changelog entries by Case, tool surface, or release-style phase when changes grow larger.

### Next
- Keep `CHANGELOG.md` updated in the same commit as future material changes.
- Consider a small reviewer checklist or CI check once the repository has more regular updates.
