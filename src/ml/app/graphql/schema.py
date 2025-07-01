# app/graphql/schema.py
import strawberry
from .resolvers import build_graph_resolver, query_graph_resolver

@strawberry.type
class GraphRAGResult:
    message: str
    indexed_length: int

@strawberry.type
class GraphRAGQueryResult:
    answer: str

@strawberry.input
class GraphRAGInput:
    raw_data: str

@strawberry.input
class GraphRAGQueryInput:
    question: str

@strawberry.type
class Query:
    @strawberry.field
    def build_graph(self, input: GraphRAGInput) -> GraphRAGResult:
        return build_graph_resolver(input.raw_data)

    @strawberry.field
    def query_graph(self, input: GraphRAGQueryInput) -> GraphRAGQueryResult:
        return query_graph_resolver(input.question)