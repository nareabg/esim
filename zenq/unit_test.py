import unittest
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .api.tables import Customer, Facts, CustomerFact, Prediction
from .clvmodels.modeling import Model

class TestMLSystem(unittest.TestCase):

    def setUp(self):
        self.engine = create_engine('postgresql://aua:mysecretpassword@localhost:5432/GLOBBING')
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        self.customer_data = {'customer_id': [1, 2, 3, 4, 5], 'gender': ['M', 'F', 'F', 'M', 'F']}
        self.facts_data = {'customer_id_uniq': [1, 1, 2, 3, 4, 5], 'location_id': [1, 1, 2, 3, 4, 5], 'location_name': ['NY', 'NY', 'CA', 'TX', 'IL', 'NY'], 'invoice_id': [1001, 1002, 1003, 1004, 1005, 1006], 'date': ['2022-01-01', '2022-01-02', '2022-01-03', '2022-01-04', '2022-01-05', '2022-01-06'], 'quantity': [2, 1, 3, 1, 2, 1], 'total_price': [100, 50, 150, 75, 100, 50]}
        self.customer_df = pd.DataFrame.from_dict(self.customer_data)
        self.facts_df = pd.DataFrame.from_dict(self.facts_data)
        self.customer_ids = self.customer_df['customer_id'].tolist()

    def test_create_customer_table(self):
        self.assertTrue(Customer.__table__.exists(self.engine))

    def test_create_facts_table(self):
        self.assertTrue(Facts.__table__.exists(self.engine))

    def test_insert_customers(self):
        # Insert customers into the database
        for index, row in self.customer_df.iterrows():
            self.session.add(Customer(customer_id=row['customer_id'], gender=row['gender']))
        self.session.commit()

        # Check that the customers were inserted correctly
        for index, row in self.customer_df.iterrows():
            customer = self.session.query(Customer).filter_by(customer_id=row['customer_id']).first()
            self.assertIsNotNone(customer)
            self.assertEqual(customer.gender, row['gender'])

    def test_insert_facts(self):
        # Insert customers into the database
        for index, row in self.customer_df.iterrows():
            self.session.add(Customer(customer_id=row['customer_id'], gender=row['gender']))
        self.session.commit()

        # Insert facts into the database
        for index, row in self.facts_df.iterrows():
            customer = self.session.query(Customer).filter_by(customer_id=row['customer_id_uniq']).first()
            self.assertIsNotNone(customer)
            facts = Facts(
                customer_id_uniq=customer.id,
                location_id=row['location_id'],
                location_name=row['location_name'],
                invoice_id=row['invoice_id'],
                date=row['date'],
                quantity=row['quantity'],
                total_price=row['total_price']
            )
            self.session.add(facts)
        self.session.commit()

        # Check that the facts were inserted correctly
        for index, row in self.facts_df.iterrows():
            customer_fact = self
