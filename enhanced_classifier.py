"""
Enhanced AI Data Classification Engine - Desktop Test Version
Clean, copy-safe implementation for your universal automation platform
"""

import pandas as pd
import numpy as np
import re
import json
from datetime import datetime
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Tuple, Any, Optional

class DataSensitivity(Enum):
    PUBLIC = 1
    INTERNAL = 2
    CONFIDENTIAL = 3
    RESTRICTED = 4
    TOP_SECRET = 5

class DataType(Enum):
    PII_NAME = "pii_name"
    PII_SSN = "pii_ssn"
    PII_EMAIL = "pii_email"
    PII_PHONE = "pii_phone"
    PII_ADDRESS = "pii_address"
    PII_DOB = "pii_date_of_birth"
    FINANCIAL_ACCOUNT = "financial_account"
    FINANCIAL_AMOUNT = "financial_amount"
    FINANCIAL_CREDIT_CARD = "financial_credit_card"
    EMPLOYEE_ID = "employee_id"
    CUSTOMER_ID = "customer_id"
    BUSINESS_METRIC = "business_metric"
    REVENUE_DATA = "revenue_data"
    DATE_BUSINESS = "date_business"
    CATEGORICAL_DATA = "categorical_data"
    NUMERIC_MEASUREMENT = "numeric_measurement"
    TEXT_DESCRIPTION = "text_description"
    UNKNOWN = "unknown"

@dataclass
class ClassificationResult:
    field_name: str
    data_type: DataType
    sensitivity: DataSensitivity
    confidence: float
    sample_values: List[str]
    patterns_detected: List[str]
    business_context: str
    recommended_action: str
    risk_factors: List[str]
    masking_strategy: str
    automation_ready: bool

