# 数据开发 Case Workbench 严苛审计报告

## 审计基线与总判断

本审计以你上传的两份设计材料为主语料：一份是方向校准与行业映射，一份是对象、目录和卡片机制的初步设计。两份文档已经清楚表达出你的核心意图：**不要做固定流程图，而要做一个围绕单个需求动态演化的 Case Space**；同时坚持**文件优先、证据优先、done 与 verified 区分、只读 HTML 由源文件生成、轻量运行时知识层而非第二知识库**。这些判断彼此一致，而且和你要解决的问题类型是匹配的。fileciteturn0file0 fileciteturn0file1

先说结论：**方向基本对，但当前版本已经开始出现“架构名词扩张”**。你在文档里同时引入了 Source Pack、Case Ledger、Event Log、Card Board、Capability Registry、Evidence Store、Trust Pack、Knowledge Compiler，以及最终的 Change Pack / Trust Pack / Learning Pack；这对一个成熟系统是合理分层，但对两周验证期来说，已经偏向“先定义完整操作系统，再证明是否好用”。你的风险不在于想法错，而在于**你已经快把验证系统，设计成了需要先被维护的系统**。fileciteturn0file1

从外部实践看，适合你的不是“固定工作流引擎”，而是“**可配置的工作项 + 多视角视图 + 自定义字段 + 依赖关系 + 自动化少量重复动作**”。GitHub Projects 明确把 Projects 定义为 adaptable、flexible 的规划与追踪工具，支持表格、看板、路线图、多视图、自定义字段、模板和自动化，而且“不强制某一种方法论”；GitLab issue boards 也强调卡片、列表、可定制元数据和不同工作流视角，而不是把所有团队塞进一条固定状态流。你的“动态任务卡而非固定流程图”是对的。citeturn2view0turn9view0turn14view1

同时，外部 agent 实践给出的建议也和你的工程直觉一致：Anthropic 在 2024 年末明确建议先找“最简单可行的方案”，只在确有收益时再增加复杂度；对 well-defined 任务，workflow 往往比 agent 更可预测；对开放式、步数无法预估的问题，agent 才有优势，而且前提是有清晰工具、环境反馈、停止条件和评估基线。你现在想暂缓多 Agent、深度同步、复杂血缘图，这不是保守，而是对。citeturn16view4turn16view5turn16view6turn16view7

所以，总判断可以压缩成一句话：**不是过度设计到该推翻，而是过度命名、过度分层、过度收口，已经超过了 MVP 所需。接下来应该砍结构，而不是再补结构。** 这个结论同时来自你自己的设计文档和外部工具/agent/数据工程实践。fileciteturn0file0 fileciteturn0file1 citeturn12view5turn14view0turn12view1turn13view1

## 过度设计在哪里以及 MVP 还能怎么砍

你现在最明显的过度设计，不是 UI，也不是技术栈，而是**一次性把“执行系统、验证系统、沉淀系统、展示系统、能力抽象系统”都定义成了一等公民**。这会带来三个直接后果。第一，录入成本上升，Case 还没跑顺就先要维护很多容器。第二，系统边界不稳，真实需求一来就会发现对象重叠。第三，实验结果会被“维护文档的勤奋程度”污染，而不是验证工作流本身是否有效。这个风险在你的目录设计里已经很明显：一个 Case 目录从一开始就包含原始材料、总览、事件、能力、卡片、证据、分析、变更、信任、沉淀多个区域；对长期仓库来说合理，对 2 周验证来说太厚。fileciteturn0file1

最该先砍掉的，不是“核心思想”，而是“收口仪式感”。**Change Pack / Trust Pack / Learning Pack 不应该作为 MVP 的三个独立包，而应该先是一个 `closeout.md` 的三个章节。** 原因很简单：在验证期，最重要的是证明这三个切面有价值，而不是证明它们值得成为目录。Great Expectations 把验证结果和期望自动转成可读文档，dbt 也在强调基于运行后 metadata 的最新状态可见性；这些实践共同说明，**“可信包”应该尽量接近自动生成或半自动汇总，而不是手工整理为高仪式感档案**。否则它很快会退化成“看起来专业，但实际上没人及时维护”的尸体文件。citeturn12view0turn11view7

