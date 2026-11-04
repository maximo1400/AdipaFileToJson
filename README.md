# Questionnaire Digitizer & Extraction API

![CI Pipeline](https://github.com/maximo1400/AdipaFileToJson/actions/workflows/ci.yml/badge.svg)

An automated assessment digitization platform built for **Giunti Psychometrics** that transforms paper-based evaluation instruments (PDF, Word, Excel) into standardized, structured JSON using Python FastAPI, React, and Google Gemini AI.

---

## Live Deployments

- **Frontend Application (Vercel):** `[Your Vercel URL will be placed here]`
- **Backend API Docs (Render):** `[Your Render URL will be placed here]/docs`
- **Backend Health Check:** `[Your Render URL will be placed here]/api/health`

---

## Architecture & Technology Stack

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Backend** | Python 3.12 · FastAPI | High-performance asynchronous REST API |
| **Package Manager** | `uv` (Astral) | Lightning-fast virtual environment and dependency manager |
| **LLM & Extraction** | Google Gemini (`gemini-3.5-flash-lite` / Free Tier) | Structured JSON schema extraction via Google AI Studio |
| **Document Parsers** | `pdfplumber`, `pypdf`, `python-docx`, `openpyxl` | Text and tabular extraction from PDF, DOCX, and XLSX |
| **Validation** | Pydantic v2 | Strict schema adherence & synchronization |
| **Containerization** | Docker & Docker Compose | Multi-stage, reproducible production container |
| **Frontend** | React 18 · Vite · TypeScript · Tailwind CSS | Interactive assessment viewer & raw JSON inspector |
| **Testing** | Pytest · HTTPX | Unit & integration test coverage for schemas and parsers |

---

## Standardized JSON Output Schema

Output conforms strictly to the challenge specification:

```json
{
  "titulo": "Questionario di esempio",
  "idioma": "it",
  "total_items": 3,
  "items": [
    {
      "numero": 1,
      "enunciado": "Mi preoccupo eccessivamente per cose di poca importanza.",
      "tipo": "escala_likert",
      "alternativas": [
        { "valor": 0, "texto": "Mai" },
        { "valor": 1, "texto": "A volte" },
        { "valor": 2, "texto": "Spesso" },
        { "valor": 3, "texto": "Sempre" }
      ],
      "respuesta_correcta": null
    },
    {
      "numero": 2,
      "enunciado": "Quale numero completa la serie: 2, 4, 8, 16, ...?",
      "tipo": "seleccion_multiple",
      "alternativas": [
        { "valor": "A", "texto": "18" },
        { "valor": "B", "texto": "24" },
        { "valor": "C", "texto": "32" }
      ],
      "respuesta_correcta": "C"
    },
    {
      "numero": 3,
      "enunciado": "Descriva una situazione recente in cui si è sentito sotto pressione.",
      "tipo": "desarrollo",
      "alternativas": [],
      "respuesta_correcta": null
    }
  ]
}
```

### Supported Item Types (`tipo`)
- `escala_likert`: Graded rating scale (e.g., frequency, degree of agreement).
- `seleccion_multiple`: Standard multiple choice items with lettered or numbered options.
- `verdadero_falso`: Binary True/False or Yes/No items.
- `desarrollo`: Open-ended response questions (`alternativas: []`, `respuesta_correcta: null`).
- `emparejamiento`: Column or premise matching items.

---

## Environment Variables

### Backend (`backend/.env`)
| Variable | Description | Default |
| :--- | :--- | :--- |
| `GEMINI_API_KEY` | Google AI Studio Free Tier API key (**Required**) | `""` |
| `GEMINI_MODEL` | Gemini model identifier | `gemini-3.5-flash-lite` |
| `MAX_FILE_SIZE_MB` | Maximum allowed upload size in megabytes | `15` |
| `ALLOWED_ORIGINS` | Permitted CORS origins (JSON array string) | `["*"]` |

> **Obtain a Free Key:** Visit [Google AI Studio](https://aistudio.google.com/), sign in with a Google account, and click **"Get API key"** -> **"Create API key"**.

### Frontend (`frontend/.env.production`)
| Variable | Description |
| :--- | :--- |
| `VITE_API_URL` | Full URL to the deployed backend on Render (e.g., `https://your-backend.onrender.com`) |

---

## Examples Folder (`/examples`)

Synthetic evaluation files and their extracted outputs are included in [`/examples`](./examples):

1. **`cuestionario_personalita.docx` / `.json`**: Italian personality and stress assessment featuring Likert scale items and open development questions.
2. **`evaluacion_logica.pdf` / `.json`**: Spanish logical reasoning evaluation with multiple choice options (including correct answer keys) and True/False questions.
3. **`skills_assessment.xlsx` / `.json`**: English multi-row tabular questionnaire demonstrating spreadsheet parsing.

---

## Local Development Quickstart

### Prerequisites
- Python 3.12+
- [`uv`](https://github.com/astral-sh/uv) (recommended) or standard Python `venv`
- Node.js 18+ or [`Bun`](https://bun.sh/)
- Docker (optional)

### 1. Backend Setup with `uv`

```bash
cd backend

# Create .env from template
cp .env.example .env
# Edit .env and insert your GEMINI_API_KEY

# Install dependencies and sync virtual environment
uv sync

# Run test suite
uv run pytest

# Start development server
uv run uvicorn app.main:app --reload --port 8000
```
API Documentation will be live at `http://localhost:8000/docs`.

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install  # or: bun install

# Start development server
npm run dev  # or: bun run dev
```
The application interface will be live at `http://localhost:3000`.

### 3. Run with Docker Compose

To run the entire backend via container:
```bash
# From root directory
GEMINI_API_KEY="your-api-key" docker compose up --build
```

---

## Running Automated Tests

Run the Pytest suite to verify file validation, parsers, and schema enforcement:

```bash
cd backend
uv run pytest -v
```

All 12 unit tests validate:
- Strict output schema conformity with the Giunti challenge example.
- Validation and rejection of unauthorized item types.
- Auto-synchronization between `items` length and `total_items`.
- PDF, DOCX, and XLSX text extraction.
- HTTP endpoint validation: file size limit enforcement, empty file rejection, and unsupported extension rejection (400 Bad Request).

---

## Deployment Guide

### Deploying the Backend on Render (Free Tier)
1. Go to [Render Dashboard](https://dashboard.render.com/) and click **New > Web Service**.
2. Connect your GitHub repository: `maximo1400/AdipaFileToJson`.
3. In service settings:
   - **Root Directory:** `backend`
   - **Runtime:** **Docker** (Render will automatically detect `backend/Dockerfile`).
   - **Plan:** Free.
4. Under **Environment Variables**, add:
   - `GEMINI_API_KEY`: your Google AI Studio API key.
5. Click **Create Web Service**. Render will build and deploy the container in ~30 seconds.

### Deploying the Frontend on Vercel (Free Tier)
1. Go to [Vercel Dashboard](https://vercel.com/) and click **Add New > Project**.
2. Import the `AdipaFileToJson` repository.
3. In project settings:
   - **Root Directory:** select `frontend`.
   - **Framework Preset:** Vite.
4. Under **Environment Variables**, add:
   - `VITE_API_URL`: `https://<your-render-service-name>.onrender.com`
5. Click **Deploy**. Vercel will build and publish your React application.

---

## Assumptions & Design Decisions
- **Free Tier Resilience:** Gemini 3.5 Flash is configured through official `google-genai` SDK with native Structured Outputs (`response_schema`), ensuring zero hallucinated schemas and zero cost.
- **Client Fallback:** The frontend permits entering a custom Gemini API key for testers who wish to use their personal quota without reconfiguring backend environment variables.
- **Render Inactivity:** On Render's Free tier, the service spins down after 15 minutes of inactivity; the initial request may take ~30-45 seconds to warm up.

---

