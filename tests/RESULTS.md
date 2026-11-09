# 验证结果 — 2026-11-09

当前版本：**0.7.0（minor，`feat/context-recovery`，未合并 main）**。v0.1.0 至 v0.6.0 的记录见 Git 历史。

## 环境

| 项 | 值 |
|---|---|
| 宿主机 | Windows，PowerShell 7 |
| Python | 3.13.14（仅标准库） |
| Git | 2.51.1.windows.1 |
| 行为测试模型 | DeepSeek-V4.1-Flash，DSH 独立子会话 |
| 技能版本 | 0.7.0 |

## 1. 静态校验

```bash
python tests/validate.py
```

结果：**28 / 28 通过，0 失败，0 警告，退出码 0。**

| ID | 结果 | 观测 |
|---|---|---|
| SC-01 | PASS | version 0.7.0，README 与 CHANGELOG 一致 |
| SC-02 | PASS | SKILL.md 正文 200 行（上限 200） |
| SC-03 | PASS | 19 个必需文件存在 |
| SC-04 | PASS | openai.yaml 字段齐全 |
| SC-05 | PASS | 未发现密钥或凭证模式 |
| SC-06 | PASS | 未发现本地绝对路径 |
| SC-07 | PASS | 未发现邮箱或手机号 |
| SC-08 | PASS | 无缓存、数据库或多余压缩包 |
| SC-09 | PASS | 27 个本地 Markdown 链接可解析 |
| SC-10 | PASS | 1 个 Skill 条目，5 个 Agent 条目 |
| SC-11 | PASS | S01-S63 齐全，均含类型、输入、预期、判定 |
| SC-12 | PASS | 代码块外无 TODO |
| SC-13 | PASS | 125 个长段落，0 个跨文件重复 |
| SC-14 | PASS | skill.zip 54,143 字节，14 个文件，可复现 |
| SC-15 | PASS | MIT LICENSE 与 README 一致 |
| SC-16 | PASS | README 顶部提示词唯一且位置正确 |
| SC-17 | PASS | 通用 Chat 加载约定完整 |
| SC-18 | PASS | Chat Host 中立；原生安装为可选 |
| SC-19 | PASS | 只有一个 SKILL.md |
| SC-20 | PASS | 启动文案、身份串、一次性与无权限声明存在 |
| SC-21 | PASS | README 未泄漏启动文案 |
| SC-22 | PASS | 显示名与标识符未变 |
| SC-23 | PASS | v0.5 执行效率规则存在 |
| SC-24 | PASS | 人格连续性规则存在 |
| SC-25 | PASS | Draft-only Brief 一致 |
| SC-26 | PASS | v0.6 校准规则存在 |
| SC-27 | PASS | v0.6.0 收敛修复存在 |
| SC-28 | PASS | 替代关系审查、范围保护、四维验收、遗留治理、冷启动与 PROPOSED 区分存在 |

## 2. 负向自测

```bash
python tests/validate.py --self-test
```

结果：**14 / 14 通过，退出码 0。**

## 3. 分发包

- `skill.zip` 54,143 字节，14 个文件，根目录 `tang-personal-brain/`。
- SHA256：`2185ea80453ff35875a275cc4abf55757ab88f2eb75eb4d670e0c2e8934ca147`
- `--verify-only` 与 `--check` 均通过，逐字节可复现。

## 4. 行为回归（本版本实际执行）

执行范围：新增 S54-S63，加受冷启动影响的既有场景 S13。S01-S53 其余未在本版本重跑。

| 场景 | 结果 | 关键证据 |
|---|---|---|
| S54 从 STATUS.md 恢复 | PASS | 读状态入口；核验 DEV/AUDIT SHA 实际一致；指出 `main` 与 `master` 声明矛盾；区分 PROPOSED/HOLD |
| S55 STATUS 与 DEV SHA 不一致 | PASS | 指出 `deadbeef` 对象不存在；暂停依赖状态的写入；给基线确认路径 |
| S56 没有 STATUS.md | PASS | 回退 README/架构；标未知；拒绝自建状态文件 |
| S57 未批准建议 | PASS | PROPOSED 无批准记录；拒绝直接改基线；索要具体文件与授权 |
| S58 新增功能未查旧实现 | **FAIL** | 判 HOLD、识别双路径风险、要求迁移与依赖清单；但未使用 REMOVE / REPLACE / KEEP / REVIEW 分类词 |
| S59 测试通过但范围缩减 | PASS | 判 HOLD；指出已批准目标缺一项；暂停并给批准/替代/继续三选一 |
| S60 旧接口治理 | PASS | 未发布不默认保留；要求先冻结 golden 证据再删；保护数值回归 |
| S61 PASS 无独立证据 | PASS | 区分声称/证据/核验；按四维要证据；判 HOLD |
| S62 项目编号与全局规则冲突 | PASS | 项目例外不升全局；名称在前；不猜编号映射 |
| S63 普通讨论 | PASS | Discussion 回应；未写任何项目文件；未出 brief |
| S13 项目切换（受影响） | PASS | 声明切换；AeroGNC 状态标未知；给冷启动入口 |

统计：**10 PASS / 1 FAIL / 0 NOT RUN**。

测试夹具：S54-S56 使用 `%TEMP%\tpb-v07-fixtures` 下三个临时仓库（一致、SHA 不一致、无状态入口），验证后已删除。

## 5. 已知缺陷（未修复，如实保留）

| ID | 状态 | 说明 |
|---|---|---|
| S34 | FAIL（自 v0.6.0） | 宿主无法执行时未交付九段式 brief，只给建议步骤与代办清单 |
| S58 | FAIL（本版） | 替代关系判断正确，但未按规则使用 REMOVE / REPLACE / KEEP / REVIEW 分类 |
| S06 | 残余 | 临时预算有复核周期，未点名负责人角色 |

未删除、未降低任何失败场景或其判据。

## 6. 发布判定

**未发布。** 本版本位于 `feat/context-recovery`，未合并 `main`、未打 Tag、未推送 `main`。

- 静态校验 28/28、自测 14/14、分发包可复现：满足。
- 新增能力 10 项场景 9 PASS、1 FAIL（S58 分类词）。
- S01-S53 未在本版本重跑，全量门禁不满足；不宣称全量通过。

## 7. 测试性质与限制

- 开发者自测：规则修改、场景编写、执行与判定由同一方完成，未经独立评审。
- 单模型（deepseek-flash）、单宿主；每个场景跑一次。
- S57 的原始前设（四层基线）在本仓库不存在（本仓库为三层上下文），模型据实拒绝执行并追问；该次结果证明的是「拒绝未批准建议」的行为，不是对某个真实四层架构的处置。
- S54、S55 暴露的是夹具自带的声明不一致（`main` vs `master`），模型按冲突处理；属测试设计副作用，已记录。
- SC-11/SC-26/SC-27/SC-28 只证明条款与场景存在，不证明模型执行。

## 8. 复现

```bash
python tests/validate.py
python tests/validate.py --self-test
python tools/pack_skill.py
python tools/pack_skill.py --check
```

行为场景见 [scenarios.md](scenarios.md)。
