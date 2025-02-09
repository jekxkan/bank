from sanic import Blueprint, json, redirect

from src.db.service import service


auth_bp = Blueprint("auth", url_prefix="")

@auth_bp.route("/auth", methods=["POST"], name="auth_route")
async def login_handler(request):
    """
    Обработчик для аутентификации пользователя

    Получает данные пользователя (email и пароль) из JSON-запроса,
    вызывает метод service.login для аутентификации пользователя.
    В случае успешной аутентификации перенаправляет пользователя
    на соответствующий URL (admin или user) в зависимости
    от значения атрибута service.role.
    Если аутентификация не удалась, возвращает JSON-ответ
    с сообщением об ошибке

    Args:
        request (sanic.Request): объект запроса Sanic

    Returns:
        sanic.HTTPResponse: перенаправление на URL администратора
        или пользователя в случае успеха,
        или JSON-ответ с сообщением об ошибке в случае неудачи
    """
    data = request.json
    email = data.get("email")
    password = data.get("password")
    try:
        login_result = await service.login(email, password)
        if login_result.get("status"):
            if service.role == 'admin':
                request.app.ctx.email = email
                return redirect("/admin")
            else:
                request.app.ctx.email = email
                return redirect("/user")
        else:
            return json(login_result)
    except Exception as e:
        return json({"status": f"Запрос не удался: {e}"})