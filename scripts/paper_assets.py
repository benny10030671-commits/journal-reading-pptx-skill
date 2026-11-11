#!/usr/bin/env python3
"""Index, preview and crop PDF evidence without redrawing it. Python 3.10+."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import sys

import pymupdf


COORDINATES = "display_points_top_left_after_remove_rotation"


def digest(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest() if hasattr(hashlib, "file_digest") else _hash_stream(stream)


def _hash_stream(stream):
    value = hashlib.sha256()
    for chunk in iter(lambda: stream.read(1024 * 1024), b""):
        value.update(chunk)
    return value.hexdigest()


def open_pdf(path):
    doc = pymupdf.open(path)
    if not doc.is_pdf or doc.needs_pass:
        doc.close()
        raise ValueError("Use an accessible, unencrypted PDF.")
    return doc


def page_at(doc, number):
    if not isinstance(number, int) or isinstance(number, bool) or not 1 <= number <= len(doc):
        raise ValueError(f"Page must be between 1 and {len(doc)} (1-based).")
    page = doc[number - 1]
    original_rotation = page.rotation
    page.remove_rotation()  # In-memory only; source PDF is never saved.
    return page, original_rotation


def checked_rect(page, bbox):
    if len(bbox) != 4 or not all(math.isfinite(v) for v in bbox):
        raise ValueError("bbox requires four finite coordinates.")
    x0, y0, x1, y1 = bbox
    if x0 >= x1 or y0 >= y1:
        raise ValueError("bbox must have positive width and height.")
    rect = pymupdf.Rect(bbox)
    if not page.rect.contains(rect):
        raise ValueError(f"bbox must be fully inside page bounds {list(page.rect)}.")
    return rect


def checked_dpi(dpi):
    if not isinstance(dpi, int) or isinstance(dpi, bool) or not 72 <= dpi <= 1200:
        raise ValueError("DPI must be an integer between 72 and 1200.")


def unused(path):
    path = Path(path)
    if path.exists():
        raise ValueError(f"Output already exists: {path}; choose a new filename.")
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def write_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def index_pdf(pdf, output):
    output = unused(output)
    with open_pdf(pdf) as doc:
        pages = []
        for number in range(1, len(doc) + 1):
            page, rotation = page_at(doc, number)
            blocks = [{"bbox": list(b[:4]), "text": b[4]} for b in page.get_text("blocks") if b[6] == 0]
            pages.append({"pdf_page": number, "pdf_page_label": page.get_label(),
                          "bounds": list(page.rect), "original_rotation": rotation,
                          "text_blocks": blocks})
        data = {"source_file": Path(pdf).name, "source_sha256": digest(pdf),
                "coordinate_system": COORDINATES, "pages": pages}
    write_json(output, data)
    return data


def get_pixels(page, rect, dpi):
    checked_dpi(dpi)
    if math.ceil(rect.width * dpi / 72) * math.ceil(rect.height * dpi / 72) > 100_000_000:
        raise ValueError("Raster exceeds 100 megapixels; reduce DPI or use a smaller region.")
    # Exclude viewer annotations (e.g. highlights) while retaining PDF page content.
    return page.get_pixmap(clip=rect, dpi=dpi, colorspace=pymupdf.csRGB, alpha=False, annots=False)


def preview_pdf(pdf, page_number, output, dpi=120):
    if Path(output).suffix.lower() != ".png":
        raise ValueError("Preview output must have a .png extension.")
    output = unused(output)
    with open_pdf(pdf) as doc:
        page, _ = page_at(doc, page_number)
        pix = get_pixels(page, page.rect, dpi)
        pix.save(output)
    return output


def crop_pdf(pdf, page_number, bbox, output, label, citation, source_id, dpi=300):
    if not all(isinstance(v, str) and v.strip() for v in [label, citation, source_id]):
        raise ValueError("label, citation and source-id must be nonempty.")
    if Path(output).suffix.lower() != ".png":
        raise ValueError("Crop output must have a .png extension.")
    output = unused(output)
    sidecar = unused(str(output) + ".json")
    with open_pdf(pdf) as doc:
        page, rotation = page_at(doc, page_number)
        rect = checked_rect(page, bbox)
        pix = get_pixels(page, rect, dpi)
        record = {"schema_version": 1, "kind": "pdf_region",
                  "source_id": source_id, "source_file": Path(pdf).name,
                  "source_sha256": digest(pdf), "pdf_page": page_number,
                  "pdf_page_label": page.get_label(), "original_rotation": rotation,
                  "coordinate_system": COORDINATES, "bbox": list(rect),
                  "dpi": dpi, "pixels": [pix.width, pix.height],
                  "label": label, "citation": citation, "annotations_included": False,
                  "image_file": output.name, "renderer": f"PyMuPDF {pymupdf.VersionBind}"}
        pix.save(output)
    record["image_sha256"] = digest(output)
    write_json(sidecar, record)
    return record


def verify_crop(sidecar, pdf):
    sidecar = Path(sidecar)
    record = json.loads(sidecar.read_text(encoding="utf-8"))
    if record.get("schema_version") != 1 or record.get("kind") != "pdf_region":
        raise ValueError("Unsupported crop metadata.")
    if record.get("coordinate_system") != COORDINATES or record.get("annotations_included") is not False:
        raise ValueError("Unsupported coordinate system or annotation setting.")
    for key in ["label", "citation", "source_id"]:
        if not isinstance(record.get(key), str) or not record[key].strip():
            raise ValueError(f"Missing {key}.")
    image_name = record["image_file"]
    if not isinstance(image_name, str) or not image_name or "/" in image_name or "\\" in image_name or ":" in image_name or image_name in (".", ".."):
        raise ValueError("image_file must be an adjacent filename.")
    image = sidecar.parent / image_name
    if digest(pdf) != record["source_sha256"]:
        raise ValueError("Source PDF hash mismatch.")
    if digest(image) != record["image_sha256"]:
        raise ValueError("Image hash mismatch.")
    with open_pdf(pdf) as doc:
        page, _ = page_at(doc, record["pdf_page"])
        expected = get_pixels(page, checked_rect(page, record["bbox"]), record["dpi"])
        actual = pymupdf.Pixmap(str(image))
        if (expected.width, expected.height, expected.n, expected.samples) != (actual.width, actual.height, actual.n, actual.samples):
            raise ValueError("Image pixels differ from re-rendered PDF region; check metadata and renderer version.")
    return {"verified": True, "image_file": image.name,
            "note": "Verified file hashes and rendered pixels; caption, crop completeness and scientific meaning still need visual review."}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    index = commands.add_parser("index", help="List text blocks and page geometry in JSON.")
    index.add_argument("pdf", type=Path)
    index.add_argument("--output", type=Path, required=True)
    for name in ("render", "crop"):
        command = commands.add_parser(name)
        command.add_argument("pdf", type=Path)
        command.add_argument("--page", type=int, required=True)
        command.add_argument("--output", type=Path, required=True)
        command.add_argument("--dpi", type=int, default=120 if name == "render" else 300)
        if name == "crop":
            command.add_argument("--bbox", type=float, nargs=4, required=True)
            command.add_argument("--label", required=True)
            command.add_argument("--citation", required=True)
            command.add_argument("--source-id", required=True)
    verify = commands.add_parser("verify", help="Verify source/image hashes and re-rendered pixels.")
    verify.add_argument("sidecar", type=Path)
    verify.add_argument("--pdf", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "index":
            data = index_pdf(args.pdf, args.output)
            result = {"output": str(args.output), "pages": len(data["pages"])}
        elif args.command == "render":
            result = {"output": str(preview_pdf(args.pdf, args.page, args.output, args.dpi))}
        elif args.command == "crop":
            data = crop_pdf(args.pdf, args.page, args.bbox, args.output, args.label, args.citation, args.source_id, args.dpi)
            result = {"output": str(args.output), "metadata": str(args.output) + ".json", "pixels": data["pixels"]}
        else:
            result = verify_crop(args.sidecar, args.pdf)
    except (ValueError, OSError, KeyError, TypeError, RuntimeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
