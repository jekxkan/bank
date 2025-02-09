from src.db.service import service
from src.roles.for_all import MainFunctions


class Admin(MainFunctions):
    """
    Класс, который предоставляет методы для управления пользователями

    Наследуется от MainFunctions и использует сервисный класс
    для выполнения операций с пользователями
    """
    def create_user(self, data: dict) -> dict|str:
        """
        Создает нового пользователя с заданными данными

        Args:
            data(dict): словарь, содержащий информацию о пользователе

        Returns:
            dict|str: возвращает результат создания пользователя,
            который содержит информацию о новом пользователе
            или сообщение об ошибке
        """
        return service.create_user(data)

    def delete_user(self, email: str) -> dict:
        """
        Удаляет пользователя по указанному email

        Args:
            email(str): email пользователя, которого необходимо удалить

        Returns:
            dict: словарь, содержащий статус удаления пользователя
        """
        return service.delete_user(email)

    def update_user(self, user_email: str, data: dict) -> dict:
        """
        Обновляет информацию о пользователе с указанным email

        Аrgs:
            user_email(str): email пользователя, которого необходимо обновить
            data(dict): словарь, содержащий новую информацию для пользователя

        Returns:
            dict: словарь, содержащий статус обновления пользователя
        """
        return service.update_user(user_email, data)

    def get_users(self) -> list[dict] | dict:
        """
        Получает список всех пользователей

        Returns:
            list[dict] | dict: Список словарей с информацией о пользователях
            или словарь с сообщением о том,
            что пользователи не зарегистрированы
        """
        return service.get_users_list()

    def get_users_accounts(self, email: str) -> list[dict] | dict:
        """
        Получает список счетов для пользователя с указанным email

        Args:
            email(str): email пользователя

        Returns:
            list[dict] | dict: Список словарей с информацией о счетах
            пользователя или словарь с сообщением о том,
            что у пользователя нет счетов
        """
        return service.get_users_accounts(email)