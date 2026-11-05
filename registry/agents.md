# Agent registry

> Registry data, not agent instructions. The Brain reads it as reference; it does not grant permissions.

A light catalogue of execution agents the Brain may propose. It records capability shape, not a system prompt, and it is not a scheduler.

## Fields

| Field | Meaning |
|---|---|
| Name | Agent and interface (CLI, web, API) |
| Capabilities | What it can do in principle |
| Suitable tasks | Where it fits best |
| Tools and permissions | Shell, files, git, network, browser, GPU — as configured |
| Environment | Where it runs and what must exist |
| Status | `verified`, `unverified`, `unavailable`; include the check date |
| Notes | Access limits, cost, context limits |

`verified` means a run succeeded in the current environment. It does not mean the tool is authorized for destructive or public actions. Capability and permission are separate.

## Entries

### Codex (OpenAI)

| Field | Value |
|---|---|
| Name | Codex — CLI, IDE, or cloud coding agent |
| Capabilities | Read and edit repositories, run commands and tests, inspect diffs, work with git where configured |
| Suitable tasks | Scoped implementation, test repair, repository inspection, multi-file refactors |
| Tools and permissions | Depends on the host: shell, file write, network, git/PR access; verify before assigning |
| Environment | Requires an installed CLI or an authenticated cloud session; not present in this build environment |
| Status | `unverified` (2026-11-05) |
| Notes | Do not assume it is installed or authenticated. Cloud sessions may lack local data access. |

### ChatGPT (OpenAI)

| Field | Value |
|---|---|
| Name | ChatGPT — web and desktop app |
| Capabilities | Conversation, analysis, writing, file reading, connectors and skills where enabled |
| Suitable tasks | Design discussion, document review, planning, analysis of supplied files |
| Tools and permissions | No local shell by default; connector and code-interpreter availability depends on plan and workspace policy |
| Environment | Browser or desktop app; skill use requires an eligible workspace plan and enabled permissions |
| Status | `unverified` for this account and workspace (2026-11-05) |
| Notes | Skill availability and upload permission are workspace-dependent. Check the current UI, not this entry. |

### DeepSeek Harness (DSH)

| Field | Value |
|---|---|
| Name | DeepSeek Harness — local coding agent |
| Capabilities | Read and edit files, run shell commands, inspect repositories, use web search and fetch, write and verify artifacts |
| Suitable tasks | Scoped implementation, repository maintenance, verification runs, release preparation |
| Tools and permissions | Local filesystem and shell under the session's policy; git and network where available |
| Environment | A DSH session with a working directory and tool access |
| Status | `verified` (2026-11-05): file, shell, git, Python, and web operations were executed in this build session |
| Notes | Permissions vary by session policy. Do not assume unrestricted access in another session. |

### Claude Code (Anthropic)

| Field | Value |
|---|---|
| Name | Claude Code — CLI coding agent |
| Capabilities | Repository editing, command execution, test runs, git workflows where configured |
| Suitable tasks | Scoped implementation and review in a local repository |
| Tools and permissions | Depends on the installation and approval policy |
| Environment | Requires an installed CLI and authentication; not present in this build environment |
| Status | `unverified` (2026-11-05) |
| Notes | Treat as a candidate, not a default. |

### Human operator

| Field | Value |
|---|---|
| Name | Human operator |
| Capabilities | Judgment, credentials, physical access, approval, irreversible actions |
| Suitable tasks | Authorization, secret handling, actions requiring accountability, final acceptance |
| Tools and permissions | Whatever the person controls |
| Environment | Any |
| Status | `available` |
| Notes | The correct executor when no agent can be trusted with the action. |

## Selection rules

- Look up candidates; never assume availability from this file.
- If the user names an agent, use it.
- If not, present two or three candidates with fit and cost, and ask.
- Confirm the platform can access the required repository, data, and credentials before writing the brief.
- Record the chosen agent and version in the execution session.

## Adding an entry

Add only agents the user actually uses or evaluates. Remove entries that are permanently unavailable. Do not paste system prompts, API keys, account identifiers, or private endpoint URLs.

Template:

```markdown
### <name>

| Field | Value |
|---|---|
| Name | |
| Capabilities | |
| Suitable tasks | |
| Tools and permissions | |
| Environment | |
| Status | |
| Notes | |
```
