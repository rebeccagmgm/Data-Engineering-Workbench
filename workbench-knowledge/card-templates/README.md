# Card Templates

这里保存 Case 中高频可复用的卡片模板。模板只描述字段、完成标准和验证方式，不保存某个具体需求的证据。

## 候选模板

- 当前用户表查询权限申请卡。
- 调度主题源表权限申请卡。
- Flow 审批等待卡。
- 目标表 DDL 核验卡。
- 采集子任务新建卡。
- 数据集新建与预览核验卡。
- 宽表预览/生成/调度核验卡。
- 推送任务测试核验卡。
- 生产上线读回卡。
- 合作方确认卡。

## 模板最小字段

```yaml
id:
type:
title:
why:
owner:
env:
status:
completion_standard:
verify_by:
evidence_needed:
blocked_by:
updated_at:
```

## 使用规则

- 模板不能替代分析；每个 Case 仍然要根据当前未知动态生成卡片。
- 模板里的完成标准必须能读回验证。
- 如果某个模板连续 2-3 个 Case 都有用，再考虑升级为自动生成逻辑或 CLI 辅助命令。
