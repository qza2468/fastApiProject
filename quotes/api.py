from fastapi import Query, Depends, APIRouter
from pydantic import BaseModel
import random
import getpass
import enum

from sqlalchemy.orm import declarative_base, Session
from sqlalchemy import create_engine, Column, Integer, Text, String

from typing import Optional, List
Base = declarative_base()

sql_engine = None


class QuoteSchema(Base):
    __tablename__ = "quotes"

    id = Column(Integer, primary_key=True)
    lang = Column(String)
    man = Column(String)
    quote = Column(Text)


class QuoteModel(BaseModel):
    quote: str
    lang: str
    id: int
    man: str

    class Config:
        orm_mode = True


class QuoteLang(str, enum.Enum):
    en = "en"
    cn = "cn"


router = APIRouter()

quotes_index_max = 0


def get_session() -> Session:
    session = Session(sql_engine)
    try:
        yield session
    finally:
        session.close()


@router.on_event("startup")
async def init():
    global quotes_index_max
    global sql_engine

    password = getpass.getpass("请输入密码")

    sql_engine = create_engine(f"mysql+pymysql://qza2468:{password}@localhost/scraped")

    session = Session(sql_engine)
    quotes_index_max = session.query(QuoteSchema).count() # if there is error just exit the program, no need for close.
    session.close()


@router.get("/hello/")
async def root():
    return {"message": "Hello World"}


@router.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@router.get("/quotes/random", response_model=QuoteModel)
async def get_quote_random(session: Session = Depends(get_session)):
    data = None
    fetch_which = random.randint(1, quotes_index_max)
    result = session.query(QuoteSchema).filter(QuoteSchema.id == fetch_which).first()

    if result:
        return result
    else:
        return {}


@router.get("/quotes/all", response_model=List[QuoteModel])
async def get_quotes_all(lang: QuoteLang = Query(None),
                         session: Session = Depends(get_session)):
    res = session.query(QuoteSchema)

    if lang:
        res = res.filter(QuoteSchema.lang == lang)

    return res.all()


@router.get("/quotes/select", response_model=QuoteModel)
async def get_quotes(i: int = Query(None, ge=0),
                     session: Session = Depends(get_session)):
    return session.query(QuoteSchema).filter(QuoteSchema.id == i).first()
