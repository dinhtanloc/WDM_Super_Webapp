from langchain.graphs import Neo4jGraph

def get_neo4j_retriever():
    graph = Neo4jGraph(
        url="bolt://localhost:7687",
        username="neo4j",
        password="password"
    )
    return graph.as_retriever()
