# Workbench Knowledge Layer

This directory stores reusable runtime knowledge for the Data Engineering
Workbench. It is not the formal long-term knowledge base. It keeps only the
templates, patterns, capability contracts, promotion candidates, and promotion
logs that help Case work run better.

## What Belongs Here

- Case card templates.
- Reusable workflow patterns.
- Tool capability contracts.
- Candidate lessons distilled from completed or replayed cases.
- Records of which candidates were promoted to a skill, CLI command, eval, or
  a more durable knowledge base.

## What Does Not Belong Here

- Raw chat logs, screenshots, attachments, or browser state.
- Complete per-case execution logs.
- Large platform readback payloads.
- Stable business knowledge that belongs in a formal knowledge base.
- Duplicate copies of long-form reference material already maintained
  elsewhere.

## Directory Map

```text
workbench-knowledge/
  README.md
  routes.md
  card-templates/
  workflow-patterns/
  capability-contracts/
  promotion-inbox/
  promotion-log.md
```

## Operating Rules

1. Distill case-local learning inside `cases/<case>/distilled/` first when that
   directory exists.
2. A promotion candidate must cite its source case and explain why it is likely
   reusable.
3. Templates, capability contracts, and workflow patterns should prove useful in
   the workbench before being promoted elsewhere.
4. Promote only after another similar case validates the pattern.
5. Record every promotion or demotion in `promotion-log.md`.
