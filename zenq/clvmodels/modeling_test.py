import unittest
from .modeling import Model

class TestModel(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.db_uri = "postgresql://user:password@localhost/db_name"
        cls.model = Model(cls.db_uri)
    
    def test_count_coding(self):
        result = self.model.count_coding()
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(result.shape[1], 7)
        self.assertTrue(all(col in result.columns for col in ['customer_id', 'date', 'invoice_id', 'quantity', 'price', 'avg_order_value', 'repeat_rate']))
        
    def test_count_cltv(self):
        result = self.model.count_cltv(days=30)
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(result.shape[1], 8)
        self.assertTrue(all(col in result.columns for col in ['customer_id', 'total_price', 'CLV', 'purchase_frequency', 'repeat_rate', 'churn_rate', 'cltv_predicted']))
        
if __name__ == '__main__':
    unittest.main()
