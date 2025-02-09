"""Добавление записей в таблицы

Revision ID: b1ad765ee3d3
Revises: 34c4f6586e70
Create Date: 2025-02-09 23:59:57.139578

"""
from decimal import Decimal
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from src.db.models import ClientInfo, AccountInfo

# revision identifiers, used by Alembic.
revision: str = 'b1ad765ee3d3'
down_revision: Union[str, None] = '34c4f6586e70'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.bulk_insert(
        ClientInfo.__table__,
        [
            {'email': 'admin@mail.com', 'password': 'root','full_name': 'Администратор'},
            {'email': 'user1@mail.com', 'password': 'password', 'full_name': 'Пользователь'}
        ]
    )
    op.bulk_insert(
        AccountInfo.__table__,
        [
            {'user_id': 1, 'balance': Decimal(1000)}
        ]
    )


def downgrade() -> None:
    pass
