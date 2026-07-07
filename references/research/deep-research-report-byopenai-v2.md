# 数据开发 Case Workbench 第二轮复审报告

## 复审结论

这次版本**比第一轮明显更接近可用**，因为你已经把 MVP 收缩到六个容器，卡片主类型压到六类，业务差异收敛到 `domain / capability`，并把 `done` 与 `verified` 拆成了两个正交维度，还把 `Claim / External Dependency / AssetRef / RunRef` 提升到一等对象，同时把 `workbench-knowledge` 从主体降级成 `promotion-inbox` 语义。就“结构是否过重”这一点，**第一轮最主要的过度分层问题，基本已经被真正解决了一大半**。fileciteturn0file0 fileciteturn0file1

但这次复审的重点不是“结构看起来是否更克制”，而是“**真实使用时会不会塌**”。我的判断是：

**现在已经可以进入真实 Case 试运行，但只能进入“受限试运行”，不能直接进入“自然语言自由执行的生产化运行”。**
原因不是目录太多，而是还有几处会直接导致没人用、状态失真、证据不可追溯、Agent 误执行、知识沉淀失控的协议缺口，尤其集中在这五个点：

- **`case.yaml`、`card`、`evidence` 的边界还不够硬**，很容易继续把“当前事实、分析过程、执行记录、证据解释”写混。fileciteturn0file0 fileciteturn0file3
- **自然语言驱动执行还缺一个可机读的执行协议**；仅靠“读卡—执行—写证据—改状态”的口头约定，不足以支撑 Agent 稳定工作。OpenAI 和 Anthropic 都把“清晰 instructions、标准化 tools、增量式单 Agent、eval 驱动”作为起点，而不是先放开自由执行。citeturn4view1turn4view2turn4view3turn3view0turn3view3turn3view5
- **证据目录还没有真正防垃圾化**。你有 `evidence/` 和 evidence card，但还没有把“证据 artifact”和“证据解释记录”彻底分层，后续很容易重新退化成日志堆。fileciteturn0file0
- **`execution_state / verification_state` 本身已经够了，但状态转移约束还不够**。现在缺的不是更多状态，而是“哪些组合允许出现、谁能改、何时必须附带证据”的硬规则。fileciteturn0file0
- **知识沉淀已经不再大而全，但仍缺真正的晋升门禁**。如果没有“复用命中后才晋升”的强约束，`promotion-inbox` 依然会慢慢变成“看起来收敛、实际上没人再看”的缓冲垃圾堆。fileciteturn0file0 fileciteturn0file1

所以，结论不是“继续从概念上砍掉一半”，而是：

**停止继续发明新对象；立即冻结最小协议；用一个真实进行中 Case 试运行；把所有问题都暴露在“协议是否支撑日常使用”上。**

## 上一轮问题的解决情况

先说清楚：这次不是“没改到位”，而是**有些问题已经实质解决，有些只是从结构问题转成了运行协议问题**。

### 已经真正解决的问题

你上一轮最危险的过度设计点，主要是这些：

| 第一轮风险 | 当前版本变化 | 我的判断 |
| --- | --- | --- |
| 目录/对象层级过多 | 收到 `case.yaml / notes.md / events.md / cards / evidence / closeout.md` 六容器 | **已实质解决** |
| 卡片类型可能固化流程 | 主类型收缩为 `task / question / blocker / evidence / decision / learning`，业务差异放入 `domain / capability` | **已实质解决** |
| `done` 与 `verified` 混淆 | 拆成 `execution_state / verification_state`，并把 verified 改为派生判断 | **已实质解决** |
| 知识层有“第二知识库”风险 | 降级为 `promotion-inbox` 语义，不再作为 MVP 主体 | **已实质解决** |
| 过早前端/多 Agent/复杂血缘 | 全部暂缓 | **已实质解决** |
| 缺少等待关系表达 | 引入 `External Dependency` 语义 | **方向正确，但还未彻底落地** |
| 缺少“系统当前相信什么” | 引入 Claim | **方向正确，但还缺边界纪律** |
| 未来聚合能力不足 | 引入 `AssetRef / RunRef` | **方向正确，且值得保留** |

