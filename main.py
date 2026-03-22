import asyncio
import uuid
import json
import os
from websockets.client import connect
from flask import Flask
from threading import Thread

# --- CONFIGURATION AUTOMATIQUE ---
USER_ID = "3BH76BU1IivJeyCGEKbtTusgviT"

app = Flask('')
@app.route('/')
def home(): return "Robot Grass de Namolo en cours..."

async def connect_to_wss():
    device_id = str(uuid.uuid4())
    print(f"[*] Connexion avec l'ID : {device_id}")
    while True:
        try:
            async with connect("wss://proxy.wynd.network:4650/", user_agent_header="Mozilla/5.0") as websocket:
                auth_msg = {
                    "id": str(uuid.uuid4()),
                    "origin_action": "AUTH",
                    "result": {
                        "browser_id": device_id,
                        "user_id": USER_ID,
                        "user_agent": "Mozilla/5.0",
                        "timestamp": 1234567,
                        "version": "2.5.0"
                    }
                }
                await websocket.send(json.dumps(auth_msg))
                print("[+] Connecté à Grass ! Gain en cours...")
                while True:
                    response = await websocket.recv()
                    print("[*] Ping reçu du serveur")
        except Exception as e:
            print(f"[!] Erreur : {e}. Nouvel essai dans 10s...")
            await asyncio.sleep(10)

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    Thread(target=run).start()
    asyncio.run(connect_to_wss())
