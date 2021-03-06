"""empty message

Revision ID: 9fe8f7a7782a
Revises: 
Create Date: 2021-02-01 02:53:13.219661

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9fe8f7a7782a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('projects',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('user_id', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('clusters',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('x_position', sa.Integer(), nullable=True),
    sa.Column('y_position', sa.Integer(), nullable=True),
    sa.Column('project_id', sa.Integer(), nullable=True),
    sa.Column('parent_cluster_id', sa.Integer(), nullable=True),
    sa.CheckConstraint('(NOT(project_id IS NULL AND parent_cluster_id IS NULL)) AND(NOT(project_id IS NOT NULL AND parent_cluster_id IS NOT NULL))'),
    sa.ForeignKeyConstraint(['parent_cluster_id'], ['clusters.id'], ),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('shared_projects',
    sa.Column('shared_proj', sa.Integer(), nullable=False),
    sa.Column('shared_user', sa.String(), nullable=True),
    sa.Column('role', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['shared_proj'], ['projects.id'], ),
    sa.PrimaryKeyConstraint('shared_proj')
    )
    op.create_table('sources',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('url', sa.String(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('content', sa.String(), nullable=True),
    sa.Column('is_included', sa.Boolean(), nullable=True),
    sa.Column('author', sa.String(), nullable=True),
    sa.Column('published_date', sa.DateTime(), nullable=True),
    sa.Column('site_name', sa.String(), nullable=True),
    sa.Column('access_date', sa.DateTime(), nullable=True),
    sa.Column('project_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('project_id', 'url')
    )
    op.create_table('edges',
    sa.Column('from_id', sa.Integer(), nullable=False),
    sa.Column('to_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['from_id'], ['sources.id'], ),
    sa.ForeignKeyConstraint(['to_id'], ['sources.id'], ),
    sa.PrimaryKeyConstraint('from_id', 'to_id')
    )
    op.create_table('items',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('source_id', sa.Integer(), nullable=True),
    sa.Column('is_note', sa.Boolean(), nullable=False),
    sa.Column('content', sa.String(), nullable=True),
    sa.Column('x_position', sa.Integer(), nullable=True),
    sa.Column('y_position', sa.Integer(), nullable=True),
    sa.Column('date_of_creation', sa.DateTime(), nullable=False),
    sa.Column('parent_project', sa.Integer(), nullable=True),
    sa.Column('parent_cluster', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['parent_cluster'], ['clusters.id'], ),
    sa.ForeignKeyConstraint(['parent_project'], ['projects.id'], ),
    sa.ForeignKeyConstraint(['source_id'], ['sources.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('items')
    op.drop_table('edges')
    op.drop_table('sources')
    op.drop_table('shared_projects')
    op.drop_table('clusters')
    op.drop_table('projects')
    # ### end Alembic commands ###
