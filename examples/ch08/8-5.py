"""create users and tokens tables

Revision ID: 1234567890ab
Revises:
Create Date: 2025-01-28 12:34:56.789012

"""

from datetime import UTC, datetime

import sqlalchemy as sa
from alembic import op

...


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.UUID(as_uuid=True)),
        sa.Column("email", sa.String(length=255)),
        sa.Column("hashed_password", sa.String(length=255)),
        sa.Column(
            "is_active", sa.Boolean(), server_default=sa.sql.expression.true()
        ),
        sa.Column("role", sa.String(), server_default=sa.text("USER")),
        sa.Column("created_at", sa.DateTime(), default=datetime.now(UTC)),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            default=datetime.now(UTC),
            onupdate=datetime.now(UTC),
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.Index("ix_users_email", "email"),
    )

    op.create_table(
        "tokens",
        sa.Column("id", sa.UUID(as_uuid=True)),
        sa.Column("user_id", sa.Integer()),
        sa.Column("expires_at", sa.DateTime()),
        sa.Column("is_active", sa.Boolean(), default=True),
        sa.Column("ip_address", sa.String(length=255), nullable=True),
        sa.Column("created_at", sa.DateTime(), default=datetime.now(UTC)),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            default=datetime.now(UTC),
            onupdate=datetime.now(UTC),
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.Index("ix_tokens_user_id", "user_id"),
        sa.Index("ix_tokens_ip_address", "ip_address"),
    )


def downgrade():
    op.drop_table("tokens")
    op.drop_table("users")
