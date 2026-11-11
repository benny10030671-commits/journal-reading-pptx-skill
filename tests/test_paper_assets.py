"""Functional extraction tests using synthetic, nonclinical PDF fixtures."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

import pymupdf

SPEC = importlib.util.spec_from_file_location("paper_assets", Path(__file__).parents[1] / "scripts" / "paper_assets.py")
assets = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(assets)


class CropTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.pdf = self.root / "source.pdf"
        with pymupdf.open() as doc:
            page = doc.new_page(width=300, height=200)
            page.insert_text((30, 60), "Panel A: test text", fontsize=15)
            page.draw_rect((20, 80, 140, 140), color=(1, 0, 0), fill=(0, 0, 1))
            page.add_highlight_annot(pymupdf.Rect(30, 45, 160, 65))
            doc.new_page(width=300, height=200)
            doc[1].insert_text((30, 60), "Rotated panel", fontsize=15)
            doc[1].set_rotation(90)
            doc.save(self.pdf)

    def crop(self, **kwargs):
        params = dict(pdf=self.pdf, page_number=1, bbox=[10, 30, 170, 160],
                      output=self.root / "figure.png", label="Figure 1A", citation="Synthetic fixture", source_id="test", dpi=144)
        params.update(kwargs)
        return assets.crop_pdf(**params)

    def test_pixels_labels_and_source_preserved(self):
        before = assets.digest(self.pdf)
        record = self.crop()
        self.assertEqual(record["pixels"], [320, 260])
        self.assertEqual(record["label"], "Figure 1A")
        self.assertEqual(record["source_sha256"], before)
        self.assertEqual(assets.digest(self.pdf), before)
        self.assertTrue(assets.verify_crop(self.root / "figure.png.json", self.pdf)["verified"])
        with pymupdf.open(self.pdf) as doc:
            expected = doc[0].get_pixmap(clip=pymupdf.Rect(10, 30, 170, 160), dpi=144, annots=False)
        actual = pymupdf.Pixmap(str(self.root / "figure.png"))
        self.assertEqual(expected.samples, actual.samples)

    def test_rotation_uses_display_coordinates(self):
        data = assets.index_pdf(self.pdf, self.root / "index.json")
        rotated = data["pages"][1]
        self.assertEqual(rotated["bounds"], [0, 0, 200, 300])
        self.assertEqual(rotated["original_rotation"], 90)
        self.assertIn("Rotated panel", rotated["text_blocks"][0]["text"])
        record = self.crop(page_number=2, bbox=rotated["bounds"])
        self.assertEqual(record["pixels"], [400, 600])
        # Check against the original viewer rendering, independently of normalization.
        with pymupdf.open(self.pdf) as doc:
            expected = doc[1].get_pixmap(dpi=144, annots=False)
        actual = pymupdf.Pixmap(str(self.root / "figure.png"))
        self.assertEqual(expected.samples, actual.samples)

    def test_invalid_crop_rejected_without_output(self):
        for bbox in [[-1, 0, 30, 30], [0, 0, 301, 10], [30, 0, 20, 10], [0, 0, float("nan"), 10]]:
            with self.subTest(bbox=bbox), self.assertRaises(ValueError):
                self.crop(bbox=bbox)
        self.assertFalse((self.root / "figure.png").exists())

    def test_invalid_page_and_metadata_rejected(self):
        for page in [0, 3]:
            with self.subTest(page=page), self.assertRaises(ValueError):
                self.crop(page_number=page)
        with self.assertRaises(ValueError):
            self.crop(citation=" ")

    def test_changed_image_detected(self):
        self.crop()
        (self.root / "figure.png").write_bytes(b"changed")
        with self.assertRaisesRegex(ValueError, "Image hash mismatch"):
            assets.verify_crop(self.root / "figure.png.json", self.pdf)

    def test_changed_source_detected(self):
        self.crop()
        other = self.root / "other.pdf"
        with pymupdf.open() as doc:
            doc.new_page()
            doc.save(other)
        with self.assertRaisesRegex(ValueError, "Source PDF hash mismatch"):
            assets.verify_crop(self.root / "figure.png.json", other)

    def test_incorrect_region_detected_even_with_unchanged_hashes(self):
        self.crop()
        sidecar = self.root / "figure.png.json"
        record = json.loads(sidecar.read_text(encoding="utf8"))
        record["bbox"] = [15, 30, 175, 160]
        assets.write_json(sidecar, record)
        with self.assertRaisesRegex(ValueError, "pixels differ"):
            assets.verify_crop(sidecar, self.pdf)

    def test_existing_output_not_overwritten(self):
        self.crop()
        before = assets.digest(self.root / "figure.png")
        with self.assertRaises(ValueError):
            self.crop()
        self.assertEqual(before, assets.digest(self.root / "figure.png"))


if __name__ == "__main__":
    unittest.main()
