# 📁 app/models/rag/multimodal_rag.py

from ml.app.models.generator.chain import HybridGraphRagGenerator
from ml.app.models.retriever.hybrid_retriever import HybridGraphRagRetriever
from ml.app.models.processor.WDM_processor import WDMProcessor
class MultimodalRAG:
    def __init__(self):
        self.generator = HybridGraphRagGenerator()
        self.retriever = HybridGraphRagRetriever()

    # def index_document(self, raw_data: str):
    #     self.retriever.create_collection()
    #     nodes, relationships = self.retriever.extract_graph_components(raw_data)
    #     node_ids = self.retriever.ingest_to_neo4j(nodes, relationships)
    #     self.retriever.ingest_to_qdrant(node_ids)
    #     return {"status": "indexed", "node_count": len(node_ids)}

    def index_document(self, pdf_path: str):
        """
        Đầu vào: đường dẫn tới file PDF
        Quy trình:
        - Dùng WDMProcessor để trích xuất text, table, image từ PDF
        - Mỗi phần tử sẽ thành một LangchainDocument
        - Với mỗi document, trích đồ thị tri thức và lưu vào Neo4j + Qdrant
        """
        print(f"[+] Bắt đầu xử lý file PDF: {pdf_path}")

        # Bước 1: Trích xuất tài liệu từ PDF bằng WDMProcessor
        processor = WDMProcessor(
            pdf_path=pdf_path,
            output_folder="./extracted_images",
            gcs_bucket_name="my-multimodalrag-images"
        )
        documents = processor.process_pdf()

        print(f"[+] Tìm thấy {len(documents)} tài liệu. Bắt đầu indexing...")

        all_node_ids = []

        for doc in documents:
            content = doc.page_content
            metadata = doc.metadata

            # Bước 2: Trích đồ thị tri thức từ nội dung của từng document
            nodes, relationships = self.retriever.extract_graph_components(content)

            # Bước 3: Lưu vào Neo4j
            node_id_map = self.retriever.ingest_to_neo4j(nodes, relationships)

            # Bước 4: Lưu vector embedding vào Qdrant
            self.retriever.ingest_to_qdrant(node_id_map)

            all_node_ids.extend(node_id_map.values())

        return {"status": "indexed", "node_count": len(all_node_ids)}

    def query(self, question: str, mode: str = "concise"):
        top_k_docs = self.generator.retriever_search(question)
        entity_ids = [doc.metadata["id"] for doc in top_k_docs]

        graph_context = self.generator.fetch_related_graph(entity_ids)

        # Fusion / rerank có thể chèn tại đây (nếu cần tích hợp thêm)
        # Ví dụ: bạn có thể làm re-score dựa vào số hop, tần suất edge, hoặc semantic reranker

        answer = self.generator.graphRAG_run(graph_context, question, mode=mode)
        return {
            "question": question,
            "context_nodes": graph_context["nodes"],
            "context_edges": graph_context["edges"],
            "answer": answer,
        }
