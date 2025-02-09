from sanic import Sanic

from src.routes.admin_route import admin_bp
from src.routes.auth import auth_bp
from src.routes.user_route import user_bp
from src.routes.webhook import webhook_bp


def create_app() -> Sanic:
   """
   Создает приложение Sanic и его конфигурацию

   Настраивает статические маршруты для HTML-страниц,
   регистрирует blueprints для различных частей приложения (auth, admin,
   user, webhook)

   Returns:
       app(Sanic): сконфигурированный экземпляр приложения Sanic
   """
   app = Sanic("payment-system")
   app.static("/", "src/static/auth.html", name="login_page")
   app.static("/admin", "src/static/admin.html", name="admin_page")
   app.static("/user", "src/static/user.html", name="user_page")
   app.static("/webhook", "src/static/webhook.html", name="webhook_page")

   @app.before_server_start
   async def setup_email(app: Sanic):
      """
         Настраивает контекстную переменную email перед запуском сервера

         Эта переменная используется при выполнении функции
         get_info_about_yourself в db/service
         (получение информации о себе после входа в аккаунт)

         Args:
             app(Sanic): экземпляр приложения Sanic
      """
      app.ctx.email = ''

   blueprints = [auth_bp, admin_bp, user_bp, webhook_bp]
   for bp in blueprints:
      app.blueprint(bp)

   return app

app = create_app()