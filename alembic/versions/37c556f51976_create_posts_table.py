"""create posts table

Revision ID: 37c556f51976
Revises: 
Create Date: 2024-01-04 13:05:49.285851

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '37c556f51976'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer, nullable=False, primary_key=True), sa.Column('title', sa.String, nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass
