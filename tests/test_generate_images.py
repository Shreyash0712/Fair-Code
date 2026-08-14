import importlib

from PIL import Image
import json
import importlib
import shutil

def test_generate_favicons(tmp_path):
    script = importlib.import_module("scripts.generate_favicons")

    script.ICONS_DIR = tmp_path
    script.LOGO_SVG = script.ROOT / "assets" / "icons" / "logo.svg"

    script.main()

    expected = {
        "favicon-16x16.png": (16, 16),
        "favicon-32x32.png": (32, 32),
        "favicon.ico": (32, 32),
        "apple-touch-icon.png": (180, 180),
        "icon-192.png": (192, 192),
        "icon-512.png": (512, 512),
    }

    for filename in expected:
        output = tmp_path / filename
        assert output.is_file(), f"Expected {filename} to be generated"
        assert output.stat().st_size > 0, f"{filename} is empty"

        with Image.open(output) as image:
            assert image.width > 0
            assert image.height > 0

        with Image.open(output) as image:
            assert image.size == expected[filename]


def test_generate_og_images(tmp_path):
    script = importlib.import_module("scripts.generate_og_images")

    test_root = script.ROOT / f".tmp-test-{tmp_path.name}"
    test_root.mkdir()

    try:
        script.THEMES["dark"]["out_dir"] = test_root / "og"
        script.THEMES["light"]["out_dir"] = test_root / "og-light"

        script.main()

        expected = ["home.png", "profiler.png"]

        for entry in json.loads(
            script.DATA_JSON.read_text(encoding="utf-8")
        ):
            expected.append(f"{entry['slug']}.png")

        for directory in (test_root / "og", test_root / "og-light"):
            for filename in expected:
                output = directory / filename
                assert output.is_file(), f"Expected {output} to be generated"
                assert output.stat().st_size > 0, f"{output} is empty"

                with Image.open(output) as image:
                    assert image.size == (1200, 630)
    finally:
        shutil.rmtree(test_root, ignore_errors=True)
