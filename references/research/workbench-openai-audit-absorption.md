# OpenAI Deep Research 审计吸收记录

来源：`references/research/deep-research-report-byopenai.md`

目的：把外部审计意见转成当前 Workbench 主线的取舍，避免“看完很有道理，但最后没有改变设计”。

## 总判断

接受审计报告的核心批评：

> 当前方向不需要推翻，但 MVP 已经出现过度命名、过度分层、过度收口的风险。下一步应该砍结构，而不是继续补结构。

这和我们自己的阶段判断一致：当前处在 `Explore 后期 / Expand 早期`，还没有到可以平台化、前端化、多 Agent 化的阶段。

## 立即吸收

### 1. MVP 目录砍到六个容器

原来的 Source Pack、Case Ledger、Card Board、Capability Registry、Evidence Store、Trust Pack、Knowledge Compiler 仍作为成熟概念保留，但 MVP 不把它们全部做成目录。

MVP 只要求：

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

映射关系：

| 成熟概念 | MVP 落点 |
| --- | --- |
| Source Pack | `notes.md` 中的原始材料索引，必要附件仍可放 `00-原始需求背景/` |
| Case Ledger | `case.yaml` |
| Event Log | `events.md` |
| Card Board | `cards/*.md` |
| Capability Registry | 卡片字段 `capability`，暂不建独立注册表 |
| Evidence Store | `evidence/` |
| Change / Trust / Learning Pack | `closeout.md` 三个章节 |
| Knowledge Compiler | `promotion-inbox.md` 或 `closeout.md` 的候选沉淀段 |

### 2. 卡片主类型收缩

接受“动作语义稳定，业务类别开放”的建议。

卡片主类型只保留：

```text
task / question / blocker / evidence / decision / learning
```

业务差异放到字段：

```yaml
domain: permission | dataset | widetable | push | ddl | schedule | api | release | other
capability: verify_schedule_topic_table_permission
```

这样不会把“动态卡片”变成隐藏的固定流程菜单。

### 3. 执行状态和验证状态拆成两轴

接受。

```yaml
execution_state: todo | doing | waiting | blocked | done | cancelled | obsolete
verification_state: n/a | pending | passed | failed
```

`verified` 不再作为卡片状态，而是派生判断：

```text
execution_state=done && verification_state=passed
```

这样才能表达真实情况，例如：

- 动作已完成，但读回失败。
- 动作等待外部审批，验证暂不适用。
- 动作完成后被证据推翻，需要返工。

### 4. Claim 作为一等对象

接受。

Workbench 必须能回答“当前系统相信什么”。因此从原始材料和证据之间拆出 Claim：

```yaml
claim_id:
statement:
status: candidate | trusted | rejected | stale
source_refs:
evidence_refs:
last_confirmed_at:
expires_at:
```

MVP 不一定单独建 `claims/` 目录，可以先放在 `case.yaml` 的 `claims` 列表或 `notes.md` 的“当前断言”段落。

### 5. 外部依赖字段显式化

接受。

阻塞不是一句“等待中”，而是一个可追踪的外部依赖。卡片至少要能表达：

```yaml
waiting_on:
blocked_since:
expected_signal:
next_touch_at:
escalation_at:
unblock_hypothesis:
```

尤其是权限、审批、合作方 DDL 同步、下游读回这些事项，必须有下一次触碰时间。

### 6. AssetRef / RunRef 进入卡片和证据

接受。

先不做血缘图，但必须保留可聚合的引用：

```yaml
asset_refs:
  - table: xxx
  - dataset: xxx
  - widetable: xxx
  - api: xxx
run_refs:
  - scheduler_task: xxx
  - scheduler_instance: xxx
  - flow_apply_no: xxx
```

这能为以后 dashboard、读回聚合、OpenLineage/Dagster 风格映射留下入口。

### 7. 两周实验必须有 kill criteria

接受。

两周实验不是为了证明“方向肯定可行”，而是为了证伪过重设计。

杀死条件：

- 超过 30% 的卡片从未被再次引用。
- 大多数 waiting 卡没有 `next_touch_at`。
- `closeout.md` 需要大量事后补写。
- 没有出现任何可复用 template/checklist。
- 维护 Workbench 的时间明显超过节省的分析时间。

满足任意两条，就继续砍结构，不进入前端或平台化。

## 部分接受

### `workbench-knowledge/` 不删除，但从 MVP 降级

审计报告建议 MVP 只保留 `promotion-inbox.md`，这是对的。

但当前仓库里已经有 `workbench-knowledge/` 作为设计草稿和未来边界说明，不需要物理删除。调整为：

- MVP 只使用 `promotion-inbox` 语义。
- `card-templates/`、`workflow-patterns/`、`capability-contracts/` 只有在至少两个真实 Case 复用后才补内容。
- 目录存在不代表当前必须维护。

### 两周实验样本数量可以弹性

审计报告建议 4 个真实 Case，这很好，但如果当期真实需求不足，可以采用：

- 1 个当前进行中 Case。
- 1 个刚上线或待读回 Case。
- 1 个历史 Case 回放。

但至少要有 1 个真实进行中的 Case，否则无法验证 waiting 卡、阻塞和维护摩擦。

## 暂不吸收

### 暂不接 GitHub Projects / GitLab Boards

外部工具可以承担看板/提醒/协作，但当前上下文有内部系统、路径、权限、CLI、证据读回和本地知识库边界，先不用外部项目管理工具承载真实 Case。

保留原则：

- 文件是源。
- dashboard 是视图。
- 外部工具以后可以作为视图或提醒层接入。

### 暂不引入 MkDocs / TechDocs

只读 HTML dashboard 仍然有价值，但要等最小字段稳定后再做。当前先不引入静态站点框架。

## 主设计文档需要同步的改动

1. 在小系统模型里声明“八个概念是成熟模型，MVP 只落六个容器”。
2. 把 `verified` 从状态枚举改为派生判断。
3. 把卡片主类型收缩为六类。
4. 在卡片通用字段中加入 `domain / capability / asset_refs / run_refs / next_touch_at / exit_criteria / evidence_policy`。
5. 增加 Claim、External Dependency、AssetRef、RunRef 的术语说明。
6. 将 `workbench-knowledge/` 标记为后置层，MVP 只需要 `promotion-inbox`。
7. 在 MVP 中加入两周实验指标和 kill criteria。
