from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from collections.abc import Iterable
from sqlalchemy_utils import database_exists

import os

currend_dir = os.path.dirname(__file__)
db_path = r'sqlite:///{}/lstore.db'.format(currend_dir)
engine = create_engine(db_path, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    if database_exists(db_path):
        return False
    else:
        Base.metadata.create_all(engine)
        return True