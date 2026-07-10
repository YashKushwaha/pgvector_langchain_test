## https://docs.langchain.com/oss/python/integrations/vectorstores/pgvectorstore


import os
import uuid
import asyncio

from dotenv import load_dotenv

from langchain_postgres import PGEngine
from langchain_core.embeddings import DeterministicFakeEmbedding
from langchain_postgres import PGVectorStore
from langchain_core.documents import Document
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

load_dotenv()


POSTGRES_USER = os.environ.get('POSTGRES_USER')  # @param {type: "string"}
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')  # @param {type: "string"}
POSTGRES_HOST = os.environ.get('POSTGRES_HOST')  # @param {type: "string"}
POSTGRES_PORT = os.environ.get('POSTGRES_PORT')  # @param {type: "string"}
POSTGRES_DB = os.environ.get('POSTGRES_DB')  # @param {type: "string"}
TABLE_NAME = os.environ.get('TABLE_NAME')  # @param {type: "string"}
VECTOR_SIZE = int(os.environ.get('VECTOR_SIZE'))  # @param {type: "int"}

SCHEMA_NAME="my_schema"

# See docker command above to launch a Postgres instance with pgvector enabled.
CONNECTION_STRING = (
    f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}"
    f":{POSTGRES_PORT}/{POSTGRES_DB}"
)
# To use psycopg3 driver, set your connection string to `postgresql+psycopg://`

# Create an SQLAlchemy Async Engine
engine = create_async_engine(CONNECTION_STRING)

pg_engine = PGEngine.from_engine(engine=engine)
embeddings = DeterministicFakeEmbedding(size=768)

docs = [
    Document(
        id=str(uuid.uuid4()),
        page_content="Red Apple",
        metadata={"description": "red", "content": "1", "category": "fruit"},
    ),
    Document(
        id=str(uuid.uuid4()),
        page_content="Banana Cavendish",
        metadata={"description": "yellow", "content": "2", "category": "fruit"},
    ),
    Document(
        id=str(uuid.uuid4()),
        page_content="Orange Navel",
        metadata={"description": "orange", "content": "3", "category": "fruit"},
    ),
]

async def check_table_exists(engine, table_name):
    query = text("""
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.tables
            WHERE table_name = :table_name
        )
    """)

    async with pg_engine._pool.connect() as conn:
        result = await conn.execute(
            query,
            {"table_name": table_name},
        )

        exists = result.scalar()

    if not exists:
        await pg_engine.ainit_vectorstore_table(
            table_name=table_name,
            vector_size=int(os.environ.get('VECTOR_SIZE', 768)) ,
        )

    return True

async def main():
    x = await check_table_exists(pg_engine, TABLE_NAME)

    print(x)

    store = await PGVectorStore.create(
        engine=pg_engine,
        table_name=TABLE_NAME,
        # schema_name=SCHEMA_NAME,
        embedding_service=embeddings,
    )

    y = await store.aadd_documents(docs)
    print(y)

    query = "I'd like a fruit."
    result = await store.asimilarity_search(query)
    print('Results for query:', query)
    print(result)
    print()
    query_vector = embeddings.embed_query(query)
    result = await store.asimilarity_search_by_vector(query_vector, k=2)
    print('Results for query:', query)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
