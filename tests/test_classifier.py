"""
Test suite for Enhanced Classifier
"""
import unittest
import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

# Import with fallback handling
try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False
    print("Warning: pandas not available, using fallback test data")

from enhanced_classifier import AIDataClassifier

class TestAIDataClassifier(unittest.TestCase):
    
    def setUp(self):
        self.classifier = AIDataClassifier()

        # Create test data (pandas or fallback)
        if HAS_PANDAS:
            self.test_data = pd.DataFrame({
                'customer_name': ['John Doe', 'Jane Smith'],
                'email': ['john@test.com', 'jane@test.com'],
                'ssn': ['123-45-6789', '987-65-4321'],
                'account_balance': [1500.50, 2750.25]
            })
        else:
            # Fallback test data as dict
            self.test_data = {
                'customer_name': ['John Doe', 'Jane Smith'],
                'email': ['john@test.com', 'jane@test.com'],
                'ssn': ['123-45-6789', '987-65-4321'],
                'account_balance': [1500.50, 2750.25]
            }
    
    def test_classifier_initialization(self):
        """Test classifier initializes correctly"""
        self.assertIsNotNone(self.classifier)
        # Check for actual attributes that exist
        self.assertTrue(hasattr(self.classifier, 'field_patterns'))
        self.assertTrue(hasattr(self.classifier, 'content_patterns'))
        self.assertTrue(hasattr(self.classifier, 'risk_levels'))
    
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
        # Use the correct method name
        summary = self.classifier.generate_executive_summary(results)

        self.assertIn('EXECUTIVE DATA CLASSIFICATION SUMMARY', summary)
        self.assertIn('Total Fields Analyzed:', summary)

if __name__ == '__main__':
    unittest.main()
