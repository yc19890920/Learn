"""First create user add role table

Revision ID: 45331b8431fc
Revises: 
Create Date: 2020-05-04 22:08:23.815119

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '45331b8431fc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('roles',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=32), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.VARCHAR(length=32), nullable=True),
    sa.Column('password', sa.VARCHAR(length=32), nullable=True),
    sa.Column('email', sa.VARCHAR(length=32), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_email_pwd', 'user', ['email', 'password'], unique=False)
    op.create_index('ix_user_pwd', 'user', ['username', 'password'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_user_pwd', table_name='user')
    op.drop_index('ix_email_pwd', table_name='user')
    op.drop_table('user')
    op.drop_table('roles')
    # ### end Alembic commands ###
