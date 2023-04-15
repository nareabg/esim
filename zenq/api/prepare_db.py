from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from tables import metadata


username = "postgres"
password = "mysecretpassword"
hostname = "localhost"  # This is the database's service name which is 'database'.
port = "5432"  # Note that this is the port inside the 'database' container.
db_name = "postgres"
DB_URL = f"postgresql://{username}:{password}@{hostname}:{port}/{db_name}"


def main():
    print("Initializing the database..", end=" ")
    
    engine = create_engine(DB_URL)
    if not database_exists(engine.url):
        create_database(engine.url)
        
    # Create the defined tables.
    metadata.create_all(bind=engine)
    
    print("done")
    
    
if _name_ == "_main_":
    main()