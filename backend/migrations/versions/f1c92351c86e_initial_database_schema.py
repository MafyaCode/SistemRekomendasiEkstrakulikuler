"""Initial database schema

Revision ID: f1c92351c86e
Revises: 
Create Date: 2025-04-03 16:12:48.641684

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f1c92351c86e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ekskul',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nama_ekskul', sa.String(length=100), nullable=False),
    sa.Column('deskripsi_ekskul', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('nama_ekskul')
    )
    op.create_table('minat',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nama_minat', sa.String(length=100), nullable=False),
    sa.Column('deskripsi_minat', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('nama_minat')
    )
    op.create_table('siswa',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nama', sa.String(length=100), nullable=False),
    sa.Column('kelas', sa.String(length=20), nullable=True),
    sa.Column('timestamp_input', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('siswa', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_siswa_nama'), ['nama'], unique=False)

    op.create_table('ekskul_minat',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ekskul_id', sa.Integer(), nullable=False),
    sa.Column('minat_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['ekskul_id'], ['ekskul.id'], ),
    sa.ForeignKeyConstraint(['minat_id'], ['minat.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('minat_siswa',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('skor', sa.Integer(), nullable=False),
    sa.Column('siswa_id', sa.Integer(), nullable=False),
    sa.Column('minat_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['minat_id'], ['minat.id'], ),
    sa.ForeignKeyConstraint(['siswa_id'], ['siswa.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('minat_siswa')
    op.drop_table('ekskul_minat')
    with op.batch_alter_table('siswa', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_siswa_nama'))

    op.drop_table('siswa')
    op.drop_table('minat')
    op.drop_table('ekskul')
    # ### end Alembic commands ###
