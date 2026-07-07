# agent-env 知识吸收记录

日期：2026-07-07

范围：本次只评估 `E:\02_area\agent-env` 中对 Case Workbench 构建有直接价值的材料。结论是：最值得吸收的是 `data-push-analysis` 的路径路由、真相环境、时间语义和核验顺序；`memory/` 里的 OpenCLI/API 经验先作为能力实现参考，不直接进入 Workbench 顶层模型。

## 总判断

Workbench 不应该把已有知识库复制一份，也不应该把数据开发流程固定成几张模板卡。更合适的方式是：

- Case 仍然保持动态卡片。
- 当 Case 属于数据推送域时，先判定工作路径：探查、分析、核验、排查。
- 每条路径只提供执行顺序和证据门槛，不预设具体会长出哪些卡。
- 高频成功经验先进入 `promotion-inbox`，复用后再晋升为卡片模板、工作流模式、能力契约或 Skill。

## 立即吸收

### 1. 数据推送域路径路由

`data-push-analysis` 把推送相关工作拆成四条路径：

| 路径 | 触发场景 | Workbench 用法 |
| --- | --- | --- |
| D 探查 | 想知道表从哪来、链路怎么走、影响哪些下游 | 生成轻量探查卡，不做核验结论 |
| A 分析 | 新需求分析、判断要建哪些任务/表/数据集 | 驱动动态拆卡和待确认问题 |
| B 核验 | 上线前后检查配置、日志、数据是否符合预期 | 生成核验卡和证据读回门槛 |
| C 排查 | 下游没数据、数据不对、任务失败 | 严格按链路、逻辑、时间、实际数据顺序推进 |

这不是固定流程图，而是 `advance_case` 的路由层。卡片仍然由当前需求、材料和证据动态生成。

### 2. 实际数据优先于“能查到的数据”

数据推送域最关键的真相边界是：实际数据等于下游业务实际看的那份，不等于任意一个可查询库中的数据。

因此 Evidence 和核验卡需要显式记录：

- `truth_environment`：test / prod / downstream_actual / historical / unknown
- `consumer_view`：下游业务实际查看的系统、库、接口、页面或人工确认来源
- `evidence_scope`：这份证据能证明什么，不能证明什么

### 3. 时间语义进入核验字段

推送链路里必须区分执行时间、数据时间和业务日期。Horae 的 `data_date` 可能只是调度标签，不能自动等同于表里的业务日期。

数据推送相关卡片建议补充：

```yaml
time_semantics:
  execution_time:
  data_time:
  business_date:
  load_mode:
  sql_date_filter:
  skip_policy:
```

这些字段不是所有卡都必填，但核验、排查和上线收口时必须说明。

### 4. 核验顺序不能被日志替代

Horae 实例 SUCCESS 只能证明某个实例状态，不能证明口径正确、目标表有数、下游已经消费。B 类核验和 C 类排查必须把配置、运行、目标数据、下游视角分开记录。

尤其是 C 类排查，建议固定顺序：

1. 先画链路，只描述上下游，不下结论。
2. 再看 SQL / 配置 / 加载模式 / skip / 调度关系。
3. 再确认执行时间、数据时间、业务日期。
4. 最后查实际写入数据和下游实际可见数据。
5. 再给根因、解释和改进建议。

### 5. 多 Agent 只用于独立卡片集合

`agent-env` 中的 orchestration 经验适合后置吸收：当 A4 当前状态盘点、B2 多任务核验、C4 多层数据查询这类任务可以独立拆开时，才使用 fan-out。主 Case 仍由一个 Agent 聚合结论，并且必须检查子任务证据。

## 暂不吸收

### memory/ 的大量 API/OpenCLI 细节

`E:\02_area\agent-env\memory` 里有很多内部 API、浏览器、鉴权和 OpenCLI 经验，对实现能力很有价值，但它们不应该进入 Case Workbench 顶层设计。

处理方式：

- 用作 `capability` 实现和调试时的参考。
- 只在某条经验跨 Case 复用后，晋升为能力契约或 Skill。
- 不把单次 API 参数、选择器、cookie 策略直接写进通用卡片模板。

### 完整复制 data-push-analysis Skill

`data-push-analysis` 本身已经是一个路由 Skill。Workbench 只吸收它的路径模型和证据边界，不复制它的工具说明和所有细则。

## 对当前 Workbench 设计的修改建议

主设计文档应补充三处：

1. 在受限自然语言协议后增加“数据推送域路由”。
2. 在任务卡通用字段中增加可选的 `domain_path`、`truth_environment`、`consumer_view`、`time_semantics`。
3. 在 evidence metadata 中增加 `truth_environment`、`consumer_view`、`evidence_scope`。

这些修改不会改变 MVP 六容器结构，也不会要求一开始做前端。

## 对金仕达历史回放 Case 的影响

`CASE-20260611-jinshida-market-push` 可以被标记为 `domain_path: verify` 加 `historical_replay`。它最值得沉淀的不是“总股本字段最终怎么做”，而是：

- 历史材料中的计划和后续实际逻辑可能不一致。
- `SUCCESS`、目标表 DDL、推送任务运行、下游实际可见数据要分别读回。
- 合作方未同步进展时，Case 只能把结论标为 historical 或 candidate，不能当作当前生产事实。
