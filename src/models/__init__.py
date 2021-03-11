#src/models/__init__.py
from sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .User import *
