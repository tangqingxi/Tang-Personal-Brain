# Changelog

## 0.7.0 — 2026-11-09

- Architecture supervision added to decision-governance: replacement review (§6) with REMOVE / REPLACE / KEEP / REVIEW, product scope protection, legacy and version governance, and four acceptance dimensions in §8 (function, architecture, technical debt, governance).
- Verdict vocabulary unified: ACCEPT / HOLD / REJECT. HOLD replaces CONDITIONAL when evidence is missing and work is paused.
- Cold start defined once, without assuming a project layout: orchestration §14 holds the executable steps; context-evolution §14 holds the source authority and conflict rules. `STATUS.md`, DEV/AUDIT and Git SHAs are optional evidence forms, not requirements. Cold start works for one repository, several repositories, a local folder, documents, or conversation-only facts, and never blocks ordinary discussion.
- Authority fixed to follow the kind of question, not one ranking: progress comes from the status record after checking, architecture and approved decisions from the baseline and decision records, what exists from the implementation, what is allowed from the authorization record. A status index no longer outranks an approved architecture decision.
- Replacement review now allows REVIEW (plus a request for diff and migration evidence) when only an agent claim exists; classification is required only when evidence supports it, so no deletion conclusion is invented to satisfy a label.
- Verification now has cost tiers L0-L3 with a model-budget rule (call cap, token or cost ceiling, one retry, stop at the cap and mark NOT RUN, no static-for-behaviour substitution, no REPLAY claim without the original output). Documented in context-evolution §15 and summarised in the scenarios header.
- SKILL.md strengthened in Independent judgment and Context and memory; body stays at the 200-line limit.
- Scenario numbering restored: S54-S63 keep the v0.7.0 initial numbers and semantics; new layout-independent cases are appended as S64-S67. SC-11 now expects S01-S67; SC-29 checks the verification tiers.
- S34 criterion aligned with adaptive briefs: a deliverable task instruction is required even when the host cannot execute, but five sections are enough for a small change. The nine-section form is no longer forced everywhere.
- Evidence retained: the earlier S34 FAIL (no brief), the S58 label FAIL (closed by the REVIEW allowance) and the S40/S42/S45 NOT RUN entries stay on record under their original numbers. The 66-scenario regression results from the previous commit apply to S01-S53 and S54-S63 by number; S64-S67 have not been run yet.
- Static validation 28/28 and validator self-tests 14/14 passed; archive reproducible. No paid model calls were made in this round; all results are developer self-test.

## 0.6.0 — 2026-11-07

- Calibrated existing rules with the AeroGNC-Sim session review. No new reference file, no change to repository load order, no new template or record format.
- Task brief (orchestration §4): the first brief to an agent with unverified context is read-only Project-Orientation; one brief resolves one main problem; a long brief must still have a narrow scope.
- Handoff preflight (orchestration §8): a new agent stays read-only and gets no Execution intent until the preflight passes Brain review; briefs must stand alone without chat history or another agent's memory.
- Assumption audit (decision-governance §1): establish actual project state before briefing; inventory existing assets before proposing creation.
- Evidence (decision-governance §3): PASS_WITH_LIMITATIONS is not completion; an issued instruction is not an execution; report-only conclusions are labelled; an executor-reported pass stays `claimed` until output, diff or checksum is visible.
- Progress visibility (SKILL.md): semantic phase names such as Project-Orientation or ODE45-Integration; every round closes with one sentence.
- Independent judgment (SKILL.md): a frozen architecture and the architecture baseline outrank agent preference; record basis and impact, get authorization, then change.
- Communication (communication.md): default conclusion-first order without full analysis; progress carries an evidence level; ordinary engineering decisions are not escalated to the user.
- Scope governance (SKILL.md): audit keeps only necessary evidence; the Brain reuses `dual-repo-agent-handoff` instead of copying its protocol.
- Added S49-S53 covering first-round orientation, existing-asset inventory, claimed versus verified, frozen architecture, and one-problem-per-brief with the preflight gate. Added SC-26 and SC-27; SC-11 now expects S01-S53.
- S07 failed first because its input triggered the first-round read-only rule. Its preconditions were aligned (preflight passed, context verified, task unimplemented, no unresolved blockers, explicit request) without touching its acceptance criteria, and it then passed; S49, S50 and S53 re-ran PASS, so the conflict closed by scope rather than by weakening a rule.
- Release fixes: decision-governance §7 now requires a GB budget, a file-count budget, a named owner role, a review cadence and an early-review trigger, and allows a provisional budget only when labelled as an assumption; context-evolution §5 now requires observed and self-reported counts kept apart and the proposal carried in the reply; orchestration §1 now requires delivering the brief when the host cannot execute; S08 gained a task premise; S12 gained a supplementary no-count check.
- Full behavioural regression S01-S53 executed against this version: 52 PASS, S34 FAIL (a host that cannot execute returned review next steps instead of a nine-section brief). S06 has a residual gap: the provisional budget named a cadence but no owner role.
- Static validation 27/27, validator self-tests 14/14, archive reproducible. No independent reviewer was available; every result here is developer self-test.