这些变化，不是 cosmetic change，而是把系统从“概念很美但会发散”拉回到了“有可能跑真实 Case”。fileciteturn0file0 fileciteturn0file1

### 还没有真正解决的问题

没解决的地方，不再是“结构太复杂”，而是以下四类“**运行时失真**”：

第一，**最小字段虽然变少了，但没有强约束时仍然会回弹**。例如 `notes.md`、`events.md`、card frontmatter、Claim、closeout 之间都能写判断、都能写证据解释，久了以后会重复、冲突、过期不同步。fileciteturn0file0

第二，**自然语言执行缺少严格协议**。OpenAI 明确把 agent 的基础定义成“model + tools + instructions”，并强调高质量 instructions、标准化工具定义、清晰动作与边界；Anthropic 也强调先从最简单的 workflow / single-agent 开始，复杂度是后加的，不是起点。你现在有对象模型，但还没有把这些对象真正变成 agent 可稳定遵守的执行协议。citeturn4view1turn4view2turn4view3turn3view0turn3view3turn3view5

第三，**证据可追溯性还没有完成“最后一公里”**。你已经知道 raw 不能直接当事实、Evidence 需要环境/时间/限制，这一点判断完全正确；但当前文档还没把“artifact 命名”“索引”“claim/card 关联”“证据解释是否单独写”固定成硬规则。缺的不是理念，是规约。fileciteturn0file0 fileciteturn0file3

第四，**两周实验的 kill criteria 还不够贴近日常使用失败模式**。目前已有“卡片未再引用、waiting 无 next_touch_at、closeout 事后补写、无模板命中、维护成本高于收益”等 kill criteria，这已经比第一轮成熟得多；但还缺会直接暴露 Agent 风险和状态失真的指标，比如“claim 无 evidence_refs 的 trusted 比例”“done 后 24 小时仍无验证计划的比例”“Agent 自动改错状态回滚次数”。fileciteturn0file1

## 最高风险的十个问题

下面这十条，是我认为**现在最可能导致系统没人用、状态失真、证据不可追溯、Agent 误执行、知识沉淀失控**的点。我不按“概念优雅度”排序，而按“最容易在真实使用中出事”排序。

### 风险清单与修改建议

1. **`notes.md` 仍然容易成为新的垃圾场**
   你现在把 Source Pack 入口、原始材料索引、分析笔记都放进 `notes.md`，这在初期很方便，但它天然会吞掉本应分别进入 Claim、Event、Card、Evidence 的内容。最终结果是：**系统有对象模型，但大家还是把重要判断写在 notes 里**。fileciteturn0file0
   **改法**：把 `notes.md` 限制成两个固定区块：`source_index` 和 `scratchpad`。任何“当前可信结论”“任务状态”“证据解释”“决策结论”一律不得只存在于 `notes.md`。一旦它影响行动，必须升级到 `case.yaml / card / evidence / decision` 中。

2. **Evidence card 与 `evidence/` artifact 边界没钉死，后期必然重复**
   当前设计里既有 evidence card，又有 `evidence/` 目录，这很合理；但如果不明确“artifact 是原始读回、evidence card 是解释层”，后面就会出现三份信息：artifact 文件、evidence card、events.md 都在重复写同一件事。fileciteturn0file0
   **改法**：强制两层分离。`evidence/` 只放 artifact 或其 sidecar metadata；evidence card 只回答四件事：**读到了什么、支持哪个 claim/card、不能证明什么、因此状态该不该变化**。不要把大段原始输出复制进 card。

3. **Claim 是正确补丁，但现在仍可能变成“另一份笔记索引”**
   你引入 Claim 是对的，因为系统必须回答“当前到底相信什么”；但如果 Claim 没有明确唯一职责，它会退化成“比 notes 更正式一点的陈述列表”。fileciteturn0file0 fileciteturn0file3
   **改法**：限定 Claim 只做“**待证明/已证明/已推翻/已过期**的陈述管理”，不记录执行过程，不记录决策原因长文，不记录行动项。Claim 必须至少带 `status / source_refs / evidence_refs / last_confirmed_at`；没有 `evidence_refs` 的 Claim 不允许升 `trusted`。

