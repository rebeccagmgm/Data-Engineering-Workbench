---
id: Q-001
kind: question
title: 是否需要刷新当前 Horae / Oracle 状态
domain: verification
capability: decide_current_readback_scope
owner: user
execution_state: todo
verification_state: n/a
priority: low
env: historical
input_refs:
  claim_refs: [C-004, C-005]
  asset_refs:
    - table:manage.MD_STOCK_DAILY_MARKET
  run_refs:
    - horae:238824
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
  - 决定是否只做历史回放，还是补当前平台读回
verification_method:
  - 用户确认
allowed_actions: [ask_user]
forbidden_actions: [write_prod, submit_external_request]
evidence_refs: []
updated_at: 2026-07-06T00:00:00+08:00
---

## 问题

第一轮建议只做历史回放。如果后续希望把这个 Case 的结论转为当前事实，需要重新读回 Horae 任务、升级状态和 manage 目标表。
