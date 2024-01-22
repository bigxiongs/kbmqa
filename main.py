import uvicorn
from fastapi import FastAPI

from routers import *

app = FastAPI()
app.include_router(token.router)
app.include_router(dialogue.router)
app.include_router(graph.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


def main():
    uvicorn.run("main:app", reload=True)


if __name__ == "__main__":
    main()
