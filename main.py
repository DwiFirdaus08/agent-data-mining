from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import analyze

app = FastAPI(title="Agent Data Mining", version="1.0.0")

# (CORS Whitelist)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://jokitugas.bananaunion.web.id", "http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["POST", "GET", "OPTIONS"],
    allow_headers=["*"],
)

# Sambungkan Router
app.include_router(analyze.router)