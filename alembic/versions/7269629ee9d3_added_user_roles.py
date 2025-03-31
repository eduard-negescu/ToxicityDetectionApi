"""Added user roles

Revision ID: 7269629ee9d3
Revises: 18631bc374d6
Create Date: 2025-03-19 11:59:14.580147

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7269629ee9d3'
down_revision: Union[str, None] = '18631bc374d6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

user_role_type = sa.Enum('USER', 'ADMIN', name='userrole')

def upgrade():
    # Create the enum type in PostgreSQL
    user_role_type.create(op.get_bind())

    # Add the role column to the users table
    op.add_column('users', sa.Column('role', user_role_type, nullable=True))

def downgrade():
    # Remove the role column from the users table
    op.drop_column('users', 'role')

    # Drop the enum type from PostgreSQL
    user_role_type.drop(op.get_bind())
