from typing import Collection
from fastapi import FastAPI, HTTPException, responses, status
from fastapi.middleware.cors import CORSMiddleware
from blockchain.api import app as blockchain_app
# App Object
app = FastAPI()
origins = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(blockchain_app, prefix="/blockchain", tags=["Blockchain"])

@app.get("/")
def read_root():
    return {"Welcome to Fast api as backend"}
