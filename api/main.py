import logging
import httpx
from fastapi import FastAPI, Request, Response, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from telegram import Update

from core.config import settings
from core.db import get_db, User, Transaction, TransactionStatus
from bot.main import application

app = FastAPI()
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def on_startup():
    """Set webhook on startup."""
    webhook_url = f"{settings.WEBHOOK_URL}/api/telegram"
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/setWebhook?url={webhook_url}")
        if response.status_code == 200:
            logger.info(f"Webhook set to {webhook_url}")
        else:
            logger.error(f"Failed to set webhook: {response.text}")

@app.post("/api/telegram")
async def telegram_webhook(request: Request):
    """Handle incoming Telegram updates."""
    data = await request.json()
    update = Update.de_json(data, application.bot)
    await application.process_update(update)
    return Response(status_code=200)

@app.post("/api/chapa/webhook")
async def chapa_webhook(request: Request, db: AsyncSession = Depends(get_db)):
    """Handle Chapa payment notifications."""
    data = await request.json()
    logger.info(f"Chapa webhook received: {data}")

    if data.get("status") == "success":
        tx_ref = data.get("tx_ref")
        if not tx_ref:
            raise HTTPException(status_code=400, detail="tx_ref missing")

        transaction = await db.get(Transaction, {"tx_ref": tx_ref}) # Simplified
        if transaction and transaction.status == TransactionStatus.PENDING:
            transaction.status = TransactionStatus.COMPLETED
            user = await db.get(User, transaction.user_id)
            if user:
                user.balance += transaction.amount
                await db.commit()
                await application.bot.send_message(
                    chat_id=user.telegram_id,
                    text=f"✅ Your deposit of {transaction.amount} ETB to Yeab Game Zone was successful!"
                )
    return Response(status_code=200)

@app.get("/health")
async def health_check():
    """Health check endpoint for Render."""
    return {"status": "ok"}