4. **`execution_state / verification_state` 已经够少，但缺少状态转移护栏**
   问题不在状态数量，而在**任何人和任何 Agent 是否都能任意改它们**。如果没有转移约束，`done + pending`、`waiting + passed`、`blocked + n/a` 都可能被乱写，最终状态会失真。fileciteturn0file0
   **改法**：不要再增状态；只增加**状态机规则**。例如：
   - `verification_state=passed` 只能在 `execution_state=done` 之后出现。
   - `waiting` 必须带 `waiting_on / expected_signal / next_touch_at`。
   - `blocked` 必须带 `unblock_hypothesis` 或新的 question/decision。
   - `done` 若 24 小时内没有验证计划，要自动标红，不允许长期挂起。
   你缺的是 transition guard，不是更多枚举值。OpenAI 和 Anthropic 的 agent 实践都把清晰 instructions、明确动作与 guardrails 作为基础，正对应这里。citeturn4view2turn4view3turn3view3turn3view5

5. **自然语言驱动“继续推进这个需求”目前仍然过于含糊**
   对人来说，这句话可理解；对 Agent 来说，这几乎没有执行边界。是继续处理 highest priority card，还是优先 unblock，还是先补证据，还是先 touch waiting 卡？如果没有明确执行协议，Agent 就会在“看起来合理”的路径上乱做事。fileciteturn0file0
   **改法**：把自然语言命令收敛成少数几种意图：
   - `推进 case`
   - `执行卡片`
   - `只分析，不执行`
   - `补证据`
   - `收尾`
   然后为每种意图定义明确的读取范围、允许动作、禁止动作、自动更新范围和需要用户确认的决策边界。没有协议，就不要开放自然语言执行。Anthropic 对 workflows 与 agents 的区分，本质上也在提醒：**先把可预测流程钉住，再放灵活代理。** citeturn3view3turn3view5

6. **External Dependency 语义是对的，但还不够“可运营”**
   你已经有 `waiting_on / blocked_since / expected_signal / next_touch_at / escalation_at` 方向，这很好；但真实世界里最容易烂掉的 waiting 卡不是“字段不够”，而是**没人知道最近有没有跟进、跟进结果是什么、是不是该升级了**。fileciteturn0file1
   **改法**：External Dependency 最少再补两个硬字段：`last_checked_at` 和 `dependency_state`。其中 `dependency_state` 只要 `open | acknowledged | satisfied | expired` 四档就够。否则 waiting 卡只会变成“记录我在等别人”，而不是“可追踪的等待关系”。

7. **`closeout.md` 可以替代三包，但前提是它必须结构化，而不是总结文**
   你把 `Change Pack / Trust Pack / Learning Pack` 合并到 `closeout.md`，我认可；这正是收缩而不是继续分包。问题在于，如果 `closeout.md` 写成一篇自由散文，它根本无法替代三包，只会成为另一个事后补写负担。fileciteturn0file0 fileciteturn0file1
   **改法**：`closeout.md` 只能有三个固定章节：
   - **Change**：改了哪些资产/配置/任务
   - **Trust**：哪些 claim 被哪些 evidence 支撑，剩余风险是什么
   - **Learning**：哪些候选值得进 promotion-inbox
   每一节都要求引用 `card_id / evidence_id / claim_id / run_ref / asset_ref`，不接受纯口头总结。

8. **`AssetRef / RunRef` 已经引入，但还没有成为真正的“锚点”**
   这一点非常关键。你现在有 AssetRef / RunRef，这已经是在为未来的 dashboard、证据聚合、 lineage 映射留钩子；OpenLineage 的核心模型也正是 `dataset / job / run` 这种最少但可扩展的锚点。fileciteturn0file1 citeturn3view6turn3view7
   **改法**：从现在开始就要求：**每张执行类卡片至少挂一个 `asset_ref` 或 `run_ref`，二者都没有的任务卡默认视为“不可核验的泛任务”，应拆小或重写。** 否则将来虽然字段存在，但仍无法聚合和回放。

