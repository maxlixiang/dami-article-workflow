#!/usr/bin/env python3
"""Non-destructive cover resizing and WebP encoding. Requires Pillow."""
import argparse
import io
import json
import sys
from pathlib import Path
from PIL import Image, ImageOps, features


def optimize(source, output, *, crop=False, width=1200, target_kb=300):
    source, output = Path(source).resolve(), Path(output).resolve()
    if output.suffix.lower() != ".webp":
        raise ValueError("Output must end in .webp")
    if source == output or output.exists():
        raise ValueError("Refusing to overwrite an existing file")
    if not 16 <= width <= 1200 or target_kb <= 0:
        raise ValueError("Width must be 16..1200; target KB must be positive")
    if not features.check("webp"):
        raise ValueError("Pillow lacks WebP support")
    with Image.open(source) as original:
        if getattr(original, "n_frames", 1) != 1:
            raise ValueError("Animated inputs are not cover images")
        image = ImageOps.exif_transpose(original)
        image.load()
        if not crop and abs(image.width / image.height - 16 / 9) > 0.01:
            raise ValueError("Input is not 16:9; inspect it before using --crop")
        out_width = int(min(width, image.width, image.height * 16 / 9) // 16) * 16
        if out_width < 16:
            raise ValueError("Input too small")
        size = (out_width, out_width * 9 // 16)
        image = ImageOps.fit(image, size, method=Image.Resampling.LANCZOS)
        image = image.convert("RGBA" if image.mode in ("RGBA", "LA") or "transparency" in image.info else "RGB")
        payload = b""
        for quality in (85, 80, 75, 70, 65, 60):
            buffer = io.BytesIO()
            image.save(buffer, format="WEBP", quality=quality, method=6)
            payload = buffer.getvalue()
            if len(payload) <= target_kb * 1024:
                break
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("xb") as handle:
        handle.write(payload)
    return {"path": str(output), "width": size[0], "height": size[1],
            "bytes": len(payload), "quality": quality,
            "within_budget": len(payload) <= target_kb * 1024}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--crop", action="store_true", help="Allow inspected center crop to 16:9")
    parser.add_argument("--width", type=int, default=1200)
    parser.add_argument("--target-kb", type=int, default=300)
    args = parser.parse_args()
    try:
        result = optimize(args.source, args.output, crop=args.crop, width=args.width, target_kb=args.target_kb)
    except (ValueError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result["within_budget"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
