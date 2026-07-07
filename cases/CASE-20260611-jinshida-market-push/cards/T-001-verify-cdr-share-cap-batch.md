---
id: T-001
kind: task
title: 核验 CDR 总股本批次路径
domain: schedule
capability: verify_scheduler_source_batch
owner: agent
execution_state: done
verification_state: passed
priority: high
env: historical
input_refs:
  claim_refs: [C-002, C-003]
  asset_refs:
    - table:pdata_news_n.t02_stk_valu_idx
  run_refs:
    - horae:201969
    - horae:70346
  source_refs: [SRC-analysis, SRC-prod-verify, SRC-actual-logic, SRC-atomic-pb]
external_dependency:
  dependency_state: satisfied
  waiting_on:
  expected_signal:
  blocked_since:
  last_checked_at: 2026-06-25T00:00:00+08:00
  next_touch_at:
  escalation_at:
  unblock_hypothesis:
exit_criteria:
  - 明确 CDR 总股本是否仍需新增 t02_stk_valu_idx_pb
  - 明确实际使用的是哪个批次/任务
verification_method:
  - 读取上线核验报告与实际开发逻辑
allowed_actions: [read_file, summarize]
forbidden_actions: [write_prod, submit_external_request]
evidence_refs: [EV-20260622-prod-verify, EV-20260625-actual-logic, EV-20260611-atomic-pb]
updated_at: 2026-07-06T00:00:00+08:00
---

## 结果

早期方案 C-002 认为需要新增 `t02_stk_valu_idx_pb` 1730h 批次。后续实际核验显示已有 201969 h16 批次，且该任务全量覆盖写入原表 `t02_stk_valu_idx` 的 `grp_id='07'` 分区，238523 从原表读取即可。

## 影响

- C-002 标记为 `stale`。
- C-003 标记为 `trusted`。
- 原子笔记中的 pb 批次路线保留为历史线索，不作为当前方案。
