#from zenq.utils import connect
# from zenq.utils import test

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
from zenq.api.config import db_uri
from sqlalchemy import func, create_engine      
from zenq.api.tables import Base, Facts
from sqlalchemy.orm import load_only, relationship, joinedload, sessionmaker
import matplotlib.pyplot as plt

 

class Visuals():

    def __init__(
        self
    ):
        self.params_ = {}
        self.engine = create_engine(db_uri)
        Base.metadata.create_all(self.engine)
        self.session = sessionmaker(bind=self.engine)()
        
 
    def total_sales_by_location(self):
        result = self.session.query(Facts.location_name, sqlalchemy.func.sum(Facts.total_price)).\
                    group_by(Facts.location_name).all()
        x = [i[0] for i in result]
        y = [i[1] for i in result]
        plt.bar(x, y)
        plt.xlabel("Location Name")
        plt.ylabel("Total Sales")
        plt.show()

        
    