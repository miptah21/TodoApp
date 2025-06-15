"""Create phone number for user column

Revision ID: 3e70917a537c
Revises: 
Create Date: 2025-05-30 00:23:24.197273

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3e70917a537c'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('users', sa.Column('phone_number', sa.String(length=15), nullable=True))
    # op.create_index(op.f('ix_users_phone_number'), 'users', ['phone_number'], unique=False)
    # # Add a comment to the column
    # with op.batch_alter_table('users', schema=None) as batch_op:
    #     batch_op.alter_column('phone_number', comment='User phone number')


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users', 'phone_number')
    # op.drop_index(op.f('ix_users_phone_number'), table_name='users')
    # with op.batch_alter_table('users', schema=None) as batch_op:
    #     batch_op.alter_column('phone_number', comment=None)
#     # Remove the comment from the column
