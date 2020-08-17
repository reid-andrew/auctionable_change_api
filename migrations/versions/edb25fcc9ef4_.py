"""empty message

Revision ID: edb25fcc9ef4
Revises: 097dfcd05240
Create Date: 2020-07-25 17:11:47.562241

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'edb25fcc9ef4'
down_revision = '995a9519c95d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('finals',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('street_address', sa.String(), nullable=True),
    sa.Column('city', sa.String(), nullable=True),
    sa.Column('state', sa.String(), nullable=True),
    sa.Column('zip_code', sa.String(), nullable=True),
    sa.Column('receipt', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_column('bids', 'state')
    op.drop_column('bids', 'zip_code')
    op.drop_column('bids', 'street_address')
    op.drop_column('bids', 'receipt')
    op.drop_column('bids', 'city')
    op.add_column('items', sa.Column('bidding_time', sa.Float(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('items', 'bidding_time')
    op.add_column('bids', sa.Column('city', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('bids', sa.Column('receipt', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('bids', sa.Column('street_address', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('bids', sa.Column('zip_code', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('bids', sa.Column('state', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_table('finals')
    # ### end Alembic commands ###
