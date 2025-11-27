"""security rework tables

Revision ID: 6f3a4b0b9c21
Revises: a7c5b0f442de
Create Date: 2024-11-11 12:00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6f3a4b0b9c21'
down_revision: Union[str, Sequence[str], None] = 'a7c5b0f442de'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create approval/audit/challenge tables and extend admin_users."""
    op.add_column("admin_users", sa.Column("totp_secret", sa.String(length=64), nullable=True))

    op.create_table(
        "approval_keys",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("admin_id", sa.Integer(), sa.ForeignKey("admin_users.id"), nullable=False),
        sa.Column("public_key_pem", sa.String(length=2000), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.UniqueConstraint("admin_id", name="uq_approval_keys_admin"),
    )

    op.create_table(
        "audit_events",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("event_type", sa.String(length=100), nullable=False),
        sa.Column("payload", sa.Text(), nullable=False),
        sa.Column("signature_hash", sa.String(length=128), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
    )

    op.create_table(
        "auth_challenges",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("admin_username", sa.String(length=80), nullable=False),
        sa.Column("method", sa.String(length=32), nullable=False),
        sa.Column("code_hash", sa.String(length=255), nullable=False),
        sa.Column("risk_score", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="pending"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("1")),
    )
    op.create_index("ix_auth_challenges_admin_username", "auth_challenges", ["admin_username"])

    op.create_table(
        "policy_decisions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("actor", sa.String(length=80), nullable=False),
        sa.Column("action", sa.String(length=80), nullable=False),
        sa.Column("decision", sa.String(length=32), nullable=False),
        sa.Column("rules", sa.Text(), nullable=False, server_default=""),
        sa.Column("evidence", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
    )


def downgrade() -> None:
    """Drop created tables/columns."""
    op.drop_index("ix_auth_challenges_admin_username", table_name="auth_challenges")
    op.drop_table("policy_decisions")
    op.drop_table("auth_challenges")
    op.drop_table("audit_events")
    op.drop_table("approval_keys")
    op.drop_column("admin_users", "totp_secret")
