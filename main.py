from fastapi import FastAPI
import login.api

app = FastAPI()

app.include_router(login.api.router, prefix="/api")


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