9. **Learning card 仍可能在运行期抢占注意力**
   当前版本把学习沉淀降级了，这是对的；但如果在 Case 进行时频繁创建 learning card，团队会很自然地开始“边做边写知识”，回到第一轮的问题。fileciteturn0file0 fileciteturn0file1
   **改法**：MVP 阶段把 learning card 视为**closeout 产物，不是运行期常驻卡片**。运行期只允许在 `events.md` 中标一条 `learning_candidate` 事件；真正生成 learning card，放到 closeout 时做。这样能最大幅度避免知识沉淀打断执行流。

10. **两周实验仍然缺“会不会真的被用”的硬判据**
   你已经有 kill criteria，这是非常大的进步；但还缺“使用粘性”和“Agent 执行错误率”。如果没有这两类指标，你可能会得到一个“结构正确但没人愿意每天维护”的系统。fileciteturn0file1
   **改法**：两周实验新增四个 kill criteria：
   - 真实 Case 中，**超过 20% 的 trusted claim 没有 evidence_refs**。
   - **超过 15% 的卡片状态修改事后被回滚**。
   - **超过 30% 的 evidence artifact 未被任何 claim/card 引用**。
   - 用户每天打开 Case 后，**超过一半时间仍需回到聊天/原始附件才能判断下一步**。
   这四条比“功能有没有做出来”更能说明产品会不会被长期使用。

## 最小可执行 Case 协议

你现在最需要的，不是新目录，而是一个**最小可执行协议**。协议的目的只有一个：让 Case 在人和 Agent 之间都保持同一种语义。

### 协议不变量

一个真实可运行的 Case，必须始终满足以下不变量：

1. **只有一个当前可信结论入口**：在 `case.yaml.current_conclusion`，并只引用 Claim，不在 `notes.md` 重复维护。fileciteturn0file0
2. **任何会影响行动的判断，都必须对应 Claim**。没有 Claim 的判断，不允许直接驱动执行。fileciteturn0file3
3. **任何状态变化，都必须能追到 Event**。没有 Event 的状态改动，默认视为不可审计。fileciteturn0file0
4. **任何 verified，都必须能追到 Evidence**。`verified` 不是口头判断，而是 `done + passed` 的派生结果。fileciteturn0file0
5. **任何 waiting，都必须有 External Dependency**。否则 waiting 与 blocked 没差别。fileciteturn0file1
6. **任何进入 closeout 的 learnings，都必须能追溯到本 Case 的具体事件、卡片或证据**。fileciteturn0file0

### 协议生命周期

建议把每个 Case 限定为下面这条最小闭环：

```text
intake
  -> claims formed
  -> cards created
  -> execute or wait
  -> evidence readback
  -> claim updated
  -> case conclusion updated
  -> closeout
```

对应到你现有文件，最佳的唯一职责分工应是：

- `notes.md`：原始输入索引和 scratchpad
- `events.md`：发生了什么
- `cards/*.md`：谁要做什么、卡在哪里、完成标准是什么
- `evidence/`：读回原件与简要元数据
- `case.yaml`：Case 当前状态和当前相信什么
- `closeout.md`：结束时的变更、信任、学习收口

### 允许的自动化边界

在受限试运行阶段，只允许 Agent 自动做这些事：

- 新建或更新 event
- 新建 evidence metadata
- 基于明确规则推进 `todo -> doing -> done`
- 基于 evidence 推进 `verification_state`
- 为 waiting/blocker 补齐缺失的依赖字段
- 生成 closeout 草稿

不允许 Agent 自动做这些事：

- 把 claim 从 `candidate` 直接升为 `trusted`，除非 evidence rules 满足
- 自动关闭 Case
- 自动把 learning 晋升到正式知识
- 自动取消/作废卡片，除非新决策已明确替代
- 自动执行任何潜在破坏性或生产写入动作，除非用户显式确认

这和 OpenAI、Anthropic 对 agent 的建议一致：先用明确定义的工具和 instructions 控制行为，再在 eval 驱动下逐步放开复杂度。citeturn4view1turn4view2turn4view3turn3view0turn3view5

## 自然语言驱动卡片执行协议

你问的关键问题是：**用户只说“继续推进这个需求 / 执行某张卡”，系统是否足够支撑 Agent 正确读卡、执行、写证据、更新状态？**

答案是：**还不够，但只差“协议层”，不是差“系统对象”。**

### 推荐的交互协议

