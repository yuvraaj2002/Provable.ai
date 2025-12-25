"""Initial migration

Revision ID: 1344a6b346e7
Revises: 
Create Date: 2025-12-25 11:19:25.018870

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1344a6b346e7'
down_revision: Union[str, Sequence[str], None] = None
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
