"""Regression tests for article-data storage (fixtures retained, no deletion)."""
import json
import tempfile
import unittest
from pathlib import Path

from validate_article import validate


class ArticleDirectoryTests(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp(prefix="dami-article-validator-"))
        self.data = self.root / "public" / "article-data"
        self.data.mkdir(parents=True)
        self.catalog = [
            {"id": "sample", "date": "2026.10.13", "category": "test",
             "title": "Sample", "excerpt": "Test article", "content": "/article-data/sample.md"},
            {"id": "report", "date": "2026.10.13", "category": "test",
             "title": "Report", "excerpt": "HTML report", "format": "html",
             "content": "/article-data/report.html", "charts": "/article-data/report.charts.json"},
        ]
        (self.data / "sample.md").write_text("# Sample\n\nBody\n", encoding="utf-8")
        (self.data / "report.html").write_text("<!doctype html><h1>Report</h1>", encoding="utf-8")
        (self.data / "report.charts.json").write_text("[]", encoding="utf-8")
        self.write_catalog()

    def write_catalog(self):
        (self.data / "index.json").write_text(json.dumps(self.catalog), encoding="utf-8")

    def test_new_directory_accepts_markdown_html_and_charts(self):
        self.assertEqual(validate(self.root), [])
        self.assertFalse((self.root / "public" / "articles").exists())

    def test_old_content_url_is_rejected(self):
        self.catalog[0]["content"] = "/articles/sample.md"
        self.write_catalog()
        self.assertTrue(any("content" in error for error in validate(self.root)))

    def test_old_chart_url_is_rejected(self):
        self.catalog[1]["charts"] = "/articles/report.charts.json"
        self.write_catalog()
        self.assertTrue(any("charts" in error for error in validate(self.root)))

    def test_missing_content_is_reported(self):
        self.catalog[0]["content"] = "/article-data/missing.md"
        self.write_catalog()
        self.assertTrue(validate(self.root))

    def test_path_traversal_is_rejected(self):
        self.catalog[0]["content"] = "/article-data/../sample.md"
        self.write_catalog()
        self.assertTrue(any("content" in error for error in validate(self.root)))


if __name__ == "__main__":
    unittest.main()
