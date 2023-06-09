"""empty message

Revision ID: 982e5b7f850d
Revises: 
Create Date: 2023-05-15 03:27:07.189567

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '982e5b7f850d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('finam_reports',
    sa.Column('date_record', sa.Date(), server_default='2001-01-01', nullable=False),
    sa.Column('date_time_record', sa.Time(), server_default='00:00:00', nullable=False),
    sa.Column('symbol_name_record', sa.VARCHAR(length=150), server_default=' ', nullable=False),
    sa.Column('account_prefix_record', sa.VARCHAR(length=50), server_default=' ', nullable=False),
    sa.Column('account_record', sa.VARCHAR(length=50), server_default=' ', nullable=False),
    sa.Column('account_id_record', sa.Integer(), server_default='0', nullable=False),
    sa.Column('isin_record', sa.VARCHAR(length=50), server_default=' ', nullable=False),
    sa.Column('type_record', sa.VARCHAR(length=500), server_default=' ', nullable=False),
    sa.Column('count_record', sa.Integer(), server_default='0', nullable=False),
    sa.Column('deal_price_record', sa.Float(precision=2), server_default='0', nullable=False),
    sa.Column('sum_record', sa.DOUBLE_PRECISION(), server_default='0', nullable=False),
    sa.Column('deal_id_record', sa.VARCHAR(length=50), server_default='', nullable=False),
    sa.Column('comment_record', sa.VARCHAR(length=500), server_default=' ', nullable=False),
    sa.Column('symbol_record', sa.VARCHAR(length=50), server_default=' ', nullable=False),
    sa.Column('datetime_add', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('date_record', 'date_time_record', 'symbol_name_record', 'account_record', 'sum_record')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('finam_reports')
    # ### end Alembic commands ###
