# app/main.py
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from app.graphql.schema import Query
import strawberry
schema = strawberry.Schema(Query)
graphql_app = GraphQLRouter(schema)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI with GraphQL"}