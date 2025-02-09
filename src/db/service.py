import os

from dotenv import load_dotenv
from sqlalchemy import and_, delete, inspect, select, update
from sqlalchemy.dialects.postgresql import insert

from src.database import DBSession
from src.db.models import AccountInfo, ClientInfo, Transaction
from src.db.schemas import (
    Account,
    AccountsList,
    Transactions,
    TransactionsList,
    UserInfo,
    UsersList,
)


load_dotenv()
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

class Service:
    """
    Сервисный класс для обработки операций базы данных,
    связанных с пользователями, счетами и платежами

    Этот класс предоставляет методы для аутентификации пользователей,
    управления пользователями, управления счетами,
    обработки платежей и получения данных.
    Он взаимодействует с базой данных с использованием SQLAlchemy.
    """
    def __init__(self):
        """
        Инициализирует Service сеансом базы данных
        и устанавливает роль пользователя в None
        """
        self.session = DBSession()
        self.role = None

    async def check_if_user_exists(self, email: str) -> ClientInfo | None:
        """
        Проверяет, существует ли пользователь с данным email в базе данных

        Args:
            email(str): email, который нужно проверить

        Returns:
            checking_result(ClientInfo | None): объект ClientInfo,
            если пользователь существует, иначе None
        """
        stmt = (
            select(ClientInfo)
            .filter(ClientInfo.email == email)
        )
        checking_result = (await self.session.execute(stmt)).scalar()
        return checking_result

    async def login(self, email: str, password: str) -> dict:
        """
        Аутентифицирует пользователя с указанным email и паролем

        Args:
            email(str): адрес электронной почты пользователя
            password(str): пароль пользователя

        Returns:
            response(dict): словарь, содержащий статус попытки входа в систему
            и, в случае успеха, URL-адрес для перенаправления пользователя.
            В случае неудачи он содержит сообщение об ошибке
        """
        checking_result = await self.check_if_user_exists(email)
        if not checking_result:
            response = {"status": False,
                        "error": "Пользователь не зарегистрирован"}
            return response
        checking_is_data_correct = (
            select(ClientInfo)
            .filter(
                and_(
                    ClientInfo.email == email,
                    ClientInfo.password == password)
            )
        )
        is_data_correct =  ((await self.session.execute(
            checking_is_data_correct
        )).scalar())
        if not is_data_correct:
            response = {"status": False, "error": "Неверный пароль"}
            return response
        if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
            self.role = "admin"
            response = {"status": True, "url": "/admin"}
            return response
        else:
            self.role = "user"
            response = {"status": True, "url": "/user"}
            return response

    async def get_info_about_yourself(self, email: str) -> ClientInfo | None:
        """
        Получает информацию о пользователе после входа в аккаунт

        Args:
            email(str): адрес электронной почты пользователя

        Returns:
            result(ClientInfo | None): объект ClientInfo,
             если пользователь существует, иначе None
        """
        getting_info = (
            select(ClientInfo)
            .where(ClientInfo.email == email)
        )
        getting_info_result = ((await self.session.execute(getting_info))
                               .scalar())
        return getting_info_result

    async def create_user(self, data: dict) -> dict|str:
        """
        Создает нового пользователя в базе данных

        Args:
            data(dict): словарь, содержащий информацию о пользователе

        Returns:
            dict|str: возвращает имя пользователя, если пользователь был создан
            , иначе возвращает сообщение о том, что пользователь уже существует
        """
        checking_result = await self.check_if_user_exists(data["email"])
        if checking_result is None:
            creating_user = (
                insert(ClientInfo)
                .values(**data)
            )
            await self.session.execute(creating_user)
            await self.session.commit()
            getting_new_user = (
                select(ClientInfo.full_name)
                .where(ClientInfo.email == data['email'])
            )
            new_user = await self.session.execute(getting_new_user)
            return new_user.scalar()
        else:
            return {'status': f"Пользователь с email {data['email']}"
                              f" уже существует"}

    async def delete_user(self, email: str):
        """
        Удаляет пользователя из базы данных на основе его email

        Args:
            email(str): email пользователя, которого необходимо удалить

        Returns:
            dict: словарь, содержащий статус попытки удаления
        """
        checking_result = await self.check_if_user_exists(email)
        if checking_result:
            del_user = (
                delete(ClientInfo)
                .where(ClientInfo.email == email)
            )
            await self.session.execute(del_user)
            await self.session.commit()
            attempting_to_del_user = (
                select(ClientInfo)
                .where(ClientInfo.email == email)
            )
            attempting_result = ((await self.session.execute(
                attempting_to_del_user
            )).scalar())
            if attempting_result is None:
                return {'status': f"Пользователь с email {email} удален"}
            else:
                return {'status': f"Пользователь с email {email} не удален"}
        else:
            return {"status": f"Пользователь с email {email} "
                              f"не зарегистрирован"}

    async def update_user(self, user_email: str, data: dict):
        """
        Обновляет информацию о пользователе в базе данных

        Args:
            user_email(str): email пользователя, информацию которого
            необходимо обновить
            data(dict): словарь, содержащий новую информацию для пользователя

        Returns:
            dict: словарь, содержащий статус попытки обновления
        """
        checking_result = await self.check_if_user_exists(user_email)
        if checking_result:
            getting_user = (
                select(ClientInfo)
                .where(ClientInfo.email == user_email)
            )
            user = (await self.session.execute(getting_user)).scalar()
            for key, value in data.items():
                setattr(user, key, value)
            inspector = inspect(user)
            changes = False
            for attr in inspector.mapper.attrs:
                history = inspector.get_history(attr.key, True)
                if history.has_changes():
                    changes = True
                    break
            if not changes:
                return {'status': 'Все поля пользователя остались прежними:'
                                  ' вы ввели те же значения'}
            await self.session.commit()
            return {"status": f"Новые данные пользователя: {user.email}, "
                              f"{user.password}, {user.full_name}"}
        else:
            return {'status': f"Пользователь с email {user_email} "
                              f"не зарегистрирован"}

    async def get_users_list(self):
        """
        Получает список всех пользователей из базы данных

        Returns:
            list[dict] | dict: список словарей, где каждый представляет
            пользователя, или словарь, содержащий сообщение о состоянии
            , если пользователей нет
        """
        getting_users_list = (
            select(ClientInfo)
            .filter(ClientInfo.email != 'admin@mail.com')
            .order_by(ClientInfo.user_id)
        )
        getting_users_list_result = ((await self.session.execute(
            getting_users_list
        )).scalars().all())
        if getting_users_list_result:
            users_list = UsersList(users =
                                   [UserInfo.model_validate(user)
                                    for user in getting_users_list_result])
            return users_list.model_dump()['users']
        else:
            return {"status": "Ни одного зарегистрированного пользователя"}

    async def get_users_accounts(self, email: str):
        """
        Получает список счетов пользователя с указанным email

        Args:
            email(str): адрес электронной почты пользователя

        Returns:
            list[dict] | dict: список словарей, где каждый представляет счет,
            или словарь, содержащий сообщение о состоянии, если пользователь
            или его счета не найдены
        """
        getting_user_id = (
            select(ClientInfo.user_id)
            .where(ClientInfo.email == email)
        )
        user_id = (await self.session.execute(getting_user_id)).scalar()
        if user_id:
            get_users_accounts_stmt = (
                select(AccountInfo)
                .where(AccountInfo.user_id == user_id)
            )
            users_accounts = (await self.session.execute(
                get_users_accounts_stmt
            )).scalars().all()

            if users_accounts:
                accounts = AccountsList(
                    accounts=[
                        Account.model_validate(account)
                        for account in users_accounts
                    ]
                )
                return accounts.model_dump()['accounts']
            else:
                return {"status": "У пользователя нет счетов"}
        else:
            return {"status": "Пользователь не зарегистрирован"}

    async def get_accounts_and_balances(self, email: str):
        """
        Получает список счетов и их балансов для пользователя с указанным email

        Args:
            email(str): адрес электронной почты пользователя

        Returns:
            list[dict] | dict: список словарей, где каждый представляет
            счет и его баланс, или словарь, содержащий сообщение о состоянии,
            если у пользователя нет счетов
        """
        getting_accounts = (
            select(AccountInfo)
            .join(ClientInfo, AccountInfo.user_id == ClientInfo.user_id)
            .where(ClientInfo.email == email)
        )
        accounts_list = ((await self.session.execute(getting_accounts))
                         .scalars().all())
        if accounts_list:
            accounts = AccountsList(
                accounts=[
                    Account.model_validate(account)
                    for account in accounts_list
                ]
            )
            return accounts.model_dump()['accounts']
        else:
            return {"status": "У вас нет счетов"}

    async def get_transactions(self, email: str):
        """
        Получает список транзакций для пользователя с указанным email

        Args:
            email(str): адрес электронной почты пользователя

        Returns:
            list[dict] | dict: список словарей, где каждый представляет платеж,
            или словарь, содержащий сообщение о состоянии,
            если у пользователя нет транзакций
        """
        getting_transactions = (
            select(Transaction)
            .join(ClientInfo, Transaction.user_id == ClientInfo.user_id)
            .where(ClientInfo.email == email)
        )
        transactions = ((await self.session.execute(getting_transactions))
                        .scalars().all())
        if transactions:
            transactions_list = TransactionsList(
                transactions_list=[
                    Transactions.model_validate(transaction)
                    for transaction in transactions
            ]
            )
            return transactions_list.model_dump()['transactions_list']
        else:
            return {'status': 'У вас нет платежей'}

    async def process_webhook(self, data: dict):
        """
        Обрабатывает запрос вебхука для обновления баланса счета
        и записи транзакций

        Args:
            data (dict): словарь, содержащий данные вебхука

        Returns:
            dict: словарь, содержащий статус обработки вебхука
        """
        getting_account = (
            select(AccountInfo)
            .where(
                and_(
                    AccountInfo.account_id == data['account_id'],
                    AccountInfo.user_id == data['user_id'])
            )
        )
        getting_account_result = ((await self.session.execute(getting_account))
                              .scalar())
        if getting_account_result is None:
            get_account_by_id = (
                select(AccountInfo)
                .where(AccountInfo.account_id == data['account_id'])
            )
            getting_account_by_id_result = (
                (await self.session.execute(get_account_by_id))
                .scalar()
            )
            if getting_account_by_id_result:
                return {"status": f"Счет с id {data['account_id']} существует,"
                                  f"но не принадлежит пользователю с id "
                                  f"{data['user_id']}"}
            else:
                self.session.add(
                    AccountInfo(user_id=data['user_id'],
                                balance=data['amount'],)
                )

        getting_transaction = (
            select(Transaction)
            .where(Transaction.account_id == data['account_id'])
        )
        getting_transaction_result = ((await self.session
                                   .execute(getting_transaction))
                                  .scalar()
                                  )
        if getting_transaction_result is None:
            self.session.add(
                Transaction(transaction_id=data['transaction_id'],
                            account_id=data['account_id'],
                            amount=data['amount'],
                            user_id=data['user_id'], )
            )
            adding_amount = (
                update(AccountInfo)
                .values(balance=AccountInfo.balance + data['amount'])
                .where(AccountInfo.account_id == data['account_id'])
            )
            await self.session.execute(adding_amount)
            await self.session.commit()
            return {"status": f"Транзакция с id {data['transaction_id']} "
                              f"проведена"}
        else:
            return {'status': "Ошибка: транзакция с таким id уже проведена"}

service = Service()