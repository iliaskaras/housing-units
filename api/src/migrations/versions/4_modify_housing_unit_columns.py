"""empty message

Revision ID: 4_modify_housing_unit_columns
Revises: 3_add_housing_units_table
Create Date: 2021-12-04 01:09:04.150876

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '4_modify_housing_unit_columns'
down_revision = '3_add_housing_units_table'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('housingunits', 'project_name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('housingunits', 'project_start_date',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('housingunits', 'community_board',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('housingunits', 'reporting_construction_type',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('housingunits', 'extended_affordability_status',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('housingunits', 'prevailing_wage_status',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('housingunits', 'extremely_low_income_units',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('housingunits', 'very_low_income_units',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('housingunits', 'low_income_units',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('housingunits', 'moderate_income_units',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('housingunits', 'middle_income_units',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('housingunits', 'other_income_units',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('housingunits', 'studio_units',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('housingunits', '_1_br_units',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('housingunits', '_2_br_units',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('housingunits', '_3_br_units',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('housingunits', '_4_br_units',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('housingunits', '_5_br_units',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('housingunits', '_6_br_units',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('housingunits', 'unknown_br_units',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('housingunits', 'counted_rental_units',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('housingunits', 'counted_homeownership_units',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('housingunits', 'all_counted_units',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('housingunits', 'total_units',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('housingunits', 'total_units',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('housingunits', 'all_counted_units',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('housingunits', 'counted_homeownership_units',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('housingunits', 'counted_rental_units',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('housingunits', 'unknown_br_units',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('housingunits', '_6_br_units',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('housingunits', '_5_br_units',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('housingunits', '_4_br_units',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('housingunits', '_3_br_units',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('housingunits', '_2_br_units',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('housingunits', '_1_br_units',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('housingunits', 'studio_units',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('housingunits', 'other_income_units',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('housingunits', 'middle_income_units',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('housingunits', 'moderate_income_units',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('housingunits', 'low_income_units',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('housingunits', 'very_low_income_units',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('housingunits', 'extremely_low_income_units',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('housingunits', 'prevailing_wage_status',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('housingunits', 'extended_affordability_status',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('housingunits', 'reporting_construction_type',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('housingunits', 'community_board',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('housingunits', 'project_start_date',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('housingunits', 'project_name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###
