import pytest

from src.db.service import Service
from src.tests.conftest import delete_transaction


@pytest.mark.asyncio
async def test_process_webhook(service: Service, test_user_data: dict,
                               test_webhook_data: dict):
    """
    Тест для вебхука

    Args:
        service(Service): экземпляр класса Service для взаимодействия
        с базой данных
        test_user_data(dict): тестовые данные пользователя
        test_webhook_data(dict): тестовые данные хука
    """
    await service.create_user(test_user_data)
    result = await service.process_webhook(test_webhook_data)
    assert "Транзакция с id test_transaction_id проведена" in result["status"]

    result = await service.process_webhook(test_webhook_data)
    assert 'Ошибка' in result["status"]

    await delete_transaction(test_webhook_data["transaction_id"])
    await service.delete_user(test_user_data["email"])


