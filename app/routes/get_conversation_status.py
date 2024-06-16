from fastapi import APIRouter, Query, HTTPException
import httpx
import os

router = APIRouter()

CHATWOOT_BASE_URL = os.getenv("CHATWOOT_BASE_URL")
CHATWOOT_API_KEY = os.getenv("CHATWOOT_API_KEY")
ACCOUNT_ID = os.getenv("ACCOUNT_ID")

@router.get("/get_conversation_status")
async def get_conversation_status(phone_number: str = Query(..., description="Phone number to get conversation status for")):
    headers = _create_headers()
    contact_id = await _get_contact_id(phone_number, headers)
    status = await _get_latest_conversation_status(contact_id, headers)
    return {"phone_number": phone_number, "status": status}

def _create_headers():
    return {
        "api_access_token": f"{CHATWOOT_API_KEY}",
        "Content-Type": "application/json"
    }

async def _get_contact_id(phone_number: str, headers: dict) -> str:
    search_url = f"{CHATWOOT_BASE_URL}/accounts/{ACCOUNT_ID}/contacts/search?q={phone_number}"

    async with httpx.AsyncClient() as client:
        response = await client.get(search_url, headers=headers)
        _handle_response_errors(response, "Failed to retrieve contact from Chatwoot")

        contact_data = response.json()
        if not contact_data or "payload" not in contact_data or not contact_data["payload"]:
            raise HTTPException(status_code=404, detail="Contact not found")

        return contact_data["payload"][0]["id"]

async def _get_latest_conversation_status(contact_id: str, headers: dict) -> str:
    conversations_url = f"{CHATWOOT_BASE_URL}/accounts/{ACCOUNT_ID}/contacts/{contact_id}/conversations"

    async with httpx.AsyncClient() as client:
        response = await client.get(conversations_url, headers=headers)
        _handle_response_errors(response, "Failed to retrieve conversations from Chatwoot")

        conversations_data = response.json()
        if not conversations_data or not conversations_data["payload"]:
            raise HTTPException(status_code=404, detail="No conversations found for this contact")

        latest_conversation = conversations_data["payload"][0]
        return latest_conversation["status"]

def _handle_response_errors(response, error_message: str):
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=error_message)