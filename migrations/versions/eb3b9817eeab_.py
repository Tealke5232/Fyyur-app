"""empty message

Revision ID: eb3b9817eeab
Revises: a6be04754617
Create Date: 2021-01-20 00:40:36.077533

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eb3b9817eeab'
down_revision = 'a6be04754617'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Artist', sa.Column('active_click', sa.Integer(), nullable=True))
    op.add_column('Song', sa.Column('active_click', sa.Integer(), nullable=True))
    op.add_column('Song', sa.Column('description', sa.String(length=240), nullable=True))
    op.add_column('Song', sa.Column('image_link', sa.String(length=500), nullable=True))
    op.add_column('Venue', sa.Column('active_click', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Venue', 'active_click')
    op.drop_column('Song', 'image_link')
    op.drop_column('Song', 'description')
    op.drop_column('Song', 'active_click')
    op.drop_column('Artist', 'active_click')
    # ### end Alembic commands ###
