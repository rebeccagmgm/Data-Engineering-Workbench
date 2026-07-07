---
id: T-004
kind: task
title: 核验目标表 TOTAL_SHARE_CAP 字段
domain: ddl
capability: verify_target_table_ddl
owner: agent
execution_state: done
verification_state: failed
priority: high
env: historical
input_refs:
  claim_refs: [C-004]
  asset_refs:
    - table:manage.MD_STOCK_DAILY_MARKET
  run_refs: []
  source_refs: [SRC-prod-verify, SRC-actual-logic]
external_dependency:
  dependency_state: acknowledged
  waiting_on: 金仕达
  expected_signal: 目标表包含 TOTAL_SHARE_CAP 字段，或推送 SQL 与目标 DDL 对齐
  blocked_since: 2026-06-22T00:00:00+08:00
  last_checked_at: 2026-06-25T00:00:00+08:00
  next_touch_at:
  escalation_at:
  unblock_hypothesis: 金仕达 ALTER TABLE ADD TOTAL_SHARE_CAP，或双方确认去掉该字段
exit_criteria:
  - 目标表 DDL 与 insert.sql 字段一致
verification_method:
  - 目标库 describe
  - 推送 insert.sql 对照
allowed_actions: [read_file, summarize]
forbidden_actions: [write_prod, submit_external_request]
evidence_refs: [EV-20260622-prod-verify, EV-20260625-actual-logic]
updated_at: 2026-07-06T00:00:00+08:00
---

## 结果

历史核验报告指出 `manage.MD_STOCK_DAILY_MARKET` 缺 `TOTAL_SHARE_CAP` 字段，而推送 `insert.sql` 写了该字段。该问题在历史核验时阻塞端到端推送。
