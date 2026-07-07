# Closeout

> 当前为 historical replay 草稿，不是正式收口。

## Change

- 历史需求目标：将 A 股和存托凭证的成交额、总股本、上市日期等字段加工到宽表，并推送至 `manage.MD_STOCK_DAILY_MARKET`。
- 关键资产：`dm_otc_test.md_stock_daily_market`、`dm_otc_n.md_stock_daily_market`、`manage.MD_STOCK_DAILY_MARKET`、`pdata_news_n.t02_stk_valu_idx`。
- 关键任务：238523、238824、238941、238963、201969。
- 引用：T-001、T-002、T-003、T-004、T-005。

## Trust

- C-001 由需求分析和原始群聊支撑，说明需求字段和推送目标。
- C-002 是早期方案判断，后续被实际逻辑修正，当前状态为 stale。
- C-003 由上线核验报告和实际逻辑支撑，说明现有 201969 h16 批次已替代新增 pb 批次路径。
- C-004 由上线核验报告和实际逻辑支撑，说明历史核验时存在目标表缺字段、推送未运行、库不匹配等上线前缺口。
- 剩余风险：如果要把这些结论作为当前生产事实，必须重新读回 Horae/Oracle 当前状态。

## Learning

- 候选沉淀 1：历史分析中的“拟新增批次表”必须允许被后续 evidence 标记 stale，不能直接晋升为知识。
- 候选沉淀 2：数据推送 Case 里，`done` 和 `verification_state=passed` 必须分开；加工跑通不等于推送链路端到端打通。
- 候选沉淀 3：目标表 DDL、推送 insert.sql、加工库/推送库一致性是推送类需求的必查核验点。
- 候选沉淀 4：测试环境 manage 库数据只能作为结构/格式核验，不能自动当成生产业务结论。
- 是否进入 promotion-inbox：待完成第一轮 Case 回放后再决定。
