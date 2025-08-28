from fastapi import FastAPI
from app.router import router

app = FastAPI(title="Perplexity MVP")

app.include_router(router, prefix="/api")
