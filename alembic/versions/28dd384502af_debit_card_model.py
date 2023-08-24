"""Debit Card model

Revision ID: 28dd384502af
Revises: cc4abee59c7c
Create Date: 2023-08-21 21:09:51.988783

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '28dd384502af'
down_revision = 'cc4abee59c7c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('debit_card',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('card_number', sa.String(length=16), nullable=False),
    sa.Column('expired_date', sa.String(), nullable=False),
    sa.Column('cvc', sa.String(), nullable=False),
    sa.Column('name_on_card', sa.String(), nullable=False),
    sa.Column('country', sa.String(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_debit_card_card_number'), 'debit_card', ['card_number'], unique=True)
    op.create_index(op.f('ix_debit_card_cvc'), 'debit_card', ['cvc'], unique=True)
    op.create_index(op.f('ix_debit_card_id'), 'debit_card', ['id'], unique=False)
    op.drop_constraint('available_room_hotel_id_fkey', 'available_room', type_='foreignkey')
    op.create_foreign_key(None, 'available_room', 'hotel', ['hotel_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('hotel_media_hotel_id_fkey', 'hotel_media', type_='foreignkey')
    op.create_foreign_key(None, 'hotel_media', 'hotel', ['hotel_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('hotel_rating_hotel_id_fkey', 'hotel_rating', type_='foreignkey')
    op.drop_constraint('hotel_rating_user_id_fkey', 'hotel_rating', type_='foreignkey')
    op.create_foreign_key(None, 'hotel_rating', 'user', ['user_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'hotel_rating', 'hotel', ['hotel_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('link_amenity_hotel_hotel_id_fkey', 'link_amenity_hotel', type_='foreignkey')
    op.create_foreign_key(None, 'link_amenity_hotel', 'hotel', ['hotel_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('link_freebie_hotel_hotel_id_fkey', 'link_freebie_hotel', type_='foreignkey')
    op.create_foreign_key(None, 'link_freebie_hotel', 'hotel', ['hotel_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'link_freebie_hotel', type_='foreignkey')
    op.create_foreign_key('link_freebie_hotel_hotel_id_fkey', 'link_freebie_hotel', 'hotel', ['hotel_id'], ['id'])
    op.drop_constraint(None, 'link_amenity_hotel', type_='foreignkey')
    op.create_foreign_key('link_amenity_hotel_hotel_id_fkey', 'link_amenity_hotel', 'hotel', ['hotel_id'], ['id'])
    op.drop_constraint(None, 'hotel_rating', type_='foreignkey')
    op.drop_constraint(None, 'hotel_rating', type_='foreignkey')
    op.create_foreign_key('hotel_rating_user_id_fkey', 'hotel_rating', 'user', ['user_id'], ['id'])
    op.create_foreign_key('hotel_rating_hotel_id_fkey', 'hotel_rating', 'hotel', ['hotel_id'], ['id'])
    op.drop_constraint(None, 'hotel_media', type_='foreignkey')
    op.create_foreign_key('hotel_media_hotel_id_fkey', 'hotel_media', 'hotel', ['hotel_id'], ['id'])
    op.drop_constraint(None, 'available_room', type_='foreignkey')
    op.create_foreign_key('available_room_hotel_id_fkey', 'available_room', 'hotel', ['hotel_id'], ['id'])
    op.drop_index(op.f('ix_debit_card_id'), table_name='debit_card')
    op.drop_index(op.f('ix_debit_card_cvc'), table_name='debit_card')
    op.drop_index(op.f('ix_debit_card_card_number'), table_name='debit_card')
    op.drop_table('debit_card')
    # ### end Alembic commands ###