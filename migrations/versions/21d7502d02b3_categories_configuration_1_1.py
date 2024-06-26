"""categories configuration 1.1

Revision ID: 21d7502d02b3
Revises: b37e9071a153
Create Date: 2024-01-24 06:23:31.949851

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '21d7502d02b3'
down_revision = 'b37e9071a153'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    '''op.create_table('Categories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=32), nullable=True),
    sa.Column('code', sa.String(length=32), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    schema='r-schema-01'
    )
    op.create_table('CircuitBraker',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('manufacturer', sa.String(length=32), nullable=True),
    sa.Column('model', sa.String(length=32), nullable=True),
    sa.Column('type', sa.String(length=32), nullable=True),
    sa.Column('rated_volate', sa.String(length=32), nullable=True),
    sa.Column('rated_current', sa.String(length=32), nullable=True),
    sa.Column('pole_conf', sa.String(length=32), nullable=True),
    sa.Column('trip_unit_type', sa.String(length=32), nullable=True),
    sa.Column('trip_current_rating', sa.String(length=32), nullable=True),
    sa.Column('operating_vol', sa.String(length=32), nullable=True),
    sa.Column('standard', sa.String(length=32), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    schema='r-schema-01'
    )
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
    op.create_table('Employees',
    sa.Column('employee_id', sa.Integer(), nullable=False),
    sa.Column('FirstName', sa.String(length=100), nullable=False),
    sa.Column('LastName', sa.String(length=100), nullable=False),
    sa.Column('Birthdate', sa.Date(), nullable=True),
    sa.Column('JobTitle', sa.String(length=100), nullable=False),
    sa.Column('UserName', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('pwhash', sa.String(length=128), nullable=True),
    sa.Column('fs_uniquifier', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('employee_id'),
    sa.UniqueConstraint('UserName'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('fs_uniquifier'),
    schema='r-schema-01'
    )
    op.create_table('Roles',
    sa.Column('r_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=32), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('r_id'),
    schema='r-schema-01'
    )'''
    op.create_table('Transformers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('manufacturer', sa.String(length=32), nullable=True),
    sa.Column('model', sa.String(length=32), nullable=True),
    sa.Column('type', sa.String(length=32), nullable=True),
    sa.Column('rated_voltage_1', sa.String(length=32), nullable=True),
    sa.Column('rated_voltage_2', sa.String(length=32), nullable=True),
    sa.Column('rated_power', sa.String(length=32), nullable=True),
    sa.Column('rated_frequency', sa.String(length=32), nullable=True),
    sa.Column('winding_Conf', sa.String(length=32), nullable=True),
    sa.Column('impedance_voltage', sa.String(length=32), nullable=True),
    sa.Column('insulation_class', sa.String(length=32), nullable=True),
    sa.Column('standard', sa.String(length=32), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    schema='r-schema-01'
    )
    '''op.create_table('Metrics',
    sa.Column('item_id', sa.Integer(), nullable=False),
    sa.Column('system_id', sa.Integer(), nullable=True),
    sa.Column('Value1', sa.String(length=100), nullable=False),
    sa.Column('Value2', sa.String(length=100), nullable=False),
    sa.Column('Value3', sa.String(length=100), nullable=False),
    sa.Column('Value4', sa.String(length=100), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('EmpID', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['EmpID'], ['r-schema-01.Employees.employee_id'], ),
    sa.ForeignKeyConstraint(['system_id'], ['r-schema-01.DeviceInventory.machine_id'], ),
    sa.PrimaryKeyConstraint('item_id'),
    schema='r-schema-01'
    )
    op.create_table('roles_users',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['r-schema-01.Roles.r_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['r-schema-01.Employees.employee_id'], ),
    schema='r-schema-01'
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('roles_users', schema='r-schema-01')
    op.drop_table('Metrics', schema='r-schema-01')
    op.drop_table('Transformers', schema='r-schema-01')
    op.drop_table('Roles', schema='r-schema-01')
    op.drop_table('Employees', schema='r-schema-01')
    op.drop_table('DeviceInventory', schema='r-schema-01')
    op.drop_table('CircuitBraker', schema='r-schema-01')
    op.drop_table('Categories', schema='r-schema-01')
    # ### end Alembic commands ###'''
