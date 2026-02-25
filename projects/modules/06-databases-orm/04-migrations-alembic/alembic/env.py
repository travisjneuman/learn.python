"""
Alembic environment configuration.

This file tells Alembic how to connect to the database and which models
to compare against when generating migrations. The critical part is
setting target_metadata to your Base.metadata — this is how autogenerate
knows what your schema should look like.
"""

from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# ── Import your models ────────────────────────────────────────────────
#
# This import is essential. Without it, Alembic cannot see your models
# and autogenerate will produce empty migrations.
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from project import Base

# ── Alembic Config ────────────────────────────────────────────────────

# This is the Alembic Config object, which provides access to the
# values within the alembic.ini file.
config = context.config

# Set up Python logging from the config file.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# This is the metadata that Alembic compares against the database.
# It comes from your Base class, which all models inherit from.
target_metadata = Base.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This generates SQL scripts without connecting to the database.
    Useful for review or applying migrations manually.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    This connects to the database and applies changes directly.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
