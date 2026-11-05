# Changelog

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
