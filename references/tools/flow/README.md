# Flow Reference Artifacts

This folder stores non-runtime reference artifacts that used to live under
`C:\Users\13246\.opencli\clis\flow`.

The `flow` adapter source should stay in the OpenCLI source repository, while
agent skills, endpoint notes, and eval fixtures live here in the workbench for
reuse and review.

## Contents

- `docs/endpoints.json`: BPM / Flow endpoint notes.
- `evals/trigger.jsonl`: trigger eval examples for the Flow skill.
- `skills/flow/SKILL.md`: agent-facing usage instructions for the Flow OpenCLI adapter.

## Source Boundary

- Runtime adapter code remains in `C:\Users\13246\.opencli\clis\flow`.
- This folder is documentation and evaluation material; OpenCLI does not need it
  to execute `opencli flow ...` commands.
