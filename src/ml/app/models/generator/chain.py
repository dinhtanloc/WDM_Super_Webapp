

# 📁 app/models/retriever/chain.py

from langchain.graphs import Neo4jGraph
from langchain.vectorstores import Qdrant
from langchain.chat_models import ChatVertexAI
from dotenv import load_dotenv
import os
import json
from qdrant_client import QdrantClient
from langchain.embeddings import GoogleGenerativeAIEmbeddings

load_dotenv(".env.local")

class HybridGraphRagGenerator:
    def __init__(self):
        self.collection_name = "graphRAGstoreds"

        self.neo4j_graph = Neo4jGraph(
            url=os.getenv("NEO4J_URI"),
            username=os.getenv("NEO4J_USERNAME"),
            password=os.getenv("NEO4J_PASSWORD")
        )

        self.embedding_model = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=os.getenv("GEMINI_API_KEY")
        )

        self.qdrant = Qdrant(
            client=QdrantClient(
                url=os.getenv("QDRANT_URL"),
                api_key=os.getenv("QDRANT_KEY")
            ),
            collection_name=self.collection_name,
            embeddings=self.embedding_model
        )

        self.llm = ChatVertexAI(model_name="gemini-pro", temperature=0.0)

    def retriever_search(self, query: str):
        retriever = self.qdrant.as_retriever(search_type="similarity", search_kwargs={"k": 5})
        return retriever.get_relevant_documents(query)

    def fetch_related_graph(self, entity_ids):
        result = self.neo4j_graph.query(f"""
        MATCH path = (e)-[*1..3]-(related_node)
        WHERE e.id IN {json.dumps(entity_ids)}
        UNWIND nodes(path) AS n
        UNWIND relationships(path) AS r
        RETURN DISTINCT n.name AS n_name, type(r) AS rel_type, startNode(r).name AS src, endNode(r).name AS tgt
        """)
        edges = set()
        nodes = set()
        for row in result:
            nodes.add(row['src'])
            nodes.add(row['tgt'])
            edges.add(f"({row['src']})-[{row['rel_type']}]->({row['tgt']})")
        return {"nodes": sorted(nodes), "edges": sorted(edges)}

    def graphRAG_run(self, graph_context, user_query, mode='concise'):
        node_str = "\n- ".join(graph_context['nodes'])
        edge_str = "\n- ".join(graph_context['edges'])
        if mode == 'concise':
            sys_prompt = "Answer ONLY from graph. One short sentence. If unsure, say unknown."
            user_prompt = f"Nodes:\n- {node_str}\n\nEdges:\n- {edge_str}\n\nQuestion: {user_query}"
        else:
            sys_prompt = "Verbose graph reasoning assistant. Explain chain-of-thought."
            user_prompt = f"Graph:\n- Nodes: {node_str}\n- Edges: {edge_str}\n\nQuestion: {user_query}"
        return self.llm.invoke(f"{sys_prompt}\n\n{user_prompt}")
