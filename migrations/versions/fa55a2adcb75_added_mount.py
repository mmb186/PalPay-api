"""added amount column to transaction table

Revision ID: fa55a2adcb75
Revises: 2d745567e4df
Create Date: 2019-02-20 13:27:35.317168

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fa55a2adcb75'
down_revision = '2d745567e4df'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tab_transactions', sa.Column('amount', sa.Float(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tab_transactions', 'amount')
    # ### end Alembic commands ###
