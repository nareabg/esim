import sqlalchemy
import pandas as pd
import IPython
import ipywidgets
from sqlalchemy import create_engine
from .tables import  Facts #, CustomerFact, Prediction
from sqlalchemy.orm import sessionmaker
# from zenq.clvmodels.modeling import ParetoNBD_CLV_Model
import pandas as pd
import ipywidgets as widgets
from IPython.display import display
from sqlalchemy.exc import IntegrityError
from .config import db_uri

class points():
    engine = create_engine(db_uri)
    Session = sessionmaker(bind=engine)
    session = Session()
    #model = ParetoNBD_CLV_Model('postgresql://aua:mysecretpassword@localhost:5432/GLOBBING')
    
    def __init__(self, filename):
        self.df = pd.read_csv(filename)

 
    def insert_facts(self):
            # Get the list of available columns from the DataFrame
            available_columns = self.df.columns.tolist()

            # Create dropdown widgets for the user to choose columns
            column_dropdowns = [widgets.Dropdown(options=available_columns, description=f'Map to {col}')
                                for col in ['customer_id', 'gender', 'location_id', 'location_name', 'invoice_id', 'date', 'quantity', 'total_price']]

            # Display the dropdown widgets
            display(*column_dropdowns)

            # Wait for the user to select columns and click the 'Submit' button
            submit_button = widgets.Button(description='Submit')
            display(submit_button)
            output = widgets.Output()

            def on_submit_button_clicked(b):
                with output:
                    # Get the chosen column names
                    column_names = [dropdown.value for dropdown in column_dropdowns]

                    # Insert the data into the Location table
                    unique_customers = self.df.drop_duplicates(subset=column_names)
                    for index, row in unique_customers.iterrows():
                        customer_id, gender, location_id, location_name, invoice_id, date, quantity, total_price = row[column_names[0]], row[column_names[1]], row[column_names[2]], row[column_names[3]], row[column_names[4]], row[column_names[5]], row[column_names[6]], row[column_names[7]]
                        try:
                            self.engine.execute(
                                Facts.__table__.insert(),
                                {'customer_id': customer_id, 'gender': gender, 'location_id': location_id,'location_name':location_name, 'invoice_id':invoice_id, 'date':date, 'quantity':quantity, 'total_price': total_price }
                            )
                            print(f'Successfully inserted location: {customer_id}, {gender},  {location_id}, {location_name}, {invoice_id}, {date}, {quantity}, {total_price} ')
                        except IntegrityError:
                            print(f'Customer {invoice_id} already exists in the table')
                self.engine.dispose()

            submit_button.on_click(on_submit_button_clicked)
            display(output)
    # Location, Customer
    
    
    
    
    
    
    
         
            
    # def insert_facts(self):
    #     # Get the list of available columns from the DataFrame
    #     available_columns = self.df.columns.tolist()

    #     # Create dropdown widgets for the user to choose columns
    #     column_dropdowns = [widgets.Dropdown(options=available_columns, description=f'Map to {col}')
    #                         for col in ['location_id', 'location_name', 'invoice_id', 'date', 'quantity', 'total_price']]

    #     # Display the dropdown widgets
    #     display(*column_dropdowns)

    #     # Wait for the user to select columns and click the 'Submit' button
    #     submit_button = widgets.Button(description='Submit')
    #     display(submit_button)
    #     output = widgets.Output()

    #     def on_submit_button_clicked(b):
    #         with output:
    #             # Get the chosen column names
    #             column_names = [dropdown.value for dropdown in column_dropdowns]

    #             # Insert the data into the Facts table
    #             for idx, (index, row) in enumerate(self.df.iterrows()):
    #                 # get the customer_id from the input data
    #                 # customer_id =  row[column_names[0]]
    #                 customer_id =  self.session.query(Customer).all()
    #                 # print(customer_id[idx].id)
    #                 # print(self.session.query(Customer))
    #                 # query the database for the corresponding Customer instance
    #                 # customer = self.session.query(Customer).filter_by(customer_id=customer_id[idx].id).all()
    #                 # print(customer)
    #                 # create a new Facts instance and set its customer attribute
    #                 facts = Facts(
    #                     customer_id_uniq=customer_id[idx].id,
    #                     location_id=row[column_names[0]],
    #                     location_name=row[column_names[1]],
    #                     invoice_id=row[column_names[2]],
    #                     date=row[column_names[3]],
    #                     quantity=row[column_names[4]],
    #                     total_price=row[column_names[5]]
    #                 )

    #                 try:
    #                     # add the new Facts instance to the session and commit the changes
    #                     self.session.merge(facts)
    #                     self.session.commit()
    #                     print(f'Successfully inserted facts for customer')
    #                 except IntegrityError as e:
    #                     print(f'Facts already exists in the table')
    #                     self.session.rollback()
    #                     # print the error message if an IntegrityError occurs
    #                     # print(f'Error inserting facts: {str(e)}')
    #                     # print(f'Facts {row[column_names[0]]}, {row[column_names[1]]}, {row[column_names[2]]}, {row[column_names[3]]}, {row[column_names[4]]}, {row[column_names[5]]} already exists in the table')

    #         self.session.close()

    #     submit_button.on_click(on_submit_button_clicked)
    #     display(output)
        
# def insert_facts(self):
    #         # Get the list of available columns from the DataFrame
    #         available_columns = self.df.columns.tolist()

    #         # Create dropdown widgets for the user to choose columns
    #         column_dropdowns = [widgets.Dropdown(options=available_columns, description=f'Map to {col}')
    #                             for col in ['location_id', 'location_name', 'invoice_id', 'date', 'quantity', 'total_price']]

    #         # Display the dropdown widgets
    #         display(*column_dropdowns)

    #         # Wait for the user to select columns and click the 'Submit' button
    #         submit_button = widgets.Button(description='Submit')
    #         display(submit_button)
    #         output = widgets.Output()
             
            # def on_submit_button_clicked(b):
            #     with output:
            #         # Get the chosen column names
            #         column_names = [dropdown.value for dropdown in column_dropdowns]

            #         # Insert the data into the Location table
            #         unique_customers = self.df.drop_duplicates(subset=column_names)
            #         for index, row in unique_customers.iterrows():
            #             location_id, location_name, invoice_id, date, quantity, total_price  = row[column_names[0]], row[column_names[1]], row[column_names[2]], row[column_names[3]], row[column_names[4]], row[column_names[5]]
            #             try:
            #                 self.engine.execute(
            #                     Facts.__table__.insert(),
            #                     {'location_id': location_id, 'location_name': location_name, 'invoice_id': invoice_id, 'date': date, 'quantity': quantity, 'total_price': total_price}
            #                 )
            #                 print(f'Successfully inserted location: {location_id}, {location_name}, {invoice_id}, {date}, {quantity}, {total_price}')
            #             except IntegrityError:
            #                 print(f'Error inserting facts: {str(e)}')
            #                 print(f'Facts {location_id}, {location_name}, {invoice_id}, {date}, {quantity}, {total_price} already exists in the table')
            #     self.engine.dispose()

            # submit_button.on_click(on_submit_button_clicked)
            # display(output)
 
