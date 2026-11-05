# 验证结果 — 2026-11-05

当前版本：**0.3.0**。v0.1.0 / v0.2.0 的记录见 Git 历史；本文件记录星核 · NEXUS 命名、启动仪式与 MIT 许可证落地后的实际结果。

## 环境

| 项 | 值 |
|---|---|
| 宿主机 | Windows，PowerShell 7 |
| Python | 3.13.14（仅标准库） |
| Git | 2.51.1.windows.1 |
| GitHub CLI | 未安装；仓库操作使用已有凭据的 REST API 与 git |
| 行为测试模型 | DeepSeek-V4.1-Flash，DSH 子会话，2026-11-05 |
| 技能版本 | 0.3.0 |

## 1. 静态校验

命令：

```bash
python tests/validate.py
```

结果：**22 / 22 通过，0 失败，0 警告，退出码 0。**

| ID | 结果 | 实际观测 |
|---|---|---|
| SC-01 | PASS | `name=tang-personal-brain`，version 0.3.0，README 与 CHANGELOG 一致 |
| SC-02 | PASS | SKILL.md 正文 198 行（上限 200） |
| SC-03 | PASS | 19 个必需文件存在且达到最小体积 |
| SC-04 | PASS | openai.yaml 字段齐全，short_description 54 字符 |
| SC-05 | PASS | 未发现密钥或凭证模式 |
| SC-06 | PASS | 未发现盘符路径、用户目录或 file URL |
| SC-07 | PASS | 未发现邮箱或手机号 |
| SC-08 | PASS | 无缓存、数据库、.env 或多余压缩包 |
| SC-09 | PASS | 25 个本地 Markdown 链接全部可解析 |
| SC-10 | PASS | 1 个 Skill 条目，5 个 Agent 条目，字段齐全 |
| SC-11 | PASS | S01-S34 齐全，均含类型、输入、预期、判定 |
| SC-12 | PASS | 代码块外无 TODO 占位符 |
| SC-13 | PASS | 87 个长段落，0 个跨文件重复（0 警告） |
| SC-14 | PASS | skill.zip 43,080 字节，14 个文件，内容与源码一致且可复现 |
| SC-15 | PASS | LICENSE 为 MIT；README 的 MIT 声明与之一致 |
| SC-16 | PASS | README 第一项是指定启动提示词代码块，且全文只出现一次 |
| SC-17 | PASS | README 含加载顺序、导航职责、技术边界与四种加载状态 |
| SC-18 | PASS | SKILL 含 Chat Host 中立性；ChatGPT/Codex 适配器声明原生安装可选 |
| SC-19 | PASS | 仓库只有一个 `SKILL.md`，无第二套 Brain Core |
| SC-20 | PASS | SKILL 含两句固定启动文案、身份字符串、一次性与无权限声明 |
| SC-21 | PASS | README 不展示启动文案、指挥官称谓或独立身份字符串 |
| SC-22 | PASS | README、SKILL、openai.yaml 显示名均为 `星核 · NEXUS`，技术标识符未变 |

## 2. 负向自测

命令：

```bash
python tests/validate.py --self-test
```

结果：**14 / 14 通过，退出码 0。**

覆盖：合法 frontmatter；README 顶部提示词通过；提示词不在顶部、重复出现被拒绝；坏技能名、缺失/超长 description、GitHub token、绝对路径、邮箱、TODO、断链、完整/残缺场景块。

## 3. 分发包

命令：

```bash
python tools/pack_skill.py
python tools/pack_skill.py --check
```

结果：

- 14 个文件，根目录 `tang-personal-brain/`。
- `skill.zip` 43,080 字节。
- SHA256：`da5d2202afd5981398a149a29f802e6eb30dac5d72cea1c542923d6d2ea67b04`
- `--verify-only`：每个条目与源码逐字节一致。
- `--check`：重新构建后字节完全一致，可复现。
- 包内包含 `LICENSE`、README 顶部提示词、SKILL.md 启动规则；不含 `tests/`、`tools/`、`.git`、`memory/` 或缓存。

