from fastapi import FastAPI, Request, Query, HTTPException
from app.requests.pause_session import pause_session
from fastapi.middleware.cors import CORSMiddleware
from app.requests.open_session import open_session
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import pprint
import httpx
import os


load_dotenv()

CHATWOOT_BASE_URL = os.getenv("CHATWOOT_BASE_URL")
CHATWOOT_API_KEY = os.getenv("CHATWOOT_API_KEY")
ACCOUNT_ID = os.getenv("ACCOUNT_ID")

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


  # Replace with your actual account ID

@app.get("/get_conversation_status")
async def get_conversation_status(phone_number: str = Query(..., description="Phone number to get conversation status for")):
    headers = {
        "api_access_token": f"{CHATWOOT_API_KEY}",
        "Content-Type": "application/json"
    }

    # Construct the Chatwoot API URL for searching contacts
    search_url = f"{CHATWOOT_BASE_URL}/accounts/{ACCOUNT_ID}/contacts/search?q={phone_number}"

    async with httpx.AsyncClient() as client:
        # Make the request to get the contact ID
        response = await client.get(search_url, headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to retrieve contact from Chatwoot")

        contact_data = response.json()
        if not contact_data or "payload" not in contact_data or not contact_data["payload"]:
            raise HTTPException(status_code=404, detail="Contact not found")

        contact_id = contact_data["payload"][0]["id"]

        # Get the latest conversation status
        conversations_url = f"{CHATWOOT_BASE_URL}/accounts/{ACCOUNT_ID}/contacts/{contact_id}/conversations"
        response = await client.get(conversations_url, headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to retrieve conversations from Chatwoot")

        conversations_data = response.json()
        if not conversations_data or not conversations_data["payload"]:
            raise HTTPException(status_code=404, detail="No conversations found for this contact")

        latest_conversation = conversations_data["payload"][0]
        status = latest_conversation["status"]

        return {"phone_number": phone_number, "status": status}