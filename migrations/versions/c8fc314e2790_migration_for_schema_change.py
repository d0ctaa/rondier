""" migration for schema change.

Revision ID: c8fc314e2790
Revises: 1c75db0d68ca
Create Date: 2024-01-15 22:39:01.375573

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c8fc314e2790'
down_revision = '1c75db0d68ca'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('DeviceInventory',
    sa.Column('machine_id', sa.Integer(), nullable=False),
    sa.Column('Make', sa.String(length=100), nullable=False),
    sa.Column('Model', sa.String(length=100), nullable=False),
    sa.Column('Year', sa.Integer(), nullable=True),
    sa.Column('SerialNumber', sa.String(length=100), nullable=False),
    sa.Column('Purpose', sa.String(length=100), nullable=False),
    sa.Column('location', sa.String(length=100), nullable=False),
    sa.Column('img', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('machine_id'),
    schema='r-schema-01'
    )
    op.drop_table('device_inventory')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('device_inventory',
    sa.Column('machine_id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('Make', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('Model', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('Year', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('SerialNumber', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('Purpose', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('location', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('img', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('machine_id', name='device_inventory_pkey')
    )
    op.drop_table('DeviceInventory', schema='r-schema-01')
    # ### end Alembic commands ###