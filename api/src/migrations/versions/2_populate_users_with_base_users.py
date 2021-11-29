"""empty message

Revision ID: 2_populate_users_with_base_users
Revises: 1_add_user_table
Create Date: 2021-11-28 21:18:13.258484

"""
import uuid

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
from application.users.enums import Group

revision = '2_populate_users_with_base_users'
down_revision = '1_add_user_table'
branch_labels = None
depends_on = None


def upgrade():
    op.execute('INSERT INTO users (uuid, email, password, user_group, is_active) VALUES (\'{0}\', \'{1}\', \'{2}\', \'{3}\', \'{4}\')'
        .format(
            str(uuid.uuid4()),
            'admin_user@admin.com',
            '123456',
            Group.admin.value,
            True)
        )
    op.execute('INSERT INTO users (uuid, email, password, user_group, is_active) VALUES (\'{0}\', \'{1}\', \'{2}\', \'{3}\', \'{4}\')'
        .format(
            str(uuid.uuid4()),
            'customer_user@customer.com',
            '123456',
            Group.customer.value,
            True)
        )


def downgrade():
    # op.execute('DELETE FROM users WHERE email=admin_user@admin.com')
    # op.execute('DELETE FROM users WHERE email=customer_user@customer.com')
    pass
