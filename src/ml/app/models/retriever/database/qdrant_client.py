from langchain.vectorstores import Qdrant
from langchain.embeddings import OpenAIEmbeddings
from qdrant_client import QdrantClient

def get_qdrant_retriever():
    client = QdrantClient(host="localhost", port=6333)
    embeddings = OpenAIEmbeddings()
    db = Qdrant(client=client, collection_name="rag_docs", embeddings=embeddings)
    return db.as_retriever()
