from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from email_validator import validate_email, EmailNotValidError

app = FastAPI()


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
