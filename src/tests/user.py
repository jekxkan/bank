import pytest

from src.db.service import Service
from src.tests.conftest import create_account, delete_account


@pytest.mark.asyncio
async def test_get_info_about_yourself(service: Service, test_user_data: dict):
    """
    Тест для получения информации о себе

    Args:
        service(Service): экземпляр класса Service для взаимодействия
        с базой данных
        test_user_data(dict): тестовые данные пользователя
    """
    await service.create_user(test_user_data)
    user_info = await service.get_info_about_yourself(test_user_data["email"])
    assert user_info.email == test_user_data["email"]
    assert user_info.full_name == test_user_data["full_name"]

    await service.delete_user(test_user_data["email"])


@pytest.mark.asyncio
async def test_get_accounts_and_balances(service: Service,
                                         test_user_data: dict,
                                         test_account_data):
    """
    Тест для получения счетов и балансов

    Args:
        service(Service): экземпляр класса Service для взаимодействия
        с базой данных
        test_user_data(dict): тестовые данные пользователя
        test_account_data(dict): тестовые данные счета
    """
    await service.create_user(test_user_data)
    await create_account(test_account_data)
    accounts = await service.get_accounts_and_balances(test_user_data["email"])
    await service.delete_user(test_user_data["email"])
    type = isinstance(accounts, list)
    if type:
        assert any([account["account_id"] == test_account_data["account_id"]
                    for account in accounts])
    else:
        assert 'нет счетов' in accounts['status']

    await delete_account(test_account_data["account_id"])
