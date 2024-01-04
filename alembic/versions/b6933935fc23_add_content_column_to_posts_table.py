"""add content column to posts table

Revision ID: b6933935fc23
Revises: 37c556f51976
Create Date: 2024-01-04 13:34:26.928895

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b6933935fc23'
down_revision: Union[str, None] = '37c556f51976'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String, nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
