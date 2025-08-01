"""remove bookmark count and likescount

Revision ID: 15ceccedcb80
Revises: 
Create Date: 2025-07-23 18:54:43.091418

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '15ceccedcb80'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('articles', 'likes_count')
    op.drop_column('articles', 'bookmark_count')
    op.create_unique_constraint(None, 'topics', ['title'])
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'topics', type_='unique')
    op.add_column('articles', sa.Column('bookmark_count', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('articles', sa.Column('likes_count', sa.INTEGER(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
