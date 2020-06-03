"""empty message

Revision ID: e5ae33e18153
Revises: e63cf70409b0
Create Date: 2020-06-04 01:59:54.994127

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e5ae33e18153'
down_revision = 'e63cf70409b0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Artist', sa.Column('phone', sa.String(length=10), nullable=True))
    op.add_column('Venue', sa.Column('phone', sa.String(length=10), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Venue', 'phone')
    op.drop_column('Artist', 'phone')
    # ### end Alembic commands ###