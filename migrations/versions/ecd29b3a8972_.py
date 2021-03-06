"""empty message

Revision ID: ecd29b3a8972
Revises: a61c9afc7e4c
Create Date: 2020-06-01 21:17:12.972582

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ecd29b3a8972'
down_revision = 'a61c9afc7e4c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Artist', sa.Column('website', sa.String(length=250), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Artist', 'website')
    # ### end Alembic commands ###
