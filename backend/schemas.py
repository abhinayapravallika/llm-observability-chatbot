from pydantic import BaseModel
from typing import Optional


class ChatRequest(BaseModel):

    message: str

    session_id: Optional[str] = None


class ChatResponse(BaseModel):

    session_id: str

    response: str


class InferenceLogSchema(BaseModel):

    session_id: str

    model: str

    provider: str

    latency: int

    input_tokens: int

    output_tokens: int

    status: str

    input_preview: str

    output_preview: str