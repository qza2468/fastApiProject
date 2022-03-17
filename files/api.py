from fastapi import APIRouter, File, HTTPException, Header, UploadFile
from pydantic import BaseModel
from fastapi.responses import FileResponse, Response

import os.path
import os

# TODO: never allow to create a file when the file is existed. VERY IMPORTANT!!!!!!
# TODO: if you meant to do that, you need delete it manually first and ```try``` create.

ROOT_PATH = "/home/qza2468"

class FileInfo(BaseModel):
    filepath: str

router = APIRouter()

def transfer_file_path(filepath: str):
    abs_path = os.path.abspath(os.path.join(ROOT_PATH, filepath))
    if os.path.commonprefix([abs_path, ROOT_PATH]) != ROOT_PATH:
        raise HTTPException(status_code=404, detail="error file path")

    return abs_path

@router.post("/files/")
async def get_file(fileinfo: FileInfo):
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
                      file_where: str = Header(None)):
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
async def create_dir(dir_where: str = Header(None)):
    abs_path = transfer_file_path(dir_where)
    try:
        os.mkdir(abs_path)
    except FileExistsError:
        raise HTTPException(status_code=404, detail="path exists")
    return Response(status_code=200)

@router.post("/files/ls/")
async def ls_dir(dirinfo: FileInfo):
    abs_path = transfer_file_path(dirinfo.filepath)

    if not os.path.exists(abs_path):
        raise HTTPException(status_code=404, detail="path no exists")
    elif os.path.isdir(abs_path):
        res = {}
        for file_name in os.listdir(abs_path):
            abs_file_path = os.path.join(abs_path, file_name)
            if os.path.isfile(abs_file_path):
                res[file_name] = "file"
            elif os.path.isdir(abs_file_path):
                res[file_name] = "dir"

        return res
    else:
        raise HTTPException(status_code=404, detail="path point to not a dir")

@router.post("/files/unlink")
async def unlink_file(fileinfo: FileInfo):
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


@router.get("/files/hello/")
async def root():
    return {"message": "Hello World"}