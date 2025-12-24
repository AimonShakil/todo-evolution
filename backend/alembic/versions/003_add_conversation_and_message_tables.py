"""Add conversation and message tables

Revision ID: 003
Revises: 002
Create Date: 2025-12-22 16:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '003'
down_revision: Union[str, None] = '002'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create conversation and message tables for Phase III."""

    # Create conversation table
    op.create_table(
        'conversation',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE')
    )

    # Create indexes for conversation
    op.create_index('ix_conversation_user_id', 'conversation', ['user_id'])
    op.create_index('ix_conversation_user_id_is_active', 'conversation', ['user_id', 'is_active'])
    op.create_index('ix_conversation_created_at', 'conversation', ['created_at'])

    # Create message table
    op.create_table(
        'message',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('conversation_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('role', sa.String(length=20), nullable=False),
        sa.Column('content', sa.String(length=4000), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversation.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
        sa.CheckConstraint("role IN ('user', 'assistant', 'tool')", name='check_message_role')
    )

    # Create indexes for message
    op.create_index('ix_message_conversation_id', 'message', ['conversation_id'])
    op.create_index('ix_message_user_id', 'message', ['user_id'])
    op.create_index('ix_message_conversation_id_created_at', 'message', ['conversation_id', 'created_at'])


def downgrade() -> None:
    """Drop conversation and message tables."""

    # Drop message table first (foreign key dependency)
    op.drop_index('ix_message_conversation_id_created_at', table_name='message')
    op.drop_index('ix_message_user_id', table_name='message')
    op.drop_index('ix_message_conversation_id', table_name='message')
    op.drop_table('message')

    # Drop conversation table
    op.drop_index('ix_conversation_created_at', table_name='conversation')
    op.drop_index('ix_conversation_user_id_is_active', table_name='conversation')
    op.drop_index('ix_conversation_user_id', table_name='conversation')
    op.drop_table('conversation')
