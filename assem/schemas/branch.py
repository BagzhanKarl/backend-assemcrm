from pydantic import BaseModel


class CreateBranchSchema(BaseModel):
    city: str
    address: str
    admin: int

