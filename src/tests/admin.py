import pytest
from sqlalchemy import select

from src.db.models import ClientInfo
from src.db.service import Service
from src.tests.conftest import create_account, delete_account


@pytest.mark.asyncio
async def test_check_if_user_exists(service: Service, test_user_data: dict):
    """
    Тест для проверки зарегестрирован ли пользователь

    Args:
        service(Service): экземпляр класса Service для взаимодействия
        с базой данных
        test_user_data(dict): тестовые данные пользователя
    """
    email = test_user_data["email"]
    result = await service.check_if_user_exists(email)
    assert result is None

    await service.create_user(test_user_data)
    result = await service.check_if_user_exists(email)
    assert result.email == email

    await service.delete_user(test_user_data["email"])


@pytest.mark.asyncio
async def test_create_user(service: Service, test_user_data: dict):
    """
    Тест для создания пользователя

    Args:
        service(Service): экземпляр класса Service для взаимодействия
        с базой данных
        test_user_data(dict): тестовые данные пользователя
    """
    new_user_name = await service.create_user(test_user_data)
    assert new_user_name == test_user_data["full_name"]

    existing_user = await service.create_user(test_user_data)
    assert "Пользователь с email" in existing_user["status"]

    await service.delete_user(test_user_data["email"])


@pytest.mark.asyncio
async def test_delete_user(service: Service, test_user_data: dict):
    """
    Тест для удаления пользователя

    Args:
        service(Service): экземпляр класса Service для взаимодействия
        с базой данных
        test_user_data(dict): тестовые данные пользователя
    """
    await service.create_user(test_user_data)
    delete_status = await service.delete_user(test_user_data["email"])
    assert "удален" in delete_status["status"]

    iamnotexist_status = await service.delete_user("iamnotexist@mail.com")
    assert "не зарегистрирован" in iamnotexist_status["status"]


@pytest.mark.asyncio
async def test_update_user(service: Service, test_user_data: dict):
    """
    Тест для обновления данных пользователя

    Args:
        service(Service): экземпляр класса Service для взаимодействия
        с базой данных
        test_user_data(dict): тестовые данные пользователя
    """
    await service.create_user(test_user_data)
    new_data = {"password": "newpassword", "full_name": "Updated Name"}
    update_status = await service.update_user(test_user_data["email"],
                                              new_data)
    assert "Новые данные пользователя" in update_status["status"]

    no_change_data = {"password": "newpassword", "full_name": "Updated Name"}
    no_change_status = await service.update_user(test_user_data["email"],
                                                 no_change_data)
    assert ("Все поля пользователя остались прежними" in
            no_change_status["status"])

    iamnotexist_status = await service.update_user("iamnotexist@example.com",
                                                   new_data)
    assert "не зарегистрирован" in iamnotexist_status["status"]

    await service.delete_user(test_user_data["email"])


@pytest.mark.asyncio
async def test_get_users_list(service: Service, test_user_data: dict):
    """
    Тест для получения списка пользователей

    Args:
        service(Service): экземпляр класса Service для взаимодействия
        с базой данных
        test_user_data(dict): тестовые данные пользователя
    """
    users_list = await service.get_users_list()
    if isinstance(users_list, dict):
        assert "Ни одного" in users_list["status"]
    else:
        await service.create_user(test_user_data)
        users_list = await service.get_users_list()
        assert isinstance(users_list, list)
        assert any([user["email"] == test_user_data["email"]
                    for user in users_list])

        await service.delete_user(test_user_data["email"])


@pytest.mark.asyncio
async def test_get_users_accounts(service: Service, test_user_data: dict,
                                  test_account_data: dict):
    """
    Тест для получения счетов пользователя

    Args:
        service(Service): экземпляр класса Service для взаимодействия
        с базой данных
        test_user_data(dict): тестовые данные пользователя
        test_account_data(dict): тестовые данные счета
    """
    email = test_user_data["email"]
    iamnotexist_accounts = await (service
                                  .get_users_accounts("iamnotexist@example.com"))
    assert "не зарегистрирован" in iamnotexist_accounts["status"]

    await service.create_user(test_user_data)
    get_user_id_stmt = (
        select(ClientInfo.user_id)
        .where(ClientInfo.email == email)
    )
    no_accounts = await service.get_users_accounts(email)
    assert "нет счетов" in no_accounts["status"]
    await service.delete_user(email)

    await service.create_user(test_user_data)
    user_id = (await service.session.execute(get_user_id_stmt)).scalar()
    test_account_data["user_id"] = user_id
    await create_account(test_account_data)
    accounts = await service.get_users_accounts(email)
    assert isinstance(accounts, list)
    assert any([account["user_id"] == test_account_data["user_id"]
                for account in accounts])

    await delete_account(test_account_data["account_id"])
    await service.delete_user(test_user_data["email"])