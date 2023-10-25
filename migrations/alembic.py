from alembic.config import Config
from alembic import command
from alembic import op
import sqlalchemy as sa


def upgrade(new_schema):
    op.execute(
        f"CREATE SCHEMA IF NOT EXISTS {new_schema} AUTHORIZATION postgres;")

    op.execute(
        f"CREATE TABLE {new_schema}.categories AS SELECT * FROM public.categories")


def downgrade():
    op.execute("DROP SCHEMA IF EXISTS new_schema CASCADE")


def run_alembic_migrations():
    alembic_config = Config(
        "/Users/dmitriyswarovski/Desktop/Python/Project/api/envelope_fastapi/alembic.ini")

    # Имя вашей миграции
    migration_name = "copy_tables"

    # Выполнить миграции
    command.upgrade(alembic_config, migration_name)
