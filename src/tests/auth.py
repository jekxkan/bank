import pytest

from src.db.service import Service


@pytest.mark.asyncio
async def test_login(service: Service, test_user_data: dict):
    """
    Тест для авторизации пользователя

    Args:
        service(Service): экземпляр класса Service для взаимодействия
        с базой данных
        test_user_data(dict): тестовые данные пользователя
    """
    await service.create_user(test_user_data)
    login_success = await service.login(test_user_data["email"],
                                        test_user_data["password"])
    assert login_success["status"] is True
    login_fail_password = await service.login(test_user_data["email"],
                                              "badpassword")
    assert login_fail_password["status"] is False
    login_fail_email = await service.login("iamnotexist@mail.com",
                                           test_user_data["password"])
    assert login_fail_email["status"] is False
    await service.delete_user(test_user_data["email"])