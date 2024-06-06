from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI

from app.routes import assistant_jebbitizer_code, identify_assets, jebbitizer_code, jebbitizer_code_v2
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
    return {"message": "Hello Jebbitizer Helper"}