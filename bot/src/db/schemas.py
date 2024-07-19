from pydantic import BaseModel


class Valute(BaseModel):
    ID: str
    NumCode: int
    CharCode: str
    Nominal: int
    Name: str
    Value: float
    VunitRate: float
