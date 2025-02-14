from pydantic import BaseModel, AnyUrl
from typing import List
import strawberry


@strawberry.type
class Transaction:  # GraphQL type for a Transaction
    sender: str
    receipt: str  # Corrected spelling to 'recipient'
    amount: float  # Or int, depending on your needs


@strawberry.type
class Block:      # GraphQL type for a Block (if not already defined)
    index: int
    transactions: List[Transaction]  # Use the Transaction type here
    proof: int
    previous_hash: str


@strawberry.type
class Chain:      # GraphQL type for the entire chain
    chain: List[Block]
    length: int


@strawberry.type
class NewTransactionRequest(BaseModel):
    sender: str
    receipt: str
    amount: float


@strawberry.type
class RegisterNode(BaseModel):
    nodes: List[AnyUrl]