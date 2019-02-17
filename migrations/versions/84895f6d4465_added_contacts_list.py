"""added contacts list

Revision ID: 84895f6d4465
Revises: 7436a8d73842
Create Date: 2019-02-17 10:20:31.793521

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '84895f6d4465'
down_revision = '7436a8d73842'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('trusted_contacts',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('contact_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['contact_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], )
    )
    op.create_unique_constraint(None, 'blacklisted_token', ['id'])
    op.add_column('users', sa.Column('last_modified_time', sa.DateTime(), nullable=True))
    op.add_column('users', sa.Column('username', sa.String(length=255), nullable=False))
    op.alter_column('users', 'password',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
    op.drop_constraint('users_public_id_key', 'users', type_='unique')
    op.create_unique_constraint(None, 'users', ['username'])
    op.drop_column('users', 'public_id')
    op.drop_column('users', 'last_updated_time')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('last_updated_time', postgresql.TIMESTAMP(), autoincrement=False, nullable=False))
    op.add_column('users', sa.Column('public_id', sa.VARCHAR(length=50), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'users', type_='unique')
    op.create_unique_constraint('users_public_id_key', 'users', ['public_id'])
    op.alter_column('users', 'password',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
    op.drop_column('users', 'username')
    op.drop_column('users', 'last_modified_time')
    op.drop_constraint(None, 'blacklisted_token', type_='unique')
    op.drop_table('trusted_contacts')
    # ### end Alembic commands ###