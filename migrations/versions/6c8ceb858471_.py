"""empty message

Revision ID: 6c8ceb858471
Revises: ebb545f031b7
Create Date: 2021-01-19 17:48:29.733961

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6c8ceb858471'
down_revision = 'ebb545f031b7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Show', sa.Column('artist_image_link', sa.String(length=500), nullable=True))
    op.add_column('Show', sa.Column('artist_name', sa.String(length=60), nullable=True))
    op.add_column('Show', sa.Column('venue_image_link', sa.String(length=500), nullable=True))
    op.add_column('Show', sa.Column('venue_name', sa.String(length=60), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Show', 'venue_name')
    op.drop_column('Show', 'venue_image_link')
    op.drop_column('Show', 'artist_name')
    op.drop_column('Show', 'artist_image_link')
    # ### end Alembic commands ###