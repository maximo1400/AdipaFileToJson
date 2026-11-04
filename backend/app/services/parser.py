import io

import docx
import openpyxl
import pdfplumber
import pypdf


class DocumentParsingError(Exception):
    """Raised when an error occurs while extracting text from an uploaded document."""


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Extracts text and structured tables from a PDF document.
    Uses pdfplumber as the primary parser and pypdf as a fallback.
    """
    extracted_parts = []
    try:
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page_num, page in enumerate(pdf.pages, start=1):
                extracted_parts.append(f"--- Page {page_num} ---")
                
                # Extract tabular data to preserve question/option layouts
                tables = page.extract_tables()
                if tables:
                    for table in tables:
                        table_rows = []
                        for row in table:
                            cleaned_row = [str(cell).strip() if cell is not None else "" for cell in row]
                            if any(cleaned_row):
                                table_rows.append(" | ".join(cleaned_row))
                        if table_rows:
                            extracted_parts.append("[TABLE]")
                            extracted_parts.append("\n".join(table_rows))
                            extracted_parts.append("[/TABLE]")
                
                # Extract general text
                page_text = page.extract_text()
                if page_text:
                    extracted_parts.append(page_text.strip())
    except Exception as e:
        # Fallback to pypdf if pdfplumber encounters an issue
        try:
            reader = pypdf.PdfReader(io.BytesIO(file_bytes))
            for page_num, page in enumerate(reader.pages, start=1):
                text = page.extract_text()
                if text:
                    extracted_parts.append(f"--- Page {page_num} ---")
                    extracted_parts.append(text.strip())
        except Exception as inner_e:
            raise DocumentParsingError(f"Failed to read PDF document: {e!s} / {inner_e!s}")

    full_text = "\n\n".join(extracted_parts).strip()
    if not full_text:
        raise DocumentParsingError("The PDF document is empty or contains only non-digitalized scanned images.")
    return full_text


def extract_text_from_docx(file_bytes: bytes) -> str:
    """
    Extracts text and tables from a Microsoft Word (.docx) document.
    """
    try:
        doc = docx.Document(io.BytesIO(file_bytes))
        extracted_parts = []

        # Extract paragraphs
        for para in doc.paragraphs:
            text = para.text.strip()
            if text:
                extracted_parts.append(text)

        # Extract tables
        for table in doc.tables:
            table_rows = []
            for row in table.rows:
                row_cells = [cell.text.strip() for cell in row.cells]
                if any(row_cells):
                    table_rows.append(" | ".join(row_cells))
            if table_rows:
                extracted_parts.append("[TABLE]")
                extracted_parts.append("\n".join(table_rows))
                extracted_parts.append("[/TABLE]")

        full_text = "\n\n".join(extracted_parts).strip()
        if not full_text:
            raise DocumentParsingError("The Word document (.docx) does not contain readable text.")
        return full_text
    except DocumentParsingError:
        raise
    except Exception as e:
        raise DocumentParsingError(f"Error parsing Word document (.docx): {e!s}")


def extract_text_from_xlsx(file_bytes: bytes) -> str:
    """
    Extracts contents from an Excel workbook (.xlsx) across all sheets and rows.
    """
    try:
        workbook = openpyxl.load_workbook(io.BytesIO(file_bytes), data_only=True)
        extracted_parts = []

        for sheet_name in workbook.sheetnames:
            sheet = workbook[sheet_name]
            extracted_parts.append(f"--- Sheet: {sheet_name} ---")
            
            sheet_rows = []
            for row in sheet.iter_rows(values_only=True):
                cells = [str(c).strip() for c in row if c is not None and str(c).strip()]
                if cells:
                    sheet_rows.append(" | ".join(cells))
            
            if sheet_rows:
                extracted_parts.append("\n".join(sheet_rows))

        full_text = "\n\n".join(extracted_parts).strip()
        if not full_text:
            raise DocumentParsingError("The Excel spreadsheet (.xlsx) does not contain data cells.")
        return full_text
    except DocumentParsingError:
        raise
    except Exception as e:
        raise DocumentParsingError(f"Error parsing Excel spreadsheet (.xlsx): {e!s}")


def parse_document(filename: str, file_bytes: bytes) -> tuple[str, str]:
    """
    Identifies document type by extension and extracts formatted text.
    Returns a tuple of (extension, extracted_text).
    """
    filename_lower = filename.lower()
    if filename_lower.endswith(".pdf"):
        return ".pdf", extract_text_from_pdf(file_bytes)
    elif filename_lower.endswith(".docx"):
        return ".docx", extract_text_from_docx(file_bytes)
    elif filename_lower.endswith(".xlsx"):
        return ".xlsx", extract_text_from_xlsx(file_bytes)
    else:
        raise DocumentParsingError(
            f"Unsupported file format for '{filename}'. Only .pdf, .docx, and .xlsx files are allowed."
        )
