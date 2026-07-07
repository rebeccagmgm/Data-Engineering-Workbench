# 数据开发 Case Workbench 最佳实践评估

> 目的：先停下来校准方向，避免把时间花在“看起来很完整、但不会减少真实工作摩擦”的系统上。

## 结论先行

当前 `data-development-case-workbench` 的方向基本是对的：它应该先是一个**文件优先、证据优先、动态任务卡驱动的 Case Space**，而不是一开始就做成完整前端、完整项目管理系统、完整知识库或多 Agent 平台。

外部审计进一步收紧了这个结论：当前不是要继续扩设计，而是要把 MVP 砍薄。第一轮吸收记录见 `references/research/workbench-openai-audit-absorption.md`。第二轮复审后，重点从“砍对象”转为“冻结可执行协议”，吸收记录见 `references/research/workbench-openai-audit-v2-absorption.md`。

更准确地说，它现在应该处在：

- `Explore 后期`：用真实需求把问题空间摸清楚。
- `Expand 早期`：把高频流程沉淀成卡片模板、能力契约、核验清单。
- 暂时不要进入 `Extract`：不要过早平台化、产品化、自动化。

判断标准不是“功能多不多”，而是：

1. 下一个相似需求是否更快进入清晰状态。
2. 阻塞点、权限、审批、等待他人这些事项是否更早暴露。
3. 测试、上线、下游读到的结果是否更容易形成可信证据。
4. 常见经验是否能在下一次自动浮出来，而不是留在聊天记录里。
5. 你的主观体感是否从“蒙头干”变成“知道现在卡在哪里”。

## 外部最佳实践给出的共同方向

### 1. 任务系统：卡片要动态，视图要可变

GitHub Projects、GitLab Issue Boards 和 Jira 的共同点不是固定流程，而是：

- 工作项是核心对象。
- 工作项有状态、负责人、标签、字段、阻塞关系。
- 同一批工作项可以用表格、看板、路线图、过滤视图来观察。
- 流程状态和流转规则可以配置，而不是把所有团队塞进同一条流程。

这直接支持我们的设计选择：

- 每个需求一个 `Case Space`。
- 每个需求内动态生成 `Card`，而不是预设固定子任务树。
- 固定的不是“任务类型”，而是卡片的最小字段：`目标 / 状态 / owner / 阻塞 / 证据 / 下一步`。
- 可以先用 Markdown/YAML 表达卡片，再生成只读 dashboard。

不建议现在做的事：

- 不要把“下游联调 / 权限 / DM宽表 / 采集批次 / 推送任务”写死成唯一流程。
- 不要先追求复杂拖拽看板。
- 不要为了像 Jira 而复制 Jira。

### 2. 文档系统：文件优先，视图可生成

Backstage TechDocs、Docs-as-Code、Diátaxis 和 ADR 的共同点是：

- 文档源文件应该可版本化、可搜索、可 diff。
- 生成网页只是消费方式，不是知识本体。
- 不同类型的知识要分开：教程、How-to、参考、解释，不能混成一锅。
- 重要决策要有轻量记录：当时背景、选择、后果。

这支持我们的设计：

- `原始需求背景/` 保留附件、聊天、流程、原始信息。
- `analysis.md` 记录当前可信结论，而不是直接覆盖原始材料。
- `cards/` 记录执行项和阻塞项。
- `evidence/` 记录测试环境核验、上线核验、下游读回。
- `decisions/` 可以用轻量 ADR 记录“为什么这么拆”“为什么先不上线”“为什么由人工申请权限”。
- HTML 可以做，但应该是由文件生成的只读视图。

不建议现在做的事：

- 不要把聊天记录直接当知识库。
- 不要一上来建设第二套完整知识库。
- 不要让前端成为唯一入口，导致文件和真实工作脱节。

### 3. Agent 系统：先从单 Agent、明确工具、评估闭环开始

OpenAI 和 Anthropic 的 Agent 实践有几个稳定共识：

- 先从最简单可行的 Agent 工作流开始。
- 工具要标准化、可测试、可复用。
- 多 Agent 适合复杂、不可预测、需要并行拆解的问题，但不是默认起点。
- Agent 要有 guardrail、sandbox、readback、eval baseline。
- Skills / procedural knowledge 要采用渐进式披露：先加载索引和路由，必要时再展开细节。

这支持我们的设计：

- Workbench 不应先做成“自动帮你完成所有需求”的黑盒 Agent。
- 它更应该先做成“你和 Codex 一起分析、拆卡、执行、核验、复盘”的协作空间。
- 每次沉淀出来的不是大段经验文，而是：
  - card template
  - workflow pattern
  - capability contract
  - verification checklist
  - failure pattern
- 真正自动化之前，先积累可回放的案例和评估样本。

不建议现在做的事：

- 不要先追求多 Agent 编排。
- 不要把“我常做的需求”直接自动执行到生产。
- 不要没有测试环境验证和下游读回就把 API 200 当完成。

### 4. 数据工程系统：可信结果比执行动作更重要

dbt、OpenLineage、Great Expectations、Dagster 等数据工程实践给出的共同方向是：

- 数据资产要有上下游关系。
- 任务运行、数据集、表、字段、测试、文档需要能被串起来。
- 验证结果应该可读、可分享、可追溯。
- “任务跑完”不等于“业务读到了正确数据”。

这与我们之前的判断一致：

- 每个 Case 不只记录“做了什么”，还要记录：
  - 涉及哪些表 / 数据集 / 宽表 / 推送 / 调度任务。
  - 哪些环境核验过。
  - 哪些下游读到了。
  - 哪些权限或审批仍然阻塞。
  - 哪些事实来自原始材料，哪些来自平台读回。
- `Trust Pack` 应该成为上线前后最重要的产物之一。

不建议现在做的事：

- 不要先发明一套复杂血缘模型。
- 不要把血缘、调度、数据集、推送全做成独立平台。
- 先让 Case 里的证据结构能映射到 `dataset / job / run / validation / downstream readback`，以后再自动化。

### 5. 可靠性系统：复盘不是写总结，是降低下一次失败概率

Google SRE 的 postmortem 文化和 DORA 指标都提醒了一点：只看吞吐量会误导。

对这个 Workbench，更合适的指标不是“一个月做了多少需求”，而是：

- 需求从进入到分析清楚的时间。
- 卡住但未显性暴露的时间。
- 测试环境一次通过率。
- 上线后返工次数。
- 下游读回缺失次数。
- 相似需求复用模板次数。
- 相似需求需要重新问的问题数量。

所以 Case 结束时不应只是“已上线”，而应产出：

- `Change Pack`：改了什么、涉及什么资产、谁确认。
- `Trust Pack`：怎么验证、谁读回、证据在哪里。
- `Learning Pack`：这次有什么可复用、有什么坑下次要提前暴露。

## 从你的知识库得到的关键约束

你的现有知识库已经有几个非常有价值的判断，不应该被新系统推翻。

### 知识四分类

`事实 / 规则 / 过程 / 经验` 必须分开：

- 事实：平台对象、表、字段、接口、任务、权限状态。
- 规则：生产只读、测试先验证、上线审批、命名规范、环境边界。
- 过程：如何新建数据集、如何提采集批次、如何核验推送、如何做上线报告。
- 经验：某次真实需求里踩过的坑，以及之后被验证有效的修正。

这意味着 Workbench 的知识沉淀不能只是一堆 Markdown。每次沉淀都要先判断类型。

### Match - Expand - Verify - Act

你的知识库里已有“渐进式知识读取”思路：

1. Match：先匹配候选知识。
2. Expand：展开必要依赖。
3. Verify：确认覆盖当前问题。
4. Act：再执行。

这非常适合作为每个 Case 的分析阶段默认节奏。

### Workbench 不是知识库本体

你的知识库已经明确过：数据开发 Workbench 的核心不是 skill market、知识库、多 Agent 平台或工具门户，而是：

```text
query -> execute -> verify -> correct -> distill
```

因此这个 Workbench 应该沉淀“工作闭环”，而不是复制一份 `agent-kb`。

### 可信变更吞吐量

AI 让“产生改动”变便宜了，真正稀缺的是“把改动变成组织可信结果”。

这说明 Workbench 的价值应该集中在：

- 明确需求。
- 正确拆解。
- 暴露阻塞。
- 收集证据。
- 降低上线不确定性。
- 把真实经验变成下一次可复用的程序性知识。

## 对当前设计的校准

### 应该保留

- 一个需求一个 `Case Space`。
- `原始需求背景/` 作为 Source Pack。
- 动态任务卡，而不是固定流程图。
- `done` 和 `verified` 分开。
- 权限、审批、等待他人都作为显式卡片。
- `event-log.md` 记录关键事实变化。
- `workbench-knowledge/` 作为轻量运行时知识层。
- 稳定经验再回流到 `agent-kb`。

