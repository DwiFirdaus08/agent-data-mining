# 1. Gunakan sistem operasi Linux dengan Python 3.9
FROM python:3.9-slim

# 2. Bikin folder kerja di dalam server
WORKDIR /app

# 3. Copy daftar library dan install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy semua file kodingan kita (main.py, routers, dll)
COPY . .

# 5. Jalankan aplikasi (Railway menyediakan PORT via env variable)
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-7860}