import sqlalchemy
import pandas as pd
from sqlalchemy import create_engine
from .tables import Location, Customer, Facts, CustomerFact, Prediction
from sqlalchemy.orm import sessionmaker
from zenq.clvmodels.modeling import Model
import pandas as pd
#import logging

class points():
    engine = create_engine('postgresql://postgres:mysecretpassword@localhost:5432/postgres')
    Session = sessionmaker(bind=engine)
    session = Session()
    model = Model('postgresql://postgres:mysecretpassword@localhost:5432/postgres')
    
    def __init__(self):
        self.df = None

    def read_csv(self, filename):
        self.df = pd.read_csv(filename)

 #   def insert_location(self, filename):
#        self.read_csv(filename)
#    print(self.df.columns)  # print column names for debugging
# 
#        # Insert the data into the Location table
#        self.df[['location_id', 'location_name']].drop_duplicates().apply(
#            lambda x: Location(location_id=x['location_id'], location_name=x['location_name']), axis=1
#        ).to_sql('Location', self.engine, schema='initial', if_exists='append', index=False)

    #def insert_location_name(self, filename):
    # Read the input CSV file into a DataFrame
    #    self.df = pd.read_csv(filename)

    # Get the list of available columns from the DataFrame
    #    available_columns = self.df.columns.tolist()

    # Ask the user to choose a column from the available columns
    #    print("Please choose a column from the following list:")
    #    for i, col in enumerate(available_columns):
    #        print(f"{i+1}. {col}")
    #        column_choice = int(input()) - 1

    # Get the chosen column name
    #    column_name = available_columns[column_choice]

    # Insert the data into the Location table
    #    self.df[[column_name]].drop_duplicates().apply(
    #        lambda x: Location(location_name=x[column_name]),
    #     axis=1
    #    ).to_sql('Location', points.engine, schema='initial', if_exists='append', index=False)

     #   print(f"{column_name} data inserted into the Location table's location_name column.")
    def insert_location_name(self, filename):
    # Read the input CSV file into a DataFrame
        self.df = pd.read_csv(filename)

    # Get the list of available columns from the DataFrame
        available_columns = self.df.columns.tolist()

    # Ask the user to choose a column from the available columns
        print("Please choose a column from the following list:")
        for i, col in enumerate(available_columns):
            print(f"{i+1}. {col}")
    
    # Read the input for the column choice and validate it
        column_choice = None
        while column_choice is None:
            choice_input = input()
            if choice_input.isdigit() and int(choice_input) in range(1, len(available_columns)+1):
                column_choice = int(choice_input) - 1
            else:
                print("Invalid input. Please choose a valid column number.")

    # Get the chosen column name
        column_name = available_columns[column_choice]

    # Insert the data into the Location table
        self.df[[column_name]].drop_duplicates().apply(
            lambda x: Location(location_name=x[column_name]),
            axis=1
        ).to_sql('Location', points.engine, schema='initial', if_exists='append', index=False)

        print(f"{column_name} data inserted into the Location table's location_name column.")

    def insert_customer(self, filename):
        self.read_csv(filename)

        # Insert the data into the Customer table
        self.df[['customer_id', 'gender']].drop_duplicates().apply(
        lambda x: Customer(customer_id=x['customer_id'], gender=x['gender']), axis=1
        ).to_sql('Customer', self.engine, schema='initial', if_exists='append', index=False)

    def insert_facts(self, filename):
    # Read the input CSV file into a DataFrame
       self.read_csv(filename)

    # Insert the data into the Facts table
       self.df[['customer_id','location_id', 'date', 'quantity', 'total_price']].drop_duplicates().apply(
       lambda x: Facts(customer_id=x['customer_id'], location_id=x['location_id'], date=x['date'], quantity=x['quantity'], total_price=x['total_price']), axis=1
       ).to_sql('Facts', self.engine, schema='initial', if_exists='append', index=False)
     
    def insert_customer_fact(self):
    # Call the count_coding function
        df = self.model.count_coding()

    # Insert the output data into the CustomerFact table
        df.apply(
           lambda x: self.session.add(CustomerFact(
               customer_id=x['customer_id'], 
               date=x['date'], 
               invoice_id=x['invoice_id'], 
               quantity=x['quantity'], 
               price=x['price'], 
               CLV=x['CLV']
             )),
             axis=1
        )
        self.session.commit()


    def insert_prediction(self):
    # Call the count_coding function
        df = self.model.count_coding()

    # Insert the output data into the CustomerFact table
        df.apply(
            lambda x: self.session.add(Prediction(
                customer_id=x['customer_id'], 
                recency=x['recency'], 
                frequency=x['frequency'],  
                monetary=x['monetary'], 
                T=x['T'],
                pred_1month=x['pred_1month']
            )),
            axis=1
        )
        self.session.commit()
 
 # create, deletem,  read
 
 
 import sqlalchemy
