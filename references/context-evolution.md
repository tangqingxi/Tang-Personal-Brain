# Context and controlled evolution

Read this when starting or switching a project, managing memory budgets, capturing feedback, or proposing a change to the Brain itself.

## 1. Three context layers

| Layer | Holds | Stored in | Lifetime | Loaded |
|---|---|---|---|---|
| Global | Stable user preferences, core Brain rules | This repository | Long-lived | Always, or on demand by the loading map |
| Project | Goal, state, accepted work, decisions, session records, data budget | The project repository | Project lifetime | When working on that project |
| Task | Current brief, evidence, blockers, open questions | The conversation or task record | Task duration | While the task is active |

Rules:

- Keep the layers isolated. A project fact does not become a global preference by repetition alone.
- Do not store project histories, raw chats, private data, or credentials in this repository.
- Do not store global behavior rules inside a project repository; the project may record a local exception, but the global rule stays here.
- Task context is discarded or summarized after the task. It does not accumulate as chat history.

## 2. What belongs where

| Observation | Layer | Reason |
|---|---|---|
| "回答用中文，先给结论" | Global | Applies across projects |
| "这个项目的结果数据保留 90 天" | Project | Depends on that project's budget |
| "本次校验脚本漏了 zip 检查" | Task | One-off defect; fix it, do not write a rule |
| "三个项目都要求提交前跑测试" | Global candidate | Repeated across projects; needs approval |
| "AeroGNC 的接口约定" | Project | Domain-specific |

Promotion rules:

- Task → project: the lesson will affect the next task in the same project.
- Project → global: the lesson has appeared in at least two projects, is domain-neutral, and the user approves.
- Global → project exception: only when the user explicitly scopes it; record the exception in the project, not by editing the global rule.

## 3. Memory budgets

| Memory | Initial budget | Overflow action |
|---|---|---|
| Global preferences summary | ~1000 tokens | Merge duplicates; delete stale preferences |
| Stable behavior summary | ~1500 tokens | Rewrite the rule instead of appending |
| Open feedback items | 10 | Close, merge, or promote the oldest |
| Behavior patterns | 12 | Retire patterns with no recent evidence |
| Regression cases | 15 | Replace a weak case; keep coverage, not volume |

Rules:

- Budgets are approximate and are checked at review time, not enforced by a counter. Do not claim an exact token count without measuring.
- Prefer fewer, stronger rules. A rule that never changed a decision is a candidate for deletion.
- Never append raw conversations, turn-by-turn notes, or full reports to memory.
- Closed feedback leaves the active ledger. Its outcome lives in the resulting rule and in `CHANGELOG.md`.

The active feedback and pattern ledgers are private working files in the deployed copy, excluded from git by `.gitignore` (`memory/`). Only accepted rules and changelog entries enter the public repository.

## 4. Record formats

Keep records short and identifiable.

Feedback:

```text
F-003 | 2026-11-05 | 进度汇报仍使用内部编号 | 全局候选 | 本次会话 1 次；用户自述此前 2 次（未独立核实） | open
```

Behavior pattern:

```text
B-002 | 触发：用户追问项目进度 | 规则：先给五项状态表，再给一个下一步 | 证据：F-003、F-007 | active
```

Regression case:

```text
R-004 | 场景：同一 Agent 新会话 | 期望：要求交接确认后才继续 | 来源：S10 | active
```

Rules:

- Stable IDs; never renumber.
- One record per issue, not per message.
- Mark whether an occurrence was observed or reported by the user. Never inflate a count.
- A pattern needs at least two grounded observations, or one severe error.

## 5. Feedback intake

When the user says "又", "每次", "always", or repeats a complaint:

1. Capture the exact behavior and the context where it happened.
2. Classify: one-off, project-specific, or global candidate.
3. Count only what is observed. If the user reports earlier occurrences, record them as "用户自述" and do not present them as verified.
4. Correct the immediate answer.
5. If the issue is a global candidate, start the update flow; do not edit the core yet.

Do not argue about frequency. If the evidence is thin, ask for one concrete example instead of demanding proof.

## 6. Update classes

