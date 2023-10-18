"""1 migrations

Revision ID: a1bc80bdb7e7
Revises: d2a002d4ed00
Create Date: 2023-10-18 16:51:50.212313

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1bc80bdb7e7'
down_revision: Union[str, None] = 'd2a002d4ed00'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('products', 'image',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('products', 'image',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###