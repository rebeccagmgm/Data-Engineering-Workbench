# 只读 Dashboard Generator 吸收记录

日期：2026-07-07

## Decision

现在可以做 `case-dashboard-generator`，但它只能是只读生成器，不是 Workbench 本体。Workbench 的 source of truth 仍是 `cases/` 下的 Markdown / YAML / evidence sidecar 文件。

## Scope

第一版只读取结构化源：

- `case.yaml`
- `cards/*.md` frontmatter
- `evidence/*.yml` sidecar
- `events.md` 中结构化事件块
- `closeout.md` 的固定章节存在性

第一版不从 Markdown 正文推断状态。

## Non-goals

不做可编辑 UI、拖拽看板、React/Vite 应用、Tauri、Electron、数据库、服务端、平台同步、自动执行、全文知识库搜索、固定流程菜单、黑盒评分或 confidence 百分比。

## Data Flow

```text
source files
  -> schema validation
  -> evidence lint
  -> disposable JSON cache / HTML
  -> read-only dashboard
```

生成物必须可删除、可重建、不可人工编辑。所有生成记录都应保留 `source_path`，方便回到源文件修正。

## Guards

- `done` 不等于 `verified`。
- `trusted` 必须引用 evidence。
- `test` evidence 不能支撑 `prod` 或 `downstream_actual` 结论。
- `historical` 不能默认当作 current fact。
- Attention lanes 只能派生，不新增 lanes 文件。
- Top 3 今日行动必须由固定规则解释，不做黑盒评分。
- Lint 分为 Error / Warning / Info，不全部阻断。

## Kill Criteria

试运行两周内满足任意两条，就停止继续投入 Dashboard Generator，回到文件结构、schema 和 lint：

- 打开后仍需花一半以上时间回聊天或原始附件判断下一步。
- Dashboard 状态误导或滞后超过 2 次。
- 为 UI 维护字段的时间明显超过节省的分析时间。
- 大多数 waiting 卡没有 `next_touch_at`。
- 超过 20% trusted claim 没有 `evidence_refs`。
- 超过 30% evidence 没有被 claim/card 引用。
- 没有提前暴露任何阻塞或证据缺口。

## Applied Changes

- 主设计文档新增 `case-dashboard-generator` 章节。
- README 增加本吸收记录入口。
- `待讨论` 中的总 dashboard 问题改为受限决策。
