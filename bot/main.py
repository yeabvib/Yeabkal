import logging
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters

from core.config import settings
from bot.handlers import matchmaking_handlers, finance_handlers, gameplay_handlers

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

def create_application() -> Application:
    """Creates and configures the Telegram Bot Application."""
    application = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()

    # Register all handlers from their respective modules
    application.add_handler(CommandHandler("start", matchmaking_handlers.start))
    application.add_handler(CommandHandler("help", matchmaking_handlers.help_command))
    application.add_handler(CommandHandler("play", matchmaking_handlers.play_command))
    application.add_handler(CommandHandler("balance", finance_handlers.balance_command))

    application.add_handler(finance_handlers.deposit_conversation_handler())
    application.add_handler(finance_handlers.withdraw_conversation_handler())

    application.add_handler(CallbackQueryHandler(matchmaking_handlers.play_button_handler, pattern=r"^play_"))
    application.add_handler(CallbackQueryHandler(matchmaking_handlers.join_game_handler, pattern=r"^join_game_"))
    application.add_handler(CallbackQueryHandler(gameplay_handlers.roll_dice_handler, pattern=r"^roll_"))
    application.add_handler(CallbackQueryHandler(gameplay_handlers.move_token_handler, pattern=r"^move_"))

    return application

application = create_application()