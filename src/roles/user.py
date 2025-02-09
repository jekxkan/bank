from src.db.service import service
from src.roles.for_all import MainFunctions


class User(MainFunctions):
    """
    Класс, представляющий пользователя и его функции

    Наследуется от MainFunctions и предоставляет методы для
    получения информации о счетах и транзакциях пользователя
    """
    def get_your_accounts_and_balances(self) -> list[dict] | dict:
        """
        Получает список счетов и балансов для текущего пользователя

        Returns:
            list[dict] | dict: список словарей, где каждый словарь содержит
            информацию о счете и балансе,
            или словарь с сообщением об ошибке, если информация не найдена
        """
        return service.get_accounts_and_balances(email=self.email)

    def get_your_transactions(self) -> list[dict] | dict:
        """
        Получает список платежей для текущего пользователя

        Returns:
            list[dict] | dict: список словарей, где каждый словарь содержит
            информацию о платежах, или словарь с сообщением об ошибке,
            если информация не найдена
        """
        return service.get_transactions(email=self.email)