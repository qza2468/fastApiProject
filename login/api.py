from fastapi import Depends, APIRouter, Body, Header
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

class UserInfoModel(UserBaseModel):
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
digest_salt = "qza2468"
TIMEOUT_FORMAT = "%Y-%m-%d %H:%M:%S"
MAX_TOKEN_PER_USER = 5

EXPIRE_TIMEOUT = datetime.timedelta(days=1)

# return the user2tokens db name
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

# try to get the token, if not exist return (None, None), else return (username, expire)
def get_cookie(redis_conn: redis.Redis, token: str):
    cookie = redis_conn.hget(REDIS_BASE, token).decode()
    if cookie:
        return cookie.split(";", 1)
    else:
        return None, None

# remove the token from token2user and user2tokens, if token to no user, then just return.
# could add an optional user_name_ to delete it from user2tokens too.
def del_cookie(redis_conn: redis.Redis, token: str, user_name_: str = None):
    username, timeout = get_cookie(redis_conn, token)
    if not username and user_name_:
        return
    elif username:
        redis_conn.hdel(REDIS_BASE, token)
        redis_conn.srem(userdb(username), token)
    elif user_name_:
        redis_conn.srem(userdb(user_name_), token)

# remove token from the username2tokens
def del_cookie_from_user(redis_conn: redis.Redis, username: str, token: str):
    redis_conn.srem(userdb(username), token)

# remove all the expired, point to null cookie and point to another user cookie.
def del_invalid_cookies_from_user(redis_conn: redis.Redis, username: str):
    cookies = redis_conn.smembers(userdb(username))

    count = 0
    for cookie in cookies:
        res = check_cookie(redis_conn, cookie)
        if res is None:
            del_cookie_from_user(redis_conn, username, cookie)
            count += 1
        elif res == "":
            del_cookie(redis_conn, cookie, username)
            count += 1
        elif res != username:
            del_cookie_from_user(redis_conn, username, cookie)
            del_cookie(redis_conn, cookie)
            count += 1

    return count


# check the token, if expired return "", if token to no user return None, else return the username
def check_cookie(redis_conn: redis.Redis, token: str):
    # TODO: should add timeout check for this cookie.

    username, timeout = get_cookie(redis_conn, token)
    if not username:
        return None

    timeout = dateutil.parser.parse(timeout)
    if datetime.datetime.now() > timeout:
        return ""
    else:
        return username

def check_cookie_depend(redis_conn: redis.Redis = Depends(get_redis_pool),
                        token: str = Header(None)):
    return check_cookie(redis_conn, token)

# create cookie for username, if cookies for a specific user too much, remove some. return username on ok, None on fail
def create_cookie(redis_conn: redis.Redis, username: str):
    if redis_conn.scard(userdb(username)) > MAX_TOKEN_PER_USER:
        remove_cookies(redis_conn, username, 1)
    cookie = secrets.token_urlsafe(64)
    # TODO: should check all token2user is respond to user2token in sometime.
    # TODO: should do something to deal with error in the follow operation.
    redis_conn.hset(REDIS_BASE, cookie, username + ';' + (datetime.datetime.now() + EXPIRE_TIMEOUT).strftime(TIMEOUT_FORMAT))
    redis_conn.sadd(userdb(username), cookie)

    return cookie

# remove `force` number cookies for username, maybe randomly remove cookie.
def remove_cookies(redis_conn: redis.Redis, username: str, force: int = 0):
    deleted = del_invalid_cookies_from_user(redis_conn, username)

    if deleted >= force:
        return

    remove_cookies_force(redis_conn, username, force - deleted)

# remove `force` number cookies randomly from username
def remove_cookies_force(redis_conn: redis.Redis, username: str, force: int = 0):
    for i in range(force):
        cookie = redis_conn.srandmember(userdb(username))
        del_cookie(redis_conn, cookie, username)

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
    return hashlib.blake2b((s + digest_salt).encode("utf-8")).hexdigest()

# username should be unique between users, and the same email could be used by multiply users
# only admin could create user.
@router.post("/createuser")
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


@router.post("/login")
async def login(user: UserBaseModel, session: Session = Depends(get_session),
                redis_conn: redis.Redis = Depends(get_redis_pool)):
    user_in_table = get_user(session, user.name)
    if not user_in_table:
        return {"ok": False, "message": "wrong username or password"}

    if hhhhash(user.password) == user_in_table.usertoken:
        cookie = create_cookie(redis_conn, user.name)

        return {"ok": True, "token": cookie}
    else:
        return {"ok": False, "message": "wrong username or password"}

@router.post("/logout")
async def logout(user: UserCookie, session: Session = Depends(get_session),
                 redis_conn: redis.Redis = Depends(get_redis_pool)):
    del_cookie(redis_conn, user.token)

# only with both username and email, could figure out whether a user exist in the system
@router.post("/exists")
async def user_exists(userinfo: UserInfoModel, session: Session = Depends(get_session)):
    user = get_user(session, username=userinfo.name, email=userinfo.email)
    if not user:
        return {"ok": False}
    else:
        return {"ok": True}
