#!/usr/bin/env python3
"""Build the downloadable Mini PRD DOCX from docs/mini-prd.md using stdlib only."""

from pathlib import Path
import re
import zipfile
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs" / "mini-prd.md"
OUTPUT = ROOT / "public" / "mini-prd.docx"
W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
CT_NS = "http://schemas.openxmlformats.org/package/2006/content-types"
ET.register_namespace("w", W_NS)
ET.register_namespace("r", R_NS)
ET.register_namespace("", REL_NS)


def tag(name: str) -> str:
    return f"{{{W_NS}}}{name}"


def text_run(parent: ET.Element, text: str, bold: bool = False) -> None:
    run = ET.SubElement(parent, tag("r"))
    if bold:
        props = ET.SubElement(run, tag("rPr"))
        ET.SubElement(props, tag("b"))
    node = ET.SubElement(run, tag("t"))
    if text.startswith(" ") or text.endswith(" ") or "  " in text:
        node.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    node.text = text


def paragraph(parent: ET.Element, text: str, style: str = "Normal") -> ET.Element:
    p = ET.SubElement(parent, tag("p"))
    ppr = ET.SubElement(p, tag("pPr"))
    ET.SubElement(ppr, tag("pStyle"), {tag("val"): style})
    if style == "ListBullet":
        ET.SubElement(
            ppr,
            tag("ind"),
            {tag("left"): "420", tag("hanging"): "210"},
        )
    for part in re.split(r"(\*\*.*?\*\*)", text):
        if not part:
            continue
        if part.startswith("**") and part.endswith("**"):
            text_run(p, part[2:-2], bold=True)
        else:
            text_run(p, part)
    return p


