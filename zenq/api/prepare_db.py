 
# sys.path.append("..")
# from tables import Facts
# # for t in metadata.sorted_tables:
# #     print(t.name)
    
# # print("-"*50)
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import declarative_base
import sys
sys.path.append("..")
from tables import Facts

print("-"*50)
print("Enter your database credentials")
username = input("Username: ")
password = input("Password: ")
db_name = input("Database name: ")

db_uri = f"postgresql://{username}:{password}@localhost/{db_name}"

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
