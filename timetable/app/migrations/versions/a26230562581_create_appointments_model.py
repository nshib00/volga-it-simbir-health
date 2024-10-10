"""Create appointments model

Revision ID: a26230562581
Revises: 40bef4a8e664
Create Date: 2024-10-04 10:28:19.989963

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a26230562581'
down_revision: Union[str, None] = '40bef4a8e664'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('appointments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('timetable_id', sa.Integer(), nullable=True),
    sa.Column('from_', sa.DateTime(), nullable=True),
    sa.Column('to', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['timetable_id'], ['timetables.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('appointments')
    # ### end Alembic commands ###