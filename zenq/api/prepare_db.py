import sys
import os
import logging
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from zenq.logger import CustomFormatter, bcolors
from .tables import Facts
from .config import db_uri

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

Facts = Facts()
metadata, engine = Facts.connect_to_db(db_uri)

class db():
 
    def main(self):
        logger.info(f"{db.__name__}/Initializing the database...")
        
        try:
            if not database_exists(engine.url):
                create_database(engine.url)
            metadata.drop_all(bind=engine)
            metadata.create_all(bind=engine)
            logger.info(f"{db.__name__}/Database successfully initialized")
        except Exception as e:
            logger.error(f"{db.__name__}/Error occurred while initializing the database: {e}")
            logger.debug(traceback.format_exc())        
        logger.info(f"{db.__name__}/Insertion successfully done") 

if __name__ == "__main__":
    mydb = db()
    mydb.main()
     