自然语言必须被翻译成**受限意图**，而不是直接当自由命令执行。建议只支持下面五种模式：

| 用户说法 | 系统意图 | 允许动作 |
| --- | --- | --- |
| 继续推进这个需求 | `advance_case` | 选当前最高优先级可执行卡；若无可执行卡，则报告阻塞/等待 |
| 执行 T-003 | `execute_card` | 仅对指定卡执行 |
| 先分析，不要执行 | `analyze_only` | 读 Case、提建议、不开工具、不改状态 |
| 补当前验证证据 | `verify_card` | 只读回，不做新变更 |
| 收尾这个 Case | `closeout_case` | 检查完成度并生成 closeout 草稿 |

### Agent 执行必须遵守的步骤

每一次执行，Agent 必须固定走这七步，不能跳：

1. **读取 Case 头部**：`case.yaml`
2. **读取目标卡片**：如果是 `advance_case`，先筛选当前可执行卡
3. **执行前校验**：检查字段是否足够
   至少要有：`kind / title / capability / owner / execution_state / verification_state / exit_criteria`
4. **生成执行意图摘要**
   要明确：
   - 我准备做什么
   - 我不会做什么
   - 要用什么能力/工具
   - 成功信号是什么
5. **执行或放弃执行**
   如果缺输入、缺权限、缺边界，则不执行，改写 blocker/question/event
6. **写回 evidence / event**
7. **按规则更新状态**
   只能改允许自动更新的字段；超边界修改必须请求确认

这是典型的“受控 workflow + 有限 agentic choice”，而不是自由代理。Anthropic 明确建议：对定义清楚的任务，workflow 的可预测性更强；Agent 适合在需要灵活判断时增量加入，而不是一开始就放任其自由决定所有执行路径。citeturn3view3turn3view5

### 卡片必须具备的“可执行性门槛”

不是所有 task card 都应允许 Agent 执行。要进入 Agent 可执行集合，至少满足这些条件：

```yaml
capability: 明确
inputs: 已知或可从 case 中解析
allowed_actions: 已声明
forbidden_actions: 已声明
exit_criteria: 可判定
verification_method: 可读回
```

如果任何一项缺失，这张卡就只能被 Agent 标为：

- `question`
- `blocked`
- 或 `needs_human_clarification`

而不应直接执行。

### 自动更新与必须人工确认的分界

**可以自动更新的内容**

- `updated_at`
- 新增 `event`
- 新增 `evidence` metadata
- `execution_state: todo -> doing -> done`
- `verification_state: pending -> passed/failed`
- `last_checked_at`
- `next_touch_at` 的建议值

**必须人工确认的内容**

- `claim.status: candidate -> trusted`
- `decision` 新建或变更
- `execution_state: done -> obsolete/cancelled`
- 任何涉及生产写入、审批提交、对外沟通发送的动作
- Case `phase` 变更到上线、归档、关闭
- `closeout.md` 定稿
- learning 的晋升

如果你不做这个分界，Agent 误执行不是“有概率会发生”，而是“迟早一定会发生”。

## 最小字段与边界模型

### case.yaml 最小 schema

你现在的 `case.yaml` 不需要再膨胀。它只需要容纳**Case 的当前头部状态**，不要把运行过程全部吸进去。

```yaml
case_id: CASE-20260706-001
title: 某某数据开发需求
status: active            # active | closing | closed
phase: analysis           # analysis | waiting | build | test | release | verify | archived
owner: user               # user | agent | partner | shared
created_at: 2026-07-06T10:00:00+08:00
updated_at: 2026-07-06T18:20:00+08:00

current_conclusion:
  summary: 当前可执行路径已明确，但仍缺测试库目标表DDL读回
  claim_refs: [C-001, C-003]

current_focus:
  card_ref: T-004
  reason: 当前最高优先级阻塞解除点

current_blocker:
  card_ref: B-001
  summary: 等待合作方同步DDL

next_action:
  summary: 读回测试库目标表DDL；若未同步则催办
  card_ref: T-004

claims:
  - claim_id: C-001
    statement: 测试库目标表DDL已同步
    status: candidate      # candidate | trusted | rejected | stale
    source_refs: [SRC-chat-20260706]
    evidence_refs: []
    last_confirmed_at:
    expires_at:
  - claim_id: C-003
    statement: 当前执行路径以测试环境核验为先
    status: trusted
    source_refs: [SRC-demand-brief]
    evidence_refs: [EV-20260706-002]
    last_confirmed_at: 2026-07-06T17:10:00+08:00
    expires_at:

open_card_refs: [T-004, B-001, Q-002]
asset_refs: [table:testdb.xxx, dataset:ds_abc]
run_refs: [flow:FL20260706001]
```

