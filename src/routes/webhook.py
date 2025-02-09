import hashlib
import hmac
import os
from decimal import Decimal

from dotenv import load_dotenv
from sanic import Blueprint, Request, json

from src.db.service import service


load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
webhook_bp = Blueprint('hook')

def check_webhook(data: dict, signature: str, SECRET_KEY: str) -> bool:
    """
    Проверяет подлинность вебхука, сравнивая полученную подпись с вычисленной

    Args:
        data(dict): данные вебхук.
        signature(str): подпись вебхука, полученная в запросе
        SECRET_KEY(str): секретный ключ, используемый для вычисления подписи

    Returns:
        bool: True, если подпись верна, иначе False
    """
    sorted_data = sorted(data.keys())
    signature_str = (''.join(str(data[key]) for key in sorted_data
                             if key != 'signature')
                     + SECRET_KEY)
    signature_sha256 = (hashlib.sha256(signature_str.encode('utf-8'))
                        .hexdigest())
    return hmac.compare_digest(signature, signature_sha256)


@webhook_bp.route('/webhook', methods=['POST'])
async def get_webhook(request: Request) -> json:
    """
    Обработчик для получения вебхука

    Получает данные из JSON-запроса,
    проверяет подлинность вебхука с помощью check_webhook,
    и если проверка прошла успешно, вызывает метод service.process_webhook
    для обработки данных вебхука.
    Возвращает JSON-ответ с результатом обработки

    Args:
        request(sanic.Request): объект запроса Sanic

    Returns:
        sanic.json: JSON-ответ, содержащий результат обработки вебхука
        или сообщение об ошибке валидации
    """
    data = request.json
    transaction_id = data['transaction_id']
    user_id = data['user_id']
    account_id = data['account_id']
    amount = data['amount']
    signature = data['signature']

    data_dict = {
        'transaction_id': transaction_id,
        'user_id': int(user_id),
        'account_id': int(account_id),
        'amount': Decimal(amount),
    }

    if check_webhook(data_dict, signature, secret_key):
        result = await service.process_webhook(data_dict)
        return json(result)
    else:
        return json({'status': 'вебхук не прошел валидацию'})