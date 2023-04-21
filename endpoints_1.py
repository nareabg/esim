# import sqlalchemy
# import pandas as pd
# import IPython
# import ipywidgets
# from sqlalchemy import create_engine
# from .tables import Customer, Facts, CustomerFact, Prediction
# from sqlalchemy.orm import sessionmaker
# from zenq.clvmodels.modeling import Model
# import pandas as pd
# import ipywidgets as widgets
# from IPython.display import display
# from sqlalchemy.exc import IntegrityError


# #import logging

# class points():
#     engine = create_engine('postgresql://aua:mysecretpassword@localhost:5432/GLOBBING')
#     Session = sessionmaker(bind=engine)
#     session = Session()
#     model = Model('postgresql://aua:mysecretpassword@localhost:5432/GLOBBING')
    
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


# #import logging

# class points():
#     engine = create_engine('postgresql://aua:mysecretpassword@localhost:5432/GLOBBING')
#     Session = sessionmaker(bind=engine)
#     session = Session()
#     model = Model('postgresql://aua:mysecretpassword@localhost:5432/GLOBBING')   
#     def __init__(self, filename):
#         self.df = pd.read_csv(filename)
#         self.columns = self.df.columns.tolist()
#         self.db_cols = {"Customer": ["gender", "customer_id"], "Facts": ["location_id", "date", "quantity", "total_price", "location_name", "gender"]}


#     def upload(self):
#         db_cols = {
#             Customer.__tablename__: [column.name for column in Customer.__table__.columns],
#             Facts.__tablename__: [column.name for column in Facts.__table__.columns]
#         }
        
#         options = {col: widgets.Dropdown(options=db_cols[table], description=col)
#                 for table in db_cols for col in db_cols[table]}
        
#         def on_button_clicked(button):
#             data = {}
#             for db_col, dropdown in options.items():
#                 csv_col = dropdown.value
#                 if csv_col:
#                     data[db_col] = self.df[csv_col]
            
#             self.save_data(data)
        
#         button = widgets.Button(description="Upload data")
#         button.on_click(on_button_clicked)
        
#         ui = widgets.VBox(list(options.values()) + [button])
#         display(ui)


#     def save_data(self, data):
#         customer_cols = [col for col in data if col in Customer.__table__.columns]
#         if customer_cols:
#             customers = pd.concat([data[col] for col in customer_cols], axis=1).drop_duplicates()
#             customers = customers.loc[:, customer_cols].dropna()
#             customers = [Customer(**row) for _, row in customers.iterrows()]
#             try:
#                 self.session.add_all(customers)
#                 self.session.commit()
#             except IntegrityError:
#                 self.session.rollback()
        
#         facts_cols = [col for col in data if col in Facts.__table__.columns]
#         if facts_cols:
#             facts = pd.concat([data[col] for col in facts_cols], axis=1).drop_duplicates()
#             facts = facts.loc[:, facts_cols].dropna()
#             facts = [Facts(**row) for _, row in facts.iterrows()]
#             try:
#                 self.session.add_all(facts)
#                 self.session.commit()
#             except IntegrityError:
#                 self.session.rollback()
         
         
#     def insert_customer_fact(self):
#     # Call the count_coding function
#         df = self.model.count_coding()

#     # Insert the output data into the CustomerFact table
#         df.apply(
#            lambda x: self.session.add(CustomerFact(
#                customer_id=x['customer_id'], 
#                date=x['date'], 
#                invoice_id=x['invoice_id'], 
#                quantity=x['quantity'], 
#                price=x['price'], 
#                CLV=x['CLV']
#              )),
#              axis=1
#         )
#         self.session.commit()


#     def insert_prediction(self):
#     # Call the count_coding function
#         df = self.model.count_coding()

#     # Insert the output data into the CustomerFact table
#         df.apply(
#             lambda x: self.session.add(Prediction(
#                 customer_id=x['customer_id'], 
#                 recency=x['recency'], 
#                 frequency=x['frequency'],  
#                 monetary=x['monetary'], 
#                 T=x['T'],
#                 pred_1month=x['pred_1month']
#             )),
#             axis=1
#         )
#         self.session.commit()
 
