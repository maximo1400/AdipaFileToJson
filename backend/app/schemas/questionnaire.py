from enum import Enum

from pydantic import BaseModel, Field, model_validator


class ItemType(str, Enum):
    """Supported assessment item types as specified in challenge requirements."""
    LIKERT_SCALE = "escala_likert"
    MULTIPLE_CHOICE = "seleccion_multiple"
    TRUE_FALSE = "verdadero_falso"
    OPEN_ENDED = "desarrollo"
    MATCHING = "emparejamiento"


class Option(BaseModel):
    """Assessment alternative / choice."""
    valor: int | str = Field(
        ...,
        description="Option identifier or score value (e.g. 0, 1, 'A', 'B', 'V', 'F')",
    )
    texto: str = Field(
        ...,
        description="Option descriptive text",
    )


class QuestionnaireItem(BaseModel):
    """Individual item or prompt within the questionnaire."""
    numero: int = Field(..., description="Sequential item number")
    enunciado: str = Field(..., description="Prompt or statement text")
    tipo: ItemType = Field(..., description="Item format type")
    alternativas: list[Option] = Field(
        default_factory=list,
        description="List of choices or answer options (empty for open-ended development items)",
    )
    respuesta_correcta: str | int | None = Field(
        default=None,
        description="Correct answer identifier if explicitly indicated in document, else null",
    )


class QuestionnaireResponse(BaseModel):
    """Standardized output schema matching challenge specification."""
    titulo: str = Field(..., description="Title of the questionnaire or test")
    idioma: str = Field(..., description="Detected ISO 639-1 language code (e.g., 'it', 'es', 'en')")
    total_items: int = Field(..., description="Total count of questionnaire items")
    items: list[QuestionnaireItem] = Field(..., description="List of structured items")

    @model_validator(mode="after")
    def sync_total_items(self):
        """Ensure total_items is strictly synchronized with the actual items count."""
        if self.items is not None:
            self.total_items = len(self.items)
        return self
