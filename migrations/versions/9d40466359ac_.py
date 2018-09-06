"""empty message

Revision ID: 9d40466359ac
Revises: 
Create Date: 2018-07-18 10:23:46.746692

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9d40466359ac'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('letter',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=5), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=30), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('city',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('regionName', sa.String(length=255), nullable=True),
    sa.Column('cityCode', sa.Integer(), nullable=True),
    sa.Column('pinYin', sa.String(length=255), nullable=True),
    sa.Column('c_letter', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['c_letter'], ['letter.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('city')
    op.drop_table('user')
    op.drop_table('letter')
    # ### end Alembic commands ###