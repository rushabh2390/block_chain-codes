from pydantic import BaseModel, AnyUrl
from typing import List


class NewTransactionRequest(BaseModel):
    sender: str
    receipt: str
    amount:float

class RegisterNode(BaseModel):
    nodes:List[AnyUrl]
