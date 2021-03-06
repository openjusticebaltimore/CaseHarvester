"""adding tables for DSCIVIL cases

Revision ID: 284bc3e20590
Revises: c3420fc7aeaf
Create Date: 2018-05-07 20:16:34.333270

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '284bc3e20590'
down_revision = 'c3420fc7aeaf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('DSCIVIL',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('case_number', sa.String(), nullable=True),
    sa.Column('court_system', sa.String(), nullable=True),
    sa.Column('claim_type', sa.String(), nullable=True),
    sa.Column('district_code', sa.Integer(), nullable=True),
    sa.Column('location_code', sa.Integer(), nullable=True),
    sa.Column('filing_date', sa.Date(), nullable=True),
    sa.Column('filing_date_str', sa.String(), nullable=True),
    sa.Column('case_status', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['case_number'], ['cases.case_number'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('complaints',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('case_number', sa.String(), nullable=True),
    sa.Column('complaint_number', sa.Integer(), nullable=True),
    sa.Column('plaintiff', sa.String(), nullable=True),
    sa.Column('defendant', sa.String(), nullable=True),
    sa.Column('complaint_type', sa.String(), nullable=True),
    sa.Column('complaint_status', sa.String(), nullable=True),
    sa.Column('status_date', sa.Date(), nullable=True),
    sa.Column('status_date_str', sa.String(), nullable=True),
    sa.Column('filing_date', sa.Date(), nullable=True),
    sa.Column('filing_date_str', sa.String(), nullable=True),
    sa.Column('amount', sa.Numeric(), nullable=True),
    sa.Column('last_activity_date', sa.Date(), nullable=True),
    sa.Column('last_activity_date_str', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['case_number'], ['cases.case_number'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('dscivil_case_history',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('case_number', sa.String(), nullable=True),
    sa.Column('event_type', sa.String(), nullable=True),
    sa.Column('complaint_number', sa.Integer(), nullable=True),
    sa.Column('date', sa.Date(), nullable=True),
    sa.Column('date_str', sa.String(), nullable=True),
    sa.Column('comment', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['case_number'], ['cases.case_number'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('dscivil_related_person',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('case_number', sa.String(), nullable=True),
    sa.Column('complaint_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('connection_to_complaint', sa.String(), nullable=True),
    sa.Column('address_1', sa.String(), nullable=True),
    sa.Column('address_2', sa.String(), nullable=True),
    sa.Column('city', sa.String(), nullable=True),
    sa.Column('state', sa.String(), nullable=True),
    sa.Column('zip_code', sa.String(), nullable=True),
    sa.Column('attorney_code', sa.Integer(), nullable=True),
    sa.Column('attorney_firm', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['case_number'], ['cases.case_number'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['complaint_id'], ['complaints.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('judgments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('case_number', sa.String(), nullable=True),
    sa.Column('complaint_id', sa.Integer(), nullable=True),
    sa.Column('judgment_type', sa.String(), nullable=True),
    sa.Column('judgment_date', sa.Date(), nullable=True),
    sa.Column('judgment_date_str', sa.String(), nullable=True),
    sa.Column('judgment_amount', sa.Numeric(), nullable=True),
    sa.Column('judgment_interest', sa.Numeric(), nullable=True),
    sa.Column('costs', sa.Numeric(), nullable=True),
    sa.Column('other_amounts', sa.Numeric(), nullable=True),
    sa.Column('attorney_fees', sa.Numeric(), nullable=True),
    sa.Column('post_interest_legal_rate', sa.Boolean(), nullable=True),
    sa.Column('post_interest_contractual_rate', sa.Boolean(), nullable=True),
    sa.Column('jointly_and_severally', sa.Integer(), nullable=True),
    sa.Column('in_favor_of_defendant', sa.Boolean(), nullable=True),
    sa.Column('possession_value', sa.Numeric(), nullable=True),
    sa.Column('possession_damages_value', sa.Numeric(), nullable=True),
    sa.Column('value_sued_for', sa.Numeric(), nullable=True),
    sa.Column('damages', sa.Numeric(), nullable=True),
    sa.Column('dismissed_with_prejudice', sa.Boolean(), nullable=True),
    sa.Column('replevin_detinue', sa.Numeric(), nullable=True),
    sa.Column('recorded_lien_date_str', sa.String(), nullable=True),
    sa.Column('recorded_lien_date', sa.Date(), nullable=True),
    sa.Column('judgment_renewed_date_str', sa.String(), nullable=True),
    sa.Column('renewed_lien_date', sa.Date(), nullable=True),
    sa.Column('renewed_lien_date_str', sa.String(), nullable=True),
    sa.Column('satisfaction_date', sa.Date(), nullable=True),
    sa.Column('satisfaction_date_str', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['case_number'], ['cases.case_number'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['complaint_id'], ['complaints.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('judgments')
    op.drop_table('dscivil_related_person')
    op.drop_table('dscivil_case_history')
    op.drop_table('complaints')
    op.drop_table('DSCIVIL')
    # ### end Alembic commands ###
