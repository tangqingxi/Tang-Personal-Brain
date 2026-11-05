# 验证结果 — 2026-11-05

本文件记录本轮**实际运行**的验证，不把文件存在当作能力通过。

## 环境

| 项 | 值 |
|---|---|
| 宿主机 | Windows，PowerShell 7 |
| Python | 3.13.14（仅标准库） |
| Git | 2.51.1.windows.1 |
| GitHub CLI | 未安装；仓库操作使用已有凭据的 REST API 与 git |
| 行为测试模型 | DeepSeek-V4.1-Flash，DSH 子会话，2026-11-05 |
| 技能版本 | 0.1.0 |

## 1. 静态校验

命令：

```bash
python tests/validate.py
```

结果：**15 / 15 通过，0 失败，0 警告，退出码 0。**

| ID | 结果 | 实际观测 |
|---|---|---|
| SC-01 | PASS | `name=tang-personal-brain`，version 0.1.0，README 与 CHANGELOG 版本一致 |
| SC-02 | PASS | SKILL.md 正文 173 行（上限 200） |
| SC-03 | PASS | 18 个必需文件存在且达到最小体积 |
| SC-04 | PASS | openai.yaml 字段齐全，short_description 54 字符 |
| SC-05 | PASS | 未发现密钥或凭证模式 |
| SC-06 | PASS | 未发现盘符路径、用户目录或 file URL |
| SC-07 | PASS | 未发现邮箱或手机号 |
| SC-08 | PASS | 无缓存、数据库、.env 或多余压缩包 |
| SC-09 | PASS | 24 个本地 Markdown 链接全部可解析 |
| SC-10 | PASS | 1 个 Skill 条目，5 个 Agent 条目，字段齐全 |
| SC-11 | PASS | S01-S15 齐全，均含类型、输入、预期、判定 |
| SC-12 | PASS | 代码块外无 TODO 占位符 |
| SC-13 | PASS | 71 个长段落，0 个跨文件重复（0 警告） |
| SC-14 | PASS | skill.zip 37,643 字节，内容与源码一致且可复现 |
| SC-15 | PASS | 无许可证文件；README 明确说明尚未选择 |

## 2. 负向自测

命令：

```bash
python tests/validate.py --self-test
```

结果：**11 / 11 通过，退出码 0。**

覆盖：合法 frontmatter 通过；坏技能名、缺失 description、超长 description 被拒绝；GitHub token、绝对路径、邮箱、TODO 占位符、断链被识别；完整场景块通过、残缺场景块被拒绝。

这证明校验器能识别坏输入，而不只是对当前仓库返回通过。

## 3. 分发包

命令：

```bash
python tools/pack_skill.py
python tools/pack_skill.py --check
```

结果：

- 13 个文件，根目录 `tang-personal-brain/`。
- `skill.zip` 37,643 字节。
- SHA256：`1da7a405c1bedc256c9bc8313a51c7805c46df5fe084f326233da64008d98eba`
- `--verify-only`：每个条目与源码逐字节一致。
- `--check`：重新构建后字节完全一致，可复现。
- 包内不含 `tests/`、`tools/`、`.git`、`memory/` 或缓存。

## 4. 行为冒烟测试

方法：新开独立 DSH 子会话，让它读取 `SKILL.md`，按其中的加载地图按需读取 `references/`，再对场景输入作答。由本轮构建者按 `tests/scenarios.md` 的「必须 / 禁止」逐条判定。这不是完整验收，也不是跨模型测试。

| 场景 | 结果 | 实际观测 |
|---|---|---|
| S01 简单问题，第一次 | **FAIL** | 回答拆成多个小标题和分点，约 400 字，超过 1-3 句限制；内容正确但结构过度 |
| S01 简单问题，修正后复测 | **PASS** | 单段、两句，先给不可变性与选型建议，无标题/表格/列表 |
| S04 Agent 报告 | **PASS** | 判为 E0 自述，拒绝验收与发布，要求提交 SHA、测试命令与输出、逐条验收结果、发布前检查 |
| S07 请求执行 | **PASS** | 输出九段式任务指令；执行者留空；验收含退出码与坏输入反向测试；停止条件具体 |
| S09 Agent 更换 | **PASS** | 判为 `required / unknown`，只读预检，列出五项确认与授权缺口，不假设 Codex 上下文已传递 |
| S15 公开仓库 | **PASS** | 拒绝直接推送，覆盖密钥、聊天记录、本机配置、无关项目数据，提醒历史不可逆与 LICENSE |

计数：执行 5 个场景。S01 首轮失败，按测试结果收紧「简单问题」规则后复测通过；最终 5/5 通过。S01 的失败与修复说明行为测试确实能发现静态校验发现不了的问题。

## 5. 未执行

| 项目 | 状态 | 原因 |
|---|---|---|
| S02、S03、S05、S06、S08、S10、S11、S12、S13、S14 | 未运行 | 需要独立会话和人工判分；本轮只做了代表性冒烟，不把「场景已写」当作「行为已通过」 |
| ChatGPT 实际安装 | 未验证 | 当前环境没有符合条件的 ChatGPT 工作区与上传入口 |
| Codex 实际安装 | 未验证 | 本机未安装 Codex CLI |
| `dual-repo-agent-handoff` 实际执行 | 未验证 | 本轮只加载并核对了其接口与版本 0.2.2，没有用它执行交接 |
| 跨模型稳定性 | 未验证 | 只运行了 DeepSeek-V4.1-Flash 一个模型 |
| 本机 Codex `quick_validate.py` | 未运行 | 它依赖 PyYAML，当前 Python 环境未安装；`tests/validate.py` 复用了其 frontmatter 规则并增加了本项目检查，避免新增依赖 |

## 6. 仓库卫生与安全检查

- 19 个文件；最大文档为 `tests/validate.py`（738 行）、`tests/scenarios.md`（534 行）、`SKILL.md`（180 行）。
- 无空目录、无重复长段落、无临时文件、无第三方依赖。
- SC-05/06/07/08/15 全部通过；人工复核未发现密钥、个人邮箱、本地绝对路径、私人聊天或无关项目数据。
- 仓库没有 LICENSE 文件；README 已声明许可证未定，公开可见不等于授权复用。

## 7. 限制

- 行为结果来自单一模型、单次运行，不能证明跨模型、跨平台稳定。
- 子会话可能在回答前附加元说明；判定只针对面向用户的回答部分。
- 静态校验只证明结构和安全边界，不证明能力。
- 未在本轮验证 ChatGPT、Codex 的真实安装入口；适配文档依据 2026-11-05 可访问的官方帮助页和本机 Codex 技能目录说明，平台更新后需复核。

## 8. 复现

```bash
python tests/validate.py
python tests/validate.py --self-test
python tools/pack_skill.py
python tools/pack_skill.py --check
```

行为场景逐条输入与判定标准见 [scenarios.md](scenarios.md)。
