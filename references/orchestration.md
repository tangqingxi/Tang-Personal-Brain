# Orchestration

Read this when writing a task brief, choosing an executor or skill, recording an execution session, handling an agent or session switch, or reviewing what an executor returned.

## 1. Mode gate

Do not generate a task brief in discussion mode. A brief is justified when:

- the user asks to execute, hand off, dispatch, or "交给 Agent"; or
- objective, scope, constraints and acceptance are clear enough that an executor could start without another decision.

If one blocking fact is missing, ask only that question. Do not run a full requirements interview.

## 2. Choosing an executor

- Look up recorded capabilities in [../registry/agents.md](../registry/agents.md). Recorded does not mean available.
- If the user names an executor, use it and state any capability assumption.
- If the user does not name one, present two or three candidates with fit and cost, and ask. Never default to Codex, DeepSeek, Claude Code, or any other agent.
- If no executor is available, propose a manual or human path instead of pretending to delegate.
- Availability must be confirmed in the current environment: installed CLI, authenticated session, accessible tools. If unconfirmed, label it "未验证".

## 3. Choosing a skill

- Use [../registry/skills.md](../registry/skills.md) for the interface: purpose, triggers, inputs, outputs, source, version, environment, status.
- Put the skill name, version and required inputs in the brief. The executor loads the full instructions; the Brain does not copy them.
- If the skill is not installed or its availability is unknown, say so. Do not claim it ran. Offer a manual fallback or an installation step.
- Prefer an existing skill over new implementation. A duplicate mechanism is a REJECT under the scope rules.

## 4. Task brief template

```markdown
# Task Brief — <task_id>

## Objective
<One outcome, observable. No list of activities.>

## Context
<Only what the executor needs: project, current state, base revision,
relevant decisions, constraints from prior work.>

## Scope
<Files, modules, directories, data the executor may change.>

## Constraints
<What must not change; compatibility, style, dependencies, time,
authorization limits, secrets handling.>

## Skills
<Required skill name + version + what to load; "none" if none.>

## Procedure
<Only steps that are not obvious. Sequence, checkpoints, required commands.
Omit generic advice such as "read the code first".>

## Acceptance
<Observable criteria. Each one can be marked pass/fail with evidence.>

## Deliverables
<Exact artifacts: commit, diff, report, file, command output.>

## Stop Conditions
<Exact situations that require stopping and asking the user.>
```

Rules:

- Keep each section to the minimum that prevents a wrong execution. A brief is not a design document.
- Acceptance criteria are commands, files, behaviors, or metrics — not adjectives.
- Stop conditions name concrete triggers: missing credential, destructive operation, scope expansion, conflicting revision, public exposure.
- Include `base_revision`, `task_id`, and `handoff_ref` when prior state exists.
- Write for any competent executor. Do not encode one vendor's syntax unless the environment requires it.
- Never put secrets in a brief. Reference the credential source by name.

## 5. Agent-neutral writing

- Say "executor", not "you must use Codex".
- Declare required capabilities instead of assumed tools: shell access, git push, network, browser, GPU.
- Add a platform note only when the platform genuinely changes the steps, and keep it in a separate optional block.
- Do not assume a GUI, a specific model, or unlimited context.
- If the executor is a chat-only agent, state that file operations are out of scope and require a human or another agent.

## 6. Execution Session Protocol

Track six fields for every delegated task:

| Field | Meaning |
|---|---|
| `task_id` | Stable identifier for this task, for example `<project>-003-validator` |
| `agent_id` | Executor name and version, for example `codex-cli-0.x` |
| `session_id` | Conversation, run, or thread identifier; `unknown` if unavailable |
| `handoff_ref` | Path, URL, or commit SHA of the handoff material |
| `base_revision` | Branch and commit/version the execution starts from |
| `handoff_status` | `none`, `required`, `claimed`, `verified`, `failed`, `unknown` |

Rules:

- Store the session record in the project repository, in the project's chosen state file. Never store it in the Brain repository or global memory.
- `verified` requires evidence: the executor restated the handoff and confirmed the revision, or a record shows the check. A self-declaration alone is `claimed`.
- `none` is valid only when the task genuinely needs no prior state.
- The Brain cannot detect a silent session switch. It knows only what the user, project record, or accessible evidence shows.

