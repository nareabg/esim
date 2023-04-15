import pandas as pd
from sqlalchemy import create_engine
from tables import Location, Customer, Facts
from sqlalchemy.orm import sessionmaker
from modeling import Model
from tables import CustomerFact
import pandas as pd

def read_csv(filename):
    df = pd.read_csv(filename)
    return df

def insert_location(filename):
    # Read the input CSV file into a DataFrame
    df = read_csv(filename)

    # Connect to the database
    engine = create_engine('postgresql://postgres:mysecretpassword@localhost:5432/postgres')

    # Insert the data into the Location table
    df[['location_id', 'location_name']].drop_duplicates().apply(
        lambda x: Location(location_id=x['location_id'], location_name=x['location_name']), axis=1
    ).to_sql('Location', engine, schema='initial', if_exists='append', index=False)

def insert_customer(filename):
    # Read the input CSV file into a DataFrame
    df = read_csv(filename)

    # Connect to the database
    engine = create_engine('postgresql://postgres:mysecretpassword@localhost:5432/postgres')

    # Insert the data into the Customer table
    df[['customer_id', 'gender']].drop_duplicates().apply(
        lambda x: Customer(customer_id=x['customer_id'], gender=x['gender']), axis=1
    ).to_sql('Customer', engine, schema='initial', if_exists='append', index=False)

def insert_facts(filename):
    # Read the input CSV file into a DataFrame
    df = read_csv(filename)

    # Connect to the database
    engine = create_engine('postgresql://postgres:mysecretpassword@localhost:5432/postgres')

    # Insert the data into the Facts table
    df[['customer_id','location_id', 'date', 'quantity', 'total_price']].drop_duplicates().apply(
        lambda x: Facts(customer_id=x['customer_id'], location_id=x['location_id'], date=x['date'], quantity=x['quantity'], total_price=x['total_price']), axis=1
    ).to_sql('Facts', engine, schema='initial', if_exists='append', index=False)
    
    


engine = create_engine('postgresql://postgres:mysecretpassword@localhost:5432/postgres')
Session = sessionmaker(bind=engine)
session = Session()

def insert_customer_fact():
    # Call the count_coding function
    model = Model('postgresql://postgres:mysecretpassword@localhost:5432/postgres')
    df = model.count_coding()

    # Insert the output data into the CustomerFact table
    df.apply(
        lambda x: session.add(CustomerFact(
            customer_id=x['customer_id'], 
            date=x['date'].timestamp(), 
            invoice_id=x['invoice_id'], 
            quantity=x['quantity'], 
            price=x['price'], 
            CLV=x['CLV']
        )),
        axis=1
    )
    session.commit()
