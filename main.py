from fastapi import FastAPI, HTTPException
from email_validator import validate_email, EmailNotValidError
from schemas import Item, User, ModelName
from validations import email_validation

app = FastAPI()

fake_items_db = [{"item_name": "Boo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


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


@app.get("/items/")
async def read_items(skip: int = 0, limit: int = 10):
    return fake_items_db[skip: skip + limit]


@app.post("/user/")
async def create_user(user: User):
    email_validation(user.email)
    return user