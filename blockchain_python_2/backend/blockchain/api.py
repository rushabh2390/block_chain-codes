
from .schemas import Block, Chain
from textwrap import dedent
from time import time
from uuid import uuid4
import strawberry
from strawberry.fastapi import GraphQLRouter
from uuid import uuid4
from typing import List
from .blockchain import Blockchain
from fastapi import FastAPI, status, responses, HTTPException
blockchain = Blockchain()
node_identifier = str(uuid4()).replace('-', '')

@strawberry.type
class Query:
    @strawberry.field
    def chain(self) -> Chain:
        # Convert blockchain.chain to a list of Block objects
        blocks = [Block(**b) for b in blockchain.chain]
        return Chain(chain=blocks, length=len(blocks))


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def mine(self) -> Block:  # Return a Block object
        last_block = blockchain.last_block
        proof = blockchain.proof_of_work(last_block)

        blockchain.new_transaction(
            sender="0",
            recipient=node_identifier,
            amount=1,
        )

        previous_hash = blockchain.hash(last_block)
        block = blockchain.new_block(proof, previous_hash)

        # Return the block as a GraphQL object
        # Use dictionary unpacking to create a Block instance
        return Block(**block)

    @strawberry.mutation
    # Corrected spelling and type
    def new_transaction(self, sender: str, receipt: str, amount: float) -> int:
        try:
            index = blockchain.new_transaction(
                sender, receipt, amount)  # Corrected variable name
            return index
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"msg": str(e)})

    @strawberry.mutation
    # Expecting a list of strings
    def register_nodes(self, nodes: List[str]) -> List[str]:
        if nodes is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail={
                    "Error": "Please supply a valid list of nodes"}
            )

        for node in nodes:
            blockchain.register_node(node)

        return list(blockchain.nodes)

    @strawberry.mutation
    def resolve_conflicts(self) -> str:  # Returns a message
        replaced = blockchain.resolve_conflicts()

        if replaced:
            return "Our chain was replaced"
        else:
            return "Our chain is authoritative"


schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema)