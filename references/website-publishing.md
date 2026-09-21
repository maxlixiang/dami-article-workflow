# 大米的小站发布规范

## 项目

- 默认本地路径：`F:\Git上的程序等等\sumin_website`
- 技术栈：Vite + React 单页网站
- 文章正文：`public/articles/*.md`
- 文章索引：`public/articles/index.json`
- GitHub：`https://github.com/maxlixiang/sumin-blog`

开始前必须检查当前代码、`git status`、文章索引和实际页面。以当前工作区为准，不假定本文件记录的页面实现永远不变。

## 发布前准备

为文章确定：

- 稳定、简短、使用小写字母和连字符的 `id`；
- `YYYY.MM.DD` 日期；
- 与现有分类粒度一致的分类；
- 准确但不夸张的标题；
- 一句话摘要；
- `/articles/<id>.md` 正文路径。

不要修改无关文章、图片、主页结构或个人经历。不要覆盖用户在 GitHub 或本地已有的修改。

## 写入网站

1. 在 `public/articles/` 新建 UTF-8 Markdown 文件。
2. 使用一个一级标题，并让它与索引中的标题一致。
3. 在 `public/articles/index.json` 顶部加入新条目，保持有效 JSON。
4. 不在正文中重复网站已经单独显示的元数据。
5. 官方链接可放在对应事实附近；只有文章确实需要时才增加参考资料或免责声明。

## 验证

至少完成：

1. 用 UTF-8 回读所有修改过的中文文件，确认没有 `U+FFFD` 乱码字符；
2. 在 Skill 目录运行：

   ```bash
   python scripts/validate_article.py "F:\\Git上的程序等等\\sumin_website"
   ```

3. 在网站目录运行 `npm run build`；
4. 启动本地页面，验证首页最新文章、全部文章页和文章独立地址；
5. 验证桌面端与手机端没有重叠或横向滚动；
6. 检查浏览器控制台；
7. 确认文章链接、返回列表和上一篇／下一篇正常。

## Git 边界

- 只有用户在当前请求中明确要求提交或发布时，才能 commit 或 push。
- 推送前先 fetch，检查本地与远端是否分叉；不要覆盖远端文章修改。
- 只暂存本次文章、索引和确有必要的相关文件。
- 构建成功不等于线上部署成功；如用户要求验证线上结果，再检查 Vercel 部署和正式域名。
- 不创建 Pull Request，除非用户明确要求。
