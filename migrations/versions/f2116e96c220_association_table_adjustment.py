"""association table adjustment

Revision ID: f2116e96c220
Revises: 5be2e7eb0ea3
Create Date: 2024-01-22 07:16:05.021290

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f2116e96c220'
down_revision = '5be2e7eb0ea3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    '''op.create_table('DeviceInventory',
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
    schema='r-schema-01')'''

    #op.add_column('Employees', sa.Column('fs_uniquifier', sa.String(length=255), nullable=True), schema='r-schema-01')
    
    '''op.create_table('Roles',
    sa.Column('r_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=32), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('r_id'),
    schema='r-schema-01'
    )
    op.create_table('Metrics',
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
    )'''
    '''op.create_table('roles_users',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['r-schema-01.Roles.r_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['r-schema-01.Employees.employee_id'], ),
    schema='r-schema-01'
    )
    op.drop_table('roles_users')'''
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('roles_users',
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('role_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['r-schema-01.Roles.r_id'], name='roles_users_role_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['r-schema-01.Employees.employee_id'], name='roles_users_user_id_fkey')
    )
    op.drop_table('roles_users', schema='r-schema-01')
    op.drop_table('Metrics', schema='r-schema-01')
    op.drop_table('Roles', schema='r-schema-01')
    op.drop_table('Employees', schema='r-schema-01')
    op.drop_table('DeviceInventory', schema='r-schema-01')
    # ### end Alembic commands ###
