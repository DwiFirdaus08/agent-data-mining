from fastapi import APIRouter
from schemas.payload import AgentRequest
from services.mining_service import execute_ml_task

router = APIRouter()

# Ubah endpoint menjadi /process biar standar kayak teman-temanmu
@router.post("/process")
async def analyze_data(request: AgentRequest):
    try:
        # Panggil otak AI kita
        hasil_teks = execute_ml_task(request.payload)

        # Kembalikan response 200 OK (Sesuai Kontrak PDF Okta)
        return {
            "status": "success",
            "task_id": request.task_id,
            "data": {
                "result": hasil_teks,
                "file_url": None  # Diisi null karena kita mengembalikan TEKS matang, bebas cloud storage!
            },
            "message": "Pemrosesan Data Mining berhasil"
        }

    except Exception as e:
        # Kembalikan response 500 Error (Sesuai Kontrak PDF Okta)
        return {
            "status": "error",
            "task_id": request.task_id,
            "data": None,
            "message": f"Internal Server Error: {str(e)}"
        }