from fastapi import Depends, APIRouter, Body, Header, HTTPException, Response
from pydantic import BaseModel

import sqlite3
import threading

import datetime
import dateutil.parser
import secrets
import hashlib
import os

dir_name = os.path.dirname(os.path.realpath(__file__))
digest_salt = "qza2468"
database_where = "foo.db"
table_name = "users"


def hhhhash(s: str):
    return hashlib.blake2b((s + digest_salt).encode("utf-8")).hexdigest()

class UserInModel(BaseModel):
    name: str
    password: str


class Cookies(dict):
    lock = threading.Lock()

    def atom_get(self, key: str) -> str:
        res = None
        with self.lock:
            res = cookies.get(key)

        return res

    def atom_set(self, key: str, val: str):
        if not key:
            raise HTTPException(404, detail="username should not be empty")
        with self.lock:
            cookies[key] = val

    def create_cookie(self, username: str) -> str:
        cookie = secrets.token_urlsafe(64)
        self.atom_set(cookie, username)

        return cookie

    def check_cookie(self, token: str):
        return self.atom_get(token)

    def del_cookie(self, token: str):
        with self.lock:
            self.pop(token, None)

    def del_cookies_for_user(self, user: str, except_list: list = None):
        if not except_list:
            except_list = []
        with self.lock:
            need_del = []
            for k_v_pair in self.items():
                if k_v_pair[1] == user and k_v_pair[0] not in except_list:
                    need_del.append(k_v_pair[0])

            for i in need_del:
                self.pop(i, None)


sqliteConn_lock = threading.Lock()
sqliteConn = None
cookies = Cookies()

router = APIRouter()


def get_cursor():
    session = sqliteConn.cursor()
    try:
        yield session
    finally:
        session.close()


# try to fetch information from database about user.
# return infos list on success, return None on failure
def get_user(cursor: sqlite3.Cursor, name: str):
    res = None
    with sqliteConn_lock:
        res = get_user_no_lock(cursor, name)

    return res
def get_user_no_lock(cursor: sqlite3.Cursor, name: str):
    res = None
    cursor.execute(f"SELECT * FROM {table_name} WHERE username=?", (name,))
    res = cursor.fetchall()

    try:
        if res and len(res) >= 1:
            res = res[0]
        else:
            res = None
    except:
        res = None

    return res
def get_user_with_check(cursor: sqlite3.Cursor, name: str, password: str) -> str:
    res = get_user(cursor, name)
    print(name)
    if not res:
        return ""

    if res[0] == hhhhash(password):
        return res[1]
    else:
        return ""

# add user if user not exist. raise 404 if user exist
def add_user(cursor: sqlite3.Cursor, name: str, password: str):
    with sqliteConn_lock:
        if get_user_no_lock(cursor, name):
            raise HTTPException(404, "user is already exist")

        print(get_user_no_lock(cursor, name))

        cursor.execute(f"INSERT INTO {table_name} (username, usertoken) VALUES (?, ?)",
                       (name, hhhhash(password)))
        sqliteConn.commit()

# a depend of cookie check, return the username if `token` is valid.
# otherwise raise 404.
# TODO: i will return all info about user if success. it will change a lot, so i will do it later.
def check_cookie_depend(token: str = Header(None),
                        cursor: sqlite3.Cursor = Depends(get_cursor)):
    if not token:
        raise HTTPException(404, "cookie is invalid")
    res = cookies.check_cookie(token)
    if not res:
        raise HTTPException(404, "cookie is invalid")

    res_2 = get_user(cursor, res)
    if not res_2:
        raise HTTPException(404, "cookie is invalid")
    return res


@router.on_event("startup")
async def init():
    global sqliteConn
    sqliteConn = sqlite3.connect(database_where, check_same_thread=False)
    cursor = sqliteConn.cursor()
    try:
        cursor.execute("CREATE TABLE IF NOT EXISTS users "
                       "(usertoken VARCHAR, username VARCHAR)")
    finally:
        cursor.close()

@router.post("/createuser")
def createuser(user_in: UserInModel,
               token: str = Header(None),
               cursor: sqlite3.Cursor = Depends(get_cursor)):
    if cookies.check_cookie(token) != "qza2468":
        raise HTTPException(404, detail="you have no right to add user")

    if len(user_in.name) > 64 or len(user_in.name) == 0:
        return HTTPException(404, "username is too long or too short")

    add_user(cursor, user_in.name, user_in.password)

    return {"ok": True, "message": "Congratulations"}


@router.post("/login")
def login(user_in: UserInModel,
          cursor: sqlite3.Cursor = Depends(get_cursor)):
    print(user_in.name, user_in.password)
    if get_user_with_check(cursor, user_in.name, user_in.password):
        cookie = cookies.create_cookie(user_in.name)

        return {"ok": True, "token": cookie}
    else:
        print("aaa")
        raise HTTPException(404, "wrong username or password")

@router.post("/logout")
def logout(token: str = Header(None)):
    cookies.del_cookie(token)

    print(cookies)
    return Response(status_code=200)
    
@router.post("/removeOtherCookies")
def removeOtherCookies(token: str = Header(None), name: str = Depends(check_cookie_depend)):
    print(cookies)
    cookies.del_cookies_for_user(name, [token])
    print(token)

    print(cookies)

    return Response(status_code=200)



# TODO:
# 这就是fastapi精彩的地方。
# 前面提到，async函数会放到event loop中执行。
# 那么，普通的函数会放到哪里呢？
# 答案是，放到thread pool中。
# 简单的说，就像官方所说，如果你不清楚你函数里的调用是否异步，那就定义为普通函数。
# 因为它可以采用多线程的方式解决。
# 反之，定义了async函数，里面却是同步的调用（第一个函数），那么这将慢的是灾难！
# https://blog.csdn.net/yyw794/article/details/108859240
