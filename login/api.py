from fastapi import Depends, APIRouter, Body
from pydantic import BaseModel
from sqlalchemy.orm import declarative_base, Session
from sqlalchemy import create_engine, Column, Integer, Text, String

import datetime
import dateutil.parser
import secrets
import hashlib


import redis

class UserBaseModel(BaseModel):
    name: str
    password: str

    class Config:
        orm_mode = True


class UserInModel(UserBaseModel):
    email: str

class UserInfoModel:
    name: str
    email: str


class UserOutModel(BaseModel):
    email: str
    token: str
    name: str

    class Config:
        orm_mode = True

class UserCookie(BaseModel):
    token: str

Base = declarative_base()

class UserInSchema(Base):
    __tablename__ = "users"

    usermail = Column(String)
    usertoken = Column(String)
    username = Column(String, primary_key=True)

router = APIRouter()

sql_engine = None
redis_pool = None

# TODO: using the format key=`token` val=`username;expired datetime`
# TODO: using the format key=`username` val=`token;token;`
# TODO: no `;` should contain in name and token.
# when give token add it to the follow two base, so that we could delete the user token when delete user or logout user.
REDIS_BASE = "token2user"
REDIS_USER_BASE = "qza2468"
TIMEOUT_FORMAT = "%Y-%m-%d %H:%M:%S"
MAX_TOKEN_PER_USER = 5

EXPIRE_TIMEOUT = datetime.timedelta(days=1)

def userdb(username: str):
    return REDIS_USER_BASE + username

def get_session():
    session = Session(sql_engine)
    try:
        yield session
    finally:
        session.close()

def get_redis_pool():
    redis_conn = redis.Redis(connection_pool=redis_pool)
    try:
        yield redis_conn
    finally:
        redis_conn.close()

def get_cookie(redis_conn: redis.Redis, token:str):
    cookie = redis_conn.hget(REDIS_BASE, token)
    return cookie.split(";", 1)

def del_cookie(redis_conn: redis.Redis, token: str):
    username, timeout = get_cookie(redis_conn, token)

    redis_conn.hdel(REDIS_BASE, token)

    redis_conn.srem(userdb(username), token)

def check_cookie(redis_conn: redis.Redis, token: str):
    # TODO: should add timeout check for this cookie.

    username, timeout = get_cookie(redis_conn, token)

    timeout = dateutil.parser.parse(timeout)
    if datetime.datetime.now() > timeout:
        del_cookie(redis_conn, token)
        return None
    else:
        return username

def add_cookie(redis_conn: redis.Redis, username: str, token: str):
    if redis_conn.scard(userdb(username)) > MAX_TOKEN_PER_USER:
        remove_old_cookie_for_user(redis_conn, username, 1)
    redis_conn.hset(REDIS_BASE, token, username + ';' + (datetime.datetime.now() + EXPIRE_TIMEOUT).strftime(TIMEOUT_FORMAT))
    redis_conn.sadd(userdb(username), token)


def remove_old_cookie_for_user(redis_conn: redis.Redis, username: str, force: int = 0):
    tokens = redis_conn.smembers(userdb(username))

    deleted = 0
    for i in tokens:
        res = check_cookie(redis_conn, i)
        if not res:
            deleted += 1

    if deleted >= force:
        return

    for i in range(force - deleted):
        redis_conn.spop(userdb(username))


@router.on_event("startup")
async def init():
    global sql_engine
    global redis_pool
    sql_engine = create_engine("sqlite:///foo.db", connect_args={"check_same_thread": False})

    redis_pool = redis.ConnectionPool(host="127.0.0.1", port=6379, db=0)

    Base.metadata.create_all(sql_engine)

def get_user(session: Session, username: str = None, email: str = None, multi: bool = False):
    res = session.query(UserInSchema)
    if username:
        res.filter(UserInSchema.username == username)
    if email:
        res.filter(UserInSchema.usermail == email)

    if not username and not email:
        return None

    if multi:
        return res.all()
    else:
        return res.first()

def hhhhash(s):
    return hashlib.md5(s)

# username should be unique between users, and the same email could be used by multiply users
# only admin could create user.
async def createuser(user: UserInModel, session: Session = Depends(get_session)):
    # TODO: should check whether this is tangled by the admin user.
    if len(user.name) > 64 or len(user.name) == 0:
        return {"ok": False, "message": "username is too long or too short"}
    elif len(user.email) > 64 or len(user.email) == 0:
        return {"ok": False, "message": "email is too long"}

    user_in_table = get_user(session, user.name)
    if user_in_table:
        return {"ok": False, "message": "user is already exist"}

    try:
        session.add(UserInSchema(username=user.name, usermail=user.email, usertoken=hhhhash(user.password)))
        session.commit()
    except Exception as e:
        return {"ok": False, "message": str(e)}

    return {"ok": True, "message": "Congratulations"}


@router.post("login")
async def login(user: UserBaseModel, session: Session = Depends(get_session),
                redis_conn: redis.Redis = Depends(get_redis_pool)):
    user_in_table = get_user(session, user.name)
    if not user_in_table:
        return {"ok": False, "message": "wrong username or password"}

    if hhhhash(user.password) == user_in_table.usertoken:
        cookie = secrets.token_urlsafe(64)
        add_cookie(redis_conn, user.name, cookie)

        return {"ok": True, "token": cookie}
    else:
        return {"ok": False, "message": "wrong username or password"}

@router.post("logout")
async def logout(user: UserCookie, session: Session = Depends(get_session),
                 redis_conn: redis.Redis = Depends(get_redis_pool)):
    del_cookie(redis_conn, user.token)

# only with both username and email, could figure out whether a user exist in the system
@router.post("exists")
async def user_exists(userinfo: UserInfoModel, session: Session = Depends(get_session)):
    user = get_user(session, username=userinfo.name, email=userinfo.email)
    if not user:
        return {"ok": False}
    else:
        return {"ok": True}
