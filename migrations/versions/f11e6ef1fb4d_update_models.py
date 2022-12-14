"""update  models

Revision ID: f11e6ef1fb4d
Revises: 
Create Date: 2022-09-18 13:15:26.890947

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'f11e6ef1fb4d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tag')
    op.drop_index('ix_posts_publish_on', table_name='posts')
    op.drop_index('ix_posts_slug', table_name='posts')
    op.drop_index('ix_posts_title', table_name='posts')
    op.drop_table('posts')
    op.drop_index('ix_tags_slug', table_name='tags')
    op.drop_table('tags')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tags',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('tags_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
    sa.Column('slug', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='tags_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_index('ix_tags_slug', 'tags', ['slug'], unique=False)
    op.create_table('posts',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('posts_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('author_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('slug', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('title', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('body', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('publish_on', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('updated_on', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['author_id'], ['users.id'], name='posts_author_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='posts_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_index('ix_posts_title', 'posts', ['title'], unique=False)
    op.create_index('ix_posts_slug', 'posts', ['slug'], unique=False)
    op.create_index('ix_posts_publish_on', 'posts', ['publish_on'], unique=False)
    op.create_table('tag',
    sa.Column('tags_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('posts_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['posts_id'], ['posts.id'], name='tag_posts_id_fkey'),
    sa.ForeignKeyConstraint(['tags_id'], ['tags.id'], name='tag_tags_id_fkey'),
    sa.PrimaryKeyConstraint('tags_id', 'posts_id', name='tag_pkey')
    )
    # ### end Alembic commands ###
