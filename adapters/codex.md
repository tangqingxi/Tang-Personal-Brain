# Codex 适配

## 适用条件

Codex 通过技能目录发现 `SKILL.md`。用户级技能目录是 `$CODEX_HOME/skills`，未设置 `CODEX_HOME` 时默认 `~/.codex/skills`。安装方式核对时间：2026-11-05，依据本机 Codex 自带的 `skill-installer` 说明。

`$CODEX_HOME` 是环境变量，不要把某台机器的绝对路径写进配置或文档。

## 安装

### 方式一：从 `skill.zip` 解压（推荐）

PowerShell：

```powershell
$skills = if ($env:CODEX_HOME) { Join-Path $env:CODEX_HOME 'skills' } else { Join-Path $HOME '.codex\skills' }
New-Item -ItemType Directory -Force -Path $skills | Out-Null
Expand-Archive -Path .\skill.zip -DestinationPath $skills -Force
```

Bash：

```bash
skills="${CODEX_HOME:-$HOME/.codex}/skills"
mkdir -p "$skills"
unzip -o skill.zip -d "$skills"
```

解压后必须存在：

```text
$CODEX_HOME/skills/tang-personal-brain/SKILL.md
```

多套一层（例如 `tang-personal-brain/tang-personal-brain/SKILL.md`）会导致 Codex 发现不到技能。

### 方式二：从仓库复制

克隆仓库后，把 `SKILL.md`、`agents/`、`references/`、`registry/`、`adapters/` 复制到 `$CODEX_HOME/skills/tang-personal-brain/`。不要复制 `.git/`、`tests/`、`tools/`、`skill.zip`。

## 验证

1. 确认文件存在：

   ```powershell
   $skills = if ($env:CODEX_HOME) { Join-Path $env:CODEX_HOME 'skills' } else { Join-Path $HOME '.codex\skills' }
   Get-Content (Join-Path $skills 'tang-personal-brain\SKILL.md') -TotalCount 12
   ```

2. 在 Codex 新会话中输入：

   ```text
   使用 $tang-personal-brain，报告 metadata version，并给出你的默认回答结构。
   ```

   预期版本 `0.1.0`，回答先给结论、区分已验证与未验证。

3. 如果技能没有被发现，检查目录层级、文件名大小写和 `SKILL.md` 的 frontmatter；然后重启 Codex 或新开会话。

## 更新

```powershell
$skills = if ($env:CODEX_HOME) { Join-Path $env:CODEX_HOME 'skills' } else { Join-Path $HOME '.codex\skills' }
Remove-Item -Recurse -Force (Join-Path $skills 'tang-personal-brain')
Expand-Archive -Path .\skill.zip -DestinationPath $skills -Force
```

更新后重新执行验证步骤。GitHub 推送不会让 Codex 自动同步；技能目录是本机副本，必须手动替换。

## 项目级使用

如果当前 Codex 版本支持项目级技能目录，把同一份技能放到项目配置的技能目录；否则使用用户级安装。

需要把 Brain 的行为固定到某个项目时，不要复制整套技能到项目里。在项目的 `AGENTS.md` 中加入 [generic.md](generic.md) 的「可移植核心段」，并写清技能版本和更新方式。这样只有一份 Core。

## 限制

- Codex 能否访问网络、git 远端或某块 GPU，取决于本机配置和审批策略；任务指令里要声明所需能力，不要假设。
- Codex 的会话上下文不会自动跨会话保留。切换会话按 `SKILL.md` 的 Execution Session Protocol 处理。
- `agents/openai.yaml` 只提供显示元数据；没有它技能仍可运行。
