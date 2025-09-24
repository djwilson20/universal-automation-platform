#!/usr/bin/env python3
"""Test script for PowerPoint generation functionality"""

import pandas as pd
import sys
import os

# Add current directory to path
sys.path.append('/home/djwil/tier0_app.py')

try:
    from german_corporate_powerpoint import GermanCorporatePowerPoint
    print("✅ Successfully imported GermanCorporatePowerPoint")
except ImportError as e:
    print(f"❌ Failed to import GermanCorporatePowerPoint: {e}")
    sys.exit(1)

# Load test data
try:
    df = pd.read_csv('/home/djwil/tier0_app.py/test_data.csv')
    print(f"✅ Test data loaded: {len(df)} rows, {len(df.columns)} columns")
except Exception as e:
    print(f"❌ Failed to load test data: {e}")
    sys.exit(1)

# Test German Corporate PowerPoint Generation
print("\n🏢 Testing German Corporate PowerPoint Generation...")

try:
    ppt_generator = GermanCorporatePowerPoint()

    # Create mock analysis results
    analysis_results = {
        'industry': {'pattern': 'manufacturing', 'confidence': 0.85},
        'gdpr_assessment': {'compliance_score': 92, 'compliance_level': 'Excellent'},
        'executive_summary': {
            'key_findings': [
                "Hohe Datenqualität mit 95% Vollständigkeit",
                "Starke Leistung in Region Süd erkennbar",
                "Product C zeigt überdurchschnittliches Wachstum"
            ],
            'strategic_recommendations': [
                "Expansion der erfolgreichen Produkte",
                "Optimierung der Kostenbasis",
                "Verstärkung des Vertriebs in Kernregionen"
            ]
        }
    }

    # Test basic functionality
    presentation = ppt_generator.create_presentation(df, analysis_results)
    print("✅ Basic presentation created successfully")

    # Save test presentation
    output_path = "/home/djwil/tier0_app.py/test_corporate_presentation.pptx"
    presentation.save(output_path)
    print(f"✅ German Corporate PowerPoint saved to: {output_path}")

    # Check file size
    file_size = os.path.getsize(output_path) / 1024  # KB
    print(f"📊 File size: {file_size:.1f} KB")

except Exception as e:
    print(f"❌ German Corporate PowerPoint generation failed: {e}")
    import traceback
    traceback.print_exc()

print("\n🎉 PowerPoint generation test completed!")
print("\n📍 Application URLs:")
print("   • German Version: http://localhost:8503")
print("   • English Version: http://localhost:8505")
print("\n📁 Test files created:")
print("   • test_data.csv - Sample data for testing")
print("   • test_corporate_presentation.pptx - German corporate PowerPoint")