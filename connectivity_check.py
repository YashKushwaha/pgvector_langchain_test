## https://docs.langchain.com/oss/python/integrations/vectorstores/pgvectorstore

# @title Set your values or use the defaults to connect to Docker { display-mode: "form" }
POSTGRES_USER = "postgres"  # @param {type: "string"}
POSTGRES_PASSWORD = "mysecretpassword"  # @param {type: "string"}
POSTGRES_HOST = "localhost"  # @param {type: "string"}
POSTGRES_PORT = "5433"  # @param {type: "string"}
POSTGRES_DB = "postgres"  # @param {type: "string"}
TABLE_NAME = "vectorstore"  # @param {type: "string"}
VECTOR_SIZE = 1024  # @param {type: "int"}

SCHEMA_NAME="my_schema"

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

import asyncio
from langchain_core.embeddings import DeterministicFakeEmbedding

embeddings = DeterministicFakeEmbedding(size=768)

from langchain_postgres import PGVectorStore

import uuid

from langchain_core.documents import Document

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



async def main():
    # x = await pg_engine.ainit_vectorstore_table(
    #     table_name=TABLE_NAME,
    #     vector_size=768,
    #     #schema_name=SCHEMA_NAME,    # Default: "public"
    # )

    # print(x)

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