#  # create, deletem,  read
# import sqlalchemy
# import pandas as pd
# import IPython
# import ipywidgets
# from sqlalchemy import create_engine
# from .tables import Customer, Facts
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.exc import IntegrityError

# class points():
#     engine = create_engine('postgresql://aua:mysecretpassword@localhost:5432/GLOBBING')
#     Session = sessionmaker(bind=engine)
#     session = Session()

#     def __init__(self, filename):
#         self.df = pd.read_csv(filename)
#         self.df.columns = [col.strip() for col in self.df.columns]
#         print(self.df.columns)

#     def insert_customer(self):
#         # Get the list of available columns from the DataFrame
#         available_columns = self.df.columns.tolist()

#         # Create dropdown widgets for the user to choose columns
#         column_dropdowns = [widgets.Dropdown(options=available_columns, description=f'Map to {col}')
#                             for col in ['customer_id', 'gender']]

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
#                 print(column_names)
#                 # Insert the data into the Customer table
#                 unique_customers = self.df.drop_duplicates(subset=column_names)
#                 for index, row in unique_customers.iterrows():
#                     customer_id, gender = row[column_names[0]], row[column_names[1]]
#                     try:
#                         self.session.add(
#                             Customer(
#                                 customer_id=customer_id,
#                                 gender=gender
#                             )
#                         )
#                         self.session.commit()
#                         print(f'Successfully inserted customer: {customer_id}, {gender}')
#                     except IntegrityError:
#                         self.session.rollback()
#                         print(f'Customer {customer_id} already exists in the table')
#             self.session.close()

#         submit_button.on_click(on_submit_button_clicked)
#         display(output)
        
        
        
            
#     def insert_facts(self):
#             # Get the list of available columns from the database table
#             available_columns = [col.name for col in Facts.__table__.columns]
#             available_columns.remove('id')
#             available_columns.remove('customer_id_uniq')
#             # Create dropdown widgets for the user to choose columns
#             column_dropdowns = [widgets.Dropdown(options=available_columns, description=f'Map to {col}')
#                                 for col in ['location_id', 'location_name', 'invoice_id', 'date', 'quantity', 'total_price']]

#             # Display the dropdown widgets
#             display(*column_dropdowns)

#             # Wait for the user to select columns and click the 'Submit' button
#             submit_button = widgets.Button(description='Submit')
#             display(submit_button)
#             output = widgets.Output()

#             def on_submit_button_clicked(b):
#                 with output:
#                     # Get the chosen column names
#                     column_names = [self.get_db_column_name(dropdown.label) for dropdown in column_dropdowns]

#                     # Insert the data into the Facts table
#                     unique_facts = self.df.drop_duplicates(subset=[column_names[2]])
#                     for index, row in unique_facts.iterrows():
#                         location_id, location_name, invoice_id, date, quantity, total_price = row[column_names[0]], row[column_names[1]], row[column_names[2]], row[column_names[3]], row[column_names[4]], row[column_names[5]]
#                         try:
#                             customer = self.session.query(Customer).filter_by(customer_id=row[column_names[6]]).one()
#                             self.session.add(
#                                 Facts(
#                                     customer_id_uniq=customer.id,
#                                     location_id=location_id,
#                                     location_name=location_name,
#                                     invoice_id=invoice_id,
#                                     date=date,
#                                     quantity=quantity,
#                                     total_price=total_price
#                                 )
#                             )
#                             self.session.commit()
#                             print(f'Successfully inserted fact: {invoice_id}, {date}, {quantity}, {total_price}')
#                         except IntegrityError:
#                             self.session.rollback()
#                             print(f'Fact {invoice_id} already exists in the table')
#                     self.session.close()

#             submit_button.on_click(on_submit_button_clicked)
#             display(output)

