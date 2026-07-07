# Capability Contracts

这里保存 Case 需要的业务能力，以及当前可用工具、fallback 和读回边界。

能力契约不是命令说明。它回答的是：

```text
为了推进 Case，我需要证明什么？
首选工具是什么？
工具不可用时怎么兜底？
这个能力能证明什么，不能证明什么？
```

## 契约模板

```yaml
capability:
purpose:
preferred_tool:
  site:
  command:
fallbacks:
  -
tool_status: available | changing | broken | unknown
business_status: todo | waiting | verified | blocked
proves:
does_not_prove:
evidence_shape:
last_verified:
notes:
```

## 候选能力

- 查 Flow 审批状态。
- 查 Horae 调度任务详情。
- 查 Horae 实例运行结果。
- 查调度主题源表权限。
- 查当前用户表权限。
- 查 szdata 需求和子任务详情。
- 新建测试数据集并预览。
- 宽表测试预览、生成和调度。
- 查 DSP 接口定义和调用日志。
- 核验目标表 DDL 和样例数据。

## 使用规则

- Case 卡片绑定 capability，不直接绑定具体命令。
- CLI 正在修改时，只改变工具状态，不改变业务卡片语义。
- 命令返回 200 不是完成标准；读回证据能支撑业务判断才算完成。
