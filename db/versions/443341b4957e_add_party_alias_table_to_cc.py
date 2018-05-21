"""add party alias table to CC

Revision ID: 443341b4957e
Revises: bc9d0d8db2e2
Create Date: 2018-05-20 20:45:49.817963

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '443341b4957e'
down_revision = 'bc9d0d8db2e2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cc_party_alias',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('plaintiff_id', sa.Integer(), nullable=True),
    sa.Column('defendant_id', sa.Integer(), nullable=True),
    sa.Column('related_person_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('case_number', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['case_number'], ['cc.case_number'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['defendant_id'], ['cc_defendants.id'], ),
    sa.ForeignKeyConstraint(['plaintiff_id'], ['cc_plaintiffs.id'], ),
    sa.ForeignKeyConstraint(['related_person_id'], ['cc_related_persons.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('cc_party_alias')
    # ### end Alembic commands ###