import pandas as pd
import IPython
import ipywidgets
from sqlalchemy import create_engine
from .tables import Location, Customer, Facts, CustomerFact, Prediction
from sqlalchemy.orm import sessionmaker
from zenq.clvmodels.modeling import Model
import pandas as pd
import ipywidgets as widgets
from IPython.display import display
from sqlalchemy.exc import IntegrityError


#import logging

class points():
    engine = create_engine('postgresql://postgres:mysecretpassword@localhost:5432/postgres')
    Session = sessionmaker(bind=engine)
    session = Session()
    model = Model('postgresql://postgres:mysecretpassword@localhost:5432/postgres')
    
    def __init__(self):
        self.df = None

    def read_csv(self, filename):
        self.df = pd.read_csv(filename)
        
    def insert_location_name(self, filename):
        # Read the input CSV file into a DataFrame
        self.df = pd.read_csv(filename)

        # Get the list of available columns from the DataFrame
        available_columns = self.df.columns.tolist()

        # Create a dropdown widget for the user to choose a column from the available columns
        column_dropdown = widgets.Dropdown(options=available_columns, description='Choose column')

        # Display the dropdown widget
        display(column_dropdown)

        # Wait for the user to select a column and click the 'Submit' button
        submit_button = widgets.Button(description='Submit')
        display(submit_button)
        output = widgets.Output()

        def on_submit_button_clicked(b):
            with output:
                # Get the chosen column name
                column_name = column_dropdown.value

                # Insert the data into the Location table
                unique_locations = self.df[[column_name]].drop_duplicates()
                for index, row in unique_locations.iterrows():
                    location_name = row[column_name]
                    try:
                        self.engine.execute(
                            Location.__table__.insert(),
                            {'location_name': location_name}
                        )
                        print(f'Successfully inserted location: {location_name}')
                    except IntegrityError:
                        print(f'Location {location_name} already exists in the table')

        submit_button.on_click(on_submit_button_clicked)
        display(output)     

    def insert_customer(self, filename):
        self.read_csv(filename)

        # Insert the data into the Customer table
        self.df[['customer_id', 'gender']].drop_duplicates().apply(
        lambda x: Customer(customer_id=x['customer_id'], gender=x['gender']), axis=1
        ).to_sql('Customer', self.engine, schema='initial', if_exists='append', index=False)

    def insert_facts(self, filename):
    # Read the input CSV file into a DataFrame
       self.read_csv(filename)

    # Insert the data into the Facts table
       self.df[['customer_id','location_id', 'date', 'quantity', 'total_price']].drop_duplicates().apply(
       lambda x: Facts(customer_id=x['customer_id'], location_id=x['location_id'], date=x['date'], quantity=x['quantity'], total_price=x['total_price']), axis=1
       ).to_sql('Facts', self.engine, schema='initial', if_exists='append', index=False)
     
    def insert_customer_fact(self):
    # Call the count_coding function
        df = self.model.count_coding()

    # Insert the output data into the CustomerFact table
        df.apply(
           lambda x: self.session.add(CustomerFact(
               customer_id=x['customer_id'], 
               date=x['date'], 
               invoice_id=x['invoice_id'], 
               quantity=x['quantity'], 
               price=x['price'], 
               CLV=x['CLV']
             )),
             axis=1
        )
        self.session.commit()


    def insert_prediction(self):
    # Call the count_coding function
        df = self.model.count_coding()

    # Insert the output data into the CustomerFact table
        df.apply(
            lambda x: self.session.add(Prediction(
                customer_id=x['customer_id'], 
                recency=x['recency'], 
                frequency=x['frequency'],  
                monetary=x['monetary'], 
                T=x['T'],
                pred_1month=x['pred_1month']
            )),
            axis=1
        )
        self.session.commit()
 
 # create, deletem,  read