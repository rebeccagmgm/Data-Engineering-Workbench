---
id: B-001
kind: blocker
title: 历史回放不能直接证明当前平台事实
domain: governance
capability: enforce_historical_replay_boundary
owner: user
execution_state: waiting
verification_state: n/a
priority: medium
env: historical
input_refs:
  claim_refs: [C-005]
  asset_refs: []
  run_refs: []
  source_refs: [SRC-prod-verify, SRC-actual-logic]
external_dependency:
  dependency_state: open
  waiting_on: 用户决定是否需要当前读回
  expected_signal: 是否将该 Case 仅用于协议回放，还是继续查当前平台状态
  blocked_since: 2026-07-06T00:00:00+08:00
  last_checked_at: 2026-07-06T00:00:00+08:00
  next_touch_at: 2026-07-07T00:00:00+08:00
  escalation_at:
  unblock_hypothesis: 如果只做协议回放，无需当前读回；如果要复用结论，需要重新查 Horae/Oracle 当前状态
exit_criteria:
  - 明确该 Case 是否仅作为 historical_replay
verification_method:
  - 用户确认
allowed_actions: [ask_user, read_file, summarize]
forbidden_actions: [write_prod, submit_external_request]
evidence_refs: []
updated_at: 2026-07-06T00:00:00+08:00
---

## 说明

该 Case 的证据主要来自 2026-06-22 和 2026-06-25 的历史核验材料。它足以验证 Workbench 协议，但不能自动代表当前平台状态。
