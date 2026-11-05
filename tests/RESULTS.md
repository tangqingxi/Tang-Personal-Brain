# 验证结果 — 2026-11-05

当前版本：**0.2.0**。v0.1.0 的初始记录见 Git 历史；本文件记录通用 Chat 升级后的实际结果。

## 环境

| 项 | 值 |
|---|---|
| 宿主机 | Windows，PowerShell 7 |
| Python | 3.13.14（仅标准库） |
| Git | 2.51.1.windows.1 |
| GitHub CLI | 未安装；仓库操作使用已有凭据的 REST API 与 git |
| 行为测试模型 | DeepSeek-V4.1-Flash，DSH 子会话，2026-11-05 |
| 技能版本 | 0.2.0 |

## 1. 静态校验

命令：

```bash
python tests/validate.py
```

结果：**19 / 19 通过，0 失败，0 警告，退出码 0。**

| ID | 结果 | 实际观测 |
|---|---|---|
| SC-01 | PASS | `name=tang-personal-brain`，version 0.2.0，README 与 CHANGELOG 一致 |
| SC-02 | PASS | SKILL.md 正文 188 行（上限 200） |
| SC-03 | PASS | 18 个必需文件存在且达到最小体积 |
| SC-04 | PASS | openai.yaml 字段齐全，short_description 54 字符 |
| SC-05 | PASS | 未发现密钥或凭证模式 |
| SC-06 | PASS | 未发现盘符路径、用户目录或 file URL |
| SC-07 | PASS | 未发现邮箱或手机号 |
| SC-08 | PASS | 无缓存、数据库、.env 或多余压缩包 |
| SC-09 | PASS | 24 个本地 Markdown 链接全部可解析 |
| SC-10 | PASS | 1 个 Skill 条目，5 个 Agent 条目，字段齐全 |
| SC-11 | PASS | S01-S24 齐全，均含类型、输入、预期、判定 |
| SC-12 | PASS | 代码块外无 TODO 占位符 |
| SC-13 | PASS | 83 个长段落，0 个跨文件重复（0 警告） |
| SC-14 | PASS | skill.zip 41,232 字节，内容与源码一致且可复现 |
| SC-15 | PASS | 无许可证文件；README 明确说明尚未选择 |
| SC-16 | PASS | README 第一项是指定启动提示词代码块，且全文只出现一次 |
| SC-17 | PASS | README 含加载顺序、导航职责、技术边界与四种加载状态 |
| SC-18 | PASS | SKILL 含 Chat Host 中立性；ChatGPT/Codex 适配器声明原生安装可选 |
| SC-19 | PASS | 仓库只有一个 `SKILL.md`，无第二套 Brain Core |

## 2. 负向自测

命令：

```bash
python tests/validate.py --self-test
```

结果：**14 / 14 通过，退出码 0。**

新增覆盖：合法的 README 顶部提示词通过；提示词不在顶部、以及提示词重复出现时被拒绝。原有覆盖仍通过：坏技能名、缺失/超长 description、GitHub token、绝对路径、邮箱、TODO、断链、完整/残缺场景块。

## 3. 分发包

命令：

```bash
python tools/pack_skill.py
python tools/pack_skill.py --check
```

结果：

- 13 个文件，根目录 `tang-personal-brain/`。
- `skill.zip` 41,232 字节。
- SHA256：`796d294d7c8d1be45f41d0c499155644d0b8c262c94e1a249ef27882b8181908`
- `--verify-only`：每个条目与源码逐字节一致。
- `--check`：重新构建后字节完全一致，可复现。
- 包内包含新的 README 顶部提示词与通用 Chat 加载约定；不含 `tests/`、`tools/`、`.git`、`memory/` 或缓存。

## 4. 通用 Chat 行为测试

方法：新开独立 DSH 子会话，按普通 Chat Host 约束执行（只对话/读取，不写文件、不执行 git）。每个子会话读取 README 与 SKILL.md 后，对 S16-S24 的输入作答，由本轮构建者按判定标准逐条判定。

