from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class DataPayload(BaseModel):
    raw: List[Dict[str, Any]]
    format: str
    columns: List[str]

class ParamsPayload(BaseModel):
    n_clusters: Optional[int] = None
    min_support: Optional[float] = None
    target_column: Optional[str] = None
    features: List[str]

class ContextPayload(BaseModel):
    user_request: Optional[str] = None

class MiningRequest(BaseModel):
    task_id: str
    task_type: str
    source: str
    data: DataPayload
    params: ParamsPayload
    context: ContextPayload