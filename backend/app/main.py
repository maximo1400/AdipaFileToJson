import logging
import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.config import get_settings

# Configure application-wide structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("app")

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


@app.middleware("http")
async def log_requests_and_timing(request: Request, call_next):
    """
    Middleware that measures request execution time, injects the X-Process-Time
    header, and outputs structured access logs for observability.
    """
    start_time = time.perf_counter()
    response = await call_next(request)
    duration = time.perf_counter() - start_time

    response.headers["X-Process-Time"] = f"{duration:.3f}s"
    logger.info(
        f"{request.method} {request.url.path} completed in {duration:.3f}s (status: {response.status_code})"
    )
    return response


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
