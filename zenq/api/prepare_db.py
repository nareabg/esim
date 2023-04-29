
# from sqlalchemy import create_engine
# from sqlalchemy_utils import database_exists, create_database
# from sqlalchemy.orm import declarative_base
# import sys
# import os
# sys.path.append("..")
# from tables import Facts

# print("Enter your database credentials")
# username = input("Username: ")
# password = input("Password: ")
# db_name = input("Database name: ")

# db_uri = f"postgresql://{username}:{password}@localhost/{db_name}"

# Facts = Facts()
# metadata, engine = Facts.connect_to_db(db_uri)

# class db():
 
#     def main(self):
#         print("Initializing the database..", end=" ")
        
#         if not database_exists(engine.url):
#             create_database(engine.url)
#         metadata.create_all(bind=engine)
    
#         print("done")

#         current_dir = os.getcwd()

#         # Change the current working directory to the module directory
#         module_dir = os.path.dirname(os.path.abspath(__file__))
#         os.chdir(module_dir)

#         # Save db_uri to config.py file
#         with open('config.py', 'w') as f:
#             f.write(f"db_uri = '{db_uri}'\n")

#         # Change the current working directory back to the original directory
#         os.chdir(current_dir)
            
# if __name__ == "__main__":
#     mydb = db()
#     mydb.main()


import sys
import os
from sqlalchemy_utils import database_exists, create_database
from .tables import Facts
from sqlalchemy import create_engine

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

        current_dir = os.getcwd()

        # Change the current working directory to the module directory
        module_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(module_dir)

        # Save db_uri to config.py file
        with open('config.py', 'w') as f:
            f.write(f"db_uri = '{db_uri}'\n")

        # Change the current working directory back to the original directory
        os.chdir(current_dir)
            
if __name__ == "__main__":
    mydb = db()
    mydb.main()

