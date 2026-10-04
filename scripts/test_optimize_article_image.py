"""Local fixture tests; no image generation/network or project writes."""
import hashlib
import importlib.util
import os
import tempfile
import unittest
from contextlib import contextmanager
from pathlib import Path
from PIL import Image

spec = importlib.util.spec_from_file_location("optimizer", Path(__file__).with_name("optimize_article_image.py"))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


@contextmanager
def fixture_dir():
    # Keep fixtures for inspection: never recursively delete a test directory.
    yield tempfile.mkdtemp(prefix="dami-image-test-", dir=os.environ.get("DAMI_IMAGE_TEST_DIR"))


class CoverTests(unittest.TestCase):
    def test_resize_and_preserve_source(self):
        with fixture_dir() as folder:
            root = Path(folder)
            source, output = root / "source.png", root / "nested/cover.webp"
            Image.new("RGB", (1920, 1080), "#d6c0a0").save(source)
            digest = hashlib.sha256(source.read_bytes()).digest()
            result = module.optimize(source, output)
            with Image.open(output) as image:
                self.assertEqual(image.format, "WEBP")
                self.assertEqual(image.size, (1200, 675))
            self.assertTrue(result["within_budget"])
            self.assertEqual(hashlib.sha256(source.read_bytes()).digest(), digest)
            with self.assertRaises(ValueError):
                module.optimize(source, output)

    def test_crop_requires_permission_and_no_upscale(self):
        with fixture_dir() as folder:
            root = Path(folder)
            source = root / "square.png"
            Image.new("RGB", (320, 320)).save(source)
            with self.assertRaises(ValueError):
                module.optimize(source, root / "no.webp")
            result = module.optimize(source, root / "crop.webp", crop=True)
            self.assertEqual((result["width"], result["height"]), (320, 180))

    def test_alpha_and_budget_warning(self):
        with fixture_dir() as folder:
            root = Path(folder)
            source = root / "alpha.png"
            Image.new("RGBA", (160, 90), (200, 100, 20, 0)).save(source)
            result = module.optimize(source, root / "alpha.webp", target_kb=0.001)
            self.assertFalse(result["within_budget"])
            self.assertEqual(result["quality"], 60)
            with Image.open(root / "alpha.webp") as image:
                self.assertEqual(image.getpixel((0, 0))[3], 0)
            with self.assertRaises(ValueError):
                module.optimize(source, root / "wrong.png")

if __name__ == "__main__":
    unittest.main()
