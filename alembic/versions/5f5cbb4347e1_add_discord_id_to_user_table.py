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
    with op.batch_alter_table("users") as batch_op:
        batch_op.add_column(sa.Column('discord_id', sa.Integer))


def downgrade():
    with op.batch_alter_table("users") as batch_op:
        batch_op.drop_column('discord_id')
