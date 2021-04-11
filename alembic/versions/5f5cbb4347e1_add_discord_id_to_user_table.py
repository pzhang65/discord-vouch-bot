"""add discord_id to User table

Revision ID: 5f5cbb4347e1
Revises:
Create Date: 2021-04-10 19:01:28.001423

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5f5cbb4347e1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('discord_id', sa.Integer))


def downgrade():
    op.drop_column('users', 'discord_id')