class AIDataClassifier:
    def __init__(self):
        self.field_patterns = {
            DataType.PII_NAME: [r'\bnames?\b', r'\bfname\b', r'\blname\b'],
            DataType.PII_EMAIL: [r'\bemail\b', r'\bmail\b'],
            DataType.PII_SSN: [r'\bssn\b', r'\bsocial_security\b'],
            DataType.PII_PHONE: [r'\bphone\b', r'\btel\b', r'\bmobile\b'],
            DataType.PII_DOB: [r'\bbirth\b', r'\bdob\b'],
            DataType.FINANCIAL_ACCOUNT: [r'\baccount\b', r'\bacct\b'],
            DataType.FINANCIAL_CREDIT_CARD: [r'\bcard\b', r'\bcredit\b'],
            DataType.EMPLOYEE_ID: [r'\bemp\b', r'\bemployee_id\b'],
            DataType.CUSTOMER_ID: [r'\bcust\b', r'\bcustomer_id\b'],
            DataType.REVENUE_DATA: [r'\brevenue\b', r'\bsales\b', r'\bearnings\b']
        }
        
        self.content_patterns = {
            DataType.PII_SSN: r'\b\d{3}-?\d{2}-?\d{4}\b',
            DataType.PII_EMAIL: r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            DataType.PII_PHONE: r'\b\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b',
            DataType.FINANCIAL_CREDIT_CARD: r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b'
        }
        
        self.risk_levels = {
            DataType.PII_SSN: DataSensitivity.TOP_SECRET,
            DataType.FINANCIAL_CREDIT_CARD: DataSensitivity.TOP_SECRET,
            DataType.PII_NAME: DataSensitivity.CONFIDENTIAL,
            DataType.PII_EMAIL: DataSensitivity.CONFIDENTIAL,
            DataType.PII_PHONE: DataSensitivity.CONFIDENTIAL,
            DataType.FINANCIAL_ACCOUNT: DataSensitivity.RESTRICTED,
            DataType.FINANCIAL_AMOUNT: DataSensitivity.CONFIDENTIAL,
            DataType.EMPLOYEE_ID: DataSensitivity.INTERNAL,
            DataType.CUSTOMER_ID: DataSensitivity.INTERNAL,
            DataType.BUSINESS_METRIC: DataSensitivity.INTERNAL
        }
        
        self.masking_strategies = {
            DataType.PII_SSN: "Full tokenization (XXX-XX-1234)",
            DataType.PII_NAME: "First name + Last initial (John D.)",
            DataType.PII_EMAIL: "Username + masked domain (john****@****.com)",
            DataType.FINANCIAL_CREDIT_CARD: "Last 4 digits only (****-****-****-1234)",
            DataType.FINANCIAL_ACCOUNT: "Masked with checksum (****1234)",
            DataType.FINANCIAL_AMOUNT: "Range buckets ($1K-$5K)"
        }

    def classify_field(self, field_name: str, sample_values: List[Any]) -> ClassificationResult:
        # Analyze field name
        field_lower = field_name.lower()
        detected_type = DataType.UNKNOWN
        confidence = 0.1
        
        # Check field name patterns
        for data_type, patterns in self.field_patterns.items():
            for pattern in patterns:
                if re.search(pattern, field_lower):
                    detected_type = data_type
                    confidence = 0.9
                    break
            if confidence > 0.5:
                break
        
        # Check content patterns if field name didn't match
        if confidence < 0.5 and sample_values:
            sample_strings = [str(val) for val in sample_values[:10] if val is not None]
            for data_type, pattern in self.content_patterns.items():
                matches = sum(1 for val in sample_strings if re.search(pattern, str(val)))
                if matches > 0:
                    match_ratio = matches / len(sample_strings)
                    if match_ratio > 0.3:
                        detected_type = data_type
                        confidence = min(0.8, match_ratio * 1.5)
                        break
        
        # Heuristic analysis for numeric data
        if confidence < 0.5 and sample_values:
            if self.is_numeric_column(sample_values):
                if self.looks_like_id(sample_values):
                    detected_type = DataType.CUSTOMER_ID
                    confidence = 0.6
                elif self.looks_like_amount(sample_values):
                    detected_type = DataType.FINANCIAL_AMOUNT
                    confidence = 0.7
        
        # Get risk assessment
        sensitivity = self.risk_levels.get(detected_type, DataSensitivity.PUBLIC)
        
        # Determine automation readiness
        automation_ready = sensitivity.value <= DataSensitivity.INTERNAL.value and confidence > 0.6
        
        # Get masking strategy
        masking_strategy = self.masking_strategies.get(
            detected_type, "Apply appropriate masking based on business requirements"
        )
        
        # Generate patterns detected
        patterns = self.detect_patterns(sample_values)
        
        # Risk factors
        risk_factors = []
        if detected_type.value.startswith('pii'):
            risk_factors.append("Contains personally identifiable information")
        if detected_type.value.startswith('financial'):
            risk_factors.append("Contains financial data requiring protection")
        
        # Recommended action
        if sensitivity == DataSensitivity.TOP_SECRET:
            action = "IMMEDIATE TOKENIZATION - Replace with irreversible tokens"
        elif sensitivity == DataSensitivity.RESTRICTED:
            action = "ENCRYPTION REQUIRED - Encrypt at rest and in transit"
        elif sensitivity == DataSensitivity.CONFIDENTIAL:
            action = "SELECTIVE MASKING - Mask sensitive portions"
        elif sensitivity == DataSensitivity.INTERNAL:
            action = "ACCESS CONTROL - Restrict to internal personnel"
        else:
            action = "STANDARD HANDLING - No special security measures required"
        
        return ClassificationResult(
            field_name=field_name,
            data_type=detected_type,
            sensitivity=sensitivity,
            confidence=confidence,
            sample_values=[str(v)[:50] for v in (sample_values[:3] if sample_values else [])],
            patterns_detected=patterns,
            business_context="general",
            recommended_action=action,
            risk_factors=risk_factors,
            masking_strategy=masking_strategy,
            automation_ready=automation_ready
        )

    def is_numeric_column(self, values: List[Any]) -> bool:
        if not values:
            return False
        numeric_count = 0
        total_count = 0
        for val in values:
            if val is not None:
                total_count += 1
                try:
                    float(str(val).replace(',', '').replace('$', ''))
                    numeric_count += 1
                except:
                    pass
        return numeric_count / max(total_count, 1) > 0.8

    def looks_like_id(self, values: List[Any]) -> bool:
        try:
            numeric_vals = []
            for val in values:
                if val is not None:
                    try:
                        numeric_vals.append(float(str(val).replace(',', '')))
                    except:
                        continue
            if len(numeric_vals) < 2:
                return False
            are_integers = all(val == int(val) for val in numeric_vals)
            unique_ratio = len(set(numeric_vals)) / len(numeric_vals)
            return are_integers and unique_ratio > 0.9
        except:
            return False

    def looks_like_amount(self, values: List[Any]) -> bool:
        try:
            numeric_vals = []
            for val in values:
                if val is not None:
                    try:
                        clean_val = str(val).replace('$', '').replace(',', '').strip()
                        numeric_vals.append(float(clean_val))
                    except:
                        continue
            if len(numeric_vals) < 2:
                return False
            has_decimals = any(val != int(val) for val in numeric_vals)
            reasonable_range = all(-1000000 <= val <= 100000000 for val in numeric_vals)
            return reasonable_range
        except:
            return False

    def detect_patterns(self, values: List[Any]) -> List[str]:
        if not values:
            return ["No values to analyze"]
        
        patterns = []
        str_values = [str(v) for v in values if v is not None]
        
        # Length analysis
        lengths = [len(s) for s in str_values]
        if len(set(lengths)) == 1:
            patterns.append(f"Fixed length: {lengths[0]} characters")
        else:
            patterns.append(f"Length range: {min(lengths)}-{max(lengths)} characters")
        
        # Uniqueness analysis
        unique_ratio = len(set(str_values)) / len(str_values)
        if unique_ratio == 1.0:
            patterns.append("All values unique (likely identifier)")
        elif unique_ratio < 0.2:
            patterns.append("Low uniqueness (likely categorical)")
        else:
            patterns.append(f"Moderate uniqueness ({unique_ratio:.1%} unique)")
        
        return patterns

    def classify_dataset(self, df: pd.DataFrame, dataset_name: str = "unknown") -> Dict[str, ClassificationResult]:
        print(f"Starting classification of dataset: {dataset_name}")
        print(f"Dataset shape: {df.shape[0]} rows, {df.shape[1]} columns")
        
        results = {}
        
        for column in df.columns:
            sample_values = df[column].dropna().head(20).tolist()
            result = self.classify_field(column, sample_values)
            results[column] = result
            print(f"Classified {column}: {result.data_type.value} (confidence: {result.confidence:.2f})")
        
        return results

    def generate_executive_summary(self, results: Dict[str, ClassificationResult]) -> str:
        total_fields = len(results)
        high_risk_fields = sum(1 for r in results.values() 
                              if r.sensitivity.value >= DataSensitivity.CONFIDENTIAL.value)
        automation_ready = sum(1 for r in results.values() if r.automation_ready)
        avg_confidence = np.mean([r.confidence for r in results.values()])
        
        risk_dist = {}
        for result in results.values():
            risk_level = result.sensitivity.name
            risk_dist[risk_level] = risk_dist.get(risk_level, 0) + 1
        
        summary = f"""
=== EXECUTIVE DATA CLASSIFICATION SUMMARY ===
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

DATASET OVERVIEW:
• Total Fields Analyzed: {total_fields}
• Analysis Confidence: {avg_confidence:.1%}

SECURITY ASSESSMENT:
• High-Risk Fields: {high_risk_fields} ({high_risk_fields/total_fields:.1%})
• Fields Ready for Automation: {automation_ready} ({automation_ready/total_fields:.1%})
• Manual Review Required: {total_fields - automation_ready}

RISK DISTRIBUTION:
"""
        
        for risk_level, count in sorted(risk_dist.items()):
            percentage = count / total_fields * 100
            summary += f"• {risk_level}: {count} fields ({percentage:.1f}%)\n"
        
        summary += f"""
KEY RECOMMENDATIONS:
• Implement immediate tokenization for {risk_dist.get('TOP_SECRET', 0)} top-secret fields
• Apply encryption for {risk_dist.get('RESTRICTED', 0)} restricted fields
• Enable automation for {automation_ready} fields to reduce manual processing
• Estimated manual work reduction: {automation_ready/total_fields:.1%}

BUSINESS IMPACT:
• Data processing can be partially automated
• Security measures tailored to actual risk levels
• Foundation ready for PowerPoint automation integration
"""
        
        return summary

    def export_for_powerpoint(self, results: Dict[str, ClassificationResult], 
                             filename: str = "classification_for_ppt.json") -> str:
        export_data = {
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'total_fields': len(results),
                'ready_for_automation': True
            },
            'executive_summary': {
                'total_fields': len(results),
                'high_risk_count': sum(1 for r in results.values() 
                                     if r.sensitivity.value >= DataSensitivity.CONFIDENTIAL.value),
                'automation_ready_count': sum(1 for r in results.values() if r.automation_ready),
                'average_confidence': float(np.mean([r.confidence for r in results.values()]))
            },
            'field_classifications': {}
        }
        
        for field_name, result in results.items():
            export_data['field_classifications'][field_name] = {
                'data_type': result.data_type.value,
                'sensitivity_level': result.sensitivity.name,
                'confidence_score': result.confidence,
                'automation_ready': result.automation_ready,
                'recommended_action': result.recommended_action,
                'masking_strategy': result.masking_strategy,
                'risk_factors': result.risk_factors
            }
        
        with open(filename, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        return filename

def create_test_data():
    return pd.DataFrame({
        'customer_id': [10001, 10002, 10003, 10004, 10005],
        'customer_name': ['John Smith', 'Sarah Johnson', 'Michael Brown', 'Lisa Davis', 'Robert Wilson'],
        'email_address': ['john.smith@email.com', 'sarah.j@company.com', 'mbrown@test.org', 'lisa.davis@work.net', 'rwilson@example.com'],
        'phone_number': ['555-123-4567', '555-987-6543', '555-555-1234', '555-777-8888', '555-999-0000'],
        'ssn': ['123-45-6789', '987-65-4321', '555-44-3333', '111-22-4444', '999-88-7777'],
        'date_of_birth': ['1985-03-15', '1992-07-22', '1978-11-08', '1990-05-13', '1988-09-30'],
        'account_balance': [15000.50, 27500.25, 8900.00, 45000.75, 12300.00],
        'credit_score': [720, 685, 750, 640, 695],
        'account_type': ['Checking', 'Savings', 'Checking', 'Premium', 'Checking'],
        'last_transaction_date': ['2024-01-15', '2024-01-14', '2024-01-13', '2024-01-12', '2024-01-11']
    })

if __name__ == "__main__":
    print("AI Data Classification Engine - Enhanced Desktop Version")
    print("=" * 60)
    
    # Initialize classifier
    classifier = AIDataClassifier()
    
    # Load test data
    print("Loading test dataset...")
    test_data = create_test_data()
    print(f"Dataset loaded: {test_data.shape[0]} rows, {test_data.shape[1]} columns")
    print()
    
    # Run classification
    print("Running AI classification...")
    results = classifier.classify_dataset(test_data, "customer_financial_data")
    print()
    
    # Generate executive summary
    print("=" * 60)
    print("EXECUTIVE SUMMARY")
    print("=" * 60)
    summary = classifier.generate_executive_summary(results)
    print(summary)
    
    # Export for PowerPoint automation
    print("Exporting results for PowerPoint automation...")
    export_file = classifier.export_for_powerpoint(results)
    print(f"Results exported to: {export_file}")
    print("Ready for integration with PowerPoint automation system!")
    
    print(f"\nClassification complete! Analyzed {len(results)} fields.")
    print("Your proprietary AI classification engine is working!")