S18、S19 使用提示词模拟“无网络”和“只读到 README”；子会话本身可以读本地文件，因此这两项验证的是对话行为，不是真实网络故障。S23 使用明确目标的补充测试，并在提示中要求九段结构，验证的是指令是否 Agent 无关、验收是否可执行，而不是“能否自动发现该格式”。

| 场景 | 结果 | 实际观测 |
|---|---|---|
| S16 仅链接 | PASS | 先读 README 再读 SKILL.md，读到后才确认；未虚构读取；只回一句 |
| S17 顶部提示词 | PASS | 严格按 README → SKILL.md 加载，回“已读取 Tang-Personal-Brain v0.2.0，可以直接交流。”，无初始化报告 |
| S18 GitHub 不可访问 | PASS | 明确说打不开、没有网络/连接器/文件读取；请用户粘贴入口；未编造规范或版本 |
| S19 只读到 README | PASS | 标记 `Partial`，说明只读到 README、`SKILL.md` 不可读；未宣称完整加载 |
| S20 不同 Chat Host | PASS | 拒绝“我是 Gemini”的虚假前提，说明 Brain 与宿主解耦；不绑定 ChatGPT |
| S21 无执行权限 | PASS | 明确不能运行测试，不伪造结果；给出本机命令和任务指令降级路径 |
| S22 只想聊天 | PASS | 正常回应读博问题，约 330 字；未生成 Task Brief、未介绍仓库结构 |
| S23 需要执行 | PASS | 输出九段式任务指令；执行者未指定、不默认 Codex；含 diff 范围、验收、认证或 non-fast-forward 停止条件；未声称执行 |
| S24 更换 Agent | PASS | 判为 `required`，列出六字段与预检；只允许只读，不假定 Claude Code 继承 Codex 上下文 |

计数：9 个场景全部执行，9 个 PASS。S16 比“最低要求”更主动：它实际读取了 SKILL.md 后才声明加载；未读取时会按失败处理。

## 5. 未执行

| 项目 | 状态 | 原因 |
|---|---|---|
| S01-S15 本版本复跑 | 未运行 | 本轮只验证新增通用 Chat 场景；这些场景在 v0.1.0 的冒烟结果不能直接算作 v0.2.0 通过 |
| 真实 GitHub URL 抓取 | 未验证 | 子会话读取的是本地仓库副本，不是真实网络访问 |
| 真实 ChatGPT / Codex 安装 | 未验证 | 当前环境没有对应客户端与入口 |
| 跨模型稳定性 | 未验证 | 只运行了 DeepSeek-V4.1-Flash 一个模型 |
| `dual-repo-agent-handoff` 实际执行 | 未验证 | 仅保留既有接口与版本记录，本轮未使用 |

## 6. 仓库卫生与安全检查

- 20 个文件；最大的文档为 `tests/scenarios.md`、`tests/validate.py`、`README.md` 与 `SKILL.md`（188 行正文）。
- 只有一个 `SKILL.md`；无重复 Brain Core、无空目录、无重复长段落、无第三方依赖。
- SC-05/06/07/08/15 全部通过；人工复核未发现密钥、个人邮箱、本地绝对路径、私人聊天或无关项目数据。
- 仓库没有 LICENSE 文件；README 已声明许可证未定，公开可见不等于授权复用。

## 7. 限制

- S18/S19 的能力限制是提示词模拟，不是真实断网或真实 404。
- S16 子会话能读本地文件，不能证明任意 Chat Host 都能读取 GitHub。
- 行为结果来自单一模型、单次运行，不能证明跨模型、跨平台稳定。
- 静态校验只证明结构、链接、安全和分发包，不证明行为。
- 通用 Chat 能否加载，最终取决于宿主是否允许读取仓库；仓库只能提供约定和诚实的状态说明。

## 8. 复现

```bash
python tests/validate.py
python tests/validate.py --self-test
python tools/pack_skill.py
python tools/pack_skill.py --check
```

行为场景逐条输入与判定标准见 [scenarios.md](scenarios.md)。
