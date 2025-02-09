from decimal import Decimal
from typing import Optional

from sqlalchemy import Index, Integer, Numeric, String
from sqlalchemy.orm import Mapped, declarative_base, mapped_column


Base = declarative_base()

class ClientInfo(Base):
    """
    Модель клиента, представляющая собой запись в таблице clients_info
    """
    __tablename__ = "clients_info"

    user_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    email: Mapped[Optional[str]] = mapped_column(String(20), unique=True)
    password: Mapped[str] = mapped_column(String(20))
    full_name: Mapped[str] = mapped_column(String(50))

    __table_args__ = (Index("idx_user_id", "user_id",
                            postgresql_using="btree"),)


class AccountInfo(Base):
    """
    Модель счета клиента, представляющая собой запись в таблице accounts
    """
    __tablename__ = "accounts"

    account_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    user_id: Mapped[int] = mapped_column(Integer)
    balance: Mapped[Decimal] = mapped_column(Numeric)

    __table_args__ = (Index("idx_user_id_in_accounts", "user_id",
                            postgresql_using="btree"),)

class Transaction(Base):
    """
    Модель транзакции, представляющая собой запись в таблице transactions
    """
    __tablename__ = "transactions"

    transaction_id: Mapped[str] = mapped_column(
        String, primary_key=True
    )
    account_id: Mapped[int] = mapped_column(Integer)
    amount: Mapped[Decimal] = mapped_column(Numeric)
    user_id: Mapped[int] = mapped_column(Integer)

    __table_args__ = (Index("idx_account_id", "account_id",
                            postgresql_using="btree"),)