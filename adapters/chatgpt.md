# ChatGPT 适配

## 两种使用方式

1. **通用 Chat（无需安装）**：复制 README 顶部的启动提示词，粘贴到 ChatGPT。前提是当前会话能联网读取 GitHub，或用户上传/粘贴 `README.md` 与 `SKILL.md`。读取不到时标记 `Unavailable`，不要假装加载。
2. **原生 Skill（可选）**：把 `skill.zip` 安装为 ChatGPT Skill。这是可选的便利方式，不是使用 Tang-Personal-Brain 的前提。

下面保留原生 Skill 的安装、验证与更新说明。

## 适用条件

ChatGPT 的 Skills 功能面向符合条件的 Business、Enterprise、Healthcare 和 Edu 工作区，并受工作区权限控制。个人账号或未启用该功能的工作区可能看不到入口。

- 界面入口与权限说明核对时间：2026-11-05，来源：[Skills in ChatGPT（OpenAI Help Center）](https://help.openai.com/zh-hans-cn/articles/20001066-skills-in-chatgpt)。
- 产品界面会变化；以当前界面的实际入口为准。

## 分发包

使用本仓库根目录的 `skill.zip`。包内结构：

```text
tang-personal-brain/
├── SKILL.md
├── agents/openai.yaml
├── references/
├── registry/
└── adapters/
```

`SKILL.md` 必须在 `tang-personal-brain/` 的根层，不能多套一层目录。`agents/openai.yaml` 提供显示名称和默认提示词。

## 安装

1. 打开 ChatGPT，在侧边栏进入 **插件**。
2. 在 **插件目录** 中选择 **技能**。
3. 选择 **创建** → **从计算机上传**。
4. 上传 `skill.zip`，等待扫描完成。
5. 如显示 **需要审核**，先查看内容再决定是否启用。
6. 安装后在技能列表中确认 `星核 · NEXUS` 已启用。

如果看不到上传入口，通常是工作区管理员关闭了「启用技能上传」或当前方案不包含技能功能。让管理员检查权限，不要在聊天中粘贴凭据。

## 验证

新开一个会话，输入：

```text
使用 $tang-personal-brain，报告你的 metadata version，并用一句话说明你的默认沟通规则。
```

预期：报告 `0.4.0`，并说明「先给结论、按问题复杂度控制长度、区分已验证与未验证」。若回答不出，说明技能未加载或被其他指令覆盖。

## 更新

1. 从 GitHub 获取新版本，重新构建或下载新的 `skill.zip`。
2. 在 **技能** 中重新上传新版本。
3. 如果界面生成了重复条目，删除旧条目后再安装新条目。
4. 用上面的验证步骤确认版本号。

GitHub 推送不会让 ChatGPT 自动同步。平台也不会替你检查远端版本；版本核验必须手动做。

## 限制

- ChatGPT 会话默认没有本地 shell，不能直接检查本地仓库或运行测试。需要执行时，由 Brain 生成任务指令，交给 Codex、DeepSeek、Claude Code 或其他执行 Agent。
- 未安装原生 Skill 时，用 README 顶部提示词即可开始；不要把安装 Skill 当作使用前提。
- 连接器和代码解释器的可用性取决于方案与工作区设置。不要让 Brain 假设它们存在。
- 技能上传会经过平台扫描；扫描通过不等于内容经你审核。
- 会话之间不共享项目上下文。项目状态要写进项目仓库，而不是依赖聊天记忆。

## 卸载

在 **技能** 中选择该技能 → 更多选项 → 删除。删除后相关会话不再自动使用它。
