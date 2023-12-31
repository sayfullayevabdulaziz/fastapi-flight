"""country model added

Revision ID: 6314676aa0b6
Revises: aa7da54c042f
Create Date: 2023-08-30 00:30:33.565330

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6314676aa0b6'
down_revision = 'aa7da54c042f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('address', sa.String(), nullable=True))
    op.add_column('user', sa.Column('birthday', sa.Date(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'address')
    op.drop_column('user', 'birthday')
    # ### end Alembic commands ###