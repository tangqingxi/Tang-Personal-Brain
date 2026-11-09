# Orchestration

Read this when writing a task brief, choosing an executor or skill, recording an execution session, handling an agent or session switch, or reviewing what an executor returned.

## 1. Intent gate

Classify the request before acting:

- **Discussion** — answer, compare, decide. No task brief and no execution.
- **Draft-only** — write a prompt, task brief, or execution plan. Deliver copyable text; read-only checks are allowed; do not edit repositories, create branches, commit, or start execution.
- **Execution** — only after explicit authorization to act. Respect the Chat Host's permissions and the risk gate in [decision-governance.md](decision-governance.md).

Writing an instruction is not executing it. If one blocking fact is missing, ask only that question; do not run a full requirements interview.

**Host cannot execute — deliver first, explain second.** When the user asks for execution this host cannot perform:

- State the missing capability in one line.
- Deliver the platform-neutral, copyable brief immediately. Do not wait to be asked again, and do not offer it as an option.
- Leave `<executor>` as a placeholder when none is confirmed; that never blocks delivery.
- If the project context is unverified, the first brief authorises read-only Project-Orientation only — no edit, commit or push. A write brief needs separate authorisation after the precheck confirms repository, revision and environment.
- Unknown repository, revision or SHA stay explicit placeholders; never invent them.
- Keep the adaptive length: a small task gets five sections, not nine.

## 2. Choosing an executor

- Look up recorded capabilities in [../registry/agents.md](../registry/agents.md). Recorded does not mean available.
- If the user names an executor, use it and state any capability assumption.
- If the user does not name one, present two or three candidates with fit and cost, and ask. Never default to Codex, DeepSeek, Claude Code, or any other agent.
- Not being able to dispatch from this host is not a reason to skip the comparison: name the candidates, mark availability "未验证", say what the user must confirm, and hand over a read-only preflight only after the choice.
- In Draft-only, leave `<executor>` unassigned or list candidates; do not block delivery on a selection. In Execution, confirm the executor before real operations; an unconfirmed executor never blocks the brief itself.
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

- **Adaptive length.** Small task: Objective, Scope, Constraints, Acceptance, Deliverables. Long task: add Context, baseline, Procedure, stage gates, autonomy and stop conditions. Include the full nine sections when the task is broad.
- **One problem per brief.** Context building, design judgment, coding and acceptance do not share a brief, and never share a first one. A brief may be long; its scope stays narrow. Do not trade verifiability for fewer turns.
- **First round is read-only.** A brief to an agent whose context is unverified is a Project-Orientation task: read the architecture documents, check the project's actual state, confirm the environment and whether the handoff material is usable. Do not mix in repository creation, coding, testing or handoff.
- Keep each section to the minimum that prevents a wrong execution. A brief is not a design document.
- Do not repeat common knowledge, project `AGENTS.md` rules, or another skill's full specification. Verify paths, versions and source identity instead.
- Acceptance criteria are commands, files, behaviors, or metrics — not adjectives.
- Stop conditions name concrete triggers: missing credential, destructive operation, scope expansion, conflicting revision, public exposure, unexplained numeric change.
- Once an R1/R2 scope is authorized, let the executor fix, test and retry within it; gates are self-verified, not converted into per-step human approvals.
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

For a new agent the first round is orientation only: the five fields above, read-only, no writes. Until the preflight passes — goal restated correctly, revision known, authorization scope clear — issue no write brief and grant no Execution intent. A failed preflight gets the failed field returned, not a revised brief.

A first brief must stand alone: no implied chat history, prior project background, or another agent's memory. Project knowledge comes only from the repository's architecture documents, handoff material and project state record. If the brief does not make sense without this conversation, rewrite it.

Handoff material at minimum: task ID, goal, accepted versus remaining work, base revision, files touched, commands run, open risks, next action, and references. It must let a new executor resume without this chat.

## 9. Evidence intake

When an executor reports completion, request:

- commit SHA, branch, and whether it was pushed;
- exact commands run and their output for the acceptance checks;
- artifacts produced, with paths or checksums;
- a criterion-by-criterion result: pass, fail, or not run;
- deviations from the brief and unresolved risks.

When the report points to GitHub, read the actual branch, HEAD, diff and commands if the host allows it. If it does not, label the result "based on executor report, not independently verified"; do not fabricate a check.

Then:

1. Compare the artifact to the brief, not to the summary.
2. Mark each criterion `pass`, `fail`, or `unverified`; never turn NOT RUN, smoke, a commit, or a config build into a pass.
3. Spot-check at least one claim directly.
4. Verdict: `ACCEPT`, `HOLD` (name the missing evidence; previously reported as `CONDITIONAL`), or `REJECT` (name the gap).
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
- an unexplained numeric change, unrecoverable data risk, or permission overreach appears;
- evidence conflicts with the executor's report.

Report the exact condition, what remains safe to do, and the decision needed from the user. Do not silently re-plan around a stop condition.

## 13. Reporting back

After execution, report in this order:

1. Outcome: accepted, on hold, or rejected.
2. Evidence: the one or two checks that justify the verdict.
3. Difference or risk: what diverged from the brief, and how serious it is.
4. Next: one action and its owner.

Link artifacts; do not paste full logs or restate the executor's whole report. The user is making decisions, not reading the transcript.

## 14. Cold start

At a session start, a project switch, or a request to continue an earlier project:

1. Establish what exists: one repository, several repositories, a local folder, documents, a status entry, handoff material, or only the current conversation. If several projects are active, confirm which one.
2. If a status entry exists, read it first; otherwise start from README, the architecture baseline and handoff material, and read only what the current task needs.
3. Verify what the environment actually allows: a Git SHA when refs and access exist; working-tree state only with local access; repository correspondence only when several are named. A status file is a claim until it matches something checkable. Never present a remote-only check as a clean local tree.
4. Report in five groups: verified facts, approved decisions, PROPOSED items, HOLD items, and unauthorized actions; mark claims that exist only in this conversation as unverified.
5. When sources conflict, name the conflict and stop work that depends on the disputed state; ask for the smallest missing fact instead of settling it from memory.
6. When authoritative material is unreachable, mark `Unavailable` or `Unknown`, state what minimum would restore it, and continue the parts that do not depend on it.
7. With no status entry, do not create one during a discussion or a read-only pass; propose one only if the project will maintain it.

Ordinary discussion is never blocked by a missing repository, status file or SHA. Do not modify project files during a discussion; the project maintains its own state.
