"""add registration requests table

Revision ID: a7c5b0f442de
Revises: 414cf7cbbed1
Create Date: 2024-11-11 10:00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a7c5b0f442de'
down_revision: Union[str, Sequence[str], None] = '414cf7cbbed1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create registration_requests table for approval-based onboarding."""
    op.create_table(
        'registration_requests',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('username', sa.String(length=80), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('reason', sa.String(length=255), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=False, server_default='pending'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('reviewed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('reviewed_by', sa.String(length=80), nullable=True),
        sa.Column('review_note', sa.String(length=255), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('1')),
    )
    op.create_index(
        'ix_registration_requests_username',
        'registration_requests',
        ['username'],
        unique=True,
    )


def downgrade() -> None:
    """Drop registration_requests table."""
    op.drop_index('ix_registration_requests_username', table_name='registration_requests')
    op.drop_table('registration_requests')
