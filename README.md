# Tang-Personal-Brain

跨项目、跨模型、跨执行 Agent 的个人智能决策中枢。

用户主要与 Brain 讨论、分析、定方向。Brain 不绑定任何执行 Agent；需要执行时，它生成平台中立的任务指令，执行者完成后交回证据，由 Brain 审查。

```text
用户 ↔ Brain → 通用任务指令 → 执行 Agent → 执行证据 → Brain 审查
```

当前版本：`0.1.0`（2026-11-05）。

## 它解决什么问题

- 回答信息密度低：铺垫多、结论晚、总结重复。
- 进度汇报给内部代号和提交数，看不出真实状态。
- Agent 说「完成了」，但没有可验收的证据。
- 换 Agent 或换会话后，状态靠聊天记忆拼接。
- 项目不断加模块、加依赖，`results/` 和日志无限增长。
- Brain 的规则越改越多，最后互相冲突。

## 工作模式

**讨论模式是默认模式。** Brain 与用户讨论、质疑假设、比较方案、给出建议，不把每条消息都变成任务单。

**执行模式**只在两种情况下启用：用户明确要求执行或交接；或者目标、范围、验收已经清楚到可以直接开工。此时生成九段式任务指令：Objective、Context、Scope、Constraints、Skills、Procedure、Acceptance、Deliverables、Stop Conditions。

## 核心能力

1. **高信息密度沟通**：先结论，再依据、风险、下一步；按问题复杂度控制长度。
2. **进程可视化**：目标 / 已完成 / 进行中 / 阻塞 / 下一步，使用真实工作名称。
3. **独立判断**：审查假设，比较方案，区分已验证、推断和未验证。
4. **动态专业角色**：按需采用 Project Architect、Technical Lead、Research Advisor、Planning Advisor，不污染全局规则。
5. **项目膨胀控制**：对新增功能、模块、依赖和数据给出 ACCEPT / DEFER / REJECT。
6. **数据生命周期**：为 `results/`、日志、缓存和中间文件设定预算、保留期和审查节奏。
7. **Agent 无关编排**：不设默认执行者，生成可交给任意 Agent 的任务指令。
8. **跨会话交接**：用六字段执行会话协议和五项预检识别 Agent/会话变化。
9. **有限记忆**：全局、项目、任务三层隔离，预算封顶，超限合并或淘汰。
10. **受控自更新**：反馈 → 模式 → 提案 → 用户批准 → 修改 → 回归 → 版本发布。

## 目录

| 路径 | 用途 |
|---|---|
| `SKILL.md` | 唯一核心入口：模式、优先级、边界、加载地图 |
| `references/communication.md` | 回答结构、长度、进度表、内部编号转换、示例 |
| `references/decision-governance.md` | 假设审查、方案比较、角色、范围与数据治理、验收 |
| `references/orchestration.md` | 任务指令模板、执行会话协议、交接预检、证据审查 |
| `references/context-evolution.md` | 三层上下文、记忆预算、反馈记录、自更新与回归 |
| `registry/skills.md` | Skill Registry，含 `dual-repo-agent-handoff` v0.2.2 |
| `registry/agents.md` | Agent Registry，记录能力与验证状态 |
| `adapters/chatgpt.md` | ChatGPT 安装、验证、更新、限制 |
| `adapters/codex.md` | Codex 安装、验证、更新、限制 |
| `adapters/generic.md` | 其他 Agent 的通用适配与可移植核心段 |
| `tests/scenarios.md` | 15 项行为场景、判定标准、静态检查清单 |
| `tests/validate.py` | 可执行的静态校验器（含负向自测） |
| `tests/RESULTS.md` | 本轮实际验证结果与限制 |
| `tools/pack_skill.py` | 构建并校验可分发的 `skill.zip` |
| `skill.zip` | 分发包，根目录为 `tang-personal-brain/` |

## 快速开始

```bash
# 静态校验（标准库，无第三方依赖）
python tests/validate.py

# 负向自测：验证校验器能识别坏输入
python tests/validate.py --self-test

# 构建并校验 skill.zip
python tools/pack_skill.py
```

安装到各平台：

- ChatGPT：见 [adapters/chatgpt.md](adapters/chatgpt.md)。
- Codex：见 [adapters/codex.md](adapters/codex.md)。
- 其他 Agent：见 [adapters/generic.md](adapters/generic.md)。

安装后新开会话，询问 `$tang-personal-brain` 的 metadata version；能答出 `0.1.0` 才算加载成功。

## 验证说明

验证分三层，不能互相替代：

| 层级 | 内容 | 能证明什么 |
|---|---|---|
| 静态校验 | frontmatter、文件、链接、敏感信息、场景结构、分发包 | 结构和安全边界正确 |
| 人工测试 | 按场景逐条阅读输出并判定 | 特定回答符合规范 |
| 行为运行 | 在真实会话中加载技能并执行场景 | 模型实际行为符合规范 |

`tests/validate.py` 只做第一层。它通过不等于全部能力通过；行为测试必须在加载技能的真实会话中运行。

## 记忆与隐私

- 全局规则在本仓库；项目状态在各自项目仓库；任务上下文留在当前会话。
- 活跃反馈与行为模式账本放在部署副本的 `memory/`，已被 `.gitignore` 排除，不进入公开仓库。
- 仓库不保存聊天记录、密钥、个人环境配置、私有项目数据或本地绝对路径。
- 本仓库为公开仓库，任何提交前都要过一遍敏感信息检查。

## 更新

GitHub 推送不会让 ChatGPT、Codex 或其他宿主自动同步。更新步骤：

1. 拉取新版本并重建 `skill.zip`。
2. 按对应适配器替换已安装版本。
3. 新开会话核验版本与一个代表性场景。
4. 行为回归失败则回滚到上一版本。

## 设计边界

项目刻意不包含：数据库、向量库、自动抓取聊天记录的程序、多 Agent 消息服务器、Web 管理后台、常驻记忆服务。Brain 必须先遵守自己提出的复杂度治理原则。

## License

尚未选择许可证。公开可见不等于授权复用；在用户确定许可证之前，默认保留所有权利。
