from sanic import Blueprint, Request, json

from src.db.serialization import MyInfoSchema
from src.roles.user import User


user_bp = Blueprint('user_route', url_prefix="/user")

@user_bp.route('/my_info', methods=['GET'])
async def my_info(request: Request) -> json:
    """
    Обработчик для получения информации о текущем пользователе

    Получает email пользователя из контекста приложения,
    создает экземпляр класса User,
    получает информацию о пользователе и возвращает ее в формате JSON

    Args:
        request(sanic.Request): объект запроса Sanic

    Returns:
        sanic.json: JSON-ответ, содержащий информацию о пользователе
    """
    email = request.app.ctx.email
    user = User(email=email)
    user_info = await user.get_info()
    schema = MyInfoSchema()
    info = schema.dump(user_info)
    return json(info)

@user_bp.route('/get_accounts', methods=['GET'])
async def get_accounts(request: Request) -> json:
    """
    Обработчик для получения списка счетов и балансов текущего пользователя

    Получает email пользователя из контекста приложения,
    создает экземпляр класса User, получает список счетов
     и балансов пользователя, возвращает его в формате JSON

    Args:
        request(sanic.Request): объект запроса Sanic

    Returns:
        sanic.json: JSON-ответ, содержащий список счетов и
        балансов пользователя
    """
    email = request.app.ctx.email
    user = User(email=email)
    accounts = await user.get_your_accounts_and_balances()
    return json(accounts)

@user_bp.route('/get_transactions', methods=['GET'])
async def get_transactions(request: Request) -> json:
    """
    Обработчик для получения списка транзакций текущего пользователя

    Получает email пользователя из контекста приложения,
    создает экземпляр класса User, получает список платежей
    пользователя и возвращает его в формате JSON

    Args:
        request(sanic.Request): объект запроса Sanic

    Returns:
        sanic.json: JSON-ответ, содержащий список платежей пользователя
    """
    email = request.app.ctx.email
    user = User(email=email)
    transactions = await user.get_your_transactions()
    return json(transactions)