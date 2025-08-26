from __future__ import with_statement
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import os, sys

config = context.config
fileConfig(config.config_file_name)

# Make 'app' importable for migrations
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.db.base import Base  # noqa
from app.models.user import User  # noqa
from app.models.document import Document  # noqa
from app.models.passcode import AccessPasscode  # noqa
from app.models.audit import AuditLog  # noqa

target_metadata = Base.metadata

def get_url():
    user = os.getenv("POSTGRES_USER", "gpp_user")
    password = os.getenv("POSTGRES_PASSWORD", "gpp_pass")
    host = os.getenv("POSTGRES_HOST", "db")
    port = os.getenv("POSTGRES_PORT", "5432")
    db = os.getenv("POSTGRES_DB", "gpp_db")
    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"

def run_migrations_offline():
    url = get_url()
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True, compare_type=True)
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section), prefix="sqlalchemy.",
        poolclass=pool.NullPool, url=get_url(),
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata, compare_type=True)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
