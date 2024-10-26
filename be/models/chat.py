from typing import Optional

from pydantic import BaseModel


class ChatRequest(BaseModel):
    request_id: str
    model: str
    messages: list[dict]
    stream: Optional[bool] = True


class AbortRequest(BaseModel):
    request_id: str
