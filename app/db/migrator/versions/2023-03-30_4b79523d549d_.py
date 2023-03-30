"""empty message

Revision ID: 4b79523d549d
Revises: edc68cb15b6f
Create Date: 2023-03-30 15:20:07.010101

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4b79523d549d'
down_revision = 'edc68cb15b6f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('participant', sa.Column('parent_id', sa.Integer(), nullable=True))
    op.drop_constraint('fk__participant__recipient_id__participant', 'participant', type_='foreignkey')
    op.create_foreign_key(op.f('fk__participant__parent_id__participant'), 'participant', 'participant', ['parent_id'], ['id'], ondelete='CASCADE')
    op.drop_column('participant', 'recipient_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('participant', sa.Column('recipient_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(op.f('fk__participant__parent_id__participant'), 'participant', type_='foreignkey')
    op.create_foreign_key('fk__participant__recipient_id__participant', 'participant', 'participant', ['recipient_id'], ['id'], ondelete='CASCADE')
    op.drop_column('participant', 'parent_id')
    # ### end Alembic commands ###
