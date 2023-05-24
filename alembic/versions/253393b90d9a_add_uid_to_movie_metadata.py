"""add uid to movie metadata

Revision ID: 253393b90d9a
Revises: 51c4e700b8f9
Create Date: 2023-05-24 19:44:37.512122

"""
from alembic import op
import sqlalchemy as sa
import snowflake

# revision identifiers, used by Alembic.
revision = '253393b90d9a'
down_revision = '51c4e700b8f9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        'movie_metadata_raw',
        sa.Column('uid', sa.DECIMAL(), autoincrement=False, nullable=False),
    )
    op.alter_column(
        'movie_metadata_raw',
        'id',
        existing_type=snowflake.sqlalchemy.custom_types._CUSTOM_DECIMAL(precision=38, scale=0),
        nullable=True,
    )


def downgrade() -> None:
    op.alter_column(
        'movie_metadata_raw',
        'id',
        existing_type=snowflake.sqlalchemy.custom_types._CUSTOM_DECIMAL(precision=38, scale=0),
        nullable=False,
    )
    op.drop_column(
        'movie_metadata_raw',
        'uid',
    )
