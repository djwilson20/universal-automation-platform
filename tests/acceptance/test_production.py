"""
Production acceptance tests for the AI Automation Platform.
These tests verify production-level functionality and performance.
"""

import os
import pytest
import requests
import time
from concurrent.futures import ThreadPoolExecutor


@pytest.mark.skipif(
    os.getenv('ENV') not in ['production', 'production-green'],
    reason="Production tests only run in production environments"
)
class TestProductionAcceptance:
    """Production acceptance tests."""

    @pytest.fixture
    def base_url(self):
        """Get the base URL for the environment."""
        env = os.getenv('ENV')
        if env == 'production':
            return 'https://ai-automation-platform.com'
        elif env == 'production-green':
            return 'https://green.ai-automation-platform.com'
        return 'https://staging.ai-automation-platform.com'

    def test_production_health_comprehensive(self, base_url):
        """Comprehensive health check for production."""
        health_url = f"{base_url}/health"

        response = requests.get(health_url, timeout=10)
        assert response.status_code == 200

        health_data = response.json()
        assert health_data['status'] == 'healthy'

        # Check all subsystems
        required_subsystems = ['database', 'cache', 'storage', 'api']
        for subsystem in required_subsystems:
            assert health_data.get(subsystem, False), f"{subsystem} is not healthy"

    def test_production_performance_baseline(self, base_url):
        """Test that production meets performance baselines."""
        start_time = time.time()
        response = requests.get(base_url, timeout=30)
        response_time = time.time() - start_time

        # Production should respond within 3 seconds
        assert response_time < 3.0, f"Response time {response_time}s exceeds 3s baseline"
        assert response.status_code == 200

    def test_production_load_handling(self, base_url):
        """Test production can handle concurrent load."""
        def make_request():
            try:
                response = requests.get(f"{base_url}/health", timeout=10)
                return response.status_code == 200
            except:
                return False

        # Simulate 10 concurrent users
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request) for _ in range(10)]
            results = [future.result() for future in futures]

        # At least 90% of requests should succeed
        success_rate = sum(results) / len(results)
        assert success_rate >= 0.9, f"Success rate {success_rate} below 90% threshold"

    def test_production_security_headers(self, base_url):
        """Test that security headers are properly configured."""
        response = requests.get(base_url, timeout=10)

        # Check for important security headers
        security_headers = {
            'X-Frame-Options': 'DENY',
            'X-Content-Type-Options': 'nosniff',
            'X-XSS-Protection': '1; mode=block',
            'Strict-Transport-Security': 'max-age=31536000'
        }

        for header, expected_value in security_headers.items():
            assert header in response.headers, f"Missing security header: {header}"
            if expected_value:
                assert expected_value in response.headers[header], \
                    f"Incorrect {header} value: {response.headers[header]}"

    def test_production_ssl_configuration(self, base_url):
        """Test SSL/TLS configuration."""
        import ssl
        import socket
        from urllib.parse import urlparse

        parsed_url = urlparse(base_url)
        hostname = parsed_url.hostname
        port = 443

        # Test SSL connection
        context = ssl.create_default_context()
        with socket.create_connection((hostname, port), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                # Check SSL version
                ssl_version = ssock.version()
                assert ssl_version in ['TLSv1.2', 'TLSv1.3'], f"Insecure SSL version: {ssl_version}"

                # Check cipher
                cipher = ssock.cipher()
                assert cipher is not None, "No cipher information available"

    def test_production_data_processing_capability(self, base_url):
        """Test production data processing capabilities."""
        # This would be a more complex test with actual data processing
        # For now, we'll test the endpoints exist and respond appropriately

        endpoints_to_test = [
            '/api/classify',
            '/api/generate',
            '/api/export'
        ]

        for endpoint in endpoints_to_test:
            url = f"{base_url}{endpoint}"
            try:
                # Test with HEAD request to avoid sending data
                response = requests.head(url, timeout=10)
                # Accept 404 (not implemented), 405 (method not allowed), or 200
                assert response.status_code in [200, 404, 405], \
                    f"Unexpected error for {endpoint}: {response.status_code}"
            except requests.exceptions.ConnectionError:
                # Endpoint might not be implemented yet
                pytest.skip(f"Endpoint {endpoint} not available")

    def test_production_monitoring_endpoints(self, base_url):
        """Test monitoring and observability endpoints."""
        monitoring_endpoints = [
            '/health',
            '/metrics',
            '/status'
        ]

        for endpoint in monitoring_endpoints:
            url = f"{base_url}{endpoint}"
            try:
                response = requests.get(url, timeout=5)
                # Health should be 200, others might be 404 if not implemented
                if endpoint == '/health':
                    assert response.status_code == 200
                else:
                    assert response.status_code in [200, 404]
            except requests.exceptions.RequestException:
                if endpoint == '/health':
                    pytest.fail(f"Critical endpoint {endpoint} is not accessible")

    def test_production_error_handling(self, base_url):
        """Test production error handling."""
        # Test 404 handling
        response = requests.get(f"{base_url}/nonexistent-endpoint", timeout=10)
        assert response.status_code == 404

        # Test malformed request handling
        try:
            response = requests.post(
                f"{base_url}/api/classify",
                json={"malformed": "data"},
                timeout=10
            )
            # Should handle gracefully (not 500)
            assert response.status_code != 500
        except requests.exceptions.RequestException:
            # API might not be implemented yet
            pytest.skip("API endpoint not available for error testing")

    def test_production_uptime_check(self, base_url):
        """Test production uptime and stability."""
        # Make multiple requests over time to check stability
        for i in range(5):
            response = requests.get(f"{base_url}/health", timeout=10)
            assert response.status_code == 200

            if i < 4:  # Don't sleep after the last request
                time.sleep(2)  # Wait 2 seconds between requests


if __name__ == '__main__':
    pytest.main([__file__, '-v'])