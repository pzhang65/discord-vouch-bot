#src/models/__init__.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///vouches.db')
Session = sessionmaker(bind=engine)
