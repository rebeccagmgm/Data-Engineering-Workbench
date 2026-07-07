# agent-kb 知识吸收记录

日期：2026-07-07

范围：本次评估 `E:\02_area\数据开发-笔记本\agent-kb` 中对 Data-Engineering-Workbench 构建有直接价值的知识。结论是：agent-kb 应作为长期知识源和经验晋升目标，而不是被 Workbench 直接复制或整体挂载。

## 总判断

Workbench 和 agent-kb 的关系应是：

```text
Case 运行时
  -> 按 match / expand / verify / act 从 agent-kb 取小包知识
  -> 在 Case 内生成卡片、证据、断言和阻塞
  -> closeout 时筛选候选经验
  -> 复用验证后再晋升回 agent-kb / Skill / 能力契约
```

agent-kb 解决“长期知识怎么组织和消费”；Workbench 解决“一个具体需求今天怎么推进、怎么读回、怎么可信收口”。两者不能混成一个系统。

## 立即吸收

### 1. 知识读取采用 match -> expand -> verify -> act

Case 不能一次性把 agent-kb 全部塞进上下文。每次需要知识时，先从 `index.md`、frontmatter、标题、aliases、tags 和 description 匹配候选主题，再沿 wikilink / See Also / 同目录邻居展开必要依赖，最后判断覆盖是否足够。

Workbench 中可落成一个 `knowledge_bundle` 记录：

```yaml
knowledge_bundle:
  query: 金仕达资讯推送需求怎么拆
  matched_notes:
    - gfdata-CLI
    - 数据集与宽表-数仓开发流程
    - 渐进式知识读取-match-expand-verify-act
  expanded_notes:
    - gfdata-查询不到表-ES索引缺失
    - 数综平台-Atlas底层架构
  coverage:
    enough_to_act: false
    gaps:
      - 目标表当前 DDL 需要平台读回
      - 下游实际消费环境未知
```

这个 bundle 是 Case 的运行证据，不是正式知识沉淀。

### 2. 知识四分类进入晋升规则

agent-kb 的“事实型 / 规则型 / 过程型 / 经验型”分类正好适合作为 Workbench closeout 的晋升路由：

| 类型 | Workbench 来源 | 晋升目标 |
| --- | --- | --- |
| 事实型 | 表结构、字段含义、任务 ID、接口字段 | Case evidence；稳定后进入数据开发/股衍笔记 |
| 规则型 | 环境边界、禁止动作、真值源判断 | AGENTS.md / Skill / Workbench docs |
| 过程型 | 需求分析、上线核验、排查步骤 | workflow pattern / Skill |
| 经验型 | 真实任务中的误判、返工、反例 | 先进入 promotion-inbox，复用后再入 agent-kb |

尤其要避免把一次历史分析直接包装成“经验型知识”。经验型必须来自真实任务的失败、纠偏和下次验证。

### 3. 成功指标改成可信变更吞吐量

Workbench 的目标不是沉淀越多知识、生成越多卡片、调用越多工具，而是提高：

```text
单位人工投入内，被证据、核验和人类判断接受的数据变更数量
```

这意味着每个 Case 不只要有 Change，还要有 Trust：

- Change：改了哪些任务、SQL、表、数据集、宽表、推送或接口。
- Trust：哪些断言被哪些证据支撑；剩余风险是什么；下游是否可读回。

现有 `closeout.md` 的 Change / Trust / Learning 三节已经覆盖这个方向，后续指标应围绕 evidence coverage、human corrections、residual risks、review time 来看。

### 4. 资产状态层作为后置目标

agent-kb 中“数据开发工作台资产状态层”提醒我们：长期看，Workbench 不能只保存聊天和工具输出，还应保存资产、分区、任务版本、运行状态、人工确认和证据链。

但 MVP 阶段不新建数据库或资产状态平台，只把这些概念体现在字段和 evidence 中：

- `asset_refs`
- `run_refs`
- `truth_environment`
- `consumer_view`
- `time_semantics`
- `evidence_scope`

等多个真实 Case 验证后，再考虑单独的 asset-state index。

### 5. 推测式调查用于复杂排查，不用于简单任务

复杂排查可以采用候选树、分支隔离、证据验证：

```text
根问题
  -> 3-5 个候选原因分支
  -> 每个分支一个低成本只读验证动作
  -> 证据挂到 branch/card
  -> 被证据支持、否定、暂停或合并
  -> 最后由 Reviewer 检查结论
```

这适合数据未到、口径不一致、链路不清、跨系统责任边界等问题。不适合一个低成本查询就能回答的简单事实问题。

## 部分吸收

### 能力注册表

`Data-Engineering-Workbench能力注册表` 很有启发，但当前 Workbench 不应先做完整 registry。MVP 只在卡片里保留 `capability`、`allowed_actions`、`forbidden_actions`、`verification_method`、`asset_refs`、`run_refs`。当工具数量和错误选型开始成为瓶颈，再建设 `agent-resource.yaml`。

### Agent OS 最小标准

当前 workspace 已经有 `AGENTS.md`、`references/tools/`、repo-local skills 和操作规则。短期要做的是让这些入口更贴近 Case 执行，而不是新建一层 Agent OS 文档。

## 不吸收

### 不整体复制 agent-kb 到 Workbench

agent-kb 是长期知识库，里面包含业务、工具、方法论、文章、信号和项目记录。Workbench 如果整体加载它，会带来三类问题：

- 读不完：上下文被无关知识占满。
- 读偏：命中一个局部笔记就过早行动。
- 读旧：历史信号被误当成当前生产事实。

正确做法是每个 Case 按需取小包知识，并把覆盖判断写清楚。

### 不把旧 4 文件实验直接回滚为当前结构

agent-kb `context.md` 记录了早期金仕达实验：`request.md / analysis.md / tool-trace.jsonl / case.json` 的极简 case 曾在短时间内跑通。这个经验很重要，但当前设计已经吸收了审计意见，升级为六容器结构。

可吸收的是“极简优先”和“证据链优先”，不是回滚文件结构。

## 对主设计文档的修改建议

1. 增加“从 agent-kb 取知识”的运行协议：match / expand / verify / act。
2. 明确 agent-kb 是长期知识源和晋升目标，不是 Workbench 的内部目录。
3. 把“可信变更吞吐量”加入 MVP 指标解释。
4. 将推测式调查标为复杂 Case 的可选执行模式。
5. 将资产状态层标为后置目标，MVP 继续用 `asset_refs / run_refs / evidence` 表达。
