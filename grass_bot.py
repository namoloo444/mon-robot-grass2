import asyncio
import websockets
import json
import random
import time

# CONFIGURATION SANS PROXY
USER_ID = "3BH76BUllivJeyCGEkbtTusgviT" 
GRASS_WS_URL = "wss://proxy.wynd.network:4650/"

async def connect_to_grass():
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    print(f"🚀 Démarrage en CONNEXION DIRECTE pour l'ID : {USER_ID}")

    while True:
        try:
            async with websockets.client.connect(
                GRASS_WS_URL,
                extra_headers={"User-Agent": user_agent}
            ) as ws:
                print("✅ Connexion établie avec le réseau Grass !")
                
                while True:
                    auth_payload = {
                        "id": str(random.getrandbits(32)),
                        "action": "AUTH",
                        "data": {
                            "user_id": USER_ID,
                            "user_agent": user_agent,
                            "timestamp": int(time.time()),
                            "version": "4.20.2",
                            "origin_action": "EXT_LIFECYCLE"
                        }
                    }
                    await ws.send(json.dumps(auth_payload))
                    print(f"💎 Heartbeat envoyé à {time.strftime('%H:%M:%S')} | Points en cours...")
                    await asyncio.sleep(random.randint(15, 25))

        except Exception as e:
            print(f"⚠️ Tentative de reconnexion dans 30s... ({e})")
            await asyncio.sleep(30)

if __name__ == "__main__":
    asyncio.run(connect_to_grass())
