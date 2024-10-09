"""Update Job model for scraped data

Revision ID: 5ed7a47c1309
Revises: 8169afe1f4ac
Create Date: 2024-10-09 23:57:00.407859

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '5ed7a47c1309'
down_revision = '8169afe1f4ac'
branch_labels = None
depends_on = None

def upgrade():
    # Create a new table with the desired schema
    op.create_table('new_job',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('company', sa.String(length=100), nullable=False),
        sa.Column('location', sa.String(length=100), nullable=True),
        sa.Column('url', sa.String(length=500), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('salary', sa.String(length=50), nullable=True),
        sa.Column('date_posted', sa.DateTime(), nullable=True),
        sa.Column('job_type', sa.String(length=50), nullable=True),
        sa.Column('experience_level', sa.String(length=50), nullable=True),
        sa.Column('employer_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['employer_id'], ['employer.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Copy data from the old table to the new table
    op.execute('INSERT INTO new_job (id, title, company, location, url, description, date_posted, employer_id) '
               'SELECT id, title, company, location, url, description, date_posted, employer_id FROM job')

    # Drop the old table
    op.drop_table('job')

    # Rename the new table to the original name
    op.rename_table('new_job', 'job')

def downgrade():
    # Create a new table with the old schema
    op.create_table('old_job',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('company', sa.String(length=100), nullable=False),
        sa.Column('location', sa.String(length=100), nullable=True),
        sa.Column('url', sa.String(length=500), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('requirements', sa.Text(), nullable=True),
        sa.Column('salary_range', sa.String(length=50), nullable=True),
        sa.Column('date_posted', sa.DateTime(), nullable=True),
        sa.Column('employer_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['employer_id'], ['employer.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Copy data from the current table to the old schema table
    op.execute('INSERT INTO old_job (id, title, company, location, url, description, date_posted, employer_id) '
               'SELECT id, title, company, location, url, description, date_posted, employer_id FROM job')

    # Drop the current table
    op.drop_table('job')

    # Rename the old schema table to the original name
    op.rename_table('old_job', 'job')