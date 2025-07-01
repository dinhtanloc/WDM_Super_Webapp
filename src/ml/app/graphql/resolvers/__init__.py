# app/graphql/resolvers/__init__.py
from ml.app.models.multimodal_rag import MultimodalRAG

rag_pipeline = MultimodalRAG()

def build_graph_resolver(raw_data: str) -> dict:
    result = rag_pipeline.index_document(raw_data)
    return {"message": "GraphRAG indexing complete", **result}

def query_graph_resolver(question: str) -> dict:
    result = rag_pipeline.query(question)
    return result