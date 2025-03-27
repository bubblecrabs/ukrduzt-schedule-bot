"""Initial migration

Revision ID: 6edd38e70512
Revises: 
Create Date: 2025-03-26 15:41:02.183363

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6edd38e70512'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('username', sa.String(length=35), nullable=True),
    sa.Column('user_faculty', sa.Integer(), nullable=True),
    sa.Column('user_course', sa.Integer(), nullable=True),
    sa.Column('user_group', sa.Integer(), nullable=True),
    sa.Column('user_group_name', sa.String(length=50), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id'),
    sa.UniqueConstraint('username')
    )
    op.create_index(op.f('ix_users_is_admin'), 'users', ['is_admin'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_is_admin'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###
