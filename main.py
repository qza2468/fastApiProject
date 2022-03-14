from fastapi import FastAPI

import quotes.api

app = FastAPI()

app.include_router(quotes.api.router, prefix="/api")
