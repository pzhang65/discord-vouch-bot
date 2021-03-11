#src/models/__init__.py
from sqlalchemy import create_engine

engine = create_engine('sqlite:///:memory:', echo=True)
db = declarative_base()

from .User import *
