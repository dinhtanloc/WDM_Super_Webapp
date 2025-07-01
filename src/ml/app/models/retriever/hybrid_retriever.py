# 📁 app/models/retriever/graph_rag_runner.py (LangChain + VertexAI Gemini version)

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

# Load environment
load_dotenv(".env.local")

# --- Configuration ---
collection_name = "graphRAGstoreds"
vector_dimension = 768

neo4j_graph = Neo4jGraph(
    url=os.getenv("NEO4J_URI"),
    username=os.getenv("NEO4J_USERNAME"),
    password=os.getenv("NEO4J_PASSWORD")
)

embedding_model = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=os.getenv("GEMINI_API_KEY")
)

qdrant = Qdrant(
    client=QdrantClient(
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_KEY")
    ),
    collection_name=collection_name,
    embeddings=embedding_model
)

# Use ChatVertexAI for both parsing and answering
llm = ChatVertexAI(model_name="gemini-pro", temperature=0.0)

# --- Data Models ---
class Triplet(BaseModel):
    h: str
    type_h: str
    r: str
    o: str
    type_t: str

class KnowledgeGraph(BaseModel):
    graph: list[Triplet]

# --- Utilities ---
def parse_triplets_with_llm(prompt_input: str) -> KnowledgeGraph:
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
    result = llm.invoke(prompt.format(input=prompt_input))
    try:
        return KnowledgeGraph.model_validate_json(result)
    except Exception as e:
        print(f"Triplet parsing failed: {e}")
        return KnowledgeGraph(graph=[])

def extract_graph_components(raw_data):
    parsed = parse_triplets_with_llm(raw_data)
    nodes, relationships = {}, []
    for triplet in parsed.graph:
        h_id = nodes.setdefault(triplet.h, {"id": str(uuid.uuid4()), "type": triplet.type_h})
        t_id = nodes.setdefault(triplet.o, {"id": str(uuid.uuid4()), "type": triplet.type_t})
        relationships.append({"source": h_id["id"], "target": t_id["id"], "type": triplet.r})
    return nodes, relationships

def ingest_to_neo4j(nodes, relationships):
    for name, props in nodes.items():
        neo4j_graph.query(f"""
            CREATE (n:{props['type']} {{id: '{props['id']}', name: '{name}'}})
        """)
    for rel in relationships:
        neo4j_graph.query(f"""
            MATCH (a {{id: '{rel['source']}'}}), (b {{id: '{rel['target']}'}})
            CREATE (a)-[:{rel['type']}]->(b)
        """)
    return {name: props["id"] for name, props in nodes.items()}

def create_collection():
    try:
        qdrant.client.get_collection(collection_name)
    except Exception:
        qdrant.client.create_collection(
            collection_name=collection_name,
            vectors_config=qmodels.VectorParams(size=vector_dimension, distance=qmodels.Distance.COSINE)
        )

def ingest_to_qdrant(node_id_mapping):
    texts = list(node_id_mapping.keys())
    metadatas = [{"id": node_id_mapping[t]} for t in texts]
    qdrant.add_texts(texts=texts, metadatas=metadatas)

def retriever_search(query):
    retriever = qdrant.as_retriever(search_type="similarity", search_kwargs={"k": 5})
    return retriever.get_relevant_documents(query)

def fetch_related_graph(entity_ids):
    result = neo4j_graph.query(f"""
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

def graphRAG_run(graph_context, user_query, mode='concise'):
    node_str = "\n- ".join(graph_context['nodes'])
    edge_str = "\n- ".join(graph_context['edges'])
    if mode == 'concise':
        sys_prompt = "Answer ONLY from graph. One short sentence. If unsure, say unknown."
        user_prompt = f"Nodes:\n- {node_str}\n\nEdges:\n- {edge_str}\n\nQuestion: {user_query}"
    else:
        sys_prompt = "Verbose graph reasoning assistant. Explain chain-of-thought."
        user_prompt = f"Graph:\n- Nodes: {node_str}\n- Edges: {edge_str}\n\nQuestion: {user_query}"
    result = llm.invoke(f"{sys_prompt}\n\n{user_prompt}")
    return result

def build_graph_from_raw(raw_data: str):
    create_collection()
    nodes, rels = extract_graph_components(raw_data)
    ids = ingest_to_neo4j(nodes, rels)
    ingest_to_qdrant(ids)

def answer_query_with_graphrag(query: str) -> str:
    docs = retriever_search(query)
    ids = [d.metadata['id'] for d in docs]
    graph_ctx = fetch_related_graph(ids)
    return graphRAG_run(graph_ctx, query)
