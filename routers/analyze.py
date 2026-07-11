from fastapi import APIRouter
import pandas as pd

# Import dari folder kita sendiri
from schemas.payload import MiningRequest
from services.mining_service import execute_ml_task

# Buat router khusus untuk fitur analisis
router = APIRouter()

@router.post("/api/v1/analyze")
async def analyze_data(request: MiningRequest):
    try:
        # Ubah JSON jadi tabel Pandas
        df = pd.DataFrame(request.data.raw)

        # Lempar datanya ke folder services untuk dimasak oleh AI
        data_kembali, kesimpulan, model_pakai = execute_ml_task(request, df)

        # Kembalikan response
        return {
            "task_id": request.task_id,
            "status": "success",
            "agent": "data_mining",
            "task_type": request.task_type,
            "result": {
                "summary": kesimpulan,
                "output_data": data_kembali 
            },
            "metrics": {
                "model_used": model_pakai,
                "processing_time_ms": 0
            }
        }

    except Exception as e:
        return {
            "task_id": request.task_id,
            "status": "error",
            "agent": "data_mining",
            "task_type": request.task_type,
            "error_message": f"Terjadi kesalahan saat memproses data: {str(e)}"
        }