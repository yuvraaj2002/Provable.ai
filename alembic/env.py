from logging.config import fileConfig
import sys

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
from app.core.database import Base
from app.models.users import User  # Import the User model for autogeneration

# Try to load settings, but fall back to alembic.ini if it fails
try:
    from app.core.config import settings
    database_url = settings.DATABASE_URL_SYNC
except Exception as e:
    # If settings can't be loaded, use the URL from alembic.ini
    database_url = config.get_main_option("sqlalchemy.url")
    if not database_url:
        print(f"Error: Could not load database URL from settings: {e}", file=sys.stderr)
        print("Please ensure your .env file is configured correctly or set sqlalchemy.url in alembic.ini", file=sys.stderr)
        sys.exit(1)

target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    # Use the database URL (from settings or alembic.ini fallback)
    url = database_url if database_url else config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # Use the database URL (from settings or alembic.ini fallback)
    config.set_main_option("sqlalchemy.url", database_url)
    
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    try:
        with connectable.connect() as connection:
            context.configure(
                connection=connection, target_metadata=target_metadata
            )

            with context.begin_transaction():
                context.run_migrations()
    except Exception as e:
        error_msg = str(e)
        if "could not translate host name" in error_msg or "nodename nor servname provided" in error_msg:
            print("\n" + "="*70, file=sys.stderr)
            print("ERROR: Cannot connect to database - DNS resolution failed", file=sys.stderr)
            print("="*70, file=sys.stderr)
            print(f"\nThe database hostname could not be resolved.", file=sys.stderr)
            print(f"This usually means:", file=sys.stderr)
            print(f"  1. You are not connected to the internet", file=sys.stderr)
            print(f"  2. The database URL is incorrect", file=sys.stderr)
            print(f"  3. The database server is down or unreachable", file=sys.stderr)
            print(f"\nDatabase URL being used: {database_url.split('@')[1] if '@' in database_url else 'hidden'}", file=sys.stderr)
            print(f"\nTo work offline, use: alembic revision --autogenerate --sql", file=sys.stderr)
            print("="*70 + "\n", file=sys.stderr)
        raise


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
