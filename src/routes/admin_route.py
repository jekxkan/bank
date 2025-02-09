from sanic import Blueprint, Request, json

from src.db.serialization import MyInfoSchema
from src.roles.admin import Admin


admin_bp = Blueprint('admin_route', url_prefix="/admin")

@admin_bp.route('/my_info', methods=['GET'])
async def my_info(request: Request) -> json:
    """
    Обработчик для получения информации об администраторе

    Получает email администратора из контекста приложения,
    создает экземпляр класса Admin, получает информацию об администраторе
    и возвращает ее в формате JSON

    Args:
        request (sanic.Request): объект запроса Sanic

    Returns:
        sanic.json: JSON-ответ, содержащий информацию об администраторе
    """
    email = request.app.ctx.email
    admin = Admin(email=email)
    admin_info = await admin.get_info()
    schema = MyInfoSchema()
    info = schema.dump(admin_info)
    return json(info)


@admin_bp.route('/create_user', methods=['POST'])
async def create_user(request: Request) -> json:
    """
    Обработчик для создания нового пользователя

    Получает email администратора из контекста приложения,
    создает экземпляр класса Admin, получает данные пользователя
    из JSON-запроса, создает нового пользователя
    и возвращает статус операции в формате JSON

    Args:
        request(sanic.Request): объект запроса Sanic

    Returns:
        sanic.json: JSON-ответ, содержащий статус создания пользователя
    """
    admin = Admin(email=request.app.ctx.email)
    data = request.json
    check_data = [True for item in data.values() if item != '']
    if len(check_data) == 3:
        new_user = await admin.create_user(data)
        if isinstance(new_user, dict):
            return json(new_user)
        elif new_user == data['full_name']:
            return json({'status': f'Пользователь {new_user} создан'})
        else:
            return json({'status': f'Пользователь {new_user} не создан'})
    else:
        return json({'status': 'Не все поля заполены'})


@admin_bp.route('/delete_user', methods=['DELETE'])
async def delete_user(request: Request) -> json:
    """
    Обработчик для удаления пользователя

    Получает email администратора из контекста приложения,
    создает экземпляр класса Admin, получает данные пользователя
    из JSON-запроса, удаляет пользователя
    и возвращает статус операции в формате JSON

    Args:
        request(sanic.Request): объект запроса Sanic

    Returns:
        sanic.json: JSON-ответ, содержащий статус удаления пользователя
    """
    admin = Admin(email=request.app.ctx.email)
    email = request.json['email']
    deleted_user = await admin.delete_user(email)
    return json(deleted_user)


@admin_bp.route('/update_user', methods=['POST'])
async def update_user(request: Request) -> json:
    """
    Обработчик для обновления информации о пользователе

    Получает email администратора из контекста приложения,
    создает экземпляр класса Admin, получает данные пользователя
    из JSON-запроса, обновляет информацию о пользователе
    и возвращает статус операции в формате JSON

    Args:
        request(sanic.Request): объект запроса Sanic

    Returns:
        sanic.json: JSON-ответ, содержащий статус обновления пользователя
    """
    admin = Admin(email=request.app.ctx.email)
    data = request.json
    user_email = data['user_email']
    del data['user_email']
    changed_data = {key: value for key, value in data.items() if value != ''}
    if changed_data == {}:
        error = {"status": "Вы не изменили ни одного значения"}
        return json(error)
    updated_user = await admin.update_user(user_email, changed_data)
    return json(updated_user)


@admin_bp.route('/get_users', methods=['GET'])
async def get_users(request: Request) -> json:
    """
    Обработчик для получения списка пользователей

    Получает email администратора из контекста приложения,
    создает экземпляр класса Admin, получает список пользователей
    и возвращает его в формате JSON

    Args:
        request(sanic.Request): объект запроса Sanic

    Returns:
        sanic.json: JSON-ответ, содержащий список пользователей
    """
    admin = Admin(email=request.app.ctx.email)
    users = await admin.get_users()
    return json(users)


@admin_bp.route('/get_users_accounts', methods=['POST'])
async def get_accounts(request: Request) -> json:
    """
    Обработчик для получения списка счетов пользователя

    Получает email администратора из контекста приложения,
    создает экземпляр класса Admin, получает данные пользователя
    из JSON-запрос и список счетов пользователя,
    возвращает его в формате JSON

    Args:
        request(sanic.Request): объект запроса Sanic

    Returns:
        sanic.json: JSON-ответ, содержащий список счетов пользователя
    """
    admin = Admin(email=request.app.ctx.email)
    email = request.json['email']
    if email:
        accounts = await admin.get_users_accounts(email)
        return json(accounts)
    else:
        return json({"status": "Введите email"})