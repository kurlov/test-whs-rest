"""empty message

Revision ID: 50aec182cb12
Revises: 1b450e3296f1
Create Date: 2018-11-12 04:24:26.759870

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '50aec182cb12'
down_revision = '1b450e3296f1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order', sa.Column('normalized', sa.String(length=255), nullable=True))
    op.create_index(op.f('ix_order_normalized'), 'order', ['normalized'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_order_normalized'), table_name='order')
    op.drop_column('order', 'normalized')
    # ### end Alembic commands ###