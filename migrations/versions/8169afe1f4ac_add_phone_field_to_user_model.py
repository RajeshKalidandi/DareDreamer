"""Add phone field to User model

Revision ID: 8169afe1f4ac
Revises: 
Create Date: 2024-10-09 23:46:55.089084

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8169afe1f4ac'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Check if the column exists before adding it
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    columns = inspector.get_columns('user')
    if 'phone' not in [col['name'] for col in columns]:
        op.add_column('user', sa.Column('phone', sa.String(length=20), nullable=True))


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'phone')
    # ### end Alembic commands ###
