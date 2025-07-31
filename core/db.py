import enum
from decimal import Decimal
from sqlalchemy import (
    create_engine, Column, Integer, String, BigInteger, Numeric, DateTime,
    ForeignKey, Enum as SQLAlchemyEnum
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.sql import func
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from .config import settings

# --- Async Setup ---
async_engine = create_async_engine(settings.DATABASE_URL, future=True, echo=False)
AsyncSessionLocal = sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)

async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

Base = declarative_base()

# --- Models ---
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False, index=True)
    username = Column(String)
    balance = Column(Numeric(10, 2), nullable=False, default=Decimal("0.00"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class GameStatus(str, enum.Enum):
    WAITING = "waiting"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FORFEITED = "forfeited"
    CANCELLED = "cancelled"

class Game(Base):
    __tablename__ = 'games'
    id = Column(Integer, primary_key=True)
    creator_id = Column(BigInteger, ForeignKey('users.telegram_id'))
    opponent_id = Column(BigInteger, ForeignKey('users.telegram_id'), nullable=True)
    stake = Column(Numeric(10, 2), nullable=False)
    win_condition = Column(Integer, nullable=False)
    status = Column(SQLAlchemyEnum(GameStatus), default=GameStatus.WAITING)
    game_state_json = Column(String, nullable=True)
    winner_id = Column(BigInteger, ForeignKey('users.telegram_id'), nullable=True)
    current_turn_player_id = Column(BigInteger, nullable=True)
    last_action_timestamp = Column(DateTime(timezone=True), server_default=func.now())
    message_id = Column(BigInteger)
    chat_id = Column(BigInteger)

class TransactionStatus(str, enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"

class TransactionType(str, enum.Enum):
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"

class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, ForeignKey('users.telegram_id'))
    tx_ref = Column(String, unique=True, nullable=False, index=True)
    amount = Column(Numeric(10, 2), nullable=False)
    type = Column(SQLAlchemyEnum(TransactionType))
    status = Column(SQLAlchemyEnum(TransactionStatus), default=TransactionStatus.PENDING)
    created_at = Column(DateTime(timezone=True), server_default=func.now())