第二个要砍的是 **单独的 `workbench-knowledge/` 目录层**。你的判断“不要建设第二知识库”是对的，但如果一开始就专门建 promotion-inbox、workflow-patterns、capability-contracts、promotion-log，你实际上已经开始建设一个缩小版知识库了。Anthropic 的 Agent Skills 经验很值得参考：它们把可复用的程序性知识放进文件夹和 `SKILL.md`，靠**渐进式加载**和**按需展开**工作，而不是先建一个完整的知识管理门户。对你来说，验证期更好的做法是：**只保留一个 `patterns-inbox.md` 或 `promotion-inbox.md`**，先记录“这次有什么值得下次少踩坑”，等真的复用两次以上，再拆目录、分类和晋升。citeturn17view0turn17view1turn17view2

第三个要砍的是 **Capability Registry 的独立存在**。你文档中把“能力层”和“工具层”分离，这个观念是好的，因为它能防止业务语义绑定到某个 CLI 命令上。问题在于：在 MVP 阶段，**能力契约应该是卡片字段，不应该先做成专门的注册表对象**。Anthropic 对 agent tools 的经验非常明确：工具要有清晰、边界明确的目的，数量要克制，命名和上下文返回要服务于任务完成；评估要和工具一起设计。换言之，你应该先看“某种能力字段是否真的让卡片更好用”，而不是先建一个看起来很正统的能力注册中心。citeturn16view0turn16view1turn16view2

如果按极限削减，我建议你的 MVP 目录只剩下面这几个文件和目录：

```text
cases/
  CASE-xxxx/
    case.yaml
    notes.md
    events.md
    cards/
    evidence/
    closeout.md
```

其中 `case.yaml` 只放当前阶段、当前可信结论、最大阻塞、下一步、负责人；`notes.md` 吸收原来的 `analysis.md` 和 Source Pack 索引；`events.md` 记录会改变判断的事件；`cards/` 放所有卡；`evidence/` 放关键截图、JSON、SQL、日志；`closeout.md` 只分三段：改了什么、怎么证明、下次记什么。你原方案里好的思想几乎都保住了，但维护成本被砍掉一半以上。这个裁剪思路，也符合 docs-as-code 和静态文档工具的一般经验：**先把 Markdown/YAML 作为源，视图和分类后置**。citeturn12view5turn14view0

## 缺失的核心对象与状态模型

你现在最大的模型缺口，不是“少一种卡片类型”，而是**缺少几个正交对象**。如果这些对象不补，系统会越来越像文档，而不像一个可演化的工作台。最关键缺的，是 **Claim 对象**，也就是“候选事实/当前断言”这一层。你已经在文字上区分了历史分析、合作方反馈、平台读回、人工确认和当前可信结论，但在对象层还没有真正把“结论”从“原始材料”和“证据”之间独立出来。结果就是：Case 里会充满散落在笔记、证据卡和事件里的判断，后续很难知道“当前系统认为真的是什么”。从你自己的文档出发，至少要把 `claim_id / statement / status / evidence_refs / source_refs / last_confirmed_at / expires_at` 作为显式对象。fileciteturn0file1

第二个缺的是 **External Dependency 对象**。你现在有 blocker card，但 blocker 仍然偏“任务形态”。而真实数据开发里，很多阻塞不是任务没做，而是**外部依赖尚未满足**，比如审批人未批、合作方未同步 DDL、主题权限尚未传播、下游未读回。依赖对象应至少有 `waiting_on / blocked_since / expected_signal / next_ping_at / escalation_at / unblock_hypothesis`。否则 waiting 和 blocked 会被写成状态，却没有被建模成能追踪的东西。GitHub 和 GitLab 都把 issue 依赖、子问题、阻塞关系作为一等协作对象，而不只是描述文本，这正是因为“关系本身”会决定工作是否可推进。citeturn10view0turn11view0turn14view1turn9view0

第三个缺的是 **AssetRef / RunRef**。你在 Case 中会涉及表、数据集、宽表、调度任务、推送任务、接口、主题、运行实例、目标库等对象；如果这些只以自然语言散落在卡片文本里，Case 之间就无法复盘、更无法做后续自动聚合。OpenLineage 的核心模型是 dataset / job / run，并通过 facets 扩展元数据；Dagster 的核心抽象则把 asset、job、schedule、sensor、asset check 分开。你现在不需要引入完整血缘系统，但至少要给卡片和证据加上 `asset_refs` 与 `run_refs`，这样未来无论接 OpenLineage 还是本地生成只读 dashboard，都不会全部重写。citeturn12view1turn11view2turn13view1turn13view3

