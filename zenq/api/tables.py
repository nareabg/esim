from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database, drop_database
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://postgres:mysecretpassword@localhost:5432/postgres')
Session = sessionmaker(bind=engine)
Base = declarative_base()
metadata = Base.metadata

# Create the initial schema
with engine.connect() as conn:
    conn.execute('CREATE SCHEMA IF NOT EXISTS initial')

# Create the result schema
with engine.connect() as conn:
    conn.execute('CREATE SCHEMA IF NOT EXISTS result')

class Location(Base):
    _tablename_ = 'Location'
    _table_args_ = {'schema': 'initial'}

    id = Column(Integer, primary_key=True)
    location_id = Column(String(50), unique=True, nullable=False)
    location_name = Column(String(50), unique=True, nullable=False)

    def _repr_(self):
        return f"<Location(id={self.id}, location_id='{self.location_id}', location_name='{self.location_name}')>"


class Customer(Base):
    _tablename_ = 'Customer'
    _table_args_ = {'schema': 'initial'}

    id = Column(Integer, primary_key=True)
    customer_id = Column(String(50), unique=True, nullable=False)
    gender = Column(String(10))

    def _repr_(self):
        return f"<Customer(id={self.id}, customer_id='{self.customer_id}', gender='{self.gender}')>"


class Facts(Base):
    _tablename_ = 'Facts'
    _table_args_ = {'schema': 'initial'}

    id = Column(Integer, primary_key=True)
    customer_id = Column(String(50), ForeignKey('initial.Customer.customer_id'), nullable=False)
    location_id = Column(String(50), ForeignKey('initial.Location.location_id'), nullable=False)
    date = Column(DateTime, nullable=False)
    quantity = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)
    gender = Column(String(10))
    unit_price = Column(Float, nullable=False, computed="total_price / quantity")

    def _repr_(self):
        return f"<Facts(id={self.id}, customer_id='{self.customer_id}', location_id='{self.location_id}', date='{self.date}', quantity={self.quantity}, total_price={self.total_price}, gender='{self.gender}', unit_price={self.unit_price})>"

