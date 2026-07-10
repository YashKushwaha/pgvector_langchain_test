# PGVector + LangChain Demo

## Summary

This is a small project that demonstrates how to use PostgreSQL with the PGVector extension as a vector store in LangChain.

The project uses Docker to run PostgreSQL locally and stores embeddings in a PGVector-backed table.

## Prerequisites

- Docker and Docker Compose
- Python
- `uv`

## Setup

Clone the repository and create the environment file:

```bash
cp .env.example .env
```

Update the values in `.env` if necessary.

## Start PostgreSQL + PGVector

Start the database container:

```bash
docker compose up -d
```

The database will be available on:

- Host: `localhost`
- Port: `5433`

To stop the container:

```bash
docker compose down
```

To stop the container and remove all database data:

```bash
docker compose down -v
```

## Install dependencies

Install the project dependencies:

```bash
uv sync
```

## Run the example

Run the sample script:

```bash
uv run python connectivity_check.py
```

## Project structure

```text
.
├── connectivity_check.py
├── docker-compose.yaml
├── .env.example
├── pyproject.toml
├── uv.lock
└── README.md

```