第四个缺口，是**把执行状态和验证状态混在了一条状态链里**。你虽然正确地区分了 done 和 verified，但当前枚举仍然是 `todo -> doing -> waiting -> blocked -> done -> verified -> obsolete`。这在早期勉强能用，到了真实生产环境就会出问题，因为“执行完成”和“验证通过”不是同一维度。比如某卡可以 `execution=done` 但 `verification=failed`；也可能 `execution=waiting_external` 同时 `verification=not_applicable`；还可能 `execution=done` 后因为读回失败再次变成 `rework`。把它们挤在一条状态链里，会迫使你用回退和特例修补。更稳的做法是把状态拆成两个正交轴：

```yaml
execution_state: todo | doing | waiting | blocked | done | cancelled
verification_state: n/a | pending | passed | failed
```

然后 `verified` 不再是状态，而是 `execution_state=done && verification_state=passed` 的派生结果。这个改动很关键，因为它直接关乎你最重视的“done 不等于 verified”。fileciteturn0file1

第五个缺口，是 **Case 级阶段状态**。你已经有“分析中 / 等确认 / 测试中 / 待升级 / 已上线 / 已归档”之类描述，但它还没有清楚地和卡片状态解耦。建议 Case 级单独保留一条轻量阶段线，例如：

| 层级 | 建议状态 |
|---|---|
| Case 阶段 | intake / analysis / execution / verify / release / observe / closed |
| 卡片执行 | todo / doing / waiting / blocked / done / cancelled |
| 卡片验证 | n-a / pending / passed / failed |
| Claim 状态 | candidate / trusted / rejected / stale |
| 依赖状态 | open / waiting / escalated / cleared / expired |

这样你才能表达一种现实常态：**Case 已进入 verify 阶段，但个别卡片仍在 waiting，某些 claim 已 stale，而另一条证据刚通过。**

## 动态任务卡怎样既灵活又不失控

你现在的任务卡思路有一个优点和一个危险。优点是你已经意识到需求会动态长出任务，不能先写死树。危险是你又在 `type` 里列出了 permission、schedule-permission、gather-subtask、dataset、widetable、push、ddl、verify、communicate 等大量业务型类型，这意味着你正在把“不要固定流程”偷换成“先准备足够多的固定类型”。这会产生一种常见假象：**表面是动态卡片，实质是隐藏流程菜单**。fileciteturn0file1

更稳的做法是把卡片设计成“**动作语义稳定，业务类别开放**”。也就是说，卡片主类型只保留少数几类，例如：

| 主类型 | 含义 |
|---|---|
| `task` | 要执行的动作 |
| `question` | 未解问题 |
| `blocker` | 外部依赖或障碍 |
| `evidence` | 证据快照 |
| `decision` | 关键决策 |
| `learning` | 候选沉淀 |

而你现在关心的 permission、dataset、push、ddl 等，应该变成 `domain` 或 `capability` 字段，而不是一上来就固化成主类型。这样做有三个好处。第一，系统对象不会越来越多。第二，不同 Case 仍能共用卡片机制。第三，后续统计时能区分“动作结构”和“业务场景”。这和 GitHub/GitLab 一类工具把工作项、字段、依赖关系和多视图分开的做法是一致的。citeturn2view0turn14view1turn9view0

为了防止动态卡片失控，我建议给每张卡加四条硬约束：

| 约束 | 目的 |
|---|---|
| 一张卡只能有一个直接 owner | 防止“大家都知道、其实没人负责” |
| 一张卡只能有一个主完成信号 | 防止完成标准模糊 |
| 一张卡最多绑定一个主阻塞原因 | 防止卡片变成问题垃圾桶 |
| 一张卡必须有下一次触碰时间 | 防止 waiting 卡永久沉底 |

对应的最小字段，我建议是下面这样：

```yaml
id: T-014
kind: task
domain: permission
title: 申请调度主题读取源表权限
purpose: 让测试任务不再报 SELECT denied
owner: 某人
created_from:
  - claim:C-007
  - event:EV-018
asset_refs:
  - table:odata_n_cso.e_xxx
  - topic:DM_OTC_N
capability: verify_schedule_topic_table_permission
execution_state: waiting
verification_state: pending
waiting_on: 数据平台审批
blocked_since: 2026-07-06
next_touch_at: 2026-07-08
exit_criteria: 任务运行不再报权限错误
evidence_policy:
  required:
    - 调度实例日志
    - 权限查询读回
supersedes: []
obsolete_reason:
```

