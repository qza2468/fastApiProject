from fastapi import FastAPI

import quotes.api
import login.api
import files.api

app = FastAPI()

app.include_router(quotes.api.router, prefix="/api")
app.include_router(login.api.router, prefix="/api")
app.include_router(files.api.router, prefix="/api")