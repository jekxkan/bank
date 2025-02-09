from decimal import Decimal
from typing import List

from pydantic import BaseModel


class UserInfo(BaseModel):
    """
    Pydantic-модель, представляющая информацию о пользователе

    Attributes:
        user_id(int): Уникальный идентификатор пользователя
        email(str): Адрес электронной почты пользователя
        password(str): Пароль пользователя
        full_name(str): Полное имя пользователя

    Config:
        from_attributes = True: разрешает создание модели непосредственно
        из атрибутов объектов
    """
    user_id: int
    email: str
    password: str
    full_name: str

    class Config:
        from_attributes = True


class UsersList(BaseModel):
    """
    Pydantic-модель, представляющая список информации о пользователях

    Attributes:
        users(List[UserInfo]): cписок объектов UserInfo
    """
    users: List[UserInfo]


class Account(BaseModel):
    """
    Pydantic-модель, представляющая информацию о счете

    Attributes:
        account_id(int): уникальный идентификатор счета
        user_id(int): идентификатор пользователя, которому принадлежит счет
        balance(Decimal): текущий баланс счета

    Config:
        from_attributes = True: разрешает создание модели непосредственно
        из атрибутов объектов
    """
    account_id: int
    user_id: int
    balance: Decimal

    class Config:
        from_attributes = True


class AccountsList(BaseModel):
    """
    Pydantic-модель, представляющая список счетов

    Attributes:
        accounts(List[Account]): список объектов Account
    """
    accounts: List[Account]


class Transactions(BaseModel):
    """
    Pydantic-модель, представляющая информацию о платеже

    Attributes:
        transaction_id(str): уникальный идентификатор платежа
        user_id(int): идентификатор пользователя, участвующего в платеже
        account_id(int): идентификатор аккаунта, участвующего в платеже
        amount(Decimal): сумма платежа

    Config:
        from_attributes = True: разрешает создание модели непосредственно
        из атрибутов объектов
    """
    transaction_id: str
    user_id: int
    account_id: int
    amount: Decimal

    class Config:
        from_attributes = True


class TransactionsList(BaseModel):
    """
    Pydantic-модель, представляющая список платежей

    Attributes:
        transactions_list(List[Transactions]): список объектов Transactions
    """
    transactions_list: List[Transactions]