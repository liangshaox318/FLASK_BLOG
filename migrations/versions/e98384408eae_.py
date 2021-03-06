"""

Revision ID: e98384408eae
Revises: 2e3b3ca8a665
Create Date: 2020-11-12 16:00:06.798935

"""

# revision identifiers, used by Alembic.
revision = 'e98384408eae'
down_revision = '2e3b3ca8a665'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('body_html', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('posts', 'body_html')
    # ### end Alembic commands ###
