---
id: D-001
kind: decision
title: 第一轮回放以实际上线情况材料作为历史真相源
domain: governance
capability: decide_replay_truth_source
owner: user
execution_state: done
verification_state: passed
priority: medium
env: historical
input_refs:
  claim_refs: [C-003, C-004, C-005]
  asset_refs: []
  run_refs: []
  source_refs: [SRC-prod-verify, SRC-actual-logic]
external_dependency:
  dependency_state:
  waiting_on:
  expected_signal:
  blocked_since:
  last_checked_at:
  next_touch_at:
  escalation_at:
  unblock_hypothesis:
exit_criteria:
  - 明确 historical_replay 中哪个材料层级优先
verification_method:
  - 对照实际核验和实际开发逻辑
allowed_actions: [read_file, summarize]
forbidden_actions: [write_prod, submit_external_request]
evidence_refs: [EV-20260622-prod-verify, EV-20260625-actual-logic]
updated_at: 2026-07-06T00:00:00+08:00
---

## 决策

第一轮回放中，原始群聊和需求分析只作为 Source Pack / Candidate Claim 来源；若它们与实际上线情况冲突，以 `03-实际上线情况` 下的核验报告和实际开发逻辑作为历史回放的更高置信来源。
