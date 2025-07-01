
# 📁 app/models/generator/chain.py

from langchain.graphs import Neo4jGraph
from langchain.embeddings import GoogleGenerativeAIEmbeddings
from langchain.vectorstores import Qdrant
from langchain.chat_models import ChatVertexAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from pydantic import BaseModel
import os
import uuid
import json
from qdrant_client import QdrantClient, models as qmodels

load_dotenv(".env.local")

# --- Setup Clients ---
class Triplet(BaseModel):
    h: str
    type_h: str
    r: str
    o: str
    type_t: str

class KnowledgeGraph(BaseModel):
    graph: list[Triplet]

class HybridGraphRagRetriever:
    def __init__(self):
        self.collection_name = "graphRAGstoreds"
        self.vector_dimension = 768

        self.neo4j_graph = Neo4jGraph(
            url=os.getenv("NEO4J_URI"),
            username=os.getenv("NEO4J_USERNAME"),
            password=os.getenv("NEO4J_PASSWORD")
        )

        self.embedding_model = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=os.getenv("GEMINI_API_KEY")
        )

        self.qdrant_client = QdrantClient(
            url=os.getenv("QDRANT_URL"),
            api_key=os.getenv("QDRANT_KEY")
        )

        self.qdrant = Qdrant(
            client=self.qdrant_client,
            collection_name=self.collection_name,
            embeddings=self.embedding_model
        )

        self.llm = ChatVertexAI(model_name="gemini-pro", temperature=0.0)

    def parse_triplets(self, text: str) -> KnowledgeGraph:
        prompt = PromptTemplate.from_template("""
        Extract triplets from the following text and output as JSON:

        {input}

        Format:
        {{
          "graph": [
            {{"h": "...", "type_h": "...", "r": "...", "o": "...", "type_t": "..."}},
            ...
          ]
        }}
        """)
        result = self.llm.invoke(prompt.format(input=text))
        try:
            return KnowledgeGraph.model_validate_json(result)
        except Exception as e:
            print("Triplet parsing error:", e)
            return KnowledgeGraph(graph=[])

    def extract_graph_components(self, raw_text: str):
        parsed = self.parse_triplets(raw_text)
        nodes, relationships = {}, []
        for triplet in parsed.graph:
            h_id = nodes.setdefault(triplet.h, {"id": str(uuid.uuid4()), "type": triplet.type_h})
            t_id = nodes.setdefault(triplet.o, {"id": str(uuid.uuid4()), "type": triplet.type_t})
            relationships.append({"source": h_id["id"], "target": t_id["id"], "type": triplet.r})
        return nodes, relationships

    def ingest_to_neo4j(self, nodes, relationships):
        for name, props in nodes.items():
            self.neo4j_graph.query(f"""
                CREATE (n:{props['type']} {{id: '{props['id']}', name: '{name}'}})
            """)
        for rel in relationships:
            self.neo4j_graph.query(f"""
                MATCH (a {{id: '{rel['source']}'}}), (b {{id: '{rel['target']}'}})
                CREATE (a)-[:{rel['type']}]->(b)
            """)
        return {name: props['id'] for name, props in nodes.items()}

    def create_collection(self):
        try:
            self.qdrant_client.get_collection(self.collection_name)
        except Exception:
            self.qdrant_client.create_collection(
                collection_name=self.collection_name,
                vectors_config=qmodels.VectorParams(size=self.vector_dimension, distance=qmodels.Distance.COSINE)
            )

    def ingest_to_qdrant(self, node_id_mapping):
        texts = list(node_id_mapping.keys())
        metadatas = [{"id": node_id_mapping[t]} for t in texts]
        self.qdrant.add_texts(texts=texts, metadatas=metadatas)
