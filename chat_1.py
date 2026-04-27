from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=1000)
    language: str = Field(default="en", pattern="^(en|tr|ar|de|ru)$")
    session_id: str | None = Field(default=None)


class SourceDocument(BaseModel):
    content: str
    source: str


class ChatResponse(BaseModel):
    answer: str
    sources: list[SourceDocument]
    language: str
    session_id: str | None
