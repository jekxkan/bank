from src.db.models import ClientInfo
from src.db.service import service


class MainFunctions:
    """
    Базовый класс для общих функций пользователя и администратора

    Предоставляет метод для получения информации о себе
    """
    def __init__(self, email: str):
        self.email = email

    def get_info(self) -> ClientInfo | None:
        """
        Получает информацию о пользователе из базы данных

        Returns:
            ClientInfo | None: информация о пользователе,
            если пользователь найден, иначе None.
        """
        info = service.get_info_about_yourself(self.email)
        return info