**为什么这个字段集够用**
因为 `case.yaml` 只回答五个问题：这是什么 Case、现在在哪个阶段、当前相信什么、卡在哪里、下一步做什么。其它执行细节不应该挤进这里。这个取舍与当前设计文档“Case Ledger 只管当前状态、结论、边界和下一步”的方向一致。fileciteturn0file0

### card 最小 schema

card 的核心目标不是“描述世界”，而是**让动作可执行、可等待、可验证**。因此不要继续往 card 里加叙事字段。

```yaml
id: T-004
kind: task                 # task | question | blocker | evidence | decision | learning
title: 读回测试库目标表DDL
domain: ddl
capability: read_table_ddl

owner: agent               # user | agent | partner | approver | platform
execution_state: todo      # todo | doing | waiting | blocked | done | cancelled | obsolete
verification_state: pending # n/a | pending | passed | failed

why: 该读回决定DDL是否已同步，影响后续数据集和推送配置
env: test
priority: high

input_refs:
  claim_refs: [C-001]
  asset_refs: [table:testdb.xxx]
  run_refs: []
  source_refs: [SRC-chat-20260706]

external_dependency:
  dependency_state:
  waiting_on:
  expected_signal:
  blocked_since:
  last_checked_at:
  next_touch_at:
  escalation_at:

exit_criteria:
  - 能读取到目标表DDL
  - 可确认关键字段是否存在

verification_method:
  - 数据库或平台DDL读回
  - 读回结果保存到evidence

allowed_actions:
  - read
  - query_platform
forbidden_actions:
  - write_prod
  - submit_external_request

evidence_refs: []
updated_at: 2026-07-06T18:20:00+08:00
```

**为什么这个字段集足够少**
因为它只保留了四个层面：目标、状态、依赖、验证。少掉了任何一个，卡片就会失控；再多加一层叙事，维护成本就会上升。和你现在文档里的方向相比，我建议的差别只有一点：**把可执行边界写死到 `allowed_actions / forbidden_actions`**，否则自然语言执行时风险过高。fileciteturn0file0 citeturn4view2turn3view0turn3view2

### evidence 最小 schema

`evidence/` 最重要的不是“大”，而是“**能索引、能回链、能说明限制**”。

建议将每条 evidence 变成“artifact + metadata sidecar”，至少有如下最小元数据：

```yaml
evidence_id: EV-20260706-004
kind: readback                # readback | confirmation | screenshot | log | export
title: 测试库表DDL读回
observed_at: 2026-07-06T18:10:00+08:00
environment: test
source: szdata table-ddl
artifact_path: evidence/20260706T1810-test-table-ddl-testdb_xxx.json

supports:
  claim_refs: [C-001]
  card_refs: [T-004]

summary: 已读回目标表DDL，关键字段a/b存在
limitations:
  - 只能证明测试环境DDL存在
  - 不证明生产环境已同步

asset_refs: [table:testdb.xxx]
run_refs: []
recorded_by: agent
```

**为什么 evidence 不该更复杂**
因为 Evidence 的职责不是写分析文章，而是做**时间戳读回与边界声明**。这也符合你在术语文档里对 Evidence 的定义：它应该是带来源、环境、时间、限制的 readback/confirmation，而不是 raw 材料或日志 dump。fileciteturn0file3

### Claim / Evidence / Card / Event / Closeout 的边界

这是你现在最需要钉死的一组边界：

