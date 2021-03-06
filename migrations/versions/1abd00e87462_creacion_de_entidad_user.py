# -*- coding: utf-8 -*-

"""Creación de entidad 'User'

Revision ID: 1abd00e87462
Revises: 309c776b77
Create Date: 2015-08-31 01:53:09.418506

"""

# revision identifiers, used by Alembic.
revision = '1abd00e87462'
down_revision = '309c776b77'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=32), nullable=True),
    sa.Column('email', sa.String(length=64), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('profile_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['profile_id'], ['profile.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_table('user')
    ### end Alembic commands ###