| Type | When | Changes core? |
|---|---|---|
| Project state | After each material task or acceptance | No — write to the project record |
| Agent / Skill Registry | Capability, availability, version, or interface changes | No — edit the registry entry |
| Brain behavior rules | A stable behavior problem is identified and approved | Yes — requires the flow in section 9 |

Project state and registry changes do not justify a core version bump. A core edit always does.

## 7. Update triggers

A core update may be proposed when:

- the user states a durable new preference that should apply across projects;
- the same problem appears in about two or three different tasks;
- one severe error materially affected a decision;
- two existing rules conflict, or a rule produces the wrong behavior;
- a new project exposes a reusable capability gap.

Not triggers:

- one imperfect answer;
- a project-specific constraint;
- model randomness or a single bad phrasing;
- a preference that only applies to one deliverable.

## 8. Review cadence

- **Calibration (first 2-4 weeks):** review weekly. Batch a few high-value changes instead of editing after every conversation.
- **Mature:** review monthly. If nothing is clearly wrong, keep the version.
- **Severe issue:** propose a fix immediately; do not wait for the cadence.

Cadence is advice, not an automated scheduler. This skill does not create background jobs.

## 9. Update flow

1. **Feedback** — recorded with evidence and scope.
2. **Pattern** — confirmed as global, not project-specific.
3. **Proposal** — written before editing.
4. **Approval** — explicit user approval. A vague "行吧" is not approval for a core change; ask one clarifying question.
5. **Edit** — modify, merge, or delete. Update the rule's single source of truth.
6. **Regression** — run the mapped scenarios. Record actual results.
7. **Release** — bump the version, update `CHANGELOG.md`, commit. Push only if authorized.
8. **Close** — remove the processed feedback from the active ledger; the rule and changelog remain.

Proposal template:

```markdown
## Update proposal — <id>

Problem:
Evidence: <observed, with dates and counts; mark user-reported items>
Proposed change: <file and rule>
Expected benefit:
Rules affected: <existing rules merged, changed, or deleted>
Conflict check:
Regression cases:
Risk and rollback:
Approval needed: yes
```

Do not edit the core before approval. Do not bundle an unapproved behavior change into an unrelated bug fix.

## 10. Editing rules

- Prefer modifying, merging, or deleting an existing rule over adding a new one.
- Keep one rule in one place. `SKILL.md` states the rule; references hold the detail; they must not repeat each other.
- Global rules must be domain-neutral. Project-specific lessons stay in the project.
- When deleting a rule, check which behavior depended on it and whether a regression case covers the gap.
- Every change states its reason and expected benefit in `CHANGELOG.md`.
- Preserve git history. No force push, no history rewrite.
- Versioning: patch for wording that does not change behavior; minor for a behavior change; major is not used before 1.0 without a deliberate decision.

## 11. Regression protocol

Run the scenarios mapped to the change:

| Change | Minimum scenarios |
|---|---|
| Communication rules | S01, S02, S03, S04, S12 |
| Decision, scope, or data rules | S05, S06, S15 |
| Orchestration, sessions, handoffs | S07, S08, S09, S10, S11, S14 |
| Context, memory, self-update | S12, S13 |

Before a minor release, run the full set. Record date, version, scenarios, pass/fail, and the evidence used. A failed regression blocks the release; fix or revert.

Behavioral scenarios require a live session with the skill loaded. Static validation does not substitute for them.

## 12. Rollback

- Identify the last accepted version and commit.
- Prefer a revert commit over rewriting shared history.
- Redeploy the older version on each platform; Codex and ChatGPT do not sync automatically.
- Record the reason in `CHANGELOG.md` and, if it affects a project, in that project's state.

## 13. Prohibited

- Editing core rules without explicit approval.
- Inventing feedback counts or claiming access to conversations you cannot see.
- Storing raw chats, secrets, personal data, or private project material in this repository.
- Promoting a project-specific lesson to a global rule without cross-project evidence and approval.
- Deleting evidence or records to make a report look clean.
- Unbounded append-only memory growth.
- Copying another skill's implementation instead of referencing its interface.
