"""empty message

Revision ID: 90de85732495
Revises: fa55a2adcb75
Create Date: 2019-03-28 04:06:06.850099

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '90de85732495'
down_revision = 'fa55a2adcb75'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tabs', sa.Column('is_group_tab', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tabs', 'is_group_tab')
    # ### end Alembic commands ###
