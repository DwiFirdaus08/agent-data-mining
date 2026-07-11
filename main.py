from fastapi import FastAPI
from routers import analyze

# Inisialisasi Aplikasi Utama
app = FastAPI(
    title="Agent Data Mining API",
    description="API untuk mengeksekusi alur CRISP-DM dan Machine Learning (Clean Architecture)",
    version="1.0.0"
)

# Sambungkan (Mount) router yang sudah kita buat
app.include_router(analyze.router)