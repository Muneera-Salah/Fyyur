"""empty message

Revision ID: e63cf70409b0
Revises: 9e8b65d19fea
Create Date: 2020-06-04 01:59:39.242359

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e63cf70409b0'
down_revision = '9e8b65d19fea'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Artist', 'phone')
    op.drop_column('Venue', 'phone')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Venue', sa.Column('phone', sa.VARCHAR(length=120), autoincrement=False, nullable=True))
    op.add_column('Artist', sa.Column('phone', sa.VARCHAR(length=120), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
