"""empty message

Revision ID: 51f5b81af285
Revises: 5e1bfb86961e
Create Date: 2020-06-03 10:39:17.534981

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '51f5b81af285'
down_revision = '5e1bfb86961e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Show', 'start_time')
    op.drop_column('Venue', 'website')
    op.drop_column('Venue', 'genres')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Venue', sa.Column('genres', postgresql.ARRAY(sa.VARCHAR()), autoincrement=False, nullable=True))
    op.add_column('Venue', sa.Column('website', sa.VARCHAR(length=250), autoincrement=False, nullable=True))
    op.add_column('Show', sa.Column('start_time', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###