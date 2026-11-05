# Changelog

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
