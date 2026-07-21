from pydantic import BaseModel, Field


class Order(BaseModel):
    customer: str
    quantity: int = Field(gt=0)