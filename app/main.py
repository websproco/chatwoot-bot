from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello Jebbitizer Helperr"}

@app.post("/bot")
async def post_bot(request: Request):
    print("#### Bot received ####")
    body = await request.json()
    print("#### Bot received ####")
    print(body)
    return JSONResponse(content={"message": "Bot received"})