import requests
import os

EVOLUTION_API_INSTANCE = os.getenv("EVOLUTION_API_INSTANCE")
EVOLUTION_API_URL = os.getenv("EVOLUTION_API_URL")
EVOLUTION_API_TOKEN = os.getenv("EVOLUTION_API_TOKEN")

def open_session(sender):
    url = f"{EVOLUTION_API_URL}/{EVOLUTION_API_INSTANCE}"
    payload = {
        "status": "opened",
        "remoteJid": sender,
    }
    headers = {
        "apikey": EVOLUTION_API_TOKEN,
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    print("#" * 50)
    print("Pause session response:")
    print(response.text)