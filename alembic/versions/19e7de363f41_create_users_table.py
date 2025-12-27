"""Create users table

Revision ID: 19e7de363f41
Revises: 1344a6b346e7
Create Date: 2025-12-25 11:18:47.900017

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '19e7de363f41'
down_revision: Union[str, Sequence[str], None] = '1344a6b346e7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Table already created in 1344a6b346e7, so this is a no-op
    pass


def downgrade() -> None:
    """Downgrade schema."""
    # Table will be dropped in 1344a6b346e7 downgrade, so this is a no-op
    pass
