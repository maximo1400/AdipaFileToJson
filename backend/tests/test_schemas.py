import pytest
from pydantic import ValidationError

from app.schemas.questionnaire import (
    ItemType,
    Option,
    QuestionnaireItem,
    QuestionnaireResponse,
)


def test_schema_conforms_to_specification_example():
    """Validates that schema output exactly matches the challenge specification."""
    data = {
        "titulo": "Questionario di esempio",
        "idioma": "it",
        "total_items": 3,
        "items": [
            {
                "numero": 1,
                "enunciado": "Mi preoccupo eccessivamente per cose di poca importanza.",
                "tipo": "escala_likert",
                "alternativas": [
                    {"valor": 0, "texto": "Mai"},
                    {"valor": 1, "texto": "A volte"},
                    {"valor": 2, "texto": "Spesso"},
                    {"valor": 3, "texto": "Sempre"},
                ],
                "respuesta_correcta": None,
            },
            {
                "numero": 2,
                "enunciado": "Quale numero completa la serie: 2, 4, 8, 16, ...?",
                "tipo": "seleccion_multiple",
                "alternativas": [
                    {"valor": "A", "texto": "18"},
                    {"valor": "B", "texto": "24"},
                    {"valor": "C", "texto": "32"},
                ],
                "respuesta_correcta": "C",
            },
            {
                "numero": 3,
                "enunciado": "Descriva una situazione recente in cui si è sentito sotto pressione.",
                "tipo": "desarrollo",
                "alternativas": [],
                "respuesta_correcta": None,
            },
        ],
    }

    questionnaire = QuestionnaireResponse.model_validate(data)
    assert questionnaire.titulo == "Questionario di esempio"
    assert questionnaire.idioma == "it"
    assert questionnaire.total_items == 3
    assert len(questionnaire.items) == 3
    assert questionnaire.items[0].tipo == ItemType.LIKERT_SCALE
    assert questionnaire.items[1].respuesta_correcta == "C"
    assert questionnaire.items[2].alternativas == []


def test_item_type_enum_values():
    """Verifies all required item types are supported."""
    assert ItemType.LIKERT_SCALE.value == "escala_likert"
    assert ItemType.MULTIPLE_CHOICE.value == "seleccion_multiple"
    assert ItemType.TRUE_FALSE.value == "verdadero_falso"
    assert ItemType.OPEN_ENDED.value == "desarrollo"
    assert ItemType.MATCHING.value == "emparejamiento"


def test_schema_rejects_invalid_item_type():
    """Ensures unknown types trigger validation errors."""
    with pytest.raises(ValidationError):
        QuestionnaireItem(
            numero=1,
            enunciado="Sample statement",
            tipo="unknown_type",
            alternativas=[],
        )


def test_total_items_auto_sync():
    """Ensures total_items synchronizes with actual item array length."""
    questionnaire = QuestionnaireResponse(
        titulo="Sync Test",
        idioma="en",
        total_items=999,  # Intentional discrepancy
        items=[
            QuestionnaireItem(
                numero=1,
                enunciado="Is this a true statement?",
                tipo=ItemType.TRUE_FALSE,
                alternativas=[
                    Option(valor="V", texto="True"),
                    Option(valor="F", texto="False"),
                ],
                respuesta_correcta="V",
            )
        ],
    )
    assert questionnaire.total_items == 1
