"""
Telethon ↔ n8n Bridge (clean version using env_config)
"""

# Auto-install required packages if missing
import sys
import subprocess
import importlib.util

required = ["httpx", "fastapi", "pydantic", "telethon", "uvicorn"]

for pkg in required:
    if importlib.util.find_spec(pkg) is None:
        print(f"Installing missing package: {pkg}")
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])

import asyncio
import logging
from typing import Optional
import httpx
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from telethon import TelegramClient, events
from telethon.sessions import StringSession

from env_config import (
    API_ID, API_HASH, TG_SESSION,
    N8N_WEBHOOK_URL, API_AUTH_TOKEN,
    LISTEN_HOST, LISTEN_PORT,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("telethon_n8n_bridge")

app = FastAPI(title="Telethon ↔ n8n Bridge", version="1.0.0")
telegram_client: Optional[TelegramClient] = None

class SendMessage(BaseModel):
    chat_id: str
    text: str

@app.post("/send", summary="Send a Telegram message via personal account")
async def send(msg: SendMessage, token: str = Query(...)):
    if token != API_AUTH_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid token")
    if telegram_client is None or not await telegram_client.is_connected():
        raise HTTPException(status_code=503, detail="Telegram client not ready")
    try:
        await telegram_client.send_message(msg.chat_id, msg.text)
        return {"ok": True}
    except Exception as exc:
        logger.exception("Failed to send message")
        raise HTTPException(status_code=500, detail=str(exc))

async def bootstrap_telegram() -> TelegramClient:
    session = StringSession(TG_SESSION) if TG_SESSION else StringSession()
    client = TelegramClient(session, API_ID, API_HASH)
    await client.start()

    if not TG_SESSION:
        print("★ Your Telegram StringSession → copy & store as TG_SESSION:")
        print(client.session.save())

    @client.on(events.NewMessage(incoming=True))
    async def _(event):
        if not N8N_WEBHOOK_URL:
            return
        payload = {
            "message_id": event.id,
            "chat_id": event.chat_id,
            "sender_id": event.sender_id,
            "text": event.raw_text,
            "date": event.date.isoformat(),
        }
        try:
            async with httpx.AsyncClient(timeout=10) as http:
                await http.post(N8N_WEBHOOK_URL, json=payload)
        except Exception as exc:
            logger.warning("POST → n8n failed: %s", exc)

    return client

async def _serve():
    global telegram_client
    telegram_client = await bootstrap_telegram()

    import uvicorn
    config = uvicorn.Config(app, host=LISTEN_HOST, port=LISTEN_PORT, loop="asyncio", log_level="info")
    server = uvicorn.Server(config)

    try:
        await asyncio.gather(
            telegram_client.run_until_disconnected(),
            server.serve()
        )
    finally:
        # clean up if interrupted
        if telegram_client:
            await telegram_client.disconnect()


if __name__ == "__main__":
    try:
        asyncio.run(_serve())
    except KeyboardInterrupt:
        print("← Shutdown requested – bye!")

