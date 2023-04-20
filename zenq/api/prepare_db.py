from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import declarative_base

# import sys
# sys.path.append("..")
from .tables import metadata


for t in metadata.sorted_tables:
    print(t.name)
    
print("-"*50)

# Base = declarative_base()
# metadata = Base.metadata

username = "postgres"
password = "mysecretpassword"
hostname = "localhost"  # This is the database's service name which is 'database'.
port = "5432"  # Note that this is the port inside the 'database' container.
db_name = "globbing"
DB_URL = f"postgresql://{username}:{password}@{hostname}:{port}/{db_name}"

class db():
    def main(self):
        print("Initializing the database..", end=" ")
    
        engine = create_engine(DB_URL)
        if not database_exists(engine.url):
            create_database(engine.url)
        
        # Create the defined tables.
        metadata.create_all(bind=engine)
    
        print("done")
    
    
if __name__ == "_main_":
    main()
    
 # go to extension press plus and enter info   