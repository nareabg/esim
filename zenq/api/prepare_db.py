from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import declarative_base
import sys
sys.path.append("..")
from .tables import metadata

for t in metadata.sorted_tables:
    print(t.name)
    
print("-"*50)

# username = "aua"
# password = "mysecretpassword"
# hostname = "localhost"  
# port = "5432"  
# db_name = "GLOBBING"
# DB_URL = f"postgresql://{username}:{password}@{hostname}:{port}/{db_name}"

# db_uri = 'postgresql://aua:mysecretpassword@localhost:5432/GLOBBING'
# engine = create_engine(db_uri)
# Session = sessionmaker(bind=engine)
# Base = declarative_base()
# metadata = Base.metadata
class db():
    def connect_to_db(self, username, password, db_name, hostname = 'localhost', port = 5432):
        # username = "aua"
        # password = "mysecretpassword"
        # hostname = "localhost"  
        # port = "5432"  
        # db_name = "GLOBBING"
        db_uri = f"postgresql://{username}:{password}@{hostname}:{port}/{db_name}"

        
    def main(self):
        print("Initializing the database..", end=" ")
    
        engine = create_engine(db_uri)
        if not database_exists(engine.url):
            create_database(engine.url)
        metadata.create_all(bind=engine)
    
        print("done")
    
if __name__ == "__main__":
    mydb = db()
    mydb.main()
