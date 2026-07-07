# Security Notes

This repository is a public, documentation-first workbench for agent-readable
data-engineering investigation patterns. It should not contain credentials,
browser state, cookies, tokens, private keys, raw trace dumps, or production
payload archives.

Before committing:

- Keep local runtime state out of git: `tmp/`, `_archive/`, `.headroom-cache/`,
  `backups/`, `_browser_state.txt`, and `*.trace`.
- Do not commit `.env` files, cookies, tokens, private keys, JDBC connection
  strings, or screenshots/logs that expose secrets.
- Prefer bounded examples and readback-oriented evidence over raw payload dumps.
- Treat production systems as read-only unless a test-environment validation and
  explicit authorization exist.

If a secret is accidentally committed, rotate it first, then remove it from git
history before continuing to use the repository.
