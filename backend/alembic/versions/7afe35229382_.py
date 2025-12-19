"""empty message

Revision ID: 7afe35229382
Revises: bfc09d39c1cc
Create Date: 2025-12-16 12:23:43.763116

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7afe35229382'
down_revision: Union[str, None] = 'bfc09d39c1cc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
