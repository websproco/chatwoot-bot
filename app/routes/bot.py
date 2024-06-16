from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
import pprint

from app.requests.pause_session import pause_session
from app.requests.open_session import open_session

router = APIRouter()

@router.post("/bot")
async def post_bot(request: Request):
    print("#### Bot received ####")
    try:
        body = await request.json()
        print("#### Bot received ####")
        pprint.pprint(body, depth=2)

        event = body.get("event")

        if event == "conversation_opened":
            meta = body.get("meta")
            sender = meta.get("sender")
            identifier = sender.get("identifier")

            # change session status to opened
            pause_session(identifier)

        if event == "conversation_resolved":
            meta = body.get("meta")
            sender = meta.get("sender")
            identifier = sender.get("identifier")

            open_session(identifier)
    except Exception as e:
        print("#### Error ####")
        print(e)
    
    return JSONResponse(content={"message": "Bot received"})