# 验证结果 — 2026-11-06

当前版本：**0.5.1（候选，fix/nexus-v0.5.1）**。v0.1.0 至 v0.5.0 的记录见 Git 历史。

## 环境

| 项 | 值 |
|---|---|
| 宿主机 | Windows，PowerShell 7 |
| Python | 3.13.14（仅标准库） |
| Git | 2.51.1.windows.1 |
| 行为测试模型 | DeepSeek-V4.1-Flash，DSH 子会话 |
| 技能版本 | 0.5.1 |

## 1. 静态校验

```bash
python tests/validate.py
```

结果：**25 / 25 通过，0 失败，0 警告，退出码 0。**

| ID | 结果 | 实际观测 |
|---|---|---|
| SC-01 | PASS | version 0.5.1，README 与 CHANGELOG 一致 |
| SC-02 | PASS | SKILL.md 正文 198 行（上限 200） |
| SC-03 | PASS | 19 个必需文件存在 |
| SC-04 | PASS | openai.yaml 字段齐全，short_description 54 字符 |
| SC-05 | PASS | 未发现密钥或凭证模式 |
| SC-06 | PASS | 未发现本地绝对路径 |
| SC-07 | PASS | 未发现邮箱或手机号 |
| SC-08 | PASS | 无缓存、数据库、.env 或多余压缩包 |
| SC-09 | PASS | 27 个本地 Markdown 链接可解析 |
| SC-10 | PASS | 1 个 Skill 条目，5 个 Agent 条目 |
| SC-11 | PASS | S01-S48 齐全，均含类型、输入、预期、判定 |
| SC-12 | PASS | 代码块外无 TODO |
| SC-13 | PASS | 100 个长段落，0 个跨文件重复 |
| SC-14 | PASS | skill.zip 47,550 字节，14 个文件，内容一致且可复现 |
| SC-15 | PASS | MIT LICENSE 与 README 一致 |
| SC-16 | PASS | README 顶部提示词唯一且位置正确 |
| SC-17 | PASS | 通用 Chat 加载约定完整 |
| SC-18 | PASS | Chat Host 中立；原生安装为可选 |
| SC-19 | PASS | 只有一个 SKILL.md |
| SC-20 | PASS | 启动文案、身份串、一次性与无权限声明存在 |
| SC-21 | PASS | README 未泄漏启动文案或独立口令 |
| SC-22 | PASS | 显示名统一为 星核 · NEXUS，技术标识符未变 |
| SC-23 | PASS | 三种意图、R0-R3、Git-native、过程成本、自适应 Brief、四类证据声明存在 |
| SC-24 | PASS | 人格连续性规则存在，无第二套人格核心 |
| SC-25 | PASS | SKILL、orchestration、generic 可移植核心均允许 Draft-only Brief；执行者可暂不指定 |

## 2. 负向自测

```bash
python tests/validate.py --self-test
```

结果：**14 / 14 通过，退出码 0。**

## 3. 分发包

```bash
python tools/pack_skill.py
python tools/pack_skill.py --check
```

- 14 个文件，根目录 `tang-personal-brain/`。
- `skill.zip` 47,550 字节。
- SHA256：`40ca501b2f9e051cdd1527bbcc2f5158ac67316777c6808d8c89ecd46a2b676c`
- `--verify-only` 与 `--check` 均通过，逐字节可复现。
- 包含 `LICENSE`，不含 `tests/`、`tools/`、`.git`、`memory/`。

## 4. 行为回归状态

v0.5.1 是修复补丁，只改 Draft-only/Execution 规则与 portable core；不把 v0.5.0 的历史结果算作 v0.5.1 结果。

| 范围 | 状态 | 说明 |
|---|---|---|
| S35 Draft-only | **PASS** | 有明确目标时交付九段式 Brief，执行者留空，未修改文件；无目标时先问一个阻塞事实，不虚构对象 |
| S36 长任务自主推进 | **PASS** | 一次授权、Gate 自验、停止条件明确；同时发现 generic portable core 仍有旧句，已修复并纳入 SC-25 |
| S42 人格 10 轮 | **PASS** | 真实连续 10 次独立消息：技术、读博、读书、自我纠错、Draft-only、Agent 报告、虚假前提、模型身份、实验设计、日常聊天；未退化、未机械自称、未重复仪式 |
| S01-S34 | **NOT RUN** | 未在 0.5.1 重跑；历史结果不计入本版本 |
| S37-S41、S43-S48 | **NOT RUN** | 未在 0.5.1 逐条重跑；v0.5.0 结果不计入本版本 |

人格 10 轮补充：会话加载时 metadata 仍为 0.5.0，随后版本号才升到 0.5.1；人格文本未改。第 7 轮正确拒绝了一个不存在的 Docker/Podman 前文，没有为了顺从虚构认错。跨模型人格一致性未验证。

## 5. 发布门禁

- 静态、负向自测、分发包、Draft-only 修复与人格 10 轮：通过。
- **S01-S48 全量回归：未完成。** 因此 0.5.1 只作为 `fix/nexus-v0.5.1` 候选，未合并到 `main`。
- 不把静态检查或 v0.5.0 结果当作全量行为通过。

## 6. 限制

- S01-S34 与 S37-S41、S43-S48 未在 0.5.1 重跑；正式 Minor 发布门禁不满足。
- 真实 GitHub 网络读取、ChatGPT/Codex 原生安装、跨模型一致性未验证。
- S42 使用真实连续消息，但仍是单一模型、单一宿主。
- 启动彩蛋未改，公开仓库中仍只是仪式，不是认证。

## 7. 复现

```bash
python tests/validate.py
python tests/validate.py --self-test
python tools/pack_skill.py
python tools/pack_skill.py --check
```

行为场景见 [scenarios.md](scenarios.md)。
