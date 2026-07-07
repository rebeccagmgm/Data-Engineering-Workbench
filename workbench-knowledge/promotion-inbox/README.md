# Promotion Inbox

这里放从 Case 收尾提取出来、但还没有晋升为正式知识的候选。

每个候选建议一个 Markdown 文件。文件名建议：

```text
YYYYMMDD-<short-topic>.md
```

## 候选模板

```markdown
# <候选标题>

## 来源 Case

## 触发事件

## 原始问题

## 为什么可能复用

## 抽象后的规则或模式

## 适用边界

## 反例 / 不适用场景

## 建议去向

- [ ] agent-kb
- [ ] workbench docs
- [ ] card template
- [ ] workflow pattern
- [ ] capability contract
- [ ] Skill
- [ ] CLI gap
- [ ] eval case

## 下次验证方式
```

## 处理状态

候选不要求马上晋升。允许状态：

- `candidate`
- `trial`
- `promoted`
- `downgraded`
- `obsolete`

状态变化写入 `../promotion-log.md`。