| 对象 | 只负责什么 | 绝不负责什么 |
| --- | --- | --- |
| Claim | 当前要证明/推翻/观察的陈述 | 执行过程、工具日志、长篇分析 |
| Evidence | 某时某地读回了什么，支持/限制什么 | 任务规划、决策归因 |
| Card | 谁在做什么、卡在哪里、怎么算完成 | 当前事实总账 |
| Event | 发生了什么变化 | 解释整件事为什么正确 |
| Closeout | Case 结束时的正式收口 | 运行期状态主账 |

如果你不强行划这个边界，所有对象都会慢慢“越界”，最后又回到第一轮：什么都记录了，但没有一个地方可信。

## 试运行判断与更简单替代方案

### 是否现在就能进入真实 Case

我的结论是：

**可以进入真实 Case 试运行，但前提是先冻结下面四条，不要继续扩设计：**

1. 冻结 `case.yaml / card / evidence` 的最小字段
2. 冻结状态转移规则
3. 冻结自然语言执行协议
4. 冻结 evidence 命名与索引规则

如果这四条不先定，试运行不是在验证产品，而是在制造更多语义漂移。

### 推荐的两周试运行方式

不要上来就“让 Agent 自然语言驱动一切”。
应该采用**一真一回放一对照**的方式：

- **一个真实进行中的 Case**：验证 waiting / blocker / evidence / closeout 的日常维护摩擦
- **一个历史已完结 Case 回放**：验证对象模型是否能重建真实过程
- **一个对照组**：同类需求继续用你原来的方式处理，比较维护成本和读回可见性

两周后只看这些指标：

| 指标 | 目标 | Kill 信号 |
| --- | --- | --- |
| 首次形成可执行卡用时 | 明显短于原方式 | 没变或更慢 |
| waiting 卡完整率 | >80% 带 `next_touch_at` | <60% |
| trusted claim 有证据率 | >90% | <80% |
| evidence 被引用率 | >70% | <50% |
| 状态回滚率 | <10% | >15% |
| closeout 事后补写比例 | <30% | >50% |
| 每日打开后能否直接知道下一步 | 大多数能 | 仍需频繁翻聊天/附件 |

这些指标比“有没有 dashboard”“字段够不够全”更说明系统值不值得继续投资。你自己的设计文件已经把两周实验视为证伪而不是庆功，这个方向是对的；现在只是需要把指标再压到“会不会被真实使用”上。fileciteturn0file1

### 是否还有更简单的替代方案

有，而且我建议你把它作为**兜底简化方案**，以防试运行时证据卡和 learning card 成为负担。

如果两周内发现维护痛感仍然偏高，下一刀不要砍 Case Space 模型本身，而是砍这两项：

- **运行期不再显式建 learning card**，仅在 closeout 里写 `learning_candidates`
- **evidence 不再建独立 evidence card**，只保留 `evidence/metadata + card.evidence_refs`

也就是说，把运行期 card 收缩成：

- `task`
- `question`
- `blocker`
- `decision`

然后把 `evidence` 和 `learning` 分别退回“索引对象”和“收尾对象”。
这会进一步降低运行期维护成本，但不会破坏整体模型。

## 最终判断

这次版本**已经不是“还要继续大砍结构”的状态**。从对象层面看，你已经把最危险的过度设计削掉了：六容器、六类卡片、双状态、Claim、External Dependency、AssetRef、RunRef、promotion-inbox 语义，这一组足以支撑 MVP。fileciteturn0file0 fileciteturn0file1

真正剩下的问题，不是“还缺多少对象”，而是“**有没有把对象变成可执行协议**”。
如果你现在继续设计新的包、新的图、新的知识层，会再次偏离目标。
如果你现在**冻结协议并进入受限试运行**，这个方向有很大概率能验证出真正值钱的东西。

我的明确建议是：

**现在进入真实 Case 试运行。不要继续扩概念；只补协议。**
但这个试运行必须满足三个边界：

- **不开放自由自然语言执行**，只开放受限意图执行
- **不开放自动生产写入或自动对外动作**
- **不让 notes、events、closeout 重新越权成为事实主账**

只要你守住这三条，这个版本已经足以进入真实 Case；
如果守不住，就算再砍目录、再砍字段，也还是会重演“没人用、状态失真、证据不可追溯、知识沉淀失控”的老问题。citeturn4view1turn4view2turn4view3turn3view0turn3view3turn3view5turn3view6turn3view7