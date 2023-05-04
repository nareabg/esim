import sys
import os
import logging

# Importing sqlalchemy libraries to work with database
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

# Importing custom logger and table from local packages
from zenq.logger import CustomFormatter, bcolors
from .tables import Facts
from .config import db_uri

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

# Creating an instance of the Facts class and connecting to the database using SQLAlchemy
Facts = Facts()
metadata, engine = Facts.connect_to_db(db_uri)

class db():
    """ 
        class provides methods for creating and managing a database 
    """
 
    def main(self):
        """
            initializing the database, dropping and creating tables using metadata
        """
        logger.info(f"{db.__name__}/Initializing the database...")
        
        try:
            # Checking if the database already exists and creating a new one if it doesn't
            if not database_exists(engine.url):
                create_database(engine.url)
            # Dropping and creating tables using metadata    
            metadata.drop_all(bind=engine)
            metadata.create_all(bind=engine)
            logger.info(f"{db.__name__}/Database successfully initialized")
        except Exception as e:
            logger.error(f"{db.__name__}/Error occurred while initializing the database: {e}")
            logger.debug(traceback.format_exc())        
        logger.info(f"{db.__name__}/Insertion successfully done") 

if __name__ == "__main__":
    # Creating an instance of the db class and running its main method
    mydb = db()
    mydb.main()
     