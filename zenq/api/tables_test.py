
import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tables import Base, Customer, Facts
import pytest

class TestTables(unittest.TestCase):

    def setUp(self):
        engine = create_engine("sqlite:///:memory:")
        Session = sessionmaker(bind=engine)
        self.session = Session()
        Base.metadata.create_all(engine)

    def test_customer_table(self):
        new_customer = Customer(customer_id="C001", gender="Male")
        self.session.add(new_customer)
        self.session.commit()
        result = self.session.query(Customer).filter_by(customer_id="C001").first()
        self.assertIsNotNone(result)

    def test_facts_table(self):
        new_customer = Customer(customer_id="C001", gender="Male")
        self.session.add(new_customer)
        self.session.commit()
        new_fact = Facts(customer=new_customer, location_id="L001", location_name="Store 1", invoice_id="I001", date="2022-01-01", quantity=2, total_price=20)
        self.session.add(new_fact)
        self.session.commit()
        result = self.session.query(Facts).filter_by(invoice_id="I001").first()
        self.assertIsNotNone(result)

    def test_tables():
        engine = create_engine('postgresql://aua:mysecretpassword@localhost:5432/test_GLOBBING')
        Session = sessionmaker(bind=engine)
        session = Session()
        Base.metadata.create_all(engine)
        customer1 = Customer(customer_id='abc123', gender='male')
        customer2 = Customer(customer_id='def456', gender='female')
        session.add_all([customer1, customer2])
        session.commit()

        facts1 = Facts(customer_id_uniq=customer1.id, location_id='loc1', location_name='Location 1', invoice_id='inv1', date='2022-04-20', quantity=2, total_price=10.0)
        facts2 = Facts(customer_id_uniq=customer2.id, location_id='loc2', location_name='Location 2', invoice_id='inv2', date='2022-04-20', quantity=3, total_price=15.0)
        session.add_all([facts1, facts2])
        session.commit()
        assert len(session.query(Customer).all()) == 2
        assert len(session.query(Facts).all()) == 2
        assert session.query(Facts).filter(Facts.customer_id_uniq == customer1.id).one().total_price == 10.0
        Base.metadata.drop_all(engine)