#             def get_db_column_name(self, label):
#                 for col in Facts.__table__.columns:
#                     if label == f'Map to {col.name}':
#                         return col.name

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
    #             column_names = [dropdown.label for dropdown in column_dropdowns]
    #             print(column_names)
    #             # Insert the data into the Facts table
    #             unique_facts = self.df.drop_duplicates(subset=[column_names[3]])
    #             for index, row in unique_facts.iterrows():
    #                 location_id, location_name, invoice_id, date, quantity, total_price = row[column_names[0]], row[column_names[1]], row[column_names[2]], row[column_names[3]], row[column_names[4]], row[column_names[5]]
    #                 try:
    #                     customer = self.session.query(Customer).filter_by(customer_id=customer_id).one()
    #                     self.session.add(
    #                         Facts(
    #                             customer_id_uniq=customer.id,
    #                             location_id=location_id,
    #                             location_name=location_name,
    #                             invoice_id=invoice_id,
    #                             date=date,
    #                             quantity=quantity,
    #                             total_price=total_price
    #                         )
    #                     )
    #                     self.session.commit()
    #                     print(f'Successfully inserted fact: {invoice_id}, {date}, {quantity}, {total_price}')
    #                 except IntegrityError:
    #                     self.session.rollback()
    #                     print(f'Fact {invoice_id} already exists in the table')
    #             self.session.close()

    #     submit_button.on_click(on_submit_button_clicked)
    #     display(output)


import sqlalchemy
import pandas as pd
import IPython
import ipywidgets
from sqlalchemy import create_engine
from .tables import Customer, Facts
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

class points():
    engine = create_engine('postgresql://aua:mysecretpassword@localhost:5432/GLOBBING')
    Session = sessionmaker(bind=engine)
    session = Session()

    def __init__(self, filename):
        self.df = pd.read_csv(filename)
        self.df.columns = [col.strip() for col in self.df.columns]
        print(self.df.columns)

    def insert_customer(self):
        # Get the list of available columns from the DataFrame
        available_columns = self.df.columns.tolist()

        # Remove columns that don't exist in the Customer table
        available_columns.remove('invoice_id')
        available_columns.remove('location_id')
        available_columns.remove('location_name')
        available_columns.remove('date')
        available_columns.remove('quantity')
        available_columns.remove('total_price')

        # Create dropdown widgets for the user to choose columns
        column_dropdowns = [widgets.Dropdown(options=available_columns, description=f'Map to {col}')
                            for col in ['customer_id', 'gender']]

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
                print(column_names)

                # Insert the data into the Customer table
                unique_customers = self.df.drop_duplicates(subset=column_names)
                for index, row in unique_customers.iterrows():
                    customer_data = {col: row[column_names[i]] for i, col in enumerate(column_names)}
                    try:
                        self.session.add(
                            Customer(**customer_data)
                        )
                        self.session.commit()
                        print(f'Successfully inserted customer: {customer_data}')
                    except IntegrityError:
                        self.session.rollback()
                        print(f'Customer {customer_data} already exists in the table')
            self.session.close()

        submit_button.on_click(on_submit_button_clicked)
        display(output)

    def insert_facts(self):
        # Get the list of available columns from the DataFrame
        available_columns = self.df.columns.tolist()
        # available_columns.remove('id')
        # available_columns.remove('customer_id_uniq')
             
        # Create dropdown widgets for the user to choose columns
        column_dropdowns = [widgets.Dropdown(options=available_columns, description=f'{col}')
                            for col in ['location_id', 'location_name', 'invoice_id', 'date', 'quantity', 'total_price']]

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
                print(column_names)

                # Insert the data into the Facts table
                unique_facts = self.df.drop_duplicates(subset=column_names[3])
                for index, row in unique_facts.iterrows():
                    fact_data = {col: row[column_names[i]] for i, col in enumerate(column_names)}
                    print(fact_data)

                    # try:
                    #     customer = self.session.query(Customer).filter_by(customer_id=fact_data['customer_id']).one()
                    #     self.session.add(
                    #         Facts(
                    #             customer_id_uniq=customer.id,
                    #             location_id=fact_data['location_id'],
                    #             location_name=fact_data['location_name'],
                    #             invoice_id=fact_data['invoice_id'],
                    #             date=fact_data['date'],
                    #              quantity=fact_data['quantity'],
                    #              total_price=fact_data['total_price']
                    #         )
                    #     )
                    #     self.session.commit()
                    #     print(f'Successfully inserted fact: {invoice_id}, {date}, {quantity}, {total_price}')
                    # except IntegrityError:
                    #     self.session.rollback()
                    #     print(f'Fact {invoice_id} already exists in the table')
                # self.session.close()

        submit_button.on_click(on_submit_button_clicked)
        display(output)
