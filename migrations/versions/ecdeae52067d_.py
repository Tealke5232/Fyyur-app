"""empty message

Revision ID: ecdeae52067d
Revises: 498c0b822ffe
Create Date: 2021-01-19 21:18:21.248024

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ecdeae52067d'
down_revision = '498c0b822ffe'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('AGenre')
    op.drop_table('VGenre')
    op.add_column('Artist', sa.Column('genres', sa.String(length=120), nullable=True))
    op.add_column('Venue', sa.Column('genres', sa.String(length=120), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Venue', 'genres')
    op.drop_column('Artist', 'genres')
    op.create_table('VGenre',
    sa.Column('id', sa.INTEGER(), server_default=sa.text('nextval(\'"VGenre_id_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
    sa.Column('venue_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['venue_id'], ['Venue.id'], name='VGenre_venue_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='VGenre_pkey')
    )
    op.create_table('AGenre',
    sa.Column('id', sa.INTEGER(), server_default=sa.text('nextval(\'"AGenre_id_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
    sa.Column('artist_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['artist_id'], ['Artist.id'], name='AGenre_artist_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='AGenre_pkey')
    )
    # ### end Alembic commands ###
