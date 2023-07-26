from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database, drop_database
import os
from dotenv import load_dotenv

from models.models import Base


load_dotenv()

class DBSession:
    def __init__(self) -> None:
        self.session = None

    def __get_engine(self):
        user = os.environ.get('user')
        psw = os.environ.get('psw')
        host = os.environ.get('host')
        port = os.environ.get('port')
        db = os.environ.get('db')
        
        url = f"postgresql://{user}:{psw}@{host}:{port}/{db}"
        
        
        if not database_exists(url):
            create_database(url)
            
        engine = create_engine(url, echo=False)
        
        Base.metadata.create_all(bind=engine)
        return engine

    def get_session(self):
        if self.session == None:
            engine = self.__get_engine()
            session = sessionmaker(bind=engine)
            self.session = session
        
        return self.session

dbController = DBSession()


