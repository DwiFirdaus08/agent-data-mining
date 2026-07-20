from pydantic import BaseModel
from typing import Optional

class PayloadData(BaseModel):
    url: Optional[str] = ""
    keyword: Optional[str] = ""
    raw_text: Optional[str] = ""

class Metadata(BaseModel):
    sender: Optional[str] = "orchestrator"
    timestamp: Optional[int] = 0

class AgentRequest(BaseModel):
    task_id: str
    agent_type: str
    payload: PayloadData
    metadata: Metadata