from pydantic import BaseModel
from typing import Optional



class ChatRequest(BaseModel):
    request_id: str
    model: str
    messages: list[dict]
    stream: Optional[bool] = True


class AbortRequest(BaseModel):
    request_id: str