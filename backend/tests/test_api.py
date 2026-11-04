from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app
from app.schemas.questionnaire import (
    ItemType,
    Option,
    QuestionnaireItem,
    QuestionnaireResponse,
)

client = TestClient(app)


def test_health_check_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert "X-Process-Time" in response.headers
    data = response.json()
    assert data["status"] == "ok"
    assert "gemini_configured" in data


def test_extract_invalid_extension():
    # Attempt to upload unsupported .txt file
    response = client.post(
        "/api/extract",
        files={"file": ("invalid.txt", b"Test content", "text/plain")},
    )
    assert response.status_code == 400
    assert "Unsupported file format" in response.json()["detail"]


def test_extract_empty_file():
    # 0 bytes file
    response = client.post(
        "/api/extract",
        files={"file": ("test.docx", b"", "application/vnd.openxmlformats-officedocument.wordprocessingml.document")},
    )
    assert response.status_code == 400
    assert "empty" in response.json()["detail"]


@patch("app.api.routes.parse_document")
@patch("app.api.routes.extract_questionnaire_from_text")
def test_extract_successful_flow(mock_extract, mock_parse):
    # Mock parser and LLM to test HTTP response contract
    mock_parse.return_value = (".docx", "Sample extracted text")
    mock_extract.return_value = QuestionnaireResponse(
        titulo="Simulated Assessment",
        idioma="en",
        total_items=1,
        items=[
            QuestionnaireItem(
                numero=1,
                enunciado="Does everything work as expected?",
                tipo=ItemType.TRUE_FALSE,
                alternativas=[
                    Option(valor="V", texto="True"),
                    Option(valor="F", texto="False"),
                ],
                respuesta_correcta="V",
            )
        ],
    )

    fake_docx = b"PK\x03\x04..."
    response = client.post(
        "/api/extract",
        files={"file": ("test.docx", fake_docx, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["titulo"] == "Simulated Assessment"
    assert data["idioma"] == "en"
    assert data["total_items"] == 1
    assert data["items"][0]["respuesta_correcta"] == "V"
