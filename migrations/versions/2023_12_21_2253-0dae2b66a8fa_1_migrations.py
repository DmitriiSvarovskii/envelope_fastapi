"""1 migrations

Revision ID: 0dae2b66a8fa
Revises: d1279f3f77ab
Create Date: 2023-12-21 22:53:15.973548

"""
from sqlalchemy.sql import text
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0dae2b66a8fa'
down_revision: Union[str, None] = 'd1279f3f77ab'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    conn = op.get_bind()
    result = conn.execute(
        text("SELECT schema_name FROM information_schema.schemata"))
    schemas = [row[0] for row in result]

    for schema in schemas:
        if schema not in ['information_schema', 'pg_catalog']:
            op.execute(text(
                f'ALTER TABLE "{schema}".delivery_fix ALTER COLUMN price TYPE INTEGER USING price::integer'))


def downgrade() -> None:
    pass
