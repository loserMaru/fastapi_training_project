from typing import Annotated

from email_validator import EmailNotValidError, validate_email
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import select

from database import (
    Hero,
    HeroCreate,
    HeroPublic,
    HeroUpdate,
    SessionDep,
    create_db_and_tables,
)
from dependencies import get_query_token
from internal import admin
from routers import items, users
from schemas import Item, ModelName, User
from validations import email_validation


app = FastAPI(dependencies=[Depends(get_query_token)])

app.include_router(users.router)
app.include_router(items.router)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_query_token)],
    responses={404: {"description": "I'm a teapot"}},
)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


fake_items_db = [{"item_name": "Boo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}

@app.post("/heroes/", response_model=HeroPublic, tags=["heroes"])
async def create_hero(hero: HeroCreate, session: SessionDep):
    db_hero = Hero.model.validate(hero)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero


@app.get("/heroes/", response_model=list[HeroPublic], tags=["heroes"])
async def read_heroes(
        session: SessionDep,
        offset: int = 0,
        limit: Annotated[int, Query(le=100)] = 100,
):
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes


@app.get("/heroes/{hero_id}", response_model=HeroPublic, tags=["heroes"])
async def read_hero(hero_id: int, session: SessionDep):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero


@app.patch("/heroes/{hero_id}", response_model=HeroUpdate, tags=["heroes"])
async def update_hero(hero_id: int, hero: HeroUpdate, session: SessionDep):
    hero_db = session.get(Hero, hero_id)
    if not hero_db:
        raise HTTPException(status_code=404, detail="Hero not found")
    hero_data = hero.model_dump(exclude_unset=True)
    hero_db.sqlmodel_update(hero_data)
    session.add(hero_db)
    session.commit()
    session.refresh(hero_db)
    return hero_db


@app.delete("/heroes/{hero_id}", tags=["heroes"])
async def delete_hero(hero_id: int, session: SessionDep):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(hero)
    session.commit()
    return {"message": "Hero deleted"}



# @app.get("/items/{item_id}")
# async def read_item(item_id: int, email: str, q: str | None = None):
#     try:
#         email = validate_email(email, check_deliverability=False)
#         email = email.normalized
#     except EmailNotValidError as e:
#         raise HTTPException(status_code=400, detail=str(e))
#     return {"item_id": item_id, "q": q, "email": email}
#
#
# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Item):
#     return {"item_price": item.price, "item_id": item_id}
#
#
# @app.get("/items/")
# async def read_items(skip: int = 0, limit: int = 10):
#     return fake_items_db[skip: skip + limit]


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


# @app.post("/user/")
# async def create_user(user: User):
#     email_validation(user.email)
#     return user
