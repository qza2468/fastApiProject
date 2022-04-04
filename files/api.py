from fastapi import APIRouter, File, HTTPException, Header, UploadFile, Depends
from pydantic import BaseModel
from fastapi.responses import FileResponse, Response

import os.path
import os
import stat
import sys

parent_dir_name = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parent_dir_name)
from login import api as loginapi

# TODO: never allow to create a file when the file is existed. VERY IMPORTANT!!!!!!
# TODO: if you meant to do that, you need delete it manually first and ```try``` create.

ROOT_PATH = "/home/qza2468"

class FileInfo(BaseModel):
    filepath: str

router = APIRouter()

def transfer_file_path(filepath: str):
    filepath = "./" + filepath # fix an error
    abs_path = os.path.abspath(os.path.join(ROOT_PATH, filepath))
    if os.path.commonprefix([abs_path, ROOT_PATH]) != ROOT_PATH:
        raise HTTPException(status_code=404, detail="error file path")

    return abs_path

@router.post("/files/get")
async def get_file(fileinfo: FileInfo,
                   username: str = Depends(loginapi.check_cookie_depend)):
    if username != "qza2468":
        raise HTTPException(status_code=401)
    abs_path = transfer_file_path(fileinfo.filepath)

    if not os.path.exists(abs_path):
        raise HTTPException(status_code=404, detail="path no exists")
    elif os.path.isfile(abs_path):
        return FileResponse(abs_path)
    elif os.path.isdir(abs_path):
        raise HTTPException(status_code=404, detail="path point to dir")
    else:
        raise HTTPException(status_code=404, detail="path point to not a dir or file")

@router.post("/files/create/")
async def create_file(file_content: UploadFile = File(...),
                      file_where: str = Header(None),
                      username: str = Depends(loginapi.check_cookie_depend)):
    if username != "qza2468":
        raise HTTPException(status_code=401)
    abs_path = transfer_file_path(file_where)
    try:
        with open(abs_path, "x") as file_object:
            file_object.write(file_content.file.read())
    except FileExistsError:
        raise HTTPException(status_code=404, detail="file exists")
    except:
        raise HTTPException(status_code=404, detail="upload error")

    return Response(status_code=200)

@router.post("files/mkdir")
async def create_dir(dir_where: str = Header(None),
                     username: str = Depends(loginapi.check_cookie_depend)):
    if username != "qza2468":
        raise HTTPException(status_code=401)
    abs_path = transfer_file_path(dir_where)
    try:
        os.mkdir(abs_path)
    except FileExistsError:
        raise HTTPException(status_code=404, detail="path exists")
    return Response(status_code=200)

@router.post("/files/ls/")
async def ls_dir(dirinfo: FileInfo,
                 username: str = Depends(loginapi.check_cookie_depend)):
    if username != "qza2468":
        raise HTTPException(status_code=401, detail="you have no right")
    abs_path = transfer_file_path(dirinfo.filepath)

    res = {}

    try:
        file_names = os.listdir(abs_path)
        file_names.append(".") # add the directory info to res.
        for file_name in file_names:
            abs_file_path = os.path.join(abs_path, file_name)
            try:
                file_stat = os.stat(abs_file_path)
            except FileNotFoundError:
                continue

            res[file_name] = {
                "st_mode": file_stat.st_mode,
                "st_nlink": file_stat.st_nlink,
                "st_uid": file_stat.st_uid,
                "st_gid": file_stat.st_gid,
                "st_size": file_stat.st_size,
                "st_atime": file_stat.st_atime,
                "st_mtime": file_stat.st_mtime,
                "st_ctime": file_stat.st_ctime,
            }
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="path no exists")
    except NotADirectoryError:
        raise HTTPException(status_code=404, detail="path not point to a dir")

    return res

@router.post("files/ls_file")
async def ls_file(fileinfo: FileInfo,
                  username: str = Depends(loginapi.check_cookie_depend)):
    if username != "qza2468":
        raise HTTPException(status_code=401)
    abs_path = transfer_file_path(fileinfo.filepath)
    try:
        file_stat = os.stat(abs_path)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="path not exists")

    return {
                "st_mode": file_stat.st_mode,
                "st_nlink": file_stat.st_nlink,
                "st_uid": file_stat.st_uid,
                "st_gid": file_stat.st_gid,
                "st_size": file_stat.st_size,
                "st_atime": file_stat.st_atime,
                "st_mtime": file_stat.st_mtime,
                "st_ctime": file_stat.st_ctime,
            }

@router.post("/files/unlink")
async def unlink_file(fileinfo: FileInfo,
                      username: str = Depends(loginapi.check_cookie_depend)):
    if username != "qza2468":
        raise HTTPException(status_code=401)
    abs_path = transfer_file_path(fileinfo.filepath)
    if os.path.samefile(abs_path, ROOT_PATH):
        raise HTTPException(status_code=404, detail="error file path")

    if not os.path.exists(abs_path):
        pass
    elif os.path.isfile(abs_path):
        os.unlink(abs_path)
    elif os.path.isdir(abs_path):
        os.rmdir(abs_path)
    else:
        raise HTTPException(status_code=404, detail="path point to no file or dir")
    return Response(status_code=200)
