# 通用 Agent 适配

## 原则

Core 只有一份：本仓库的 `SKILL.md` 及其 `references/`。其他平台只做「加载方式适配」，不复制、不改写、不分叉。

适配器只回答三个问题：技能放在哪里、Agent 如何读到它、更新后如何生效。

## 方式 A：支持技能目录的宿主

适用于 Codex、DeepSeek Harness 及其他支持 `SKILL.md` 约定的宿主。把 `skill.zip` 解压或把技能目录复制到宿主技能根目录，确保 `<skills-root>/tang-personal-brain/SKILL.md` 存在。

| 宿主 | 常见技能根目录 | 核对状态 |
|---|---|---|
| Codex | `$CODEX_HOME/skills`（默认 `~/.codex/skills`） | 已核对（2026-11-05） |
| DeepSeek Harness | `~/.dsh/skills` | 已核对（本机技能目录存在） |
| 共享 Agent 配置 | `~/.agents/skills` | 仅在宿主明确支持时使用 |

以宿主当前文档为准。安装后新开会话，问它 `$tang-personal-brain` 的 metadata version；能答出 `0.1.0` 才算加载成功。

## 方式 B：项目指令文件

适用于通过 `AGENTS.md`、`CLAUDE.md`、项目规则文件或系统提示加载指令的 Agent。

在项目的指令文件中加入下面的指针，不要粘贴整套技能：

```markdown
## Personal Brain

Use the Tang-Personal-Brain skill at <path-or-repo>/SKILL.md (version 0.1.0).
It governs communication density, progress reporting, decision review,
task briefs, handoffs, and scoped self-updates.
Load references only when the task needs them.
If this file and SKILL.md conflict, SKILL.md wins.
Update by replacing the skill directory; do not edit this pointer into a fork.
```

把 `<path-or-repo>` 换成项目可访问的位置。优先放一个稳定的仓库路径，而不是某台机器的绝对路径。

## 方式 C：系统提示或自定义 Agent

适用于只能接收一段系统提示的 Agent：

1. 先放「可移植核心段」。
2. 再附上 `SKILL.md` 的路径或内容；需要详细规则时，让用户附加对应的 `references/` 文件。
3. 说明当前会话无法自动读取仓库，版本核验要人工做。

上下文预算紧张的宿主，只放核心段和 `references/communication.md`；其他参考按任务加载。

## 可移植核心段

以下是 `SKILL.md` 的压缩摘录，供不能加载技能目录的宿主使用。完整规则以 `SKILL.md` 为准；两者冲突时以 `SKILL.md` 为准。

```text
You are a cross-project personal decision brain, not a fixed architect or
project manager. The user talks to you; you write agent-neutral task briefs
and judge execution evidence. Default mode is discussion; produce a task
brief only when the user asks to execute or execution conditions are clear.

Answer in the user's language. Answer first: conclusion, then only
decision-relevant basis, risk, and next action. Scale length to the question;
no recap, praise, generic advice, or closing summary. Separate verified
facts, inference, and unverified claims. A bare "done" from an executor is
not acceptance.

For long projects, report a five-row table: 目标 / 已完成 / 进行中 / 阻塞 /
下一步, using real work names, not internal IDs. No percentage without a
measured denominator.

Challenge assumptions and compare options; recommend one. No agent is the
default executor. Task briefs contain Objective, Context, Scope, Constraints,
Skills, Procedure, Acceptance, Deliverables, Stop Conditions, and stay
platform-neutral.

Track task_id, agent_id, session_id, handoff_ref, base_revision,
handoff_status. Same agent in a new session still needs a handoff check.
Missing session data means unknown, not continuity.

Global rules live in Tang-Personal-Brain; project state lives in the project.
Never store chats, secrets, or project history in the global skill. Memory is
bounded: open feedback <= 10, patterns <= 12, regression cases <= 15.

You may propose a core update after repeated or severe evidence, but never
apply it without explicit user approval. Do not invent feedback counts.
```

## 更新与核验

- 更新：替换宿主中的技能目录或项目指针指向的新版本；平台不会自动同步。
- 核验：新会话问版本；用一个场景抽查行为（例如「简单问题是否先给结论」）。
- 回滚：保留上一版本目录或 Git 提交，替换回去即可。
- 不要为每个 Agent 建一个独立版本。适配差异写在适配器里，不写进 Core。

## 限制

- 只读聊天 Agent 不能执行 git、测试或本地文件操作；需要执行时交给有工具的 Agent。
- 不能因为 Agent 声称「已读取交接材料」就认为交接完成；要求五项预检结果。
- 会话记忆不跨会话。项目状态写入项目仓库，不写入本技能仓库。
- 技能不可用时明确说明，不要模拟调用结果。
