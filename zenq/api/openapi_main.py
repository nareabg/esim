# import connexion
# from config import db_uri

# print("DB URI:", db_uri)

# app = connexion.App(__name__, specification_dir="./")
# app.add_api("swagger.yml")


# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=8081, debug=True)


import pandas as pd
import connexion
from sqlalchemy.exc import IntegrityError
from tables import Facts
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from config import db_uri


engine = create_engine(db_uri)
Session = sessionmaker(bind=engine)
session = Session()
def insert_facts(filename, customer_id, gender, invoice_id, date, quantity, total_price):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(filename)
    print(f"Inserting facts for customer {customer_id} from file {filename}")

    # Loop through the rows of the DataFrame and insert each one into the database
    for i, row in df.iterrows():
        fact = Facts(
            customer_id=row[customer_id],
            gender=row[gender],
            invoice_id=row[invoice_id],
            date=row[date],
            quantity=row[quantity],
            total_price=row[total_price]
        )
        try:
            session.add(fact)
            session.commit()
        except IntegrityError:
            session.rollback()
            print(f"Skipping row with duplicate invoice_id: {row[invoice_id]}")
            continue
    print("Finished inserting facts")
    # Close the session
    session.close()

app = connexion.FlaskApp(__name__)
app.add_api('swagger.yml')

if __name__ == '__main__':
    app.run(port=8081)
