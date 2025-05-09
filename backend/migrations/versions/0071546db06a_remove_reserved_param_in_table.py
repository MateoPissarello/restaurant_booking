"""remove reserved param in table

Revision ID: 0071546db06a
Revises: 1c0696c7c0f0
Create Date: 2025-04-28 09:05:43.003170

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0071546db06a'
down_revision: Union[str, None] = '1c0696c7c0f0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tables', 'reserved')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tables', sa.Column('reserved', sa.BOOLEAN(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
