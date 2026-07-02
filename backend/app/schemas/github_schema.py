from pydantic import BaseModel

class CloneRepositoryRequest(BaseModel):
    url: str