# 大米文章工作流

`dami-article-workflow` 是为“大米的小站”定制的 Codex Skill，用于对 Word 或 Markdown 文稿进行事实核查、改写和润色，并在授权后发布。它不是所有文章上传的必经步骤。

它不是通用洗稿工具，也不处理视频或音频。核心工作是把事实核查、人设适配、自然表达校准、文字编辑和网站发布连接成一套可重复执行的流程。

## 主要能力

- 读取 `.docx` 和 `.md` 文稿；
- 提取并核查机构、项目、法律、数字、时间等事实主张；
- 按大米当前职业经历调整叙述身份和语气；
- 清理模板化 AI 腔、报告腔和说教感，同时保护事实、限定条件与专业语域；
- 根据原稿质量选择轻度润色、中度改编或深度重构；
- 生成符合“大米的小站”格式的标题、摘要、分类、文章 ID 和 Markdown 正文；
- 在明确授权后更新网站、构建、浏览器验证并提交 GitHub；
- 使用校验脚本检查 UTF-8、文章索引、重复 ID、日期、正文路径和 Markdown 一级标题；也兼容目录中的 HTML 文章与图表 JSON，不因此触发内容编辑。

默认认为用户拥有所提供文稿的原创、转发或改编权限，不重复进行常规版权审查，也不强制添加“灵感来源”章节。官方资料链接仍可用于支持事实或增强文章可信度。

## 工作模式

### 审核模式

适合判断文章是否适合发表，不修改原稿和网站。

```text
$dami-article-workflow 帮我审核这篇 Word 文章是否适合我发表，先不要修改。
```

输出事实问题、人设冲突和建议的编辑强度。

### 草稿模式

适合完成事实核查和改写，但暂不发布。

```text
$dami-article-workflow 对这篇 Markdown 文章进行事实核查，改成符合我人设的版本，先给我审稿。
```

如果请求没有明确说明是否发布，Skill 默认使用草稿模式。

也可以明确要求在事实和人设处理之后减少模板化 AI 腔：

```text
$dami-article-workflow 核查并改写这篇文章，保持法律表述准确，再按我的写作声线减少 AI 味，先不要发布。
```

### 编辑后发布模式

只有用户明确要求发布、更新网站或提交 GitHub 时才执行网站和 Git 操作。

```text
$dami-article-workflow 帮我核查并改写这篇 Word 文章，发布到大米的小站，验证后提交 GitHub。
```

### 直接发布：不需要调用文章编辑 Skill

已有终稿只需上线、HTML 专题原样导入、只改来源标记或其他元数据时，不自动调用这个 Skill，也不核查事实、匹配人设或消除 AI 味。只做网站接入、必要的资源与格式兼容检查、UTF-8 回读、构建、浏览器验证，以及明确授权的 Git 操作。

例如直接告诉 Codex：

```text
这篇文章原样发布到网站，正文和标题不要修改，不做事实核查或改写，标为 AI 共研，检查后提交 GitHub。
```

明确要求仅调整格式时，只调整指定格式。若仍显式调用本 Skill 并要求原样发布，也以“不修改”为准，跳过编辑流程。HTML 本身不在此 Skill 的编辑范围内，直接使用网站的 HTML 专题支持。

## 人设基础

Skill 使用可维护的 [`references/persona.md`](references/persona.md) 作为事实档案，当前包括：

- 法律与计算机交叉背景；
- 南加州大学 LLM；
- 中美法律实践经历；
- 当前在企业负责美国市场相关法律事务；
- 重点方向为产品合规与知识产权；
- 关注 AI、法律科技和 Vibe Coding；
- 不包装成资深行业权威或自媒体从业者。

人设文件也规定了雇主信息、内部数据、客户信息和具体法律意见的保密边界。

## 自然表达校准

Skill 会在事实核查和人设适配之后进行自然表达校准，重点处理空泛开场、纠正读者的姿态、教师式自问自答、机械排比、报告腔、重复总结和强行升华。

这一步不以规避 AI 检测为目标，不输出所谓“AI 率”，也不会通过编造经历、故意写错或强塞口头禅来制造“人味”。单独出现一个连接词、引号、破折号或排比句也不会自动触发修改。

[`references/writing-voice.md`](references/writing-voice.md) 保存稳定的写作偏好；用户提供自己的最终修改版后，可以在明确授权下逐步更新这份声线档案。

## 安装

将仓库克隆到 Codex Skills 目录：

```powershell
git clone https://github.com/maxlixiang/dami-article-workflow.git "$HOME\.codex\skills\dami-article-workflow"
```

如果目标目录已经存在，先确认本地是否有需要保留的修改，不要直接覆盖。新安装的 Skill 通常从下一轮任务开始可用。

## 使用

推荐显式调用：

```text
$dami-article-workflow <你的要求>
```

由于 Skill 允许自动发现，类似“帮我核查并改写这篇 Word 文章，发布到大米的小站”的请求通常也能触发；显式写出 Skill 名称最可靠。

## 项目结构

```text
dami-article-workflow/
├─ SKILL.md
├─ agents/
│  └─ openai.yaml
├─ references/
│  ├─ persona.md
│  ├─ editorial-workflow.md
│  ├─ natural-writing.md
│  ├─ writing-voice.md
│  └─ website-publishing.md
└─ scripts/
   └─ validate_article.py
```

- `SKILL.md`：模式选择、执行流程和权限边界；
- `persona.md`：大米的真实经历、合适视角与禁止夸大的内容；
- `editorial-workflow.md`：事实核查、改写强度和网站文章风格；
- `natural-writing.md`：自然表达检查、保护边界与终稿自检；
- `writing-voice.md`：与人设事实分离的大米长期写作声线；
- `website-publishing.md`：网站集成、构建、浏览器检查和 Git 要求；
- `validate_article.py`：网站文章目录的确定性校验。

## 校验

验证 Skill 结构：

```powershell
python -X utf8 "$HOME\.codex\skills\.system\skill-creator\scripts\quick_validate.py" .
```

验证“大米的小站”文章目录：

```powershell
python -X utf8 scripts\validate_article.py "F:\Git上的程序等等\sumin_website"
```

校验脚本只负责文章目录、编码和元数据等确定性检查，不能替代事实核查、网站构建和浏览器验证。

## 更新

仓库版本更新后，如果本机安装的是下载副本，需要重新同步本机的 `C:\Users\Hunt\.codex\skills\dami-article-workflow`。更新前应检查本机副本是否存在尚未保存的个性化修改。
