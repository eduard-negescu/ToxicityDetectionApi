"""empty message

Revision ID: 1ec80219ed99
Revises: 7269629ee9d3
Create Date: 2025-03-25 18:16:20.593805

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1ec80219ed99'
down_revision: Union[str, None] = '7269629ee9d3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('prompts', sa.Column('model_rating', sa.String(), nullable=True))
    op.drop_column('prompts', 'output')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('prompts', sa.Column('output', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('prompts', 'model_rating')
    # ### end Alembic commands ###
