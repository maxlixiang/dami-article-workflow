#!/usr/bin/env python3
"""Validate the Markdown/HTML article catalog used by 大米的小站."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


REQUIRED_FIELDS = ("id", "date", "category", "title", "excerpt", "content")
ID_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
DATE_PATTERN = re.compile(r"^\d{4}\.\d{2}\.\d{2}$")
H1_PATTERN = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)


def read_utf8(path: Path) -> str:
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(f"不是有效 UTF-8：{path}") from exc
    if "\ufffd" in text:
        raise ValueError(f"包含乱码替换字符 U+FFFD：{path}")
    return text


def validate(project_root: Path) -> list[str]:
    errors: list[str] = []
    index_path = project_root / "public" / "articles" / "index.json"
    if not index_path.is_file():
        return [f"找不到文章索引：{index_path}"]

    try:
        catalog = json.loads(read_utf8(index_path))
    except (ValueError, json.JSONDecodeError) as exc:
        return [f"文章索引读取失败：{exc}"]

    if not isinstance(catalog, list):
        return ["文章索引顶层必须是数组"]

    seen_ids: set[str] = set()
    seen_content: set[str] = set()

    for position, entry in enumerate(catalog, start=1):
        label = f"第 {position} 条"
        if not isinstance(entry, dict):
            errors.append(f"{label}不是对象")
            continue

        for field in REQUIRED_FIELDS:
            if not isinstance(entry.get(field), str) or not entry[field].strip():
                errors.append(f"{label}缺少非空字段：{field}")

        if any(field not in entry or not isinstance(entry[field], str) for field in REQUIRED_FIELDS):
            continue

        article_id = entry["id"]
        if not ID_PATTERN.fullmatch(article_id):
            errors.append(f"{label}的 id 不符合小写连字符格式：{article_id}")
        if article_id in seen_ids:
            errors.append(f"重复的文章 id：{article_id}")
        seen_ids.add(article_id)

        if not DATE_PATTERN.fullmatch(entry["date"]):
            errors.append(f"{label}的日期应为 YYYY.MM.DD：{entry['date']}")

        content = entry["content"]
        article_format = entry.get("format", "markdown")
        extension = ".html" if article_format == "html" else ".md"
        if article_format not in ("html", "markdown"):
            errors.append(f"{label}的 format 应为 markdown 或 html")
        if not content.startswith("/articles/") or not content.endswith(extension) or ".." in Path(content).parts:
            errors.append(f"{label}的 content 应为 /articles/*{extension}：{content}")
            continue
        if "sourceType" in entry and entry["sourceType"] not in ("original", "repost", "ai-research"):
            errors.append(f"{label}的 sourceType 无效")
        if content in seen_content:
            errors.append(f"重复的正文路径：{content}")
        seen_content.add(content)

        article_path = project_root / "public" / content.lstrip("/")
        if not article_path.is_file():
            errors.append(f"正文文件不存在：{article_path}")
            continue

        try:
            markdown = read_utf8(article_path)
        except ValueError as exc:
            errors.append(str(exc))
            continue

        if article_format == "html":
            if not markdown.strip():
                errors.append(f"HTML 正文为空：{article_path.name}")
            charts = entry.get("charts")
            if charts:
                if not isinstance(charts, str) or not charts.startswith("/articles/") or not charts.endswith(".json") or ".." in Path(charts).parts:
                    errors.append(f"{label}的 charts 应为 /articles/*.json")
                else:
                    try:
                        specs = json.loads(read_utf8(project_root / "public" / charts.lstrip("/")))
                        if not isinstance(specs, list):
                            errors.append(f"{label}的图表配置应为数组")
                    except (OSError, ValueError) as exc:
                        errors.append(f"{label}的图表配置读取失败：{exc}")
            continue

        headings = H1_PATTERN.findall(markdown)
        if len(headings) != 1:
            errors.append(f"{article_path.name} 应有且只有一个一级标题，当前为 {len(headings)} 个")
        elif headings[0].strip() != entry["title"].strip():
            errors.append(
                f"{article_path.name} 的一级标题与索引标题不一致："
                f"{headings[0].strip()} != {entry['title'].strip()}"
            )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_root", type=Path, help="大米的小站项目根目录")
    args = parser.parse_args()

    project_root = args.project_root.expanduser().resolve()
    errors = validate(project_root)
    if errors:
        print(f"[FAIL] 发现 {len(errors)} 个问题：", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    index_path = project_root / "public" / "articles" / "index.json"
    article_count = len(json.loads(read_utf8(index_path)))
    print(f"[OK] {article_count} 篇文章通过目录、UTF-8、元数据和标题检查。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