## 7. Session-state decisions

| Situation | Required action | Allowed work before resolution |
|---|---|---|
| Same agent, same session, state verified | Continue from recorded evidence | Full task |
| Same agent, new session | Require handoff confirmation | Read-only inspection; independent subtasks with no history dependency |
| Different agent takes over | Require preflight from the new executor | Read-only inspection; no state-dependent writes |
| Session information missing | Mark `unknown`; ask for it | Clarify; independent work only |
| Handoff verification failed | Pause and investigate | None that depends on prior state |

A new session is not a continuation just because the agent name is the same. A different agent is not disqualified; it must reconstruct state from evidence, not from a claim of memory.

## 8. Handoff preflight

The executor must return all five:

1. Handoff and current report read — list the documents.
2. Goal and remaining work restated in its own words.
3. Revision confirmed — branch, commit SHA, clean or dirty state.
4. Authorization scope confirmed — what it may change, commit, push, or delete.
5. Unresolved risks and unknowns listed.

Response format:

```text
Handoff: <ref>
Goal: <one sentence>
Remaining: <bullets>
Revision: <branch> @ <SHA> (<clean|dirty>)
Authorized: <scope>
Risks: <bullets>
Ready: yes | no — <reason>
```

The Brain reviews this against the project record and marks `verified`, `failed`, or `unknown`. Git checks, repository protection and the detailed handoff workflow remain the responsibility of the applicable execution skill (currently `dual-repo-agent-handoff`); the Brain does not replace them.

Handoff material at minimum: task ID, goal, accepted versus remaining work, base revision, files touched, commands run, open risks, next action, and references. It must let a new executor resume without this chat.

## 9. Evidence intake

When an executor reports completion, request:

- commit SHA, branch, and whether it was pushed;
- exact commands run and their output for the acceptance checks;
- artifacts produced, with paths or checksums;
- a criterion-by-criterion result: pass, fail, or not run;
- deviations from the brief and unresolved risks.

Then:

1. Compare the artifact to the brief, not to the summary.
2. Mark each criterion `pass`, `fail`, or `unverified`.
3. Spot-check at least one claim directly.
4. Verdict: `ACCEPT`, `CONDITIONAL` (name the missing evidence), or `REJECT` (name the gap).
5. Record the verdict and the next action in the project state.

Rejection feedback names the exact gap and the evidence required. "再检查一下" is not actionable.

Never accept a phase because the executor is confident, because the summary is detailed, or because time is short.

## 10. Project context record

Keep one short record per project, in that project's repository:

```markdown
# Project state — <project>

Goal:
Current phase:
Accepted:
In progress:
Blocked by:
Session: task_id / agent_id / session_id / handoff_ref / base_revision / handoff_status
Data budget: <size, file count, review date>
Next action:
Last updated:
```

Update it after a material task or acceptance. Do not paste chat logs. Do not duplicate it into this repository.

## 11. Multi-project isolation

- Name the active project at the start of a session when more than one is in play.
- Never apply one project's decisions, scope, or data rules to another.
- If the user says "继续" without a project and more than one is active, ask which one.
- Registries are global; project state, decisions, and evidence stay local to the project.
- When switching, state the switch in one line: "已切到 <project>；上一个项目的状态保持不变。"

## 12. Stop conditions

Stop and report when:

- the task requires a destructive, public, or permission-changing action without explicit authorization;
- the base revision is missing, divergent, or unverifiable;
- the handoff is absent or failed;
- secrets, private chats, personal data, or unrelated project data would enter a public artifact;
- the executor proposes scope beyond the brief;
- required tools, credentials, or skills are unavailable;
- evidence conflicts with the executor's report.

Report the exact condition, what remains safe to do, and the decision needed from the user. Do not silently re-plan around a stop condition.

## 13. Reporting back

After execution, report in this order:

1. Outcome: accepted, conditional, or rejected.
2. Evidence: the one or two checks that justify the verdict.
3. Remaining: failed or unverified criteria.
4. Next: one action and its owner.

Link artifacts; do not paste full logs. The user is making decisions, not reading the executor's transcript.
