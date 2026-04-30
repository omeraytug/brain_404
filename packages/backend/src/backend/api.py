from fastapi import FastAPI, HTTPException
from backend.model import chat
from backend.schemas import (
    ChatResponse,
    ChatRequest,
    DocumentListResponse,
    DocumentResponse,
)
from rag.retrieval import get_document, list_document_names

app = FastAPI()


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/ask")
async def ask(query: ChatRequest) -> ChatResponse:
    result = await chat(query.question)

    return result


@app.post("/ingest")
async def ingest():
    return {
        "status": "stub",
        "endpoint": "/ingest",
        "detail": "Not wired to vector ingest; swap to pipeline when ready.",
    }


@app.get("/documents", response_model=DocumentListResponse)
async def list_documents(include_extension: bool = False) -> DocumentListResponse:
    return DocumentListResponse(
        documents=list_document_names(include_extension=include_extension)
    )


@app.get("/documents/{document_name}", response_model=DocumentResponse)
async def get_document_by_name(document_name: str) -> DocumentResponse:
    normalized = document_name if document_name.endswith(".md") else f"{document_name}.md"
    doc = get_document(normalized)
    if doc is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return DocumentResponse(**doc)
