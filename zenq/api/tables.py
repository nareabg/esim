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



engine = create_engine('postgresql://aua:mysecretpassword@localhost:5432/GLOBBING')
Session = sessionmaker(bind=engine)
Base = declarative_base()
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


class Customer(Base):
        __tablename__ = 'Customer'
        __table_args__ = {'schema': 'initial'}

        id = Column(Integer, primary_key=True)
        customer_id = Column(String(50), unique=True, nullable=False)
        gender = Column(String(10))


class Facts(Base):
        __tablename__ = 'Facts'
        __table_args__ = {'schema': 'initial'}

        id = Column(Integer, primary_key=True)
        customer_id_uniq = Column(Integer, ForeignKey('initial.Customer.id'), nullable=False)
        location_id = Column(String(50), nullable=False)
        location_name = Column(String(50), nullable=False)
        invoice_id = Column(String(50),unique= True, nullable=False)
        date = Column(DateTime, nullable=False)
        quantity = Column(Float, nullable=False)
        total_price = Column(Float, nullable=False)
        
        @property
        def unit_price(self):
            return self.total_price / self.quantity

        customer = relationship("Customer", backref="Facts")
        # def __repr__(self):
        #     return f"<Facts(id={self.id}, customer_id='{self.customer_id}', location_id='{self.location_id}', date='{self.date}', quantity={self.quantity}, total_price={self.total_price}, gender='{self.gender}', unit_price={self.unit_price})>"


class CustomerFact(Base):
        __tablename__ = 'CustomerFact'
        __table_args__ = {'schema': 'result'}

        id = Column(Integer, primary_key=True)
        customer_id = Column(String(50), unique=True, nullable=False)
        date = Column(Integer, nullable=False)
        invoice_id = Column(Integer, nullable=False)
        quantity = Column(Float, nullable=False)
        price = Column(Float, nullable=False)
        CLV = Column(Float, nullable=False)
        

        # def _repr_(self):
        #     return f"<CustomerFact(id={self.id}, customer_id='{self.customer_id}', date='{self.date}', invocie_id='{self.invoice_id}', quantity='{self.quantity}', price='{self.price}', CLV='{self.CLV}')>"



class Prediction(Base):
        __tablename__  = 'Prediction'
        __table_args__ = {'schema': 'result'}

        id = Column(Integer, primary_key=True)
        customer_id = Column(String(50), unique=True, nullable=False)
        recency = Column(Float, nullable=False)
        frequency = Column(Integer, nullable=False)
        monetary = Column(Float, nullable=False)
        T = Column(Float, nullable=False)
        pred_1month = Column(Float, nullable=False)


        # def _repr_(self):
        #     return f"<CustomerFact(id={self.id}, customer_id='{self.customer_id}', recency='{self.recency}', frequency='{self.frequency}', monetary='{self.monetary}', T='{self.T}', pred_1month='{self.pred_1month}')>"

for t in metadata.sorted_tables:
    print(t.name)
        
print("-"*50)