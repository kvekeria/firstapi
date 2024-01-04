"""add users table

Revision ID: c7d16ee402f8
Revises: b6933935fc23
Create Date: 2024-01-04 14:47:21.610640

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c7d16ee402f8'
down_revision: Union[str, None] = 'b6933935fc23'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table('users', sa.Column('id', sa.Integer, primary_key=True))
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