实践里最容易把系统拖死的，不是缺字段，而是**卡片粒度不受控**。因此我建议你明确四条拆分规则：如果一张卡出现两个 owner、两个外部依赖、两个主证据方法，或者估计要跨两个工作日，就强制拆卡；如果一张卡只是“继续跟进”“再看看”，则不允许创建，必须挂到某个现有 blocker 或 question 下；如果一张卡没有 `exit_criteria`，视为无效；如果 waiting 卡没有 `next_touch_at`，系统每天把它打回。这个治理方式，本质上是在把“动态”限制在有反馈闭环的范围内，而不是容忍无限增殖。citeturn10view0turn11view1turn16view7

你提出的 done / verified 区分非常重要，但它要真正落地，**必须把验证设计成“读回协议”，而不是“补充说明”**。Great Expectations 的 Data Docs 之所以有用，是因为它把 expectations 和 validation results 编译成可读文档，重点不在“写报告”，而在“让验证结果天然成为文档”；dbt 的 Catalog 也是依赖作业运行后的 metadata 来保持最新生产视图。你的 Trust Pack 也应该这样思考：先定义每类卡需要什么可读回的证据，再从证据生成收口，而不是反过来用 closeout 手工追述。citeturn12view0turn11view7

## 知识沉淀如何避免变成垃圾堆

你已经有“事实 / 规则 / 过程 / 经验”分层意识，这比多数系统好很多。但真正的问题不是分类，而是**晋升机制**。如果没有严格的晋升门槛，所有知识库都会从“组织经验”退化为“整理过的聊天记录”。Diátaxis 之所以有价值，不只是因为分成 tutorial、how-to、reference、explanation，而是它要求内容围绕用户实际需求组织，并明确不同内容形态不该混写。对你来说，最大的风险就是把“某次需求里的局部经验”写成“通用规范”，然后在下一次误导自己。citeturn7view0

我建议把你的知识沉淀只允许走三段式晋升：

| 阶段 | 允许内容 | 不允许内容 |
|---|---|---|
| `inbox` | 本次 Case 学到的候选经验 | 任何“正式规范”口吻 |
| `pattern` | 至少在两个 Case 复用过的模板/检查项 | 只适用于单一历史需求的描述 |
| `contract` | 已有稳定输入、输出、限制、证据要求的能力说明 | 没有评估样本、没有失败边界的“理想描述” |

判定规则也要更严：一条知识如果**没有改变下次行为**，就不是知识；如果**下一次没有被命中**，就仍然只是案例；如果**命中了但没减少工作量或误判**，要降级；如果**没有明确适用条件与反例**，禁止晋升。SRE 的 postmortem 文化之所以强调 follow-up actions 和 recurrence prevention，也是同样逻辑：复盘不是写总结，而是降低再次失败的概率。citeturn8view1

你当前最需要的知识沉淀形式，不是长文，而是四类轻对象：

| 形式 | 为什么最有用 |
|---|---|
| card template | 能直接减少拆卡成本 |
| verification checklist | 能减少“done 但不可信” |
| capability note | 能减少工具误用 |
| failure pattern | 能提前暴露常见误判 |

Anthropic 的 Agent Skills 经验也支持这种做法：把程序性知识包装成文件夹、元信息、补充文件和必要脚本，靠渐进式加载按需读取，而不是把所有知识一次性塞进上下文。对你来说，这意味着知识沉淀应当尽量**短、可触发、可组合、可废弃**。一篇“新增推送最佳实践大全”远不如一条“新增推送若目标表为覆盖模式，测试成功仍需生产读回 rowcount 与分区落点”的 checklist 条目有用。citeturn17view0turn17view1turn17view2

还有一个经常被忽视但非常致命的点：**知识必须有过期机制**。数据开发里的“经验”非常容易随平台权限模型、菜单位置、审批链、字段口径和 CLI 输出格式变化而过时。如果你不加 `last_used_at / last_verified_at / superseded_by / stale_after`，半年后知识层只会变成有害缓存，而不是资产。你在本地文档里已经很清楚地提醒过“历史 raw 只作线索，不作当前事实”；这个原则同样应该用于知识层本身。fileciteturn0file1

## 是否应该先用现成工具而不是自研