def add_table(parent: ET.Element, rows: list[list[str]]) -> None:
    if not rows:
        return
    tbl = ET.SubElement(parent, tag("tbl"))
    tbl_pr = ET.SubElement(tbl, tag("tblPr"))
    ET.SubElement(tbl_pr, tag("tblStyle"), {tag("val"): "TableGrid"})
    borders = ET.SubElement(tbl_pr, tag("tblBorders"))
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        ET.SubElement(
            borders,
            tag(edge),
            {tag("val"): "single", tag("sz"): "4", tag("space"): "0", tag("color"): "D8DCE7"},
        )
    margins = ET.SubElement(tbl_pr, tag("tblCellMar"))
    for edge in ("top", "start", "bottom", "end"):
        ET.SubElement(margins, tag(edge), {tag("w"): "90", tag("type"): "dxa"})

    column_count = max(len(row) for row in rows)
    grid = ET.SubElement(tbl, tag("tblGrid"))
    for _ in range(column_count):
        ET.SubElement(grid, tag("gridCol"), {tag("w"): str(9000 // column_count)})

    for row_index, row_data in enumerate(rows):
        row = ET.SubElement(tbl, tag("tr"))
        for cell_index in range(column_count):
            cell = ET.SubElement(row, tag("tc"))
            tc_pr = ET.SubElement(cell, tag("tcPr"))
            if row_index == 0:
                ET.SubElement(tc_pr, tag("shd"), {tag("fill"): "EEEAF9", tag("val"): "clear"})
            p = ET.SubElement(cell, tag("p"))
            ppr = ET.SubElement(p, tag("pPr"))
            ET.SubElement(ppr, tag("spacing"), {tag("after"): "35", tag("line"): "235", tag("lineRule"): "auto"})
            value = row_data[cell_index].strip() if cell_index < len(row_data) else ""
            for part in re.split(r"(\*\*.*?\*\*)", value):
                if not part:
                    continue
                if part.startswith("**") and part.endswith("**"):
                    text_run(p, part[2:-2], bold=True)
                else:
                    text_run(p, part, bold=(row_index == 0))


def parse_table_line(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def build_document(markdown: str) -> bytes:
    document = ET.Element(tag("document"))
    body = ET.SubElement(document, tag("body"))
    lines = markdown.splitlines()
    index = 0
    while index < len(lines):
        line = lines[index].strip()
        if not line or line == "---":
            index += 1
            continue
        if line.startswith("|"):
            table_rows: list[list[str]] = []
            while index < len(lines) and lines[index].strip().startswith("|"):
                cells = parse_table_line(lines[index])
                if not all(re.fullmatch(r":?-{3,}:?", cell.replace(" ", "")) for cell in cells):
                    table_rows.append(cells)
                index += 1
            add_table(body, table_rows)
            continue
        if line.startswith("# "):
            paragraph(body, line[2:].strip(), "Title")
        elif line.startswith("## "):
            paragraph(body, line[3:].strip(), "Heading1")
        elif line.startswith("### "):
            paragraph(body, line[4:].strip(), "Heading2")
        elif line.startswith("- "):
            paragraph(body, "• " + line[2:].strip(), "ListBullet")
        else:
            paragraph(body, line)
        index += 1

    sect = ET.SubElement(body, tag("sectPr"))
    ET.SubElement(sect, tag("pgSz"), {tag("w"): "11906", tag("h"): "16838"})
    ET.SubElement(
        sect,
        tag("pgMar"),
        {
            tag("top"): "900",
            tag("right"): "950",
            tag("bottom"): "900",
            tag("left"): "950",
            tag("header"): "500",
            tag("footer"): "500",
            tag("gutter"): "0",
        },
    )
    return ET.tostring(document, encoding="utf-8", xml_declaration=True)


def styles_xml() -> bytes:
    styles = ET.Element(tag("styles"))
    defaults = ET.SubElement(styles, tag("docDefaults"))
    rpr_default = ET.SubElement(defaults, tag("rPrDefault"))
    rpr = ET.SubElement(rpr_default, tag("rPr"))
    ET.SubElement(rpr, tag("rFonts"), {tag("ascii"): "Aptos", tag("hAnsi"): "Aptos", tag("eastAsia"): "Aptos"})
    ET.SubElement(rpr, tag("sz"), {tag("val"): "21"})
    ppr_default = ET.SubElement(defaults, tag("pPrDefault"))
    ppr = ET.SubElement(ppr_default, tag("pPr"))
    ET.SubElement(ppr, tag("spacing"), {tag("after"): "125", tag("line"): "285", tag("lineRule"): "auto"})

    style_specs = [
        ("Normal", "paragraph", None, 21, "283044", False),
        ("Title", "paragraph", None, 46, "332666", True),
        ("Heading1", "paragraph", "Normal", 30, "4B35A8", True),
        ("Heading2", "paragraph", "Normal", 24, "31245F", True),
        ("ListBullet", "paragraph", "Normal", 21, "283044", False),
        ("TableGrid", "table", None, 21, "283044", False),
    ]
    for name, kind, based_on, size, color, bold in style_specs:
        style = ET.SubElement(styles, tag("style"), {tag("type"): kind, tag("styleId"): name})
        ET.SubElement(style, tag("name"), {tag("val"): name})
        if based_on:
            ET.SubElement(style, tag("basedOn"), {tag("val"): based_on})
        if name == "Normal":
            ET.SubElement(style, tag("qFormat"))
        if kind == "paragraph":
            style_ppr = ET.SubElement(style, tag("pPr"))
            if name.startswith("Heading"):
                ET.SubElement(style_ppr, tag("keepNext"))
                ET.SubElement(style_ppr, tag("spacing"), {tag("before"): "250", tag("after"): "100"})
            if name == "Title":
                ET.SubElement(style_ppr, tag("spacing"), {tag("before"): "180", tag("after"): "220"})
            style_rpr = ET.SubElement(style, tag("rPr"))
            ET.SubElement(style_rpr, tag("rFonts"), {tag("ascii"): "Aptos Display" if name != "Normal" else "Aptos", tag("hAnsi"): "Aptos Display" if name != "Normal" else "Aptos"})
            if bold:
                ET.SubElement(style_rpr, tag("b"))
            ET.SubElement(style_rpr, tag("color"), {tag("val"): color})
            ET.SubElement(style_rpr, tag("sz"), {tag("val"): str(size)})
    return ET.tostring(styles, encoding="utf-8", xml_declaration=True)


def write_docx(document_xml: bytes) -> None:
    content_types = ET.Element(f"{{{CT_NS}}}Types")
    ET.SubElement(content_types, f"{{{CT_NS}}}Default", {"Extension": "rels", "ContentType": "application/vnd.openxmlformats-package.relationships+xml"})
    ET.SubElement(content_types, f"{{{CT_NS}}}Default", {"Extension": "xml", "ContentType": "application/xml"})
    ET.SubElement(content_types, f"{{{CT_NS}}}Override", {"PartName": "/word/document.xml", "ContentType": "application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"})
    ET.SubElement(content_types, f"{{{CT_NS}}}Override", {"PartName": "/word/styles.xml", "ContentType": "application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"})

    rels = ET.Element(f"{{{REL_NS}}}Relationships")
    ET.SubElement(rels, f"{{{REL_NS}}}Relationship", {"Id": "rId1", "Type": "http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument", "Target": "word/document.xml"})

    doc_rels = ET.Element(f"{{{REL_NS}}}Relationships")
    ET.SubElement(doc_rels, f"{{{REL_NS}}}Relationship", {"Id": "rId1", "Type": "http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles", "Target": "styles.xml"})

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(OUTPUT, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("[Content_Types].xml", ET.tostring(content_types, encoding="utf-8", xml_declaration=True))
        archive.writestr("_rels/.rels", ET.tostring(rels, encoding="utf-8", xml_declaration=True))
        archive.writestr("word/document.xml", document_xml)
        archive.writestr("word/styles.xml", styles_xml())
        archive.writestr("word/_rels/document.xml.rels", ET.tostring(doc_rels, encoding="utf-8", xml_declaration=True))


if __name__ == "__main__":
    write_docx(build_document(SOURCE.read_text(encoding="utf-8")))
    print(f"Created {OUTPUT}")
