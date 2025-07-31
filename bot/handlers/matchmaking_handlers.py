from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from core.db import User, get_db

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Greets the user and creates an account if one doesn't exist."""
    user_id = update.effective_user.id
    username = update.effective_user.username or "user"
    async for db in get_db():
        user = await db.get(User, user_id)
        if not user:
            new_user = User(telegram_id=user_id, username=username)
            db.add(new_user)
            await db.commit()
            await update.message.reply_text("🎲 Welcome to Yeab Game Zone! Your account has been created.")
        else:
            await update.message.reply_text(f"Welcome back to Yeab Game Zone, {username}!\nUse /play to start a game.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Shows a help message."""
    help_text = (
        "Yeab Game Zone Commands:\n"
        "/play - Start a new Ludo game\n"
        "/deposit - Add funds to your wallet\n"
        "/withdraw - Request a withdrawal\n"
        "/balance - Check your current balance\n"
        "/help - Show this message"
    )
    await update.message.reply_text(help_text)

# ... Other matchmaking handlers ...