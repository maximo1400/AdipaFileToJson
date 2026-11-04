from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.config import get_settings

settings = get_settings()

app = FastAPI(
    title="Giunti Psychometrics - Questionnaire Parser API",
    description=(
        "Automated digitization API converting questionnaires and psychometric assessments "
        "from PDF, Word (.docx), and Excel (.xlsx) files into standardized JSON."
    ),
    version=settings.version,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS configuration allowing cross-origin requests from frontend (Vercel, local dev, etc.)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(router, prefix="/api")


@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Welcome to the Questionnaire Parser API",
        "docs": "/docs",
        "health": "/api/health",
    }


def main():
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()
