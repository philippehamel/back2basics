"""create bronze events table

Revision ID: 3cec86ec8945
Revises:
Create Date: 2026-11-07 21:10:46.218729

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "3cec86ec8945"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("CREATE SCHEMA bronze;")
    op.execute("""
        CREATE TABLE bronze.events (
            id              BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            device_id       TEXT NOT NULL,
            event_timestamp TIMESTAMPTZ NOT NULL,
            event_type      TEXT NOT NULL,
            value           DOUBLE PRECISION NOT NULL,
            ingested_at     TIMESTAMPTZ NOT NULL DEFAULT current_timestamp
        );
        """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP TABLE bronze.events;")
    op.execute("DROP SCHEMA bronze;")
