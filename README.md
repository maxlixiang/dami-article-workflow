# 大米文章工作流

`dami-article-workflow` 是为“大米的小站”定制的 Codex Skill，用于把已有的 Word 或 Markdown 文稿整理成事实可靠、符合大米真实经历、并能直接进入网站发布流程的文章。

它不是通用洗稿工具，也不处理视频或音频。核心工作是把事实核查、人设适配、文字编辑和网站发布连接成一套可重复执行的流程。

## 主要能力

- 读取 `.docx` 和 `.md` 文稿；
- 提取并核查机构、项目、法律、数字、时间等事实主张；
- 按大米当前职业经历调整叙述身份和语气；
- 根据原稿质量选择轻度润色、中度改编或深度重构；
- 生成符合“大米的小站”格式的标题、摘要、分类、文章 ID 和 Markdown 正文；
- 在明确授权后更新网站、构建、浏览器验证并提交 GitHub；
- 使用校验脚本检查 UTF-8、文章索引、重复 ID、日期、正文路径和一级标题。

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

### 发布模式

只有用户明确要求发布、更新网站或提交 GitHub 时才执行网站和 Git 操作。

```text
$dami-article-workflow 帮我核查并改写这篇 Word 文章，发布到大米的小站，验证后提交 GitHub。
```

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
│  └─ website-publishing.md
└─ scripts/
   └─ validate_article.py
```

- `SKILL.md`：模式选择、执行流程和权限边界；
- `persona.md`：大米的真实经历、合适视角与禁止夸大的内容；
- `editorial-workflow.md`：事实核查、改写强度和网站文章风格；
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
