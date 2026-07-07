# OpenAI Deep Research 第二轮复审吸收记录

来源：`references/research/deep-research-report-byopenai-v2.md`

目的：把第二轮复审从“设计是否过重”转为“协议是否可执行”的修正项，避免继续发明新对象。

## 总判断

接受第二轮复审的主结论：

> 当前版本已经可以进入真实 Case 试运行，但只能是受限试运行；不能直接进入自然语言自由执行的生产化运行。

本轮不再继续砍对象，也不新增大型模块。需要冻结的是四类协议：

1. `case.yaml / card / evidence` 最小字段。
2. 状态转移规则。
3. 自然语言执行协议。
4. evidence 命名、索引和回链规则。

## 立即吸收

### 1. notes.md 降级为 source_index + scratchpad

`notes.md` 不能成为新的事实主账。它只允许承载：

- 原始材料索引。
- 临时 scratchpad。

任何会影响行动的判断，必须升级到：

- `case.yaml` 的 Claim 或 current conclusion。
- `cards/*.md` 的任务、问题、阻塞或决策。
- `evidence/*.yml` 的证据解释。
- `events.md` 的状态变化记录。

### 2. 自然语言必须先翻译成受限意图

MVP 不开放自由自然语言执行。只支持五类受限意图：

| 用户说法 | 系统意图 | 含义 |
| --- | --- | --- |
| 继续推进这个需求 | `advance_case` | 选择当前最高优先级可执行卡；无可执行卡则报告阻塞/等待 |
| 执行 T-003 | `execute_card` | 只对指定卡执行 |
| 先分析，不要执行 | `analyze_only` | 读 Case、提建议，不开工具、不改状态 |
| 补当前验证证据 | `verify_card` | 只读回证据，不做新变更 |
| 收尾这个 Case | `closeout_case` | 检查完成度并生成 closeout 草稿 |

### 3. Agent 执行卡片固定七步

每次执行必须走：

1. 读取 `case.yaml`。
2. 读取目标卡；若是 `advance_case`，先筛选可执行卡。
3. 执行前校验字段是否足够。
4. 生成执行意图摘要。
5. 执行或放弃执行。
6. 写回 evidence / event。
7. 按规则更新状态；超边界必须请求确认。

### 4. 自动更新与人工确认边界

Agent 可以自动更新：

- `updated_at`
- 新增 `event`
- 新增 evidence metadata
- `execution_state: todo -> doing -> done`
- `verification_state: pending -> passed/failed`
- `last_checked_at`
- 建议 `next_touch_at`

必须人工确认：

- `claim.status: candidate -> trusted`
- 新建或修改 decision
- `execution_state: done -> obsolete/cancelled`
- 生产写入、审批提交、对外沟通发送
- Case phase 进入上线、归档、关闭
- `closeout.md` 定稿
- learning 晋升

### 5. 状态转移增加 guard

不新增状态，只增加转移约束：

- `verification_state=passed` 只能在 `execution_state=done` 后出现。
- `waiting` 必须带 `waiting_on / expected_signal / next_touch_at`。
- `blocked` 必须带 `unblock_hypothesis` 或新的 question/decision。
- `done` 后 24 小时内没有验证计划，要标红或生成 follow-up。

### 6. evidence 使用 artifact + metadata sidecar

`evidence/` 不是日志堆。每条 evidence 至少有：

- artifact 原件。
- metadata sidecar，记录 `evidence_id / kind / observed_at / environment / source / artifact_path / supports / summary / limitations / asset_refs / run_refs / recorded_by`。

Evidence card 如果存在，只做解释层；不复制大段原始输出。

### 7. closeout.md 必须结构化

`closeout.md` 固定三节：

- `Change`：改了哪些资产、配置、任务。
- `Trust`：哪些 Claim 被哪些 Evidence 支撑，剩余风险是什么。
- `Learning`：哪些候选值得进入 promotion-inbox。

每节必须引用 `card_id / evidence_id / claim_id / run_ref / asset_ref`，不接受纯口头总结。

### 8. 新增两周试运行指标

新增 kill criteria：

- 超过 20% 的 trusted claim 没有 evidence_refs。
- 超过 15% 的卡片状态修改事后被回滚。
- 超过 30% 的 evidence artifact 未被任何 claim/card 引用。
- 用户每天打开 Case 后，超过一半时间仍需回到聊天或原始附件才能判断下一步。

## 部分接受

### evidence card 可保留，但不是必需

第二轮建议如果维护痛感高，可以取消运行期 evidence card，只保留 `evidence/metadata + card.evidence_refs`。

当前主设计保留 evidence card 作为可选解释层；两周试运行如果发现重复维护，就降级为 metadata-only。

### learning card 降级为 closeout 产物

运行期不鼓励创建 learning card。运行期只记录 `learning_candidate` event；closeout 时再决定是否生成 learning 候选。

## 不吸收

暂无需要明确拒绝的建议。第二轮报告的方向与当前主线一致：停止扩概念，只补协议，然后真实 Case 试运行。

## 主设计文档需要同步的改动

1. 明确 `notes.md` 的边界。
2. 增加受限自然语言意图。
3. 增加 Agent 七步执行协议。
4. 增加自动更新/人工确认边界。
5. 增加状态转移 guard。
6. 增加 evidence artifact + metadata sidecar 规则。
7. 增加结构化 closeout 规则。
8. 增加新的两周试运行指标和 kill criteria。
