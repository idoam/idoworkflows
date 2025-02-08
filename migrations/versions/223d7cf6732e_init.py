"""init

Revision ID: 223d7cf6732e
Revises: 
Create Date: 2025-02-08 18:22:25.354292

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '223d7cf6732e'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('patternedge', schema=None) as batch_op:
        batch_op.add_column(sa.Column('trigger', sqlmodel.sql.sqltypes.AutoString(), nullable=False))

    with op.batch_alter_table('patternnode', schema=None) as batch_op:
        batch_op.add_column(sa.Column('dataform_pydantic_str', sqlmodel.sql.sqltypes.AutoString(), nullable=False))
        batch_op.drop_column('dataform_template')

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('patternnode', schema=None) as batch_op:
        batch_op.add_column(sa.Column('dataform_template', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True))
        batch_op.drop_column('dataform_pydantic_str')

    with op.batch_alter_table('patternedge', schema=None) as batch_op:
        batch_op.drop_column('trigger')

    # ### end Alembic commands ###
