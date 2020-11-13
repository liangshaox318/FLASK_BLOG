"""

Revision ID: 37dd70bce408
Revises: 3cb332104c5a
Create Date: 2020-11-13 16:34:41.336181

"""

# revision identifiers, used by Alembic.
revision = '37dd70bce408'
down_revision = '3cb332104c5a'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('follows',
    sa.Column('follower_id', sa.Integer(), nullable=False),
    sa.Column('followed_id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['followed_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['follower_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('follower_id', 'followed_id')
    )
    op.drop_table('follws')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('follws',
    sa.Column('follower_id', sa.INTEGER(), nullable=False),
    sa.Column('followed_id', sa.INTEGER(), nullable=False),
    sa.Column('timestamp', sa.DATETIME(), nullable=True),
    sa.ForeignKeyConstraint(['followed_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['follower_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('follower_id', 'followed_id')
    )
    op.drop_table('follows')
    # ### end Alembic commands ###
