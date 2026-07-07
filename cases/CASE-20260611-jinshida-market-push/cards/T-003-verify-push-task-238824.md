---
id: T-003
kind: task
title: 核验推送任务 238824
domain: push
capability: verify_hive_to_oracle_push
owner: agent
execution_state: done
verification_state: failed
priority: high
env: historical
input_refs:
  claim_refs: [C-004]
  asset_refs:
    - table:manage.MD_STOCK_DAILY_MARKET
    - table:dm_otc_n.md_stock_daily_market
  run_refs:
    - horae:238824
  source_refs: [SRC-prod-verify, SRC-actual-logic]
external_dependency:
  dependency_state: acknowledged
  waiting_on: 金仕达 / 数据开发 / 升级流程
  expected_signal: 推送任务实际运行成功且目标表读回数据
  blocked_since: 2026-06-22T00:00:00+08:00
  last_checked_at: 2026-06-25T00:00:00+08:00
  next_touch_at:
  escalation_at:
  unblock_hypothesis: 修复目标表字段和库表配置后，手工触发推送联调
exit_criteria:
  - 推送任务有成功实例
  - manage.MD_STOCK_DAILY_MARKET 能读回本链路推送数据
verification_method:
  - Horae 实例日志
  - manage Oracle 目标表读回
allowed_actions: [read_file, summarize]
forbidden_actions: [write_prod, submit_external_request]
evidence_refs: [EV-20260622-prod-verify, EV-20260625-actual-logic]
updated_at: 2026-07-06T00:00:00+08:00
---

## 结果

历史核验显示 238824 在当时从未运行，且存在目标表字段缺失、加工库与推送源库不一致等问题，因此不能标记为验证通过。

## 备注

这是一个很好的 `execution_state=done` 但 `verification_state=failed` 示例：核验动作完成了，但核验结果不通过。
