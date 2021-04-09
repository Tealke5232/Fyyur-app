"""empty message

Revision ID: 038525ea4581
Revises: ecdeae52067d
Create Date: 2021-01-19 21:24:18.379002

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '038525ea4581'
down_revision = 'ecdeae52067d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Venue', 'genres')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Venue', sa.Column('genres', sa.VARCHAR(length=120), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
