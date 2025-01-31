"""init

Revision ID: c6eb9093ca95
Revises: 
Create Date: 2025-01-29 17:57:19.994707

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'c6eb9093ca95'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('pattern',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('description', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('stepform',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('formfield',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('step_form_id', sa.Integer(), nullable=True),
    sa.Column('label', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('description', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('is_required', sa.Boolean(), nullable=False),
    sa.Column('entry_type', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('entry_props', sa.JSON(), nullable=True),
    sa.ForeignKeyConstraint(['step_form_id'], ['stepform.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('instance',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('pattern_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['pattern_id'], ['pattern.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('patternstep',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('pattern_id', sa.Integer(), nullable=True),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('description', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('category', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('status', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('form_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['form_id'], ['stepform.id'], ),
    sa.ForeignKeyConstraint(['pattern_id'], ['pattern.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('stepedge',
    sa.Column('prev_id', sa.Integer(), nullable=False),
    sa.Column('next_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['next_id'], ['patternstep.id'], ),
    sa.ForeignKeyConstraint(['prev_id'], ['patternstep.id'], ),
    sa.PrimaryKeyConstraint('prev_id', 'next_id')
    )
    op.create_table('stepinstance',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('instance_id', sa.Integer(), nullable=True),
    sa.Column('pattern_step_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['instance_id'], ['instance.id'], ),
    sa.ForeignKeyConstraint(['pattern_step_id'], ['patternstep.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('stepinstance')
    op.drop_table('stepedge')
    op.drop_table('patternstep')
    op.drop_table('instance')
    op.drop_table('formfield')
    op.drop_table('stepform')
    op.drop_table('pattern')
    # ### end Alembic commands ###
