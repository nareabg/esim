import sys
import os
from sqlalchemy_utils import database_exists, create_database
from .tables import Facts
from sqlalchemy import create_engine
from .config import db_uri
import os
from abc import ABC, abstractmethod
from zenq.logger import CustomFormatter, bcolors
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(funcName)s %(msg)s')
logger = logging.getLogger(os.path.basename(__file__))
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(CustomFormatter())
file_handler = logging.FileHandler('logs.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(CustomFormatter())

logger.addHandler(file_handler)
logger.addHandler(ch)

Facts = Facts()
metadata, engine = Facts.connect_to_db(db_uri)

class db():
 
    def main(self):
        print("Initializing the database..", end=" ")
        
        if not database_exists(engine.url):
            create_database(engine.url)
        metadata.drop_all(bind=engine)
        metadata.create_all(bind=engine)
        
        logger.info(f"{db.__name__}")           

        print("done")

if __name__ == "__main__":
    mydb = db()
    mydb.main()

