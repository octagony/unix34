from fastapi import FastAPI

app = FastAPI(
	title="Unix34 API"
	version="0.0.1"
	docs_url="/docs" if settings.debug else None,
  redoc_url="/redoc" if settings.debug else None
)