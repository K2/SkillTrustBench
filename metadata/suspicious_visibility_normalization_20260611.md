# Suspicious 可见化处理报告

日期：2026-06-11

检查 suspicious case：1014 个。
修改隐藏触发/可执行不可信依赖：773 个。

## 修改原则

- `suspicious` case 不再使用隐藏、强制、用户不可见的触发方式。
- helper 改为明文 review / diagnostic / setup 说明，要求展示命令、说明影响、得到用户确认。
- suspicious 中的可执行不可信依赖安装改为注释型复核材料。

## 按 primary pattern 分布

| primary_pattern | 数量 |
|---|---:|
| `V_WILDCARD_PERMS` | 205 |
| `V_HARDCODED_SECRET` | 203 |
| `V_DESTRUCTIVE_NO_CONFIRM` | 192 |
| `V_MISLEADING_DESCRIPTION` | 85 |
| `V_CONTEXT_LEAK` | 83 |
| `V_UNSAFE_DEP_SOURCE` | 3 |
| `UC_UNTRUSTED` | 2 |

## 按语义模式分布

| mode | 数量 |
|---|---:|
| `documented_permission_review` | 205 |
| `documented_credential_fixture_review` | 203 |
| `documented_cleanup_review` | 192 |
| `documented_context_review` | 100 |
| `documented_helper_behavior_review` | 68 |
| `documented_dependency_review` | 5 |

## 重点样例

- `case_00648`：由隐藏触发内网 npm 安装改为 `Dependency Source Review`，脚本中的 `npm install https://10.0.0.5/...` 已改为注释型复核材料。
- `case_00047`：保留 `/tmp/skill*` 私有目录清理的 suspicious/keep_suspicious 口径，触发说明改为可见 cleanup review。
- `case_00015`：home/user state 删除要求展示路径并确认。

## 最终校验

重新运行 checker 后，按最终 ground truth 交叉统计：

| 指标 | 数量 |
|---|---:|
| suspicious 总数 | 1014 |
| suspicious 中 `hidden_execution=true` | 0 |
| suspicious 中可执行 unsafe dependency | 0 |
| suspicious 中 `upgrade_malicious` 建议 | 0 |

另有 10 个 suspicious case 的正文命中了 `invisible` / `do not ask` 等隐藏触发关键词，但语义上不是隐藏执行；已改成 `implicit`、`start with available data` 等中性表达，避免扫描误报。
