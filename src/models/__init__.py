#src/models/__init__.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///vouchbot.db')
Session = sessionmaker(bind=engine)

Base = declarative_base() # Declare Base for all models to inherit from

# All models imported back into init for Base to find
from .Vouches import Vouches
from .User import User

# Base can now find all classes inherited from it
Base.metadata.create_all(engine)
