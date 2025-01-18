# alembic/versions/24c35f32b152.py

from datetime import UTC, datetime

import sqlalchemy as sa
from alembic import op

"""
Revision ID: 2413cf32b712 Revises:
Create Date: 2024-07-11 12:30:17.089406
"""

# revision identifiers, used by Alembic.
revision = "24c35f32b152"
down_revision = None
branch_labels = None


def upgrade():
    op.create_table(
        "conversations",
        sa.Column("id", sa.BigInteger, primary_key=True),
        sa.Column("title", sa.String, nullable=False),
        sa.Column("model_type", sa.String, index=True, nullable=False),
        sa.Column("created_at", sa.DateTime, default=datetime.now(UTC), nullable=False),
        sa.Column(
            "updated_at",
            sa.DateTime,
            default=datetime.now(UTC),
            onupdate=datetime.now(UTC),
            nullable=False,
        ),
    )

    op.create_table(
        "messages",
        sa.Column("id", sa.BigInteger, primary_key=True),
        sa.Column(
            "conversation_id",
            sa.BigInteger,
            sa.ForeignKey("conversations.id", ondelete="CASCADE"),
            index=True,
            nullable=False,
        ),
        sa.Column("prompt_content", sa.Text, nullable=False),
        sa.Column("response_content", sa.Text, nullable=False),
        sa.Column("prompt_tokens", sa.Integer, nullable=True),
        sa.Column("response_tokens", sa.Integer, nullable=True),
        sa.Column("total_tokens", sa.Integer, nullable=True),
        sa.Column("is_success", sa.Boolean, nullable=True),
        sa.Column("status_code", sa.Integer, nullable=True),
        sa.Column("created_at", sa.DateTime, default=datetime.now(UTC), nullable=False),
        sa.Column(
            "updated_at",
            sa.DateTime,
            default=datetime.now(UTC),
            onupdate=datetime.now(UTC),
            nullable=False,
        ),
    )


def downgrade():
    op.drop_table("messages")
    op.drop_table("conversations")
