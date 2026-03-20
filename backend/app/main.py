from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes_exams import router as exams_router
from app.api.routes_questions import router as questions_router
from app.api.routes_stats import router as stats_router
from app.api.routes_units import router as units_router

app = FastAPI(
    title="Active Recall Quiz API",
    version="0.1.0",
    description="Markdown-based study and exam backend for preparing written exams.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(units_router, prefix="/api")
app.include_router(questions_router, prefix="/api")
app.include_router(exams_router, prefix="/api")
app.include_router(stats_router, prefix="/api")


@app.get("/health")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
