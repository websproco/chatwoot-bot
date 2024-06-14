from simple_chatwoot import ChatWoot

def search_contacts(account_id, search_key, api_access_token):
    DOMAIN = "https://unitychat.webspro.co"
    API_ACCESS_TOKEN = api_access_token
    ACCOUNT_ID = account_id
    INBOX_ID = "2"
    chatwoot = ChatWoot(DOMAIN, API_ACCESS_TOKEN, ACCOUNT_ID, INBOX_ID)
    contacts = chatwoot.search_contacts(search_key)
    return contacts