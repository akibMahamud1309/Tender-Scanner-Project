"""Add current listing metadata to tenders.

Revision ID: 20260828_0002
Revises: 20260828_0001
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "20260828_0002"
down_revision = "20260828_0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "tenders",
        sa.Column("metadata", postgresql.JSONB(), server_default=sa.text("'{}'::jsonb"), nullable=False),
    )
    op.alter_column("tenders", "metadata", server_default=None)


def downgrade() -> None:
    op.drop_column("tenders", "metadata")
