import os
from decimal import Decimal
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Telegram
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    WEBHOOK_URL: str = os.getenv("WEBHOOK_URL", "")
    BOT_OWNER_ID: int = int(os.getenv("BOT_OWNER_ID", 0))

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")

    # Payment Gateway
    CHAPA_API_KEY: str = os.getenv("CHAPA_API_KEY", "")
    CHAPA_API_URL: str = "https://api.chapa.co/v1"

    # Game Rules
    MIN_DEPOSIT: Decimal = Decimal("20.00")
    COMMISSION_RATE: Decimal = Decimal("0.10") # 10%
    FORFEIT_WARNING_SECONDS: int = 60
    FORFEIT_DEADLINE_SECONDS: int = 90

    # Ensure critical variables are set
    if not TELEGRAM_BOT_TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN environment variable not set")
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL environment variable not set")

settings = Settings()