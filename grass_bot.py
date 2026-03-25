import asyncio
import websockets
import json
import random
import time

# CONFIGURATION FINALE AVEC TON TOKEN
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzYW50aWNoIjpkIiwidWlkIjo2ZWE4NmU4Yy1hMWI4LTRhMmItYmI4MC1lMmliMjcyNWZzIiwiaXNzIjoiZ3Jhc3MubmV0IiwidHlwZSI6ImNFUTVFUilsImlhdCI6MTc3NDQxMjgyNCwibmJmIjoxNzc0NDEyODI0LCJleHAiOjE4MDU1MTY4MjQsImF1ZCI6Ind5bmQubmV0dmsiLCJpc3MiOiJodHRwczovL3d5bmQubmV0YW1hZW09YXdzLmVnbnVsOndWJsaWMifQ.Q5W_ZArLkh5tz6mLjJVUE39QdJ8Ih9X1ktFd3f7aw9EHmhc3cLFrqJ0hMR3ZttthTL4UfF02EgVzNJslNbBXmmuuyaFob39gDHEGPMub"
WS_URL = "wss://proxy.wynd.network:4650/"

async def run_grass():
    user_agent = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36"
    print("🚀 Bot Grass démarré. Connexion au compte en cours...")

    while True:
        try:
            async with websockets.connect(
                WS_URL,
                extra_headers={
                    "User-Agent": user_agent,
                    "Authorization": f"Bearer {TOKEN}"
                }
            ) as ws:
                print("✅ Connecté au réseau Grass ! Vos points augmentent...")
                
                while True:
                    # Envoi d'un signal d'activité (Heartbeat)
                    heartbeat = {
                        "id": str(random.getrandbits(32)),
                        "action": "AUTH",
                        "data": {
                            "timestamp": int(time.time()),
                            "version": "4.20.2",
                            "origin_action": "EXT_LIFECYCLE"
                        }
                    }
                    await ws.send(json.dumps(heartbeat))
                    print(f"💎 Signal envoyé à {time.strftime('%H:%M:%S')} | Session active")
                    
                    # Pause réaliste entre 15 et 25 secondes
                    await asyncio.sleep(random.randint(15, 25))

        except Exception as e:
            print(f"⚠️ Reconnexion dans 60s : {e}")
            await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(run_grass())
