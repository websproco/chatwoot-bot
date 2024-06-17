from fastapi import APIRouter, Body, HTTPException
from pydantic import BaseModel, Field
import httpx
import os
from simple_chatwoot import ChatWoot
from typing import Optional


router = APIRouter()

CHATWOOT_BASE_URL = os.getenv("CHATWOOT_BASE_URL")
CHATWOOT_API_KEY = os.getenv("CHATWOOT_API_KEY")
ACCOUNT_ID = os.getenv("ACCOUNT_ID")
DOMAIN = os.getenv("CHATWOOT_DOMAIN")
INBOX_ID = os.getenv("CHATWOOT_INBOX_ID")

class AssignConversationRequest(BaseModel):
    phone_number: str = Field(..., description="Phone number to assign conversation for")
    assignee_id: Optional[int] = Field(None, description="Optional team or agent ID to assign the conversation to")
    assignee_type: Optional[str] = Field(None, description="Optional type of assignee: 'agent' or 'team'")

@router.post("/assign_conversation")
async def assign_conversation(request: AssignConversationRequest):
    headers = _create_headers()
    contact_id = await _get_contact_id(request.phone_number, headers)
    conversation_id = await _get_latest_conversation_id(contact_id, headers)            

    _open_conversation(ACCOUNT_ID, conversation_id, CHATWOOT_API_KEY, INBOX_ID)

    if request.assignee_id is not None and request.assignee_type:
        await _assign_conversation(conversation_id, request.assignee_id, request.assignee_type, headers)
        if request.assignee_type == 'team':
            await _assign_conversation(conversation_id, 0, 'agent', headers)

    return {
        "phone_number": request.phone_number,
        "conversation_id": conversation_id,
        "assigned_to": request.assignee_id,
        "assignee_type": request.assignee_type
    }

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

async def _get_latest_conversation_id(contact_id: str, headers: dict) -> str:
    conversations_url = f"{CHATWOOT_BASE_URL}/accounts/{ACCOUNT_ID}/contacts/{contact_id}/conversations"

    async with httpx.AsyncClient() as client:
        response = await client.get(conversations_url, headers=headers)
        _handle_response_errors(response, "Failed to retrieve conversations from Chatwoot")

        conversations_data = response.json()
        if not conversations_data or not conversations_data["payload"]:
            raise HTTPException(status_code=404, detail="No conversations found for this contact")

        latest_conversation = conversations_data["payload"][0]
        return latest_conversation["id"]

async def _assign_conversation(conversation_id: str, assignee_id: Optional[int], assignee_type: Optional[str], headers: dict):
    assign_url = f"{CHATWOOT_BASE_URL}/accounts/{ACCOUNT_ID}/conversations/{conversation_id}/assignments"

    payload = {}
    if assignee_type == 'agent':
        payload = {"assignee_id": assignee_id}
    elif assignee_type == 'team':
        payload = {"team_id": assignee_id}
    else:
        raise HTTPException(status_code=400, detail="Invalid assignee type. Must be 'agent' or 'team'.")

    async with httpx.AsyncClient() as client:
        response = await client.post(assign_url, json=payload, headers=headers)
        _handle_response_errors(response, "Failed to assign the conversation")

def _handle_response_errors(response, error_message: str):
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=error_message)

def _open_conversation(account_id, conversation_id, api_access_token, inbox_id):
    chatwoot = ChatWoot(DOMAIN, api_access_token, account_id, inbox_id)
    status = chatwoot.toggle_conversation_status(conversation_id, 'open')
    if not status:
        raise HTTPException(status_code=500, detail="Failed to open the conversation")