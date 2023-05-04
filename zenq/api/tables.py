import sqlalchemy
import logging
import os
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime, exc, Sequence, UniqueConstraint , text
from sqlalchemy_utils import database_exists, create_database, drop_database
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from sqlalchemy.schema import CreateSchema

# Importing custom logger from local packages
from zenq.logger import CustomFormatter, bcolors

# Basic logging configuration and initialization
logging.basicConfig(level=logging.DEBUG, format = "/%(asctime)s / %(name)s / %(levelname)s / %(message)s /%(filename)s/%(lineno)d/")
logger = logging.getLogger(os.path.basename(__file__))
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(CustomFormatter())
file_handler = logging.FileHandler('zenq/api/logs.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(CustomFormatter())

logger.addHandler(file_handler)
logger.addHandler(ch)

# Create a base class for SQLAlchemy's ORM to inherit from
Base = declarative_base()

class Facts(Base):
    def connect_to_db(self, db_uri):
        logger.info(f"{self.connect_to_db.__name__}/Connecting to the database.") 
        # Create a database engine
        engine = create_engine(db_uri)
        # Create a session factory for the engine
        Session = sessionmaker(bind=engine)
        # Get the metadata object associated with the database tables
        metadata = Base.metadata
        with engine.connect() as conn:
            try:
                # Create a schema named 'initial' if it doesn't exist yet
                conn.execute(CreateSchema('initial', if_not_exists=True))
            except exc.SQLAlchemyError:
                logger.error(f"{self.connect_to_db.__name__}/Failed to create schema 'initial'")
                pass
        with engine.connect() as conn:
            try: 
                # Create a schema named 'result' if it doesn't exist yet
                conn.execute(CreateSchema('result',  if_not_exists=True))
            except exc.SQLAlchemyError:
                logger.error(f"{self.connect_to_db.__name__}/Failed to create schema 'result'")
                pass       
        # Return the metadata and engine objects for further use    
        return metadata, engine
    
    # Define the Facts table
    __tablename__ = 'Facts'
    __table_args__ = {'schema': 'initial'}

    id = Column(Integer, primary_key=True)
    customer_id = Column(String(50), nullable=False)
    gender = Column(String(10))
    invoice_id = Column(String(50),unique= True, nullable=False)
    date = Column(DateTime, nullable=False)
    quantity = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)   
     
     # Define a property for unit price, which is calculated by dividing total price by quantity
    @property
    def unit_price(self):
        return self.total_price / self.quantity
    
    # Define the LOGS table
    class LOGS(Base):
        __tablename__ = 'LOGS'
        __table_args__ = {'schema': 'initial'}
        id = Column(Integer, primary_key=True)
        level = Column(String(10), nullable=False)
        file_name = Column(String(200), nullable=False)
        func_name = Column(String(200), nullable=False)
        message = Column(String(2000), nullable=False)
        line_number = Column(Integer, nullable=False)
        load_time = Column(DateTime, nullable=False)     
    
    # Define the CLTV table          
    class CLTV(Base):
        __tablename__ = 'CLTV'
        __table_args__ = {'schema': 'result'}
        id = Column(Integer, primary_key=True)
        customer_id = Column(String(50), nullable=False)
        min_date = Column(DateTime, nullable=False)
        recency = Column(Integer, nullable=False)
        T = Column(Integer, nullable=False)
        frequency = Column(Integer, nullable=False)
        monetary = Column(Float, nullable=False)

    # Define the CustomerAlive table
    class CustomerAlive(Base):
        __tablename__ = 'CustomerAlive'
        __table_args__ = {'schema': 'result'}
        id = Column(Integer, primary_key=True)
        Customer = Column(String(50), nullable=False)
        Probability_of_being_Alive = Column(Float, nullable=False)

    # Define the Prediction table
    class Prediction(Base):
        __tablename__ = 'Prediction'
        __table_args__ = {'schema': 'result'}
        id = Column(Integer, primary_key=True)
        Customer = Column(String(50), nullable=False)
        Expected_Purchases_30 = Column(Float, nullable=False)
        Expected_Purchases_90 = Column(Float, nullable=False)
        Expected_Purchases_180 = Column(Float, nullable=False)
        Expected_Purchases_360 = Column(Float, nullable=False)
    
    # Define the RFMScore table    
    class RFMScore(Base):
        __tablename__ = 'RFMScore'
        __table_args__ = {'schema': 'result'}
        id = Column(Integer, primary_key=True)
        customer_id = Column(String(50), nullable=False)
        recency_score = Column(Integer, nullable=False)
        frequency_score = Column(Integer, nullable=False)
        monetary_score=Column(Integer, nullable=False)
        RFM_SCORE = Column(Integer, nullable=False)
        segment = Column(String(50), nullable=False)
    
    # Define the ParetoParameters table    
    class ParetoParameters(Base):     
        __tablename__ = 'ParetoParameters'
        __table_args__ = {'schema': 'result'}        
        id = Column(Integer, primary_key=True)
        r = Column(Float, nullable=False)
        alpha = Column(Float, nullable=False)
        s = Column(Float, nullable=False)
        beta = Column(Float, nullable=False)
       
