import io

import docx
import openpyxl
import pytest

from app.services.parser import (
    DocumentParsingError,
    extract_text_from_docx,
    extract_text_from_xlsx,
    parse_document,
)


def create_sample_docx_bytes() -> bytes:
    doc = docx.Document()
    doc.add_heading("Personality Assessment", level=1)
    doc.add_paragraph("1. I worry about minor things.")
    table = doc.add_table(rows=1, cols=2)
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = "Option"
    hdr_cells[1].text = "Score"
    buf = io.BytesIO()
    doc.save(buf)
    return buf.getvalue()


def create_sample_xlsx_bytes() -> bytes:
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Questions"
    ws.append(["ID", "Prompt", "Type", "Options"])
    ws.append([1, "What is the capital of Italy?", "seleccion_multiple", "A: Rome, B: Milan"])
    buf = io.BytesIO()
    wb.save(buf)
    return buf.getvalue()


def test_extract_text_from_docx():
    docx_bytes = create_sample_docx_bytes()
    text = extract_text_from_docx(docx_bytes)
    assert "Personality Assessment" in text
    assert "1. I worry about minor things." in text
    assert "Option" in text


def test_extract_text_from_xlsx():
    xlsx_bytes = create_sample_xlsx_bytes()
    text = extract_text_from_xlsx(xlsx_bytes)
    assert "--- Sheet: Questions ---" in text
    assert "capital of Italy" in text


def test_parse_document_router_and_invalid_extension():
    docx_bytes = create_sample_docx_bytes()
    ext, text = parse_document("my_test.docx", docx_bytes)
    assert ext == ".docx"
    assert "Personality Assessment" in text

    # Unsupported format
    with pytest.raises(DocumentParsingError) as exc_info:
        parse_document("document.txt", b"hello world")
    assert "Unsupported file format" in str(exc_info.value)


def test_empty_docx_raises_error():
    doc = docx.Document()
    buf = io.BytesIO()
    doc.save(buf)
    with pytest.raises(DocumentParsingError):
        extract_text_from_docx(buf.getvalue())
