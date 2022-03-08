"""added relationship between user and message

Revision ID: a24e6b333a4b
Revises: 
Create Date: 2022-03-08 10:40:18.205154

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a24e6b333a4b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('message', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'message', 'user', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'message', type_='foreignkey')
    op.drop_column('message', 'user_id')
    # ### end Alembic commands ###