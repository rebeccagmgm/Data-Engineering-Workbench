# Local File And Code Search

Use this note when a task depends on local files, source code, SQL, configs,
logs, historical notes, exported documents, or a user-provided directory.

This is not a standalone tool. It describes how an agent should use local file
search to investigate confirmed workspaces and candidate paths.

## When To Use

- The user provides a local directory, codebase, or evidence path.
- You need to find a file, code entrypoint, SQL fragment, config value, or
  historical note.
- You need to confirm whether a resource has entered the investigation scope.
- You need to map what was searched and what remains unsearched.

## Search Rules

Prefer `rg` and `rg --files`:

```powershell
rg --files <directory>
rg "<keyword>" <directory>
```

Use bounded output and exclude noisy generated folders unless they are the
explicit target:

```powershell
rg "<keyword>" <directory> -g "!tmp/**" -g "!_archive/**" -g "!node_modules/**"
```

In PowerShell, list directories with:

```powershell
Get-ChildItem -Recurse <directory>
```

## What Local Search Can Prove

- A file, code fragment, config value, or SQL fragment exists in the searched
  material.
- The current investigation searched specific paths and keywords.
- A historical note or implementation describes a behavior at the time it was
  written.

## What Local Search Cannot Prove

- That production is currently deployed with the same behavior.
- That a workflow actually succeeded.
- That no matching resource exists anywhere.
- That historical material is still current business truth.

## Reporting

When reporting local search results, state:

- Which directories were searched.
- Which exclusions were applied.
- Which files were read.
- Which binary or unsupported files were skipped.
- Which findings are historical and need live verification.
