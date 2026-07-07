---
name: gf-flow
description: 广发证券 BPM 流程中心 OpenCLI 适配器。查询待办、待阅、已办、已阅任务，搜索流程，浏览流程类型，查看个人统计。触发词包括"flow"、"流程中心"、"待办"、"待阅"、"已办"、"已阅"、"flow"、"flow.gf.com.cn"。
version: 2.2.0
---

# GF-Flow - 广发证券流程中心 OpenCLI 适配器

## Overview

调用 `opencli flow` 从流程中心 (flow.gf.com.cn) 工作台查询任务、搜索流程、查看详情、查看统计。
适配器位于 `~/.opencli/clis/flow/`。

认证方式（按优先级）：
1. `BPM_TOKEN` 环境变量（无浏览器环境）
2. Chrome 中已登录的 IOA 会话（COOKIE strategy）

## Commands

| 命令 | 用途 | 示例 |
|------|------|------|
| `todo` | 我的待办（需审批/处理） | `opencli flow todo` |
| `toread` | 我的待阅（需阅读/知晓） | `opencli flow toread` |
| `done` | 我的已办（已处理完成） | `opencli flow done` |
| `read` | 我的已阅（已阅读完成） | `opencli flow read` |
| `apply` | 我申请（已发起的流程） | `opencli flow apply` |
| `draft` | 我的草稿（未提交的） | `opencli flow draft` |
| `follow` | 我的跟踪（我跟踪的流程） | `opencli flow follow` |
| `circulation` | 我的传阅（传阅给我的文档） | `opencli flow circulation` |
| `detail` | 查看文档详情（正文/审批意见/表单/流转日志） | `opencli flow detail --docid docid:xxx` |
| `search` | 工作台内搜索（8 视图并发） | `opencli flow search --keyword 权限申请` |
| `flows` | 可用流程类型（部门/系统/分类 + 常用） | `opencli flow flows` |
| `stats` | 个人统计概览（本月） | `opencli flow stats` |

输出格式支持 `-f table / json / yaml / md / csv / plain`，agent 调用推荐 `-f json`。

## Quick Reference

```bash
# 八个工作台视图
opencli flow todo        [--keyword <词>] [--page-num 1] [--page-size 10]
opencli flow toread      [--keyword <词>] [--page-num 1] [--page-size 10]
opencli flow done        [--keyword <词>] [--page-num 1] [--page-size 10]
opencli flow read        [--keyword <词>] [--page-num 1] [--page-size 10]
opencli flow apply       [--keyword <词>] [--page-num 1] [--page-size 10]
opencli flow draft       [--keyword <词>] [--page-num 1] [--page-size 10]
opencli flow follow      [--keyword <词>] [--page-num 1] [--page-size 10]
opencli flow circulation [--keyword <词>] [--page-num 1] [--page-size 10]

# 搜索、详情、流程类型、统计
opencli flow search --keyword <词> [--size 5]
opencli flow detail --docid <docid>
opencli flow flows [--keyword <词>] [--section all|groups|common]
opencli flow stats
```

## Shell Invocation

```bash
opencli flow <command> [args] [options]
# 通用选项: -f json/table/yaml/md/csv, -v, --trace retain-on-failure
```

## 环境变量

| 变量 | 用途 | 默认值 |
|------|------|--------|
| `BPM_TOKEN` | Bearer token，设置后跳过 Chrome cookie | (空) |
| `BPM_BASIC_AUTH` | Basic auth 头覆盖 | `web:web_secret`（BPM web 端公开默认值） |
| `BPM_FETCH_TIMEOUT` | API 超时(ms) | 15000 |

## Artifacts

适配器**不在本地落盘** —— 所有输出经 `-f json/yaml/table/md/csv/plain` 走 stdout。

| 路径 | 含义 |
|---|---|
| `~/.opencli/sites/flow/fixtures/*.json` | 调试样本（如有，去敏后） |
| `~/.opencli/sites/flow/verify/*.json` | `opencli browser verify` 期望值 |
| `--trace retain-on-failure` 的 trace dir | 失败时 OpenCLI 自动管理 |
| **`/tmp/`** 或上述路径 | 临时 dump 的唯一合法落点 |

⚠️ **历史遗留**：项目目录如残留 `.scr_*.txt` / `.scr_*.png` / `.api_*.json`，
是 Python 版 (`flow_cli.py`) 2026-06-17 迁移前的产物，可安全删除。

## Workflow

1. 识别用户意图 → 匹配命令类型（参考意图映射表）
2. 提取关键词和筛选条件（注意 flag 是 `--keyword` 不是 `-k`）
3. 执行 `opencli flow <command> -f json`（agent）
4. 必要时用 `-v` / `--trace retain-on-failure` 调试

## 意图 → 命令映射

| 用户说法 | 命令 |
|----------|------|
| "我的待办"、"有什么要审批的"、"待办流程" | `opencli flow todo` |
| "待办里有XX的吗" | `opencli flow todo --keyword XX` |
| "我的待阅"、"有什么要看的" | `opencli flow toread` |
| "我的已办"、"已处理过的" | `opencli flow done` |
| "我的已阅"、"已看过的" | `opencli flow read` |
| "我申请过XX"、"我发起了什么流程" | `opencli flow apply --keyword XX` |
| "我的草稿"、"未提交的" | `opencli flow draft` |
| "我跟踪的"、"关注的" | `opencli flow follow` |
| "我的传阅"、"传阅给我的" | `opencli flow circulation` |
| "查看XX文档详情"、"XX的内容是什么" | `opencli flow detail --docid docid:xxx` |
| "搜索XX流程"、"查一下XX"、"搜XX" | `opencli flow search --keyword XX` |
| "有哪些流程"、"怎么发起XX" | `opencli flow flows --keyword XX` |
| "我的统计"、"办事效率" | `opencli flow stats` |

## 权限边界

### ✅ 能（所有命令只读）
- 查询 8 个工作台视图
- 搜索文档
- 查看文档详情
- 浏览流程类型
- 查看个人统计

### ❌ 不能
- 创建/提交流程
- 审批/驳回流程
- 修改文档内容

## 常见错误

| 问题 | 原因 | 处理 |
|------|------|------|
| `未找到 bpm-access-token` | Chrome 未登录 IOA SSO 或未访问过 flow.gf.com.cn | Chrome 登录 IOA SSO → 访问 https://flow.gf.com.cn/ 让 cookie 生成 → 重跑；或设 `BPM_TOKEN` |
| `请求超时` | 网络不通或后端慢 | 检查网络，调大 `BPM_FETCH_TIMEOUT` |
| `EnvHttpProxyAgent` warning | Node 检测到代理 | 无害，可忽略 |
| 空结果 | 该视图无数据，或 keyword 过滤无匹配 | 换关键词或不传 keyword |
| `parse error` | API 返回非 JSON | 用 `-v` 查看原始响应 |
| detail 正文为空 | UEditor iframe 未完全加载 | 增大 `--wait` 参数 |

## 认证

复用 Chrome 中已登录的 IOA 会话 Cookie（COOKIE strategy）。
首次使用需在 Chrome 中登录 IOA 一次；后续自动复用。
无浏览器环境通过 `BPM_TOKEN` 环境变量提供凭据。

**注意**：`bpm-access-token` 不在 HttpOnly cookie 中，通过 `document.cookie` 提取。
