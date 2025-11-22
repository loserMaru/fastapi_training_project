from pydantic import BaseModel
from enum import Enum


class ModelName(str, Enum):
    alexnet = 'alexnet'
    resnet = 'resnet'
    lenet = 'lenet'


class Item(BaseModel):
    name: str
    price: float
    email: str
    is_offer: bool | None = None


class User(BaseModel):
    email: str
    password: str
    login: str
