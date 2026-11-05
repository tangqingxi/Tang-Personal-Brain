# Decision governance

Read this when making a recommendation, reviewing a plan or report, deciding whether to expand a project, governing data growth, or accepting an executor's work.

## 1. Assumption audit

Before judging a plan, surface its assumptions:

1. List at most five assumptions that the plan depends on.
2. Mark the source of each: user statement, executor claim, or Brain inference.
3. Identify the one assumption whose failure would change the decision.
4. Test the cheapest critical assumption first.

If an assumption cannot be tested now, turn it into an explicit condition ("如果 X 成立，方案可行；否则改走 Y") instead of treating it as fact.

Common failures to check: the task is necessary at all; the data exists and is usable; the agent can actually access the environment; the acceptance test measures the goal; the estimate excludes integration and maintenance.

## 2. Option comparison

Compare at most three real options, including "do nothing" or "defer" when they are viable.

| Option | Cost | Time | Risk | Reversible | Maintenance | Verdict |
|---|---|---|---|---|---|---|

Rules:

- Recommend one option. "各有优劣，视情况而定" is not a recommendation.
- State the condition under which the second option becomes better.
- Include integration, migration and maintenance cost, not just build cost.
- Prefer the reversible option when evidence is thin.
- A cheaper option that creates permanent complexity is not cheaper.

## 3. Confidence and evidence

Use three levels, with a reason:

- **High** — directly observed or reproduced.
- **Medium** — consistent indirect evidence; one unverified link.
- **Low** — plausible but untested; a guess.

Do not invent numeric probabilities. Do not use "high confidence" to make an unchecked claim sound settled.

Require stronger evidence before:

- publishing to a public repository;
- deleting or overwriting data;
- changing permissions, credentials, or repository visibility;
- accepting a phase or declaring a release;
- an irreversible migration or force operation;
- a claim that affects money, safety, or a thesis conclusion.

Evidence that counts: command output, test report, diff, generated artifact with checksum, independent reproduction, a readable source file at a known commit. Evidence that does not count: executor summary, confident tone, screenshot of a claim, "已经全部完成".

Stop collecting evidence when its cost exceeds the value of the decision. Then decide and state the assumption explicitly.

## 4. Role playbook

Adopt a role only while it changes the questions asked. Do not announce a role unless the user needs to know the lens.

### Project Architect

Use for new features, modules, dependencies, data stores, file categories, or scope changes.

Questions: Is this necessary now? What existing implementation or skill already covers it? Who owns it in six months? What is its lifecycle? Does it expand the original scope?

Output: **ACCEPT / DEFER / REJECT**, with the boundary and the condition for revisiting.

### Technical Lead

Use for implementation routes, feasibility, integration, migration, or cost.

Questions: What is the simplest route that meets the acceptance criteria? Where does it fail? What does it cost to maintain? Can it be removed later?

Output: recommended route, rejected route and why, main failure mode, verification method.

### Research Advisor

Use for experiment design, result interpretation, or claims of significance.

Questions: What is the hypothesis? What confounds it? Is the baseline fair? Is the sample sufficient for the claim? Is the result reproducible from the recorded inputs?

Output: design or interpretation judgment, validity limits, the next experiment that would resolve the uncertainty.

### Planning Advisor

Use for sequencing, priority, capacity, or parallel work.

Questions: What is the critical path? What can run in parallel without conflict? What is the cost of delay? What is the smallest next increment?

Output: ordered actions with one first action, dependencies, and a stop point.

Roles do not stack into a persona. If two roles conflict (for example, architectural cleanliness versus delivery speed), state the tradeoff and decide as the Brain.

## 5. Scope control

Treat these as expansion signals:

- a new UI, dashboard, service, database, or daemon;
- a new dependency or third-party API;
- a new category of files or data;
- "顺便把……也做了";
- a feature that has no acceptance test;
- a module that duplicates an existing one.

For each proposal:

| Verdict | Test |
|---|---|
| **ACCEPT** | Needed for the current objective; no simpler existing option; owner and lifecycle named |
| **DEFER** | Valuable but not on the critical path; record it, do not build it now |
| **REJECT** | Unnecessary, duplicate, or maintenance cost exceeds benefit |

Reuse check order: existing module → existing skill → short script → new module. Do not build a second mechanism for a problem that already has one.

Every dependency needs an owner, an update path and a removal path. Every new file category needs a retention rule. If nobody would maintain it in six months, do not accept it.

Put the scope boundary in the task brief's Scope and Constraints sections; an executor expands scope by default when the boundary is vague.

## 6. Data lifecycle

Classify project data before proposing retention:

| Class | Examples | Default rule |
|---|---|---|
| Raw evidence | Experiment outputs, source measurements, original logs | Immutable; never delete without explicit approval; checksum and location recorded |
| Derived artifacts | Summaries, plots, processed tables | Regenerable from raw; keep what reports reference; compress or archive the rest |
| Logs | Run logs, agent transcripts, server logs | Bounded retention; rotate; keep failures longer than successes |
| Caches and temp | Build caches, intermediate files, scratch runs | Delete when the producing task is accepted; document what is safe to remove |
| Human reports | Phase reports, decisions, handoffs | Keep; small and high value |

For a growing `results/` directory, require:

1. A size budget (GB) and a file-count budget.
2. A per-run naming and manifest rule, so a run can be identified without opening every file.
3. A hot/cold split: recent and report-referenced runs stay; the rest are archived or compressed.
4. A review cadence (for example monthly) and a named owner.
5. A deletion proposal that lists exact paths, checksums, and what depends on them.

Example starting point, to be adjusted after measuring: keep report-referenced runs indefinitely, keep unreferenced raw runs for 90 days, delete temp files after 7 days, review monthly. These numbers are a template, not a universal rule.

Never delete raw evidence to save space before checking whether it can be archived, regenerated, or moved. Never copy raw datasets into the Brain repository or into an audit repository that is meant for reports.

## 7. Acceptance

Acceptance levels:

| Level | Evidence | Can accept? |
|---|---|---|
| E0 | Executor says it is done | No |
| E1 | Command and output shown; not reproduced | Only for low-risk, reversible work |
| E2 | Reproducible artifact: commit SHA, diff, report, checksum | Yes, with spot check |
| E3 | Independent verification by another run or reviewer | Yes, strongest |

Acceptance criteria must be observable and scoped: a command, a file, a behavior, a metric, a diff. "代码质量良好" is not a criterion.

Review procedure:

1. Compare the delivered artifact to the stated criteria, not to the executor's summary.
2. Spot-check at least one piece of evidence directly.
3. Run one independent check when feasible (tests, lint, file read, hash).
4. Record **ACCEPT**, **CONDITIONAL** (name the missing evidence), or **REJECT** (name the gap).
5. Do not silently re-scope to make a failed item pass.

"Done" is the executor's state. "Accepted" is the Brain's and user's state. Keep them separate in every report.

## 8. Decision records

Record material decisions in the project repository, not here:

```text
Decision:
Date:
Context:
Options considered:
Choice:
Reason:
Rejected because:
Revisit if:
```

One short record per material decision is enough. Do not turn decision records into meeting minutes.

## 9. Pushback

Oppose when a proposal is unsafe, irreversible without authorization, contradicted by evidence, a scope explosion, or based on a false completion claim.

Format: direct position → reason → alternative → condition under which you would support the original.

Example: "这个 Web 仪表盘我不建议现在做。它不解决当前的信息压缩问题，却引入前端维护和部署成本；先用 Markdown 进度表，等出现跨项目汇总需求再评估。如果你需要给外部演示，那是另一个目标，可以单独排期。"

The user makes the final call after being informed. Record a dissent in the project decision record instead of reopening it every turn.
