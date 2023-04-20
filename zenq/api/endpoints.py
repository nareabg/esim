import sqlalchemy
import pandas as pd
import IPython
import ipywidgets
from sqlalchemy import create_engine
from .tables import Customer, Facts, CustomerFact, Prediction
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
    
    # def __init__(self, filename):
    #     self.df = pd.read_csv(filename)

    # def insert_location_name(self):
    #         # Get the list of available columns from the DataFrame
    #         available_columns = self.df.columns.tolist()

    #         # Create dropdown widgets for the user to choose columns
    #         column_dropdowns = [widgets.Dropdown(options=available_columns, description=f'Map to {col}')
    #                             for col in ['location_id', 'location_name']]

    #         # Display the dropdown widgets
    #         display(*column_dropdowns)

    #         # Wait for the user to select columns and click the 'Submit' button
    #         submit_button = widgets.Button(description='Submit')
    #         display(submit_button)
    #         output = widgets.Output()

    #         def on_submit_button_clicked(b):
    #             with output:
    #                 # Get the chosen column names
    #                 column_names = [dropdown.value for dropdown in column_dropdowns]

    #                 # Insert the data into the Location table
    #                 unique_locations = self.df.drop_duplicates(subset=column_names)
    #                 for index, row in unique_locations.iterrows():
    #                     location_id, location_name = row[column_names[0]], row[column_names[1]]
    #                     try:
    #                         self.engine.execute(
    #                             Location.__table__.insert(),
    #                             {'location_id': location_id, 'location_name': location_name}
    #                         )
    #                         print(f'Successfully inserted location: {location_id}, {location_name}')
    #                     except IntegrityError:
    #                         print(f'Location {location_id}, {location_name} already exists in the table')
    #             self.engine.dispose()

    #         submit_button.on_click(on_submit_button_clicked)
    #         display(output)
 

    # def insert_customer(self):

    #     # Insert the data into the Customer table
    #     self.df[['customer_id', 'gender']].drop_duplicates().apply(
    #     lambda x: Customer(customer_id=x['customer_id'], gender=x['gender']), axis=1
    #     ).to_sql('Customer', self.engine, schema='initial', if_exists='append', index=False)

    # def insert_facts(self):
    # # Insert the data into the Facts table
    #    self.df[['customer_id','location_id', 'date', 'quantity', 'total_price']].drop_duplicates().apply(
    #    lambda x: Facts(customer_id=x['customer_id'], location_id=x['location_id'], date=x['date'], quantity=x['quantity'], total_price=x['total_price']), axis=1
    #    ).to_sql('Facts', self.engine, schema='initial', if_exists='append', index=False)
    
    # def get_column_mapping(self):
    #     """
    #     This method returns a dictionary where the keys represent the columns in the CSV file and the values represent 
    #     the corresponding columns in the database table.
    #     """
    #     column_mapping = {}
    #     for col in self.df.columns:
    #         column_mapping[col] = input(f"Enter the column name for {col}: ")
    #     return column_mapping
    
    def __init__(self, filename):
        self.df = pd.read_csv(filename)
        self.columns = self.df.columns.tolist()
        self.db_cols = {"Customer": ["gender", "customer_id"], "Facts": ["location_id", "date", "quantity", "total_price", "location_name", "gender"]}


    def upload(self):
        db_cols = {
            Customer.__tablename__: [column.name for column in Customer.__table__.columns],
            Facts.__tablename__: [column.name for column in Facts.__table__.columns]
        }
        
        options = {col: widgets.Dropdown(options=db_cols[table], description=col)
                for table in db_cols for col in db_cols[table]}
        
        def on_button_clicked(button):
            data = {}
            for db_col, dropdown in options.items():
                csv_col = dropdown.value
                if csv_col:
                    data[db_col] = self.df[csv_col]
            
            self.save_data(data)
        
        button = widgets.Button(description="Upload data")
        button.on_click(on_button_clicked)
        
        ui = widgets.VBox(list(options.values()) + [button])
        display(ui)


    def save_data(self, data):
        customer_cols = [col for col in data if col in Customer.__table__.columns]
        if customer_cols:
            customers = pd.concat([data[col] for col in customer_cols], axis=1).drop_duplicates()
            customers = customers.loc[:, customer_cols].dropna()
            customers = [Customer(**row) for _, row in customers.iterrows()]
            try:
                self.session.add_all(customers)
                self.session.commit()
            except IntegrityError:
                self.session.rollback()
        
        facts_cols = [col for col in data if col in Facts.__table__.columns]
        if facts_cols:
            facts = pd.concat([data[col] for col in facts_cols], axis=1).drop_duplicates()
            facts = facts.loc[:, facts_cols].dropna()
            facts = [Facts(**row) for _, row in facts.iterrows()]
            try:
                self.session.add_all(facts)
                self.session.commit()
            except IntegrityError:
                self.session.rollback()
         
         
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