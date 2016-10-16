import os

from sqlalchemy import *

metadata = MetaData()
for i in range(os.environ.get('NUMBER_OF_TABLES', 50)):
    Table('sample_table_{}'.format(i), metadata,
          Column('id', Integer, primary_key=True),
          Column('a1', String(100)),
          Column('a2', String(100)),
          Column('a3', String(100)),
          Column('a4', String(100)),
          Column('a5', String(100)),
          Column('a6', String(100)),
          Column('a7', String(100)),
          Column('a8', String(100)),
          Column('a9', String(100)),
          Column('date', DateTime()))
