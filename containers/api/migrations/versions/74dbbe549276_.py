"""empty message

Revision ID: 74dbbe549276
Revises: b491f47d7777
Create Date: 2019-05-25 18:24:12.928398

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '74dbbe549276'
down_revision = 'b491f47d7777'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('password_hash', sa.String(length=255), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'password_hash')
    # ### end Alembic commands ###
