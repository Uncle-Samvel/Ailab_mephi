from abc import ABC, abstractmethod
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DataBaseClient(ABC):
    def __init__(self, user, password, host, port, database):
        self.DATABASE_URL = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'
        self.engine = create_engine(self.DATABASE_URL)
        self.Session = sessionmaker(bind=self.engine)

    @abstractmethod
    def create_tables(self):
        pass

    @abstractmethod
    def update_tables(self):
        pass
