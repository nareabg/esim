import sys
import os
from sqlalchemy_utils import database_exists, create_database
from .tables import Facts
from sqlalchemy import create_engine
from .config import db_uri

Facts = Facts()
metadata, engine = Facts.connect_to_db(db_uri)

class db():
 
    def main(self):
        print("Initializing the database..", end=" ")
        
        if not database_exists(engine.url):
            create_database(engine.url)
        metadata.create_all(bind=engine)
    
        print("done")
            
if __name__ == "__main__":
    mydb = db()
    mydb.main()