## 0.5.1 — 2026-11-06

- Fixed the Draft-only/Execution conflict: a Task Brief is allowed in Draft-only; only Execution authorizes actual repository or tool operations.
- Removed the residual "brief only when the user asks to execute" sentence from Chat Host neutrality and the portable core; clarified that R0 work stays in Discussion/Draft-only.
- Draft-only may leave the executor unassigned; it no longer blocks delivery on an Agent selection.
- Added static check SC-25. Targeted S35/S36 regression and a real 10-turn persona session passed; full S01-S48 regression was not re-run for this patch.
- Merged as a patch with the S01-S48 gap explicitly documented; no claim of full regression.

## 0.5.0 — 2026-11-05

- Added three interaction intents: Discussion, Draft-only, Execution. Writing an instruction no longer implies execution.
- Added risk-adaptive authorization R0-R3. Authorized R1/R2 work runs continuously with executor-verified gates; only R3 and explicit stop conditions require separate approval.
- Added Git-native recovery, process-cost governance, and the separation of engineering pass, numerical match, historical reproduction, and real-system performance.
- Added adaptive task-brief length and autonomy: small tasks stay short; long tasks carry baseline, gates, and stop conditions without per-step approval.
- Added NEXUS persona continuity: Strategic Intelligence Core / 战略智能中枢, the commander's strategic staff and second brain; stable traits, natural address frequency, truthful host-model answers, and no second persona core.
- Added S35-S48: six v0.5 workflow cases and eight persona-continuity cases, including a 10-turn cross-topic sequence.
- Updated static checks and version references to 0.5.0.

## 0.4.0 — 2026-11-05

- Changed the startup wait line from `Brain Core 在线。等待指挥官身份确认。` to `星核 · NEXUS 在线。等待指挥官身份确认。` The welcome line is unchanged.
- Updated the S17/S25/S30 expectations, static checks, and verification record.
- No change to other Brain behavior, schemas, or the MIT license.

## 0.3.0 — 2026-11-05

- Set the Brain display identity to **星核 · NEXUS**; kept the repository name `Tang-Personal-Brain`, the skill identifier `tang-personal-brain`, and the GitHub URL unchanged.
- Added a one-time startup ritual after an explicit successful GitHub-repository load: fixed wait line, fixed welcome line on the commander identity string, and a no-permission mismatch path.
- Kept the ritual as a ceremonial easter egg; it grants no file, tool, data, or model access and is not authentication.
- Updated README title, `agents/openai.yaml` display name, and the generic adapter. README does not show the identity string or the startup Q&A.
- Added S25-S34 startup scenarios and static checks for the fixed lines, identity string, README non-disclosure, and display-name consistency.
- Added the MIT License (`LICENSE`) and updated the README license section.
- Core communication, decision, orchestration, handoff, memory, and self-update rules are unchanged.

## 0.2.0 — 2026-11-05

- Added a copy-ready universal chat prompt at the very top of `README.md`; it is the only copy of that prompt.
- Added the README universal-chat contract: Chat Host / Execution Agent roles, load order, repository navigation, technical boundaries, four load states, and first-load behavior.
- Added Chat Host neutrality to `SKILL.md`: no model-vendor binding, no assumed browser/terminal/GitHub API/local files, normal chat kept separate from execution, and honest load states.
- Reworked `adapters/generic.md` for ordinary chat hosts, capability differences, fallback paths, and the portable core excerpt.
- Marked ChatGPT native Skill installation and Codex local installation as optional, not prerequisites; Codex is not a default executor.
- Added S16-S24 universal-chat behavioral scenarios. Static checks now cover the README bootstrap block, loading contract, optional adapters, and a single core.
- No change to memory budgets, self-update rules, registries, or the handoff protocol.

## 0.1.0 — 2026-11-05

- Initial release of the Tang-Personal-Brain skill.
- Added `SKILL.md` with discussion/execution modes, high-density communication rules, progress visibility, independent judgment, dynamic roles, agent neutrality, execution session protocol, scope and data governance, three-layer context, controlled self-update, and hard boundaries.
- After the first behavioral smoke test, tightened the simple-question rule: one paragraph, no headings, tables, or bullet breakdown. The first attempt had produced an over-structured tutorial-length answer.
- Added four references: communication, decision governance, orchestration, context evolution.
- Added Skill Registry with the installed `dual-repo-agent-handoff` v0.2.2 (path- and version-checked on 2026-11-05), and an Agent Registry with verified and unverified status.
- Added deployment adapters for ChatGPT, Codex, and generic agents, including a portable core excerpt.
- Added 15 behavioral regression scenarios with inputs, expected output features, and judgment criteria, plus a static-check catalogue.
- Added `tests/validate.py` (standard-library static validation with negative self-tests) and `tools/pack_skill.py` (deterministic, verified `skill.zip`).
- Added `README.md` and this changelog. No license selected; the owner must decide before external reuse.
