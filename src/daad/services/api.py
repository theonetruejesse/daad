from fastapi import FastAPI

API = FastAPI()


@API.get("/hello")
async def hello():
    return {"message": "Hello, World!"}
