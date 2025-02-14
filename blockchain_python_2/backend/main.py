from typing import Collection
from fastapi import FastAPI, HTTPException, responses, status
from fastapi.middleware.cors import CORSMiddleware
from blockchain.api import graphql_app as blockchaingraph_app
# App Object
app = FastAPI(
    title="Blockchain-2",
    Description="FastApi + GraphQL",
    version="2.0.0",
)
origins = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(blockchaingraph_app, prefix="/graphql", tags=["GraphQL"])

@app.get("/")
def read_root():
    return {"Welcome to Fast api as backend"}
