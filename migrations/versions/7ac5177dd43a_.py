"""empty message

Revision ID: 7ac5177dd43a
Revises: 0dd7a5a5078e
Create Date: 2022-10-22 00:12:03.758723

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7ac5177dd43a'
down_revision = '0dd7a5a5078e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('prevision', sa.String(length=120), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'prevision')
    # ### end Alembic commands ###