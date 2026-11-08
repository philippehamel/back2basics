set dotenv-load

check:
    uv run ruff format
    uv run ruff check --fix
    uv run mypy src tests

migrate:
    uv run alembic upgrade head

rollback:
    uv run alembic downgrade -1

db-status:
    uv run alembic current

query:
    docker compose up -d --wait
    psql