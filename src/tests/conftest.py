from decimal import Decimal

import pytest
from sqlalchemy import delete
from sqlalchemy.dialects.postgresql import insert

from src.db.models import AccountInfo, Transaction
from src.db.service import Service


@pytest.fixture()
def service():
    """
    Фикстура, предоставляющая экземпляр класса Service

    Используется в тестах для сервиса базы данных
    """
    return Service()


@pytest.fixture
def test_user_data() -> dict:
    """
    Фикстура, предоставляющая тестовые данные пользователя

    Returns:
        test_user_data(dict): словарь, содержащий тестовые данных пользователя
    """
    test_user_data = {
        "email": "test@mail.com",
        "password": "test",
        "full_name": "Test User"
    }

    return test_user_data


@pytest.fixture
def test_account_data() -> dict:
    """
    Фикстура, предоставляющая тестовы данные счета

    Returns:
        test_account_data(dict): словарь, содержащий тестовые данные счета
    """
    test_account_data = {
        "user_id": 20,
        "account_id": 123,
        "balance": Decimal(100),
    }

    return test_account_data


@pytest.fixture
def test_webhook_data():
    """
    Фикстура, предоставляющая тестовые данные вебхука

    Returns:
        test_webhook_data(dict): словарь, содержащий тестовые данные вебхука
    """
    test_webhook_data = {
            "transaction_id": "test_transaction_id",
            "user_id": 1,
            "account_id": 123,
            "amount": Decimal(50),
        }

    return test_webhook_data


async def create_account(data: dict):
    """
    Асинхронно создает новый счет в базе данных

    Args:
        data(dict): словарь, содержащий информацию о счете
    """
    session = Service().session
    stmt = (
        insert(AccountInfo)
        .values(user_id=data["user_id"],
                balance=data["balance"]
        )
    )
    await session.execute(stmt)
    await session.commit()


async def delete_account(data: int):
    """
    Асинхронно удаляет счет из базы данных по ID

    Args:
        data(int): ID счета, который нужно удалить
    """
    session = Service().session
    stmt = (
        delete(AccountInfo)
        .where(AccountInfo.account_id == data)
    )
    await session.execute(stmt)
    await session.commit()


async def delete_transaction(data: str):
    """
    Асинхронно удаляет платеж из базы данных по его ID

    Args:
        data(str): ID платежа, который нужно удалить
    """
    session = Service().session
    stmt = (
        delete(Transaction)
        .where(Transaction.transaction_id == data)
    )
    await session.execute(stmt)
    await session.commit()
