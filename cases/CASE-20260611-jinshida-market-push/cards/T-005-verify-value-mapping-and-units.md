---
id: T-005
kind: task
title: 核验字段映射和单位差异
domain: data_quality
capability: verify_field_mapping
owner: agent
execution_state: done
verification_state: pending
priority: medium
env: historical
input_refs:
  claim_refs: [C-001, C-004]
  asset_refs:
    - table:dm_otc_test.md_stock_daily_market
    - table:manage.MD_STOCK_DAILY_MARKET
  run_refs:
    - horae:238523
  source_refs: [SRC-analysis, SRC-solution, SRC-prod-verify, SRC-actual-logic]
external_dependency:
  dependency_state: open
  waiting_on: 历史材料 / 金仕达确认
  expected_signal: 明确 MK_CODE、UPDATE_TIME、tot_equi 单位是否符合金仕达最终口径
  blocked_since:
  last_checked_at: 2026-07-06T00:00:00+08:00
  next_touch_at:
  escalation_at:
  unblock_hypothesis: 通过实际逻辑和目标表样例判断哪些差异为可接受，哪些需业务确认
exit_criteria:
  - 明确 MK_CODE 固定值与交易所代码差异
  - 明确 UPDATE_TIME 使用源表更新时间还是推送时间
  - 明确 tot_equi 单位和是否需要换算
verification_method:
  - 对照需求分析、实现方案、实际逻辑和上线核验报告
allowed_actions: [read_file, summarize]
forbidden_actions: [write_prod, submit_external_request]
evidence_refs: [EV-20260611-analysis, EV-20260611-solution, EV-20260622-prod-verify, EV-20260625-actual-logic]
updated_at: 2026-07-06T00:00:00+08:00
---

## 当前判断

历史材料显示字段映射存在多处演化：`MK_CODE` 从固定 `'1'` 到实际交易所代码，`UPDATE_TIME` 从推送时间到源表 `rec_upd_time`，`tot_equi` 单位需要确认或已在实际逻辑里说明为万股。

## 后续

作为 historical replay，先保留 pending；若要当前复用，需要重新向最终口径或当前系统读回确认。
