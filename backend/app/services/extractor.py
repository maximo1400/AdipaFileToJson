import logging

from google import genai
from google.genai import types
from google.genai.errors import APIError

from app.config import get_settings
from app.schemas.questionnaire import QuestionnaireResponse

logger = logging.getLogger(__name__)


class LLMExtractionError(Exception):
    """Raised when structured LLM extraction fails."""


SYSTEM_INSTRUCTION = """
You are an expert psychometrician and AI data extractor specializing in converting assessment questionnaires and psychological tests into standardized JSON formats.

Your task is to analyze the extracted document text (from PDF, Word, or Excel) and structure all assessment items into the required JSON schema.

Schema requirements:
1. 'titulo': Detect or infer the title of the questionnaire or test. If no explicit title exists, generate a concise descriptive title based on content.
2. 'idioma': Detect the primary language using standard ISO 639-1 code (e.g., 'it' for Italian, 'es' for Spanish, 'en' for English).
3. 'total_items': Total count of items found in the questionnaire.
4. 'items': List of structured items in sequential order. Each item must contain:
   - 'numero': Item number (1, 2, 3...).
   - 'enunciado': The question, prompt, or statement text.
   - 'tipo': Must be strictly one of:
     * 'escala_likert': Statements rated on an agreement or frequency scale (e.g., Never, Sometimes, Often, Always; 1 to 5).
     * 'seleccion_multiple': Multiple choice questions with distinct alternatives (A, B, C, D...).
     * 'verdadero_falso': Binary items with True/False, Yes/No, or Verdadero/Falso choices.
     * 'desarrollo': Open-ended development questions without predefined options ('alternativas' must be an empty list []).
     * 'emparejamiento': Matching items pairing elements between premises or columns.
   - 'alternativas': List of objects {'valor': int or str, 'texto': str}. For 'desarrollo' items, this must be [].
   - 'respuesta_correcta': If the document explicitly provides or marks the correct answer (via answer key, asterisk, bolding, or note), include its 'valor'. Otherwise, set to null.

5. If the document does not contain any questions, questionnaire items, or psychological test content, return 'total_items': 0 and 'items': [].
"""


def extract_questionnaire_from_text(
    extracted_text: str,
    api_key: str | None = None,
    model_name: str | None = None,
) -> QuestionnaireResponse:
    """
    Submits extracted document text to the Gemini API utilizing Structured Outputs
    conforming directly to the QuestionnaireResponse schema.
    """
    settings = get_settings()
    effective_api_key = api_key or settings.gemini_api_key
    effective_model = model_name or settings.effective_model

    if not effective_api_key:
        raise LLMExtractionError(
            "GEMINI_API_KEY is not configured. Please provide it in the request or environment variables."
        )

    try:
        client = genai.Client(api_key=effective_api_key)
        prompt = (
            f"Analyze the following document text and digitize the questionnaire items:\n\n"
            f"--- BEGIN DOCUMENT ---\n"
            f"{extracted_text}\n"
            f"--- END DOCUMENT ---"
        )

        response = client.models.generate_content(
            model=effective_model,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                response_mime_type="application/json",
                response_schema=QuestionnaireResponse,
                temperature=0.1,
            ),
        )

        if not response.text:
            raise LLMExtractionError(f"Model '{effective_model}' returned an empty response.")

        result = QuestionnaireResponse.model_validate_json(response.text)

        # Explicit validation for questionnaire presence
        if result.total_items == 0 or len(result.items) == 0:
            raise LLMExtractionError(
                "No questionnaire items or questions were detected in the processed document."
            )

        return result

    except APIError as e:
        logger.error(f"Gemini API error on model '{effective_model}': {e}")
        raise LLMExtractionError(f"Gemini API error: {e!s}")
    except LLMExtractionError:
        raise
    except Exception as e:
        logger.exception("Unexpected error during LLM extraction")
        raise LLMExtractionError(f"Extraction failed: {e!s}")
