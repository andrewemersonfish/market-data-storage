"""Simple tables matching pandas

Revision ID: 03fce6cba803
Revises: 
Create Date: 2024-12-26 14:19:39.526465

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '03fce6cba803'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('day_aggs',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('ticker', sa.Text(), nullable=True),
    sa.Column('volume', sa.Integer(), nullable=True),
    sa.Column('open', sa.Float(), nullable=True),
    sa.Column('close', sa.Float(), nullable=True),
    sa.Column('high', sa.Float(), nullable=True),
    sa.Column('low', sa.Float(), nullable=True),
    sa.Column('window_start', sa.Integer(), nullable=True),
    sa.Column('transactions', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('minute_aggs',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('ticker', sa.Text(), nullable=True),
    sa.Column('volume', sa.Integer(), nullable=True),
    sa.Column('open', sa.Float(), nullable=True),
    sa.Column('close', sa.Float(), nullable=True),
    sa.Column('high', sa.Float(), nullable=True),
    sa.Column('low', sa.Float(), nullable=True),
    sa.Column('window_start', sa.Integer(), nullable=True),
    sa.Column('transactions', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('trades',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('ticker', sa.Text(), nullable=True),
    sa.Column('conditions', sa.Float(), nullable=True),
    sa.Column('correction', sa.Integer(), nullable=True),
    sa.Column('exchange', sa.Integer(), nullable=True),
    sa.Column('price', sa.Float(), nullable=True),
    sa.Column('sip_timestamp', sa.BigInteger(), nullable=True),
    sa.Column('size', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('trades')
    op.drop_table('minute_aggs')
    op.drop_table('day_aggs')
    # ### end Alembic commands ###
