
from typing import Collection
from fastapi import HTTPException, Depends, APIRouter, responses, status
from .blockchain import Blockchain
from .schemas import RegisterNode, NewTransactionRequest
from textwrap import dedent
from time import time
from uuid import uuid4
app = APIRouter()
blockchain = Blockchain()
node_identifier = str(uuid4()).replace('-', '')

@app.get("/mine")
async def get_mine():
    last_block = blockchain.last_block
    proof = blockchain.proof_of_work(last_block)

    # We must receive a reward for finding the proof.
    # The sender is "0" to signify that this node has mined a new coin.
    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )

    # Forge the new Block by adding it to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return responses.JSONResponse(response, status_code=status.HTTP_200_OK)


@app.get("/chain")
async def get_chain():
    response = {"chain": blockchain.chain, "length": len(blockchain.chain)}
    return responses.JSONResponse(content=response, status_code=status.HTTP_200_OK)


@app.post("/transactions/new")
async def new_transaction(n_trans: NewTransactionRequest):
    try:
        values = n_trans.model_dump()

        # # Check that the required fields are in the POST'ed data
        # required = {'sender', 'recipient', 'amount'}
        # if not all(k in values for k in required):
        #     return 'Missing values', 400

        # Create a new Transaction
        index = blockchain.new_transaction(
            values['sender'], values['receipt'], values['amount'])

        response = {'message': f'Transaction will be added to Block {index}'}
        return responses.JSONResponse(content=response, status_code=status.HTTP_201_CREATED)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"msg": str(e)})


@app.post('/nodes/register')
def register_nodes(reg_node: RegisterNode):
    values = reg_node.model_dump()

    nodes = values.get('nodes')
    if nodes is None:
        return responses.JSONResponse(content={"Error": "Please supply a valid list of nodes"}, status_code=status.HTTP_400_BAD_REQUEST)

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return responses.JSONResponse(content=response, status_code=status.HTTP_201_CREATED)


@app.get('/nodes/resolve')
def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }

    return responses.JSONResponse(content=response, status_code=status.HTTP_200_OK)
