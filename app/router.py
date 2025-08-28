from fastapi import APIRouter, HTTPException
from app.models.schemas import QueryRequest, AnswerResponse
from app.services.retriever import hybrid_retrieve
from app.services.llm_client import generate_answer
from app.services.citation import format_citations

router = APIRouter()


@router.post("/query", response_model=AnswerResponse)
async def query_endpoint(req: QueryRequest):
    try:
        # Retrieve relevant documents
        docs = await hybrid_retrieve(req.query, top_k=5)

        if not docs:
            raise HTTPException(status_code=404, detail="No relevant information found")

        # Generate answer with context
        answer = await generate_answer(req.query, docs)

        # Format citations
        citations = format_citations(docs)

        return AnswerResponse(answer=answer, citations=citations)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")


@router.get("/health")
async def health_check():
    return {"status": "healthy"}