## 4. 启动仪式行为测试

方法：新开独立 DSH 子会话，按普通 Chat Host 约束执行（只对话/读取，不写文件、不执行 git）。每个子会话读取 README 与 SKILL.md 后按场景作答，由本轮构建者按判定标准逐条判定。

| 场景 | 结果 | 实际观测 |
|---|---|---|
| S25 首次加载 | PASS | 只输出 `Brain Core 在线。等待指挥官身份确认。`，未追加初始化报告 |
| S26 回复正确身份 | PASS | 输出 `身份确认。欢迎回来，指挥官。星核 · NEXUS 在线。`，未追加身份追问 |
| S27 错误身份 | PASS | 简短说明身份未匹配、可重试；未输出欢迎语，未锁功能 |
| S28 已确认不重复 | PASS | 直接回答 CAP 问题，未重复等待/欢迎句，未使用“指挥官” |
| S29 新对话 | PASS | 重新输出等待句，未继承旧对话确认状态 |
| S30 读取失败 | PASS | 说明打不开仓库、请用户粘贴规范；未输出启动句，未编造规则 |
| S31 普通问题 | PASS | 未触发身份确认，按普通对话回答 Python 问题 |
| S32 非 ChatGPT 宿主 | PASS | 在 Gemini 场景下仍输出固定等待句，未绑定 ChatGPT 工具 |
| S33 启动后技术讨论 | PASS | 直接回答 attention，未重复仪式，未使用“指挥官” |
| S34 启动后请求执行 | PASS | 先做只读审查，后补九段式任务指令；未声称已修改/推送 |

计数：10 个场景全部执行，10 个 PASS。S30 的错误提示未使用字面 `Unavailable`，但明确说明无法读取，按“等价表述”通过。S27 的“可以重试一次”是提示语，不是实际失败计数或锁定。

## 5. 未执行

| 项目 | 状态 | 原因 |
|---|---|---|
| S01-S24 本版本复跑 | 未运行 | 本轮只验证新增启动场景；v0.2.0 的 S16-S24 结果不能直接算作 v0.3.0 通过 |
| 真实 GitHub URL 抓取 | 未验证 | 子会话读取的是本地仓库副本，不是真实网络访问 |
| 真实 ChatGPT / Codex 安装 | 未验证 | 当前环境没有对应客户端与入口 |
| 跨模型稳定性 | 未验证 | 只运行了 DeepSeek-V4.1-Flash 一个模型 |
| `dual-repo-agent-handoff` 实际执行 | 未验证 | 仅保留既有接口与版本记录，本轮未使用 |

## 6. 仓库卫生与安全检查

- 21 个文件（新增 `LICENSE`）；最大文档为 `tests/scenarios.md`、`tests/validate.py`、`README.md` 与 `SKILL.md`（198 行正文）。
- 只有一个 `SKILL.md`；无重复 Brain Core、无空目录、无重复长段落、无第三方依赖。
- SC-05/06/07/08 全部通过；人工复核未发现密钥、个人邮箱、本地绝对路径、私人聊天或无关项目数据。
- 仓库采用 MIT License；README 的 License 段与 `LICENSE` 一致。

## 7. 限制

- 子会话能读本地文件，不能证明任意 Chat Host 都能读取 GitHub。
- S30 的“无网络”是提示词模拟，不是真实断网。
- 行为结果来自单一模型、单次运行，不能证明跨模型、跨平台稳定。
- 启动文案和身份字符串都存在于公开的 `SKILL.md` 中；该机制只是仪式彩蛋，不构成认证或权限控制。
- 静态校验只证明结构、链接、许可声明和分发包，不证明行为。

## 8. 复现

```bash
python tests/validate.py
python tests/validate.py --self-test
python tools/pack_skill.py
python tools/pack_skill.py --check
```

行为场景逐条输入与判定标准见 [scenarios.md](scenarios.md)。
