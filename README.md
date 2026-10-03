# 大米文章工作流

为“大米的小站”处理 Word 或 Markdown 文稿，宗旨是：**尽量不改变原文，只做最小必要修改。**

## 四项能力

| 能力 | 默认行为 |
| --- | --- |
| 事实核查 | 可选，默认关闭；明确要求核查时必须执行 |
| 人设适配 | 编辑流程必做，局部修正身份冲突；没有问题就不改 |
| 网站格式适配 | 编辑流程必做，只调整网站所需格式和元数据 |
| 发布与验证 | 明确要求发布时接入网站；明确要求提交 GitHub 时提交和推送 |

自然表达校准已从工作流删除：不去 AI 味、不统一声线、不自动润色或重构。保留原观点、表达、顺序和案例；不能把文风改写藏在“人设适配”或“格式适配”中。

## 两种常用调用

### 不核查，适配后发布

```text
$dami-article-workflow 这篇文章已经核查过，不用再做事实核查。只做人设适配和网站格式适配，尽量保留原文，发布到网站并提交 GitHub。
```

### 先核查，再适配和发布

```text
$dami-article-workflow 先做事实核查，再做人设适配和网站格式适配。只改必要的地方，完成后发布到网站并提交 GitHub。
```

核查开启时不能跳过重要事实；核查关闭时不会重复研究，也不会宣称本轮已经核查。技术验证与事实核查是两回事，跳过事实核查不跳过 UTF-8、构建和页面检查。

### 人工审核，暂不发布

```text
$dami-article-workflow 不做事实核查，只做人设和网站格式适配，给我修改前后对比，先不要发布或提交。
```

仅说“适配”“修改”或“发布”不会自动开启核查。未明确授权发布时只交付草稿。发现必须大幅重构的问题，先交给用户决定，不擅自扩大改动。

## 原样上传不需要编辑 Skill

已有终稿原样发布、只改元数据或导入 HTML 时，走普通网站接入，不自动调用文章编辑流程。例如：

```text
这篇 HTML 原样发布，内容不修改，不调用编辑 Skill，标为 AI 共研，检查后提交 GitHub。
```

即使显式调用本 Skill，“不改内容”的要求也优先：跳过编辑流程。HTML、视频和音频不属于 Skill 的文稿编辑范围。

## 资料与安装

- [SKILL.md](SKILL.md)：核查开关、模式和权限边界。
- [persona.md](references/persona.md)：真实身份、经历和保密边界；当次确认的信息优先，不虚构或夸大。
- [editorial-workflow.md](references/editorial-workflow.md)：最小修改、人设与网站格式规范、可选核查。
- [website-publishing.md](references/website-publishing.md)：网站接入、技术验证及 Git 边界。
- scripts/validate_article.py：文章目录、编码和元数据校验，也兼容网站中的 HTML 与图表配置。

旧的 natural-writing.md 和 writing-voice.md 仅保留作历史资料，已标记停用，不再加载、执行或参与改写。没有删除历史文件。

仓库：[maxlixiang/dami-article-workflow](https://github.com/maxlixiang/dami-article-workflow)。本机安装目录为 C:\Users\Hunt\.codex\skills\dami-article-workflow；更新时先检查本机个性化修改，再同步明确变更的文件，不覆盖无关资料。默认允许自动发现，显式写出 $dami-article-workflow 更可靠。

## 校验

```powershell
python -X utf8 "C:\Users\Hunt\.codex\skills\.system\skill-creator\scripts\quick_validate.py" .
python -X utf8 scripts/validate_article.py "F:\Git上的程序等等\sumin_website"
```

结构校验不能证明文章事实真实性。原始输入文件不会被覆盖；用户默认拥有原稿使用权限，不强制添加来源章节。
