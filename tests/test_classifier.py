"""
Test suite for Enhanced Classifier
"""
import unittest
import pandas as pd
import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from enhanced_classifier import AIDataClassifier

class TestAIDataClassifier(unittest.TestCase):
    
    def setUp(self):
        self.classifier = AIDataClassifier()
        
        # Create test data
        self.test_data = pd.DataFrame({
            'customer_name': ['John Doe', 'Jane Smith'],
            'email': ['john@test.com', 'jane@test.com'],
            'ssn': ['123-45-6789', '987-65-4321'],
            'account_balance': [1500.50, 2750.25]
        })
    
    def test_classifier_initialization(self):
        """Test classifier initializes correctly"""
        self.assertIsNotNone(self.classifier)
        self.assertTrue(hasattr(self.classifier, 'semantic_analyzer'))
    
    def test_data_classification(self):
        """Test basic data classification functionality"""
        results = self.classifier.classify_dataset(self.test_data, "test_data")
        
        # Check that all fields were classified
        self.assertEqual(len(results), 4)
        
        # Check specific classifications
        self.assertIn('customer_name', results)
        self.assertIn('ssn', results)
        
        # SSN should be classified as high risk
        ssn_result = results['ssn']
        self.assertEqual(ssn_result.data_type.value, 'pii_ssn')
        self.assertGreaterEqual(ssn_result.confidence, 0.8)
    
    def test_executive_summary_generation(self):
        """Test executive summary generation"""
        results = self.classifier.classify_dataset(self.test_data, "test_data")
        summary = self.classifier.generate_classification_report(results)
        
        self.assertIn('EXECUTIVE SUMMARY', summary)
        self.assertIn('Total fields analyzed:', summary)

if __name__ == '__main__':
    unittest.main()
