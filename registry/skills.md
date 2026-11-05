# Skill registry

The Brain only needs each skill's interface. The executor loads the full instructions when the task requires them; this registry never copies another skill's implementation.

## Fields

| Field | Meaning |
|---|---|
| Name | Skill identifier used in task briefs |
| Purpose | One sentence on the capability |
| Triggers | When the Brain should consider it |
| Inputs | Required and optional inputs |
| Outputs | Artifacts or decisions the skill produces |
| Source | Install source or package; public URL when one exists |
| Version | Version string checked from the installed copy |
| Environment | Hosts and runtime requirements |
| Status | `available`, `unverified`, `unavailable`; add the check date |

Status is environment-specific. `available` means it was loaded or run successfully in the current environment, not that every host has it.

## Entries

### dual-repo-agent-handoff

| Field | Value |
|---|---|
| Name | `dual-repo-agent-handoff` |
| Purpose | Recover and continue a software or research project from a development repository and a separate audit repository, with evidence manifests and verifiable handoffs. |
| Triggers | A task supplies two GitHub repository links; an agent takes over or resumes a phase; a phase needs acceptance or an audit report; an agent switch needs a handoff. |
| Inputs | Development repo URL, audit repo URL (or first-time bootstrap), current task, optional phase name. |
| Outputs | Recovery snapshot; bounded task execution in DEV; phase report and evidence manifest in AUDIT; self-contained handoff; verification result. |
| Source | Local skill package; no public upstream URL recorded in the installed metadata. |
| Version | `0.2.2` (from `SKILL.md` metadata, checked 2026-11-05) |
| Environment | Installed in the DSH user skill directory (`~/.dsh/skills/dual-repo-agent-handoff`). Requires `git` 2.x; its Python helpers require Python 3.9+ and use the standard library only. Other hosts need the bundle installed first. |
| Status | `available` in DSH on 2026-11-05: loaded successfully and its `SKILL.md` contract read. Its scripts were not executed in that check. |

Interface details the Brain may rely on:

- Bootstrap: two repository URLs are sufficient; DEV and AUDIT roles are inferred from content.
- Evidence: `scripts/build_manifest.py` generates a manifest with SHA256 hashes; `scripts/verify_evidence.py <audit-root> <manifest>` checks local evidence bytes; `scripts/check_handoff.py <dev> <audit> --phase <phase>` checks handoff consistency.
- Boundary: git inspection, repository protection and the handoff procedure belong to this skill. The Brain only decides when a handoff is required and reviews the confirmation.

Do not claim this skill ran unless it was actually invoked. Do not reproduce its protocol in a task brief; name the skill and version and let the executor load it.

## Adding an entry

1. Verify the installed copy and read its `SKILL.md` metadata.
2. Record the interface, not the full instructions.
3. Mark status with the environment and check date.
4. Use the full execution spec only through the executor.

Template:

```markdown
### <name>

| Field | Value |
|---|---|
| Name | `<name>` |
| Purpose | |
| Triggers | |
| Inputs | |
| Outputs | |
| Source | |
| Version | |
| Environment | |
| Status | |
```
