import asyncio
import websockets
import json
import random
import time
from python_socks.async_proxy import Proxy

# CONFIGURATION CORRIGÉE
USER_ID = "3BH76BUllivJeyCGEkbtTusgviT" 
PROXY_ADDR = "socks5://127.0.0.1:40001" # Port 40001 pour correspondre au YAML de Cloudflare
GRASS_WS_URL = "wss://proxy.wynd.network:4650/"

async def connect_to_grass():
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    proxy = Proxy.from_url(PROXY_ADDR)
    
    print(f"🚀 Démarrage du mode furtif pour l'ID : {USER_ID}")

    while True:
        try:
            # Passage par le proxy Cloudflare WARP
            async with proxy.connect(dest_host="proxy.wynd.network", dest_port=4650) as sock:
                async with websockets.client.connect(
                    GRASS_WS_URL,
                    sock=sock,
                    extra_headers={"User-Agent": user_agent}
                ) as ws:
                    print("✅ Connexion établie via Cloudflare WARP")
                    
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
                        print(f"💎 Heartbeat envoyé à {time.strftime('%H:%M:%S')} | Récolte de points active")
                        
                        # Délai aléatoire pour simuler une activité réelle
                        await asyncio.sleep(random.randint(15, 25))

        except Exception as e:
            print(f"⚠️ Erreur de connexion : {e}. Nouvelle tentative dans 30s...")
            await asyncio.sleep(30)

if __name__ == "__main__":
    try:
        asyncio.run(connect_to_grass())
    except KeyboardInterrupt:
        pass
