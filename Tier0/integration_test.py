#!/usr/bin/env python3
"""
Comprehensive Integration Test
Tests all components working together
"""

import pandas as pd
import numpy as np
import sys
import os
import traceback

# Add current directory to path
sys.path.append('/home/djwil/tier0_app.py')

def test_data_analysis():
    """Test core data analysis functionality"""
    print("\n📊 Testing Core Data Analysis...")

    try:
        from app_english import EnterpriseAIAnalytics

        # Create test data
        df = pd.DataFrame({
            'Revenue': np.random.randint(10000, 50000, 100),
            'Cost': np.random.randint(5000, 30000, 100),
            'Region': np.random.choice(['North', 'South', 'East', 'West'], 100),
            'Product': np.random.choice(['A', 'B', 'C'], 100),
            'Date': pd.date_range('2024-01-01', periods=100)
        })

        analytics = EnterpriseAIAnalytics()

        # Test industry detection
        industry_result = analytics.detect_industry_pattern(df)
        print(f"✅ Industry detection: {industry_result}")

        # Test anomaly detection
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            anomaly_result, _ = analytics.advanced_anomaly_detection(df, numeric_cols)
            if anomaly_result:
                print(f"✅ Anomaly detection: Found {len(anomaly_result.get('indices', []))} anomalies")
            else:
                print("✅ Anomaly detection: No anomalies detected")

        # Test executive summary generation
        analysis_results = {'industry': industry_result}
        executive_summary = analytics.generate_executive_summary(df, analysis_results, industry_result['pattern'])
        print(f"✅ Executive summary generated: {len(executive_summary['key_findings'])} findings")

        return True

    except Exception as e:
        print(f"❌ Data analysis test failed: {e}")
        traceback.print_exc()
        return False

def test_powerpoint_generation():
    """Test PowerPoint generation functionality"""
    print("\n🎯 Testing PowerPoint Generation...")

    try:
        from german_corporate_powerpoint import create_german_corporate_powerpoint

        # Create test data
        df = pd.DataFrame({
            'Revenue': np.random.randint(10000, 50000, 50),
            'Cost': np.random.randint(5000, 30000, 50),
            'Region': np.random.choice(['North', 'South', 'East', 'West'], 50)
        })

        # Create mock analysis results
        analysis_results = {
            'industry': {'pattern': 'manufacturing', 'confidence': 0.85},
            'gdpr_assessment': {'compliance_score': 92, 'compliance_level': 'Excellent'},
            'executive_summary': {
                'header': {
                    'title': 'Test Analysis',
                    'industry': 'Manufacturing',
                    'timestamp': '22/09/2025'
                },
                'key_findings': [
                    "High data quality detected",
                    "Strong performance in South region",
                    "Product diversification opportunity"
                ],
                'strategic_recommendations': [
                    "Expand successful product lines",
                    "Optimize cost structure",
                    "Strengthen regional presence"
                ]
            }
        }

        # Test German corporate PowerPoint
        ppt_buffer = create_german_corporate_powerpoint(df, analysis_results)
        print(f"✅ German corporate PowerPoint generated: {len(ppt_buffer.getvalue())} bytes")

        return True

    except Exception as e:
        print(f"❌ PowerPoint generation test failed: {e}")
        traceback.print_exc()
        return False

def test_data_validation():
    """Test data validation functionality"""
    print("\n🔍 Testing Data Validation...")

    try:
        from app_english import validate_data

        # Test with good data
        good_data = pd.DataFrame({
            'A': [1, 2, 3, 4, 5],
            'B': ['a', 'b', 'c', 'd', 'e'],
            'C': [1.1, 2.2, 3.3, 4.4, 5.5]
        })

        issues, recommendations, quality = validate_data(good_data)
        print(f"✅ Data validation (good data): Quality = {quality}")

        # Test with problematic data
        bad_data = pd.DataFrame({
            'A': [1, None, 3, None, 5],
            'B': ['a', 'b', 'a', 'b', 'a'],  # Duplicates
            'C': [None, None, None, None, None]  # All missing
        })

        issues, recommendations, quality = validate_data(bad_data)
        print(f"✅ Data validation (bad data): Quality = {quality}, Issues = {len(issues)}")

        # Test with empty data
        empty_data = pd.DataFrame()
        issues, recommendations, quality = validate_data(empty_data)
        print(f"✅ Data validation (empty data): Quality = {quality}")

        return True

    except Exception as e:
        print(f"❌ Data validation test failed: {e}")
        traceback.print_exc()
        return False

def test_imports():
    """Test all critical imports"""
    print("\n📦 Testing Critical Imports...")

    try:
        # Test main application imports
        import streamlit
        print("✅ Streamlit imported")

        import plotly.express
        import plotly.graph_objects
        print("✅ Plotly imported")

        import sklearn
        print("✅ Scikit-learn imported")

        from pptx import Presentation
        print("✅ python-pptx imported")

        # Test custom modules
        from app_english import EnterpriseAIAnalytics
        print("✅ EnterpriseAIAnalytics imported")

        from german_corporate_powerpoint import GermanCorporatePowerPoint
        print("✅ GermanCorporatePowerPoint imported")

        return True

    except Exception as e:
        print(f"❌ Import test failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Run comprehensive integration tests"""
    print("🧪 COMPREHENSIVE INTEGRATION TEST")
    print("=" * 50)

    tests = [
        ("Import Test", test_imports),
        ("Data Validation Test", test_data_validation),
        ("Data Analysis Test", test_data_analysis),
        ("PowerPoint Generation Test", test_powerpoint_generation)
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"\n🔄 Running {test_name}...")
        if test_func():
            passed += 1
            print(f"✅ {test_name} PASSED")
        else:
            print(f"❌ {test_name} FAILED")

    print("\n" + "=" * 50)
    print(f"📋 INTEGRATION TEST SUMMARY")
    print(f"✅ Passed: {passed}/{total}")
    print(f"❌ Failed: {total - passed}/{total}")

    if passed == total:
        print("🎉 ALL TESTS PASSED - System is ready for production!")
    else:
        print("⚠️ Some tests failed - Review errors above")

    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)