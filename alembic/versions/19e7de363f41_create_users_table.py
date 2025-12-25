"""Create users table

Revision ID: 19e7de363f41
Revises: 3031490a0117
Create Date: 2025-12-25 11:18:47.900017

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '19e7de363f41'
down_revision: Union[str, Sequence[str], None] = '3031490a0117'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('users',
        sa.Column('google_sub', sa.String(255), primary_key=True, index=True),
        sa.Column('email', sa.String(), unique=True, index=True, nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('profile_picture', sa.String(), nullable=True),
        sa.Column('last_login', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), onupdate=sa.text('now()')),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('users')
