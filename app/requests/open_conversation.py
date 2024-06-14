
from simple_chatwoot import ChatWoot
import os

DOMAIN = os.getenv("CHATWOOT_DOMAIN")

def open_conversation(account_id, conversation_id, api_access_token, inbox_id):    
    API_ACCESS_TOKEN = api_access_token
    ACCOUNT_ID = account_id
    INBOX_ID = inbox_id
    chatwoot = ChatWoot(DOMAIN, API_ACCESS_TOKEN, ACCOUNT_ID, INBOX_ID)
    status = chatwoot.toggle_conversation_status(conversation_id, 'open')
    return status

def close_conversation(account_id, conversation_id, api_access_token, inbox_id):
    API_ACCESS_TOKEN = api_access_token
    ACCOUNT_ID = account_id
    INBOX_ID = inbox_id
    chatwoot = ChatWoot(DOMAIN, API_ACCESS_TOKEN, ACCOUNT_ID, INBOX_ID)
    status = chatwoot.toggle_conversation_status(conversation_id, 'close')
    return status