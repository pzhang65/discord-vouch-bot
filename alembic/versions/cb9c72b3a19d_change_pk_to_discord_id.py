"""Change PK to discord_id

Revision ID: cb9c72b3a19d
Revises: 5f5cbb4347e1
Create Date: 2021-04-11 02:22:37.888099

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cb9c72b3a19d'
down_revision = '5f5cbb4347e1'
branch_labels = None
depends_on = None

'''
Ended up using db browser to manually change pk
'''
def upgrade():
    pass

def downgrade():
    pass
