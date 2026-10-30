from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings

from routers import posts, tags, sync

app = FastAPI(
    title="Unix34 API",
    version="1.0.0",
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(posts.router)
app.include_router(tags.router)
app.include_router(sync.router)

@app.get("/")
async def root():
    return {
        "status": "ok",
        "app": "Unix34 API",
        "version": "1.0.0",
        "environment": settings.app_env
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "debug": settings.debug}