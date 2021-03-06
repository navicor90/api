# -*- coding: utf-8 -*-

"""Creación de comentarios para análisis

Revision ID: 3c6208d72ac0
Revises: 1bd92883a744
Create Date: 2015-10-17 20:45:35.339463

"""

# revision identifiers, used by Alembic.
revision = '3c6208d72ac0'
down_revision = '1bd92883a744'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('analysis_comment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('datetime', sa.DateTime(), nullable=True),
    sa.Column('comment', sa.UnicodeText(), nullable=True),
    sa.Column('analysis_id', sa.Integer(), nullable=True),
    sa.Column('profile_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['analysis_id'], ['analysis.id'], ),
    sa.ForeignKeyConstraint(['profile_id'], ['profile.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('analysis_comment')
    ### end Alembic commands ###
