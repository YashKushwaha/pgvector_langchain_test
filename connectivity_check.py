# @title Set your values or use the defaults to connect to Docker { display-mode: "form" }
POSTGRES_USER = "postgres"  # @param {type: "string"}
POSTGRES_PASSWORD = "mysecretpassword"  # @param {type: "string"}
POSTGRES_HOST = "localhost"  # @param {type: "string"}
POSTGRES_PORT = "5433"  # @param {type: "string"}
POSTGRES_DB = "postgres"  # @param {type: "string"}
TABLE_NAME = "vectorstore"  # @param {type: "string"}
VECTOR_SIZE = 1024  # @param {type: "int"}

# See docker command above to launch a Postgres instance with pgvector enabled.
CONNECTION_STRING = (
    f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}"
    f":{POSTGRES_PORT}/{POSTGRES_DB}"
)
# To use psycopg3 driver, set your connection string to `postgresql+psycopg://`

from langchain_postgres import PGEngine

from sqlalchemy.ext.asyncio import create_async_engine

# Create an SQLAlchemy Async Engine
engine = create_async_engine(
    CONNECTION_STRING,
)

pg_engine = PGEngine.from_engine(engine=engine)
