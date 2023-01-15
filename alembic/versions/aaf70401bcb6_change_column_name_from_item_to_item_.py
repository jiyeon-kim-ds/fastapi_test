"""Change column name from item to item_name

Revision ID: aaf70401bcb6
Revises: d3c052010209
Create Date: 2023-01-14 22:39:36.338473

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'aaf70401bcb6'
down_revision = 'd3c052010209'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ledgers', sa.Column('item_name', sa.String(length=255), nullable=True))
    op.drop_column('ledgers', 'item')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ledgers', sa.Column('item', mysql.VARCHAR(collation='utf8mb4_cs_0900_ai_ci', length=255), nullable=True))
    op.drop_column('ledgers', 'item_name')
    # ### end Alembic commands ###