### 应该补强

- 为每个 Case 增加 `Change Pack / Trust Pack / Learning Pack` 收口。
- 为每个卡片增加 `evidence_required` 或 `verification_method` 字段。
- 为知识沉淀增加“是否真的复用过”的判断，不要一次案例就升格为强规则。
- 为每个 workflow pattern 增加适用条件和反例。
- 为权限/审批类卡片增加 `blocked_since`、`waiting_on`、`next_ping_date`。

### 应该暂缓

- 完整前端编辑器。
- 多 Agent 自动执行。
- 独立完整知识库。
- 复杂血缘图库。
- 复杂流程建模器。
- 与所有平台的深度双向同步。

## “不做无用功”的功能门槛

任何新功能如果不能回答下面至少一个问题，就先不做：

1. 它能否让一个新需求更快被分析清楚？
2. 它能否让阻塞、等待、审批更早被看见？
3. 它能否让测试/上线/下游读回证据更完整？
4. 它能否减少下一次相似需求的重复提问？
5. 它能否让某个高频平台操作更可验证、更少出错？
6. 它能否产出可复用的模板、能力契约或核验清单？

如果一个功能连续两个真实 Case 没有被使用，就放进 `parking-lot.md`，不要继续打磨。

## 推荐阶段路线

### 第 0 阶段：选一个真实 Case 试运行

目标：不用写系统，先验证结构是否贴合真实工作。

产物：

- 一个历史或当前需求的 Case Space。
- `原始需求背景/`
- `analysis.md`
- `cards/*.md`
- `evidence/*.md`
- `event-log.md`
- `closeout.md`

验收：

- 能不能一眼看到当前状态。
- 能不能一眼看到谁卡住。
- 能不能一眼看到哪些结论有证据。
- 能不能从这次 Case 提炼出 1-3 个可复用模板。

### 第 1 阶段：模板化高频卡片

目标：只沉淀真实出现过、重复概率高的卡。

候选模板：

- 申请表查询权限。
- 申请调度主题权限。
- 新建需求采集子任务。
- 新建数据集。
- 新增宽表。
- 新增推送任务。
- 测试环境核验。
- 上线后下游读回。

验收：

- 每个模板都有适用条件、输入、owner、证据要求、完成判定。
- 模板不是流程强制项，只是拆卡时的候选。

### 第 2 阶段：生成只读 Dashboard

目标：让你每天能看见所有 Case 和卡点。

形式：

- 先生成静态 HTML。
- 只读。
- 从 Markdown/YAML 生成。
- 不承载编辑逻辑。

核心视图：

- Case 列表。
- 今日阻塞。
- 等待我处理。
- 等待他人/审批。
- 即将上线。
- 缺少核验证据。
- 可沉淀知识候选。

验收：

- dashboard 不是主系统，只是视图。
- 修改仍回到文件。
- 真实需求中每天会打开看。

### 第 3 阶段：能力契约和评估样本

目标：把 CLI / OpenCLI / Horae / szdata / DSP / QC 等能力变成可验证的工具契约。

每个能力契约至少包含：

- 能做什么。
- 不能做什么。
- 所属环境。
- 是否允许写。
- 输入是什么。
- 输出是什么。
- 成功判定是什么。
- 下游读回怎么做。
- 常见失败是什么。

同时从真实 Case 中抽取 eval 样本：

- 需求描述。
- 期望拆卡。
- 必须检查的知识。
- 必须产生的证据。
- 错误拆解示例。

## 是否需要一开始做 HTML / 前端

建议：

- 可以做 `只读 HTML dashboard`。
- 不建议一开始做完整前端应用。

原因：

- 当前真正不稳定的是对象模型和工作流边界，不是 UI。
- 文件结构还需要被真实 Case 打磨。
- 只读 HTML 能快速提升可见性，又不会把你锁进复杂前端状态管理。
- 等 3-5 个真实 Case 跑完，再决定是否需要编辑型前端。

最小可行 HTML：

- 读取所有 Case 的 `case.yaml` / `cards/*.md`。
- 展示 Case 状态和阻塞卡。
- 点击跳到本地文件路径。
- 不做写入。
- 不做账号体系。
- 不做平台同步。

## 是否需要单独知识库

建议：

- Workbench 内保留一套**轻量运行时知识层**。
- 不建设第二个完整知识库。

边界：

