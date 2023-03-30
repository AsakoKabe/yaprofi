"""empty message

Revision ID: 6e672dcd46a5
Revises: a1e8ad938340
Create Date: 2023-03-30 14:49:47.964758

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6e672dcd46a5'
down_revision = 'a1e8ad938340'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('fk__participant__recipient_id__participant', 'participant', type_='foreignkey')
    op.drop_column('participant', 'recipient_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('participant', sa.Column('recipient_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('fk__participant__recipient_id__participant', 'participant', 'participant', ['recipient_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###