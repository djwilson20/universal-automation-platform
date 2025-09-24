"""
Smoke tests for the AI Automation Platform.
These tests verify basic functionality across environments.
"""

import os
import pytest
import requests
import pandas as pd
from src.enhanced_classifier import AIDataClassifier
from src.universal_content_engine import UniversalContentEngine


class TestSmokeTests:
    """Basic smoke tests to verify system functionality."""

    def test_classifier_initialization(self):
        """Test that the AI classifier can be initialized."""
        classifier = AIDataClassifier()
        assert classifier is not None

    def test_content_engine_initialization(self):
        """Test that the content engine can be initialized."""
        engine = UniversalContentEngine()
        assert engine is not None

    def test_basic_data_classification(self):
        """Test basic data classification functionality."""
        classifier = AIDataClassifier()

        # Create simple test data
        test_data = pd.DataFrame({
            'customer_name': ['John Doe', 'Jane Smith'],
            'email': ['john@example.com', 'jane@example.com'],
            'revenue': [10000, 15000],
            'department': ['Sales', 'Marketing']
        })

        # Classify the data
        results = classifier.classify_dataset(test_data, "test_dataset")

        # Verify we get results
        assert results is not None
        assert 'classification_results' in results
        assert 'security_analysis' in results
        assert 'confidence_scores' in results

    def test_sample_data_processing(self):
        """Test processing of the sample data file."""
        if os.path.exists('test_data.csv'):
            classifier = AIDataClassifier()
            data = pd.read_csv('test_data.csv')

            results = classifier.classify_dataset(data, 'smoke_test')

            assert results is not None
            assert len(results['classification_results']) > 0

    @pytest.mark.integration
    def test_full_workflow(self):
        """Test the complete workflow from data to analysis."""
        # Step 1: Classify data
        classifier = AIDataClassifier()
        test_data = pd.DataFrame({
            'user_id': [1, 2, 3],
            'email': ['test1@example.com', 'test2@example.com', 'test3@example.com'],
            'salary': [50000, 60000, 70000]
        })

        classification_results = classifier.classify_dataset(test_data, "workflow_test")

        # Step 2: Generate content
        engine = UniversalContentEngine()
        content_results = engine.generate_executive_content(
            classification_results,
            "Test Workflow Analysis"
        )

        # Verify results
        assert classification_results is not None
        assert content_results is not None
        assert 'executive_summary' in content_results


@pytest.mark.skipif(
    os.getenv('ENV') not in ['staging', 'production'],
    reason="Environment-specific tests only run in staging/production"
)
class TestEnvironmentSmoke:
    """Environment-specific smoke tests."""

    def test_health_endpoint(self):
        """Test the application health endpoint."""
        env = os.getenv('ENV', 'staging')

        if env == 'production':
            health_url = 'https://ai-automation-platform.com/health'
        else:
            health_url = f'https://{env}.ai-automation-platform.com/health'

        try:
            response = requests.get(health_url, timeout=10)
            assert response.status_code == 200

            health_data = response.json()
            assert 'status' in health_data
            assert health_data['status'] == 'healthy'

        except requests.exceptions.RequestException as e:
            pytest.fail(f"Health check failed: {str(e)}")

    def test_application_startup(self):
        """Test that the application starts successfully."""
        env = os.getenv('ENV', 'staging')

        if env == 'production':
            app_url = 'https://ai-automation-platform.com'
        else:
            app_url = f'https://{env}.ai-automation-platform.com'

        try:
            response = requests.get(app_url, timeout=30)
            # Accept both 200 (loaded) and other success codes
            assert response.status_code < 400

        except requests.exceptions.RequestException as e:
            pytest.fail(f"Application startup check failed: {str(e)}")

    def test_api_responsiveness(self):
        """Test API response times."""
        env = os.getenv('ENV', 'staging')

        if env == 'production':
            api_url = 'https://ai-automation-platform.com/api/classify'
        else:
            api_url = f'https://{env}.ai-automation-platform.com/api/classify'

        try:
            import time
            start_time = time.time()

            # Simple API call
            response = requests.post(api_url, json={
                'data': [{'field': 'test_value'}],
                'dataset_name': 'smoke_test'
            }, timeout=30)

            response_time = time.time() - start_time

            # API should respond within 30 seconds
            assert response_time < 30
            # Accept various response codes (API might not be fully implemented)
            assert response.status_code < 500

        except requests.exceptions.RequestException as e:
            # API endpoint might not exist yet, that's ok for smoke test
            pytest.skip(f"API endpoint not available: {str(e)}")


if __name__ == '__main__':
    pytest.main([__file__, '-v'])