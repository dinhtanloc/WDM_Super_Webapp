# 📁 app/models/rag/multimodal_rag.py

from ml.app.models.generator.chain import GraphGenerator
from ml.app.models.retriever.hybrid_retriever import GraphRetriever

class MultimodalRAG:
    def __init__(self):
        self.generator = GraphGenerator()
        self.retriever = GraphRetriever()

    def index_document(self, raw_data: str):
        self.generator.create_collection()
        nodes, relationships = self.generator.extract_graph_components(raw_data)
        node_ids = self.generator.ingest_to_neo4j(nodes, relationships)
        self.generator.ingest_to_qdrant(node_ids)
        return {"status": "indexed", "node_count": len(node_ids)}

    def query(self, question: str, mode: str = "concise"):
        top_k_docs = self.retriever.retriever_search(question)
        entity_ids = [doc.metadata["id"] for doc in top_k_docs]

        graph_context = self.retriever.fetch_related_graph(entity_ids)

        # Fusion / rerank có thể chèn tại đây (nếu cần tích hợp thêm)
        # Ví dụ: bạn có thể làm re-score dựa vào số hop, tần suất edge, hoặc semantic reranker

        answer = self.retriever.graphRAG_run(graph_context, question, mode=mode)
        return {
            "question": question,
            "context_nodes": graph_context["nodes"],
            "context_edges": graph_context["edges"],
            "answer": answer,
        }
