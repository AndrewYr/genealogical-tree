import typing as T
from genealogical_tree.app.config import config
from sqlalchemy.ext.associationproxy import association_proxy
import sqlalchemy as sa
import sqlalchemy.orm
from gino import Gino
from sqlalchemy import Table

db = Gino()


class PersonModel(db.Model):
    __tablename__ = 'person'
    __table_args__ = {'schema': config.DB_SCHEMA}

    id = sa.Column('id', sa.BigInteger, autoincrement=True, primary_key=True)
    family_id = sa.Column('family_id', sa.BigInteger, primary_key=False)
    parent_id = sa.Column('parent_id', sa.BigInteger, primary_key=False)
    name = sa.Column('name', sa.String(255), nullable=False)
    # surname = sa.Column('surname', sa.String(255), nullable=True)
    # patronymic = sa.Column('patronymic', sa.String(255), nullable=True)
    # birthday = sa.Column('birthday', sa.DateTime(), nullable=True)


PersonModel: Table = PersonModel.__table__