答案是：**是，而且应当非常偏向“先组装，不先产品化”**。这是我最明确的判断之一。你的“文件优先、Markdown/YAML 记录、后续再生成只读 HTML dashboard”本身，就是一种对现成工具生态极其友好的路线。MkDocs 就是为 Markdown + YAML 配置驱动的静态项目文档而设计；Backstage TechDocs 也是 docs-like-code，把 Markdown 源文件生成可读文档站。你完全没必要在 2 周验证期先做自己的前端。citeturn14view0turn12view5

如果你只需要**多人协作、责任分配、依赖关系、看板视图、自动提醒**，GitHub Projects / GitHub Issues / GitLab issue boards 已经提供了你最需要的能力：自定义字段、子问题、依赖关系、多视图、自动化和可追踪状态。GitHub 还支持内建 workflow，把状态变化自动映射到项目项上；GitLab 则强调 issue board 的视图定制、列表、 assignee、status 等不同组织方式。它们不等于你的 Workbench，但足够承担“工作项容器”的职责。citeturn2view0turn10view0turn11view0turn11view1turn14view1turn9view0

真正值得自研的部分，不是工作项 UI，而是**你这个场景特有的对象语义**。具体说，只有下面三层值得你自己掌控：

| 层 | 建议 |
|---|---|
| Case 语义层 | 自己定义；这是你的核心差异 |
| 证据与验证层 | 自己定义；这是可信交付的关键 |
| 知识晋升规则 | 自己定义；这是长期复用的护城河 |

而下面几层，优先借用现成工具：

| 层 | 建议 |
|---|---|
| 文件存储与版本控制 | Git 仓库即可 |
| 静态站点 | MkDocs 或 TechDocs |
| 看板/表格/UI | GitHub Projects 或 GitLab boards，必要时再接 |
| 任务提醒/自动化 | 先用现成 automation 或简单脚本 |
| 图谱/血缘展示 | 先不做，自留映射能力 |

这个边界很重要，因为 Anthropic 也提醒过：太多框架和抽象层会遮蔽真实提示、真实工具返回和真实故障，使系统更难 debug，并诱使团队在还没证明收益前就加复杂度。你现在最需要的不是“Workbench 产品”，而是“**可被真实需求证明有用的 Case 协议**”。citeturn16view5turn16view7

顺着这个边界再往前推一步：你现在不应该自建的还有**复杂血缘图和平台深度双向同步**。OpenLineage 和 Dagster 的价值在于提醒你未来应该把 dataset / job / run / asset / check / schedule 等对象区分开来，但这不等于你现在就要做自己的 lineage plane。先把 ID、引用和验证点定义对，后面若需要映射到这些模型，再做。citeturn12view1turn13view1turn13view3

## 两周最小实验与最严厉的十条批评

如果只给你 **2 周**，我建议实验目标不要写成“验证产品方向”，而要写成更残酷、更可证伪的一句：

**文件优先的 Case Workbench，是否能比你当前做法更早暴露阻塞、更完整留下验证证据、并在第二次相似需求中减少重复分析。**

这个目标必须用真实需求验证，而不是只用历史案例回放。因为历史回放会天然美化系统，真实运行才会暴露“没人想维护”“字段没用”“卡片过多”“等待项沉底”这些致命问题。DORA 一再提醒，不要为指标和精确集成付出过高前期成本；先围绕吞吐与稳定性进行能驱动改进的轻量测量。你的实验也该如此。citeturn8view0

两周实验我建议这样切：

| 项目 | 最小做法 |
|---|---|
| 样本 | 4 个真实 Case：2 个在做、1 个刚进入分析、1 个刚上线需要读回 |
| 结构 | 只用 `case.yaml + notes.md + events.md + cards/ + evidence/ + closeout.md` |
| 参与者 | 你自己 + 至少 1 位能接手看的同事或未来的你自己 |
| 记录方式 | 所有新增信息先记 `events.md`，所有动作都落卡，所有可信证据都入 `evidence/` |
| 结束条件 | 至少 1 个 Case 完整走到 closeout，至少 1 个 Case 出现阻塞并被显式追踪，至少 1 条 pattern 在第二个 Case 被复用 |

实验期间只看六个指标：

