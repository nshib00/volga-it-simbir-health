"""Add ondelete and onupdate in refresh_tokens

Revision ID: 2dc35f456a89
Revises: b15cf45f2919
Create Date: 2024-10-27 11:31:40.206297

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2dc35f456a89'
down_revision: Union[str, None] = 'b15cf45f2919'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('refresh_tokens_user_id_fkey', 'refresh_tokens', type_='foreignkey')
    op.create_foreign_key(None, 'refresh_tokens', 'users', ['user_id'], ['id'], onupdate='CASCADE', ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'refresh_tokens', type_='foreignkey')
    op.create_foreign_key('refresh_tokens_user_id_fkey', 'refresh_tokens', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###