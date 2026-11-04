import logging
import os
from typing import Annotated

from fastapi import APIRouter, File, HTTPException, UploadFile, status

from app.config import get_settings
from app.schemas.questionnaire import QuestionnaireResponse
from app.services.extractor import LLMExtractionError, extract_questionnaire_from_text
from app.services.parser import DocumentParsingError, parse_document

logger = logging.getLogger(__name__)

# Use RFC 9110 compliant status code or fallback
UNPROCESSABLE_STATUS = 422
router = APIRouter()


@router.get("/health", tags=["Health"])
def health_check():
    """Service health check endpoint for monitoring and uptime probes."""
    settings = get_settings()
    has_api_key = bool(settings.gemini_api_key.strip())
    return {
        "status": "ok",
        "app": settings.app_name,
        "version": settings.version,
        "gemini_configured": has_api_key,
        "model": settings.effective_model,
    }


@router.post(
    "/extract",
    response_model=QuestionnaireResponse,
    status_code=status.HTTP_200_OK,
    tags=["Extraction"],
    summary="Process assessment file and return standardized questionnaire JSON",
    responses={
        200: {"description": "Questionnaire successfully extracted"},
        400: {"description": "Invalid file format or empty payload"},
        413: {"description": "Uploaded file exceeds maximum permitted size"},
        422: {"description": "Unprocessable document or no questionnaire items detected"},
        500: {"description": "Internal server or LLM service failure"},
    },
)
async def extract_questionnaire(
    file: Annotated[
        UploadFile,
        File(description="Assessment document (.pdf, .docx, or .xlsx)"),
    ],
):
    settings = get_settings()

    # 1. Validate filename and extension
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Filename was not provided.",
        )

    _, ext = os.path.splitext(file.filename.lower())
    if ext not in settings.allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Unsupported file format: '{ext}'. "
                f"Allowed formats: {', '.join(settings.allowed_extensions)}"
            ),
        )

    # 2. Read bytes and check size
    try:
        file_bytes = await file.read()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to read uploaded file: {e!s}",
        )

    max_bytes = settings.max_file_size_mb * 1024 * 1024
    if len(file_bytes) > max_bytes:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=(
                f"File size ({round(len(file_bytes) / (1024 * 1024), 2)} MB) "
                f"exceeds maximum allowed limit of {settings.max_file_size_mb} MB."
            ),
        )

    if len(file_bytes) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The uploaded file is empty (0 bytes).",
        )

    # 3. Parse text from document
    logger.info(f"Processing upload '{file.filename}' ({len(file_bytes) / 1024:.1f} KB)")
    try:
        _, extracted_text = parse_document(file.filename, file_bytes)
        logger.info(f"Parsed {len(extracted_text)} characters from '{file.filename}'")
    except DocumentParsingError as e:
        logger.warning(f"Failed to parse document '{file.filename}': {e!s}")
        raise HTTPException(
            status_code=UNPROCESSABLE_STATUS,
            detail=str(e),
        )
    except Exception as e:
        logger.error(f"Unexpected error parsing '{file.filename}': {e!s}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Document parsing error: {e!s}",
        )

    # 4. Structured extraction via Gemini LLM
    try:
        result = extract_questionnaire_from_text(
            extracted_text=extracted_text,
        )
        logger.info(
            f"Successfully digitized '{result.titulo}': {result.total_items} items (lang: '{result.idioma}')"
        )
        return result
    except LLMExtractionError as e:
        logger.warning(f"LLM extraction error for '{file.filename}': {e!s}")
        raise HTTPException(
            status_code=UNPROCESSABLE_STATUS,
            detail=str(e),
        )
    except Exception as e:
        logger.error(f"Unexpected LLM extraction failure for '{file.filename}': {e!s}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected extraction failure: {e!s}",
        )