| 指标 | 你要看什么 |
|---|---|
| 初次分析成形时间 | 从需求进入到产生第一版可信拆卡要多久 |
| 阻塞提前暴露率 | 阻塞是在执行前暴露，还是执行后踩坑才发现 |
| 死卡率 | 创建后从未被再次触碰或被证明有用的卡占比 |
| 验证完整率 | done 卡中有多少最终拿到了读回证据 |
| 文档维护负担 | 每次更新是否超过你可接受的工作摩擦 |
| 复用命中率 | 第二次相似需求是否真的复用了 checklist/template |

同时必须设立**杀死条件**。如果两周后出现下面任何两条，就应当判定当前方案过重，需要继续砍，而不是继续开发：

| 终止信号 | 含义 |
|---|---|
| 超过 30% 的卡片从未被再次引用 | 卡片粒度设计失败 |
| 大多数 waiting 卡没有下一次触碰日期 | 阻塞模型失败 |
| closeout 需要额外补写大量内容 | 收口模型失败 |
| 没有出现任何可复用 template/checklist | 沉淀模型失败 |
| 维护 Workbench 的时间明显超过节省的分析时间 | 产品价值未成立 |

下面是我对你当前方案最严厉的 **10 条批评**，以及对应改法。它们不是礼貌建议，而是“如果不改，极可能在真实场景里失效”的位置。下面这些批评综合了你上传的设计文本以及外部关于灵活工作项、验证、工具边界、知识渐进加载和简单优先的实践。fileciteturn0file0 fileciteturn0file1 citeturn14view1turn16view5turn17view1turn8view1

| 严厉批评 | 为什么危险 | 改法 |
|---|---|---|
| 你在验证一个方法，却先设计了一套小平台 | 这会把“文档维护能力”误判成“方法有效” | 先把对象砍到 6 个文件级容器，再跑真实 Case |
| 你把收口做得太体面了 | Change/Trust/Learning Pack 很容易变成“事后整理秀” | 先合并成 `closeout.md` 三个章节，只有被频繁使用后才拆包 |
| 你口头上反对固定流程，模型上却在偷偷固定流程 | `permission / dataset / push / ddl ...` 这些主类型会把团队推回菜单式拆卡 | 卡片主类型收缩到 task/question/blocker/evidence/decision/learning，业务差异移到 `domain` |
| 你把执行状态和验证状态混成一条线 | 现实中会出现 done+failed、waiting+n/a、done+pending 等组合，单枚举表达不了 | 拆成 `execution_state` 和 `verification_state` 两个正交字段 |
| 你没有把“当前断言”建成对象 | 结果会是证据、结论、聊天线索混在一起，没人知道当前可信判断是什么 | 新增 Claim 对象，显式维护 candidate/trusted/rejected/stale |
| 你把 blocker 当任务写，但没有建模依赖本身 | waiting 卡会沉底，催办、升级、过期全靠人工记忆 | 增加 dependency/wait 对象，至少记录 `waiting_on / blocked_since / next_touch_at / escalation_at` |
| 你说不建第二知识库，但已经开始建第二知识库的骨架了 | `workbench-knowledge` 很容易快速膨胀成另一个无人治理的仓库 | MVP 只留一个 `promotion-inbox.md`，复用两次以上再拆目录 |
| 你想做 dashboard，但还没有稳定的最小字段 | 先做界面只会把不稳的模型固化成维护负担 | 先用脚本生成最薄的只读列表页；没有 5 个活跃 Case 前，不要做前端工程 |
| 你还没有定义“Case 何时真正关闭” | 没有观察窗和残余风险，很多需求只是“我做完了”，不是“组织可信了” | Case 关闭需满足：执行完成、验证通过、残余风险记录、观察期结束或移交明确 |
| 你的两周实验如果没有杀死条件，就一定会得出“方向可行” | 这是假验证，只会把 sunk cost 合理化 | 预先写清 kill criteria，并承诺满足即继续砍，而不是继续补功能 |

最终我给这个方向的评级是：**值得继续，但必须先收缩，不配扩张。** 你已经找到了正确问题，也抓到了正确原则；现在真正需要的不是“更完整设计”，而是“更少对象、更硬边界、更快证伪”。如果你能在两周内证明三件事——阻塞更早暴露、验证证据更完整、相似需求第二次更少重问——这个方向就成立；反之，即使目录再漂亮、命名再高级，也只是一个会被你自己绕开的文档系统。fileciteturn0file0 fileciteturn0file1 citeturn8view0turn8view1turn16view4turn16view7