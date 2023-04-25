import sqlalchemy
from sqlalchemy import exc
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils import database_exists, create_database, drop_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import CreateSchema
from sqlalchemy import Sequence, UniqueConstraint 
from sqlalchemy import text
from sqlalchemy.orm import relationship

Base = declarative_base()

class Facts(Base):
    def connect_to_db(self, db_uri):
        engine = create_engine(db_uri)
        Session = sessionmaker(bind=engine)
        metadata = Base.metadata
        # Create the initial schema
        with engine.connect() as conn:
            try:
                conn.execute(CreateSchema('initial', if_not_exists=True))
            except exc.SQLAlchemyError:
                pass

        # Create the result schema
        with engine.connect() as conn:
            try: 
                conn.execute(CreateSchema('result',  if_not_exists=True))
            except exc.SQLAlchemyError:
                pass

        return metadata, engine

    __tablename__ = 'Facts'
    __table_args__ = {'schema': 'initial'}

    id = Column(Integer, primary_key=True)
    customer_id = Column(String(50), nullable=False)
    gender = Column(String(10))
    location_id = Column(String(50), nullable=False)
    location_name = Column(String(50), nullable=False)
    invoice_id = Column(String(50),unique= True, nullable=False)
    date = Column(DateTime, nullable=False)
    quantity = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)
        
    @property
    def unit_price(self):
        return self.total_price / self.quantity
 