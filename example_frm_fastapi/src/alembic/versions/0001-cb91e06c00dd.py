"""0001

Revision ID: cb91e06c00dd
Revises: 
Create Date: 2022-11-26 03:24:21.074881

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cb91e06c00dd'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('example',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_example_id'), 'example', ['id'], unique=False)
    op.create_index(op.f('ix_example_name'), 'example', ['name'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_example_name'), table_name='example')
    op.drop_index(op.f('ix_example_id'), table_name='example')
    op.drop_table('example')
    # ### end Alembic commands ###
