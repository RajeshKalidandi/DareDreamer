from alembic import op
import sqlalchemy as sa

def upgrade():
    # Add any new columns or modifications here
    # For example:
    # op.add_column('job', sa.Column('source', sa.String(length=50), nullable=True))
    pass

def downgrade():
    # Add corresponding downgrade operations
    # For example:
    # op.drop_column('job', 'source')
    pass