- `agent-kb` 是长期知识库。
- `workbench-knowledge/` 是 Case 工作时的候选模板、路由、能力契约、沉淀入口。
- Case 里的 `learnings/` 是临时沉淀。
- 只有经过复用或核验的内容，再提升到 `agent-kb`。

这与 Flow2Spec 一类实践相似：本地 `.Knowledge` 更像路由、结构和增量沉淀层，不是复制完整业务知识。

## 可选外部工具评估

这些不是当前必做项，只是未来到对应阶段时的候选。

| 需求 | 候选方向 | 当前建议 |
| --- | --- | --- |
| 看板 / 项目管理 | GitHub Projects、GitLab Boards、Plane、OpenProject | 先不接入，等卡片模型稳定 |
| 文档站 | MkDocs、Backstage TechDocs | 可在只读 dashboard 之后评估 |
| 决策记录 | ADR 模板 | 可以立刻轻量使用 |
| 数据校验报告 | Great Expectations、dbt tests 风格 | 先模仿报告结构，不急着接入 |
| 血缘模型 | OpenLineage dataset/job/run | 先让证据字段可映射 |
| 调度/资产抽象 | Dagster asset 思路 | 先作为概念参考 |

## 建议立即更新到设计文档的原则

1. Workbench 的第一目标是提升“可信变更吞吐量”，不是提升自动化炫技程度。
2. Case 的结束产物必须包含 `Change Pack / Trust Pack / Learning Pack`。
3. 卡片模板只能来自真实 Case，不能凭空枚举。
4. Dashboard 只能先做只读生成视图。
5. Workbench Knowledge Layer 是运行时路由和沉淀层，不是第二知识库。
6. 多 Agent 和深度自动化必须等待 eval 样本与能力契约成熟。

## 参考来源

### 官方 / 行业实践

- [GitHub Docs - Planning and tracking with Projects](https://docs.github.com/en/issues/planning-and-tracking-with-projects)
- [Atlassian Jira - Work with issue workflows](https://support.atlassian.com/jira-cloud-administration/docs/work-with-issue-workflows/)
- [GitLab Docs - Issue boards](https://docs.gitlab.com/user/project/issue_board/)
- [Backstage TechDocs](https://backstage.io/docs/features/techdocs/)
- [Diátaxis documentation framework](https://diataxis.fr/)
- [Architecture Decision Records](https://github.com/architecture-decision-record/architecture-decision-record)
- [DORA metrics](https://dora.dev/guides/dora-metrics/)
- [Google SRE - Postmortem Culture](https://sre.google/sre-book/postmortem-culture/)
- [OpenAI - A practical guide to building AI agents](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/)
- [OpenAI Academy - Workspace agents](https://openai.com/academy/workspace-agents/)
- [Anthropic - Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)
- [Anthropic - Writing effective tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents)
- [Anthropic - Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- [dbt Docs - Documentation](https://docs.getdbt.com/docs/build/documentation)
- [OpenLineage Docs](https://openlineage.io/docs/)
- [Great Expectations - Data Docs](https://docs.greatexpectations.io/docs/0.18/reference/learn/terms/data_docs/)
- [Dagster Concepts](https://docs.dagster.io/getting-started/concepts)
- [Plane - open source project management](https://github.com/makeplane/plane)
- [Flow2Spec usage guide](https://github.com/Lands-1203/Flow2Spec/blob/main/docs/en/usage-guide.md)

### 本地知识库

- `E:\02_area\数据开发-笔记本\agent-kb\知识库设计\知识四分类-事实规则过程经验.md`
- `E:\02_area\数据开发-笔记本\agent-kb\知识库设计\知识库消费层路由协议.md`
- `E:\02_area\数据开发-笔记本\agent-kb\知识库设计\渐进式知识读取-match-expand-verify-act.md`
- `E:\02_area\数据开发-笔记本\agent-kb\工程方法\数据智能体架构设计\data-engineer-workbench产品闭环架构.md`
- `E:\02_area\数据开发-笔记本\agent-kb\工程方法\数据智能体架构设计\可信变更吞吐量.md`
- `E:\02_area\数据开发-笔记本\agent-kb\工程方法\AI协作\评估验证与质量门禁\Agent可观测到Evals闭环.md`
- `E:\02_area\数据开发-笔记本\agent-kb\知识库设计\开发过程生成知识图谱.md`
- `E:\02_area\数据开发-笔记本\agent-kb\工程方法\工程治理\3X阶段化工程治理.md`
