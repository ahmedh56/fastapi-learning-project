"""add content column to posts table

Revision ID: 505987cebd73
Revises: 2e272c2e045d
Create Date: 2025-02-08 04:08:34.608106

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '505987cebd73'
down_revision: Union[str, None] = '2e272c2e045d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass
