from fastapi import APIRouter
from ml.app.models.multimodal_rag import MultimodalRAG

router = APIRouter()
rag_pipeline = MultimodalRAG()

@router.post("/graphrag/build/")
def build_graph(data: dict):
    raw = data.get("raw_data")
    if not raw:
        return {"error": "Missing raw_data"}
    result = rag_pipeline.index_document(raw)
    return {"message": "GraphRAG indexing complete", **result}

@router.post("/graphrag/query/")
def query_graphrag(data: dict):
    question = data.get("question")
    if not question:
        return {"error": "Missing question"}
    result = rag_pipeline.query(question)
    return result