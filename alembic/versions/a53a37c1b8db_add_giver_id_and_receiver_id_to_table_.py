"""Add giver_id and receiver_id to table vouches

Revision ID: a53a37c1b8db
Revises: cb9c72b3a19d
Create Date: 2021-04-11 11:48:58.726819

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a53a37c1b8db'
down_revision = 'cb9c72b3a19d'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("vouches") as batch_op:
        batch_op.add_column(sa.Column('giver_id', sa.Integer))
        batch_op.add_column(sa.Column('receiver_id', sa.Integer))


def downgrade():
    with op.batch_alter_table("vouches") as batch_op:
        batch_op.drop_column('giver_id')
        batch_op.drop_column('receiver_id')
