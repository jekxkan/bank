from marshmallow import Schema, fields


class MyInfoSchema(Schema):
    """
    Marshmallow-схема для сериализации информации о пользователе.

    Эта схема определяет, как представлять данные пользователя
    при преобразовании их в формат JSON (сериализация)

    Attributes:
        id(fields.Int): ID пользователя. Аргумент `attribute="user_id"`
        сопоставляет это поле с атрибутом `user_id` объекта,
        который сериализуется
        email(fields.Str): представляет email пользователя
        full_name(fields.Str): представляет полное имя пользователя
    """
    id = fields.Int(attribute="user_id")
    email = fields.Str()
    full_name = fields.Str()