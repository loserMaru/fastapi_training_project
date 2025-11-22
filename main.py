from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from email_validator import validate_email, EmailNotValidError
from enum import Enum

app = FastAPI()


class ModelName(str, Enum):
    alexnet = 'alexnet'
    resnet = 'resnet'
    lenet = 'lenet'


class Item(BaseModel):
    name: str
    price: float
    email: str
    is_offer: bool | None = None


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, email: str, q: str | None = None):
    try:
        email = validate_email(email, check_deliverability=False)
        email = email.normalized
    except EmailNotValidError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"item_id": item_id, "q": q, "email": email}


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_price": item.price, "item_id": item_id}


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}
