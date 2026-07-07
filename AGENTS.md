# Data Engineering Workbench Agent Rules

This workspace is for data-engineering skills, references, investigation notes, and handoff material. It is not the live OpenCLI adapter source tree.

## OpenCLI Source Locations

When working on `szdata` or `szdatatest` OpenCLI adapters, do not search this workspace as if it contains the adapter source. The live private adapter source is:

```text
C:\Users\13246\.opencli\clis\szdata
C:\Users\13246\.opencli\clis\szdatatest
```

Workspace files under `references/`, `skills/`, `tmp/`, and `_archive/` can explain behavior or preserve evidence, but they are not the source of truth for adapter code.

Before editing or reviewing OpenCLI behavior, read:

```text
references/tools/opencli.md
references/tools/szdata-agent-cli-audit.md
references/tools/szdata.md
references/tools/szdata-operations/README.md
```

## Environment Boundary

- `szdata` is production: `data.gf.com.cn`.
- `szdatatest` is test: `datatest.gf.com.cn`.
- Read-only query, investigation, and production-state confirmation may use `szdata`.
- Any form/save/submit/delete/generate/preview/edit-config action must be researched and validated in `szdatatest` first.
- Production writes on `szdata` require a passing `szdatatest` validation and explicit user authorization.
- For internal form workflows, success means the downstream or follow-up page can read the result, not just that an API returned 200.

## Search Hygiene

Use `rg` and `rg --files` first. Keep broad searches bounded and avoid mixing old traces into current conclusions.

Default exclusions for broad searches:

```text
tmp/
_archive/
.headroom-cache/
node_modules/
dist/
build/
coverage/
_browser_state.txt
*.trace
```

If a historical trace or archived note is useful, state that it is historical evidence and verify current behavior against the live adapter source or current read-only platform data.

## Codex Thread Coordination

When the user asks to track, summarize, or coordinate other Codex conversations in this workspace, use:

```text
references/tools/codex-thread-monitor.md
tmp/codex-thread-dashboard.md
```

The dashboard is a working coordination snapshot for this `Data-Engineering-Workbench` workspace. It is not a source of business truth. Promote stable findings into the relevant `references/` or `skills/` docs after verification.

## OpenCLI Working Rules

- Discover commands with `opencli list -f json`, `opencli <site> --help`, and `opencli <site> <command> --help`.
- For `szdata` / `szdatatest` / `szdata_detail` audit or optimization, follow `references/tools/szdata-agent-cli-audit.md`: use the generic CLI audit ideas only as method, not as permission to rebuild the OpenCLI platform.
- Treat `--help` as command discovery and argument confirmation, not as the main behavior-verification method. To save context, do not paste or ingest full help output during reviews; filter for command names or key flags with `rg` / `Select-String` unless the full help text is explicitly needed.
- Verify OpenCLI behavior with bounded `-f json` dry-runs, read-only self-checks, and downstream readback. A command appearing in `--help` only proves registration and visible options, not correctness.
- Place high-frequency production workflow commands in `szdata`; place low-frequency diagnostics, audit, explanation, and historical readback in `szdata_detail`; place test validation and write/lifecycle probes in `szdatatest`; place retired, slow, risky, or misleading commands in `archive`.
- Name commands by task family: keep the same prefix for the same question type, and put the subject/dimension at the suffix. Example: `table-permission-mine`, `table-permission-topic`, and `table-permission-role` belong to the same table-permission family with different subject dimensions.
- For internal UI workflows that will become OpenCLI adapters, use the Codex Chrome Extension as the reconnaissance path when page state matters: claim the real Chrome tab, inspect DOM/form validation/network behavior, and compare the visible UI state with OpenCLI/API readback before declaring success. Then encode the stable behavior as an OpenCLI command with explicit strategy, bounded output, and readback verification. This is especially required for form pages where HTTP 200 or backend detail values may still leave frontend required fields invalid.
- Prefer `-f json` for agent work.
- Keep list/detail commands paginated or preview-limited. Do not dump giant SQL, field lists, or raw JSON unless the user explicitly asks.
- OpenCLI private adapter edits belong under `C:\Users\13246\.opencli\clis\<site>\`.
- Use `apply_patch` for manual edits.
- After editing an adapter, run `node --check` on changed `.js` files and a small command-level smoke test.
- Do not add hidden production write commands. Name and document every write path clearly.
- Chrome-backed OpenCLI and direct Codex Chrome control can contend for browser-extension/native-host sessions. Treat OpenCLI as the primary business-system channel. The OpenCLI Browser Bridge default profile is aliased as `opencli-business`; keep business adapters on that profile. For direct Codex Chrome control, prefer the separate Chrome profile named `用户1` instead of the Default business profile. Do not run Chrome control and Chrome-backed OpenCLI in parallel. Before any OpenCLI command after Codex Chrome control, call `browser.tabs.finalize({ keep: [] })` and dispose the browser client if available (`agent.browsers.dispose()`). If `Detached while handling command`, pre-navigation failure, or tab enumeration hangs occur, first suspect Chrome/OpenCLI contention; dispose direct Chrome control, then retry one OpenCLI command sequentially.

## Documentation Rules

When behavior, commands, adapters, or platform workflows change, update the relevant docs in this workspace:

```text
references/tools/opencli.md
references/tools/szdata.md
references/tools/szdata-operations/README.md
skills/data-engineering-investigation/SKILL.md
```

Operation-specific behavior belongs in `references/tools/szdata-operations/`. Keep persistent rules in docs, not only in chat prompts.

## Encoding And Mojibake Hygiene

- Treat common Chinese mojibake marker characters, including Unicode code points `U+951B`, `U+9286`, `U+95AB`, `U+935B`, `U+93C1`, `U+4E63`, and replacement character `U+FFFD`, as file content corruption, not a display glitch.
- Do not make tiny local fixes inside a heavily corrupted section; rewrite the affected section or file as clean UTF-8 text.
- After editing Chinese docs, scan the touched file for typical mojibake markers with `rg -n -P "\x{951B}|\x{9286}|\x{95AB}|\x{935B}|\x{93C1}|\x{4E63}|\x{FFFD}" <file>`.
- When rewriting command maps such as `COMMANDS.md`, verify representative beginning, middle, and ending lines render correctly before reporting completion.
- Keep adapter source code and command docs UTF-8; avoid mixing shell encodings or copying already-corrupted text back into files.
