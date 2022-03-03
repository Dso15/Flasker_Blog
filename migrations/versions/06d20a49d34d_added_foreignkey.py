"""Added ForeignKey

Revision ID: 06d20a49d34d
Revises: cd0bdda36c66
Create Date: 2022-02-24 12:18:33.953755

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '06d20a49d34d'
down_revision = 'cd0bdda36c66'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('poster_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'post', 'user', ['poster_id'], ['id'])
    op.drop_column('post', 'author')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('author', mysql.VARCHAR(length=255), nullable=True))
    op.drop_constraint(None, 'post', type_='foreignkey')
    op.drop_column('post', 'poster_id')
    # ### end Alembic commands ###