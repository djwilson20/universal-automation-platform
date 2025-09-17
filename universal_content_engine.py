"""
Universal Content Engine
Transforms classified data into presentation-ready business content
Format-agnostic output for PowerPoint, web presentations, or reports
"""

import json
import pandas as pd
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enhanced_classifier import AIDataClassifier, DataSensitivity, DataType

@dataclass
class SlideContent:
    title: str
    subtitle: str
    content_type: str  # 'text', 'chart', 'table', 'bullet_points'
    content: Any
    speaker_notes: str
    priority: int  # 1-5, for ordering slides

@dataclass
class ChartData:
    chart_type: str  # 'pie', 'bar', 'line', 'donut'
    title: str
    data: Dict[str, Any]
    description: str

@dataclass
class PresentationStructure:
    title: str
    subtitle: str
    executive_summary: str
    slides: List[SlideContent]
    appendix_data: Dict[str, Any]
    metadata: Dict[str, Any]

class BusinessNarrativeEngine:
    """Generates business-focused narrative content from classification data"""
    
    def __init__(self):
        self.risk_messaging = {
            DataSensitivity.TOP_SECRET: {
                'urgency': 'CRITICAL',
                'action_required': 'Immediate tokenization and access restriction',
                'business_impact': 'High regulatory and compliance risk'
            },
            DataSensitivity.RESTRICTED: {
                'urgency': 'HIGH',
                'action_required': 'Encryption and controlled access implementation',
                'business_impact': 'Moderate regulatory risk, potential data breach exposure'
            },
            DataSensitivity.CONFIDENTIAL: {
                'urgency': 'MEDIUM',
                'action_required': 'Selective masking and access controls',
                'business_impact': 'Standard security measures required'
            },
            DataSensitivity.INTERNAL: {
                'urgency': 'LOW',
                'action_required': 'Internal access controls sufficient',
                'business_impact': 'Minimal additional security requirements'
            },
            DataSensitivity.PUBLIC: {
                'urgency': 'NONE',
                'action_required': 'Standard handling procedures',
                'business_impact': 'No additional security measures needed'
            }
        }

    def generate_executive_summary(self, classification_results: Dict) -> str:
        """Generate executive-level summary focusing on business impact"""
        
        total_fields = classification_results['executive_summary']['total_fields']
        high_risk_count = classification_results['executive_summary']['high_risk_count']
        automation_ready = classification_results['executive_summary']['automation_ready_count']
        avg_confidence = classification_results['executive_summary']['average_confidence']
        
        # Calculate automation potential
        automation_percentage = (automation_ready / total_fields) * 100
        manual_reduction = f"{automation_percentage:.0f}%"
        
        # Risk assessment
        risk_level = "HIGH" if high_risk_count > total_fields * 0.3 else "MEDIUM" if high_risk_count > 0 else "LOW"
        
        summary = f"""
Our analysis of {total_fields} data fields reveals significant opportunities for process automation while maintaining appropriate security controls.

KEY FINDINGS:
• {automation_ready} of {total_fields} fields ({manual_reduction}) are ready for immediate automation
• {high_risk_count} fields require enhanced security measures before processing
• Overall data classification confidence: {avg_confidence:.0%}
• Risk profile: {risk_level} - appropriate controls identified

BUSINESS IMPACT:
• Potential reduction in manual data processing: {manual_reduction}
• Enhanced compliance through automated security classification
• Improved data governance and audit capabilities
• Foundation established for scalable automation workflows

RECOMMENDED ACTIONS:
• Implement automated processing for low-risk, high-confidence fields
• Deploy security measures for sensitive data categories
• Establish governance framework for ongoing data classification
• Begin pilot automation program with identified safe data sets
"""
        return summary.strip()

    def generate_risk_narrative(self, field_classifications: Dict) -> str:
        """Generate business-focused risk assessment narrative"""
        
        risk_counts = {}
        high_risk_fields = []
        
        for field_name, field_data in field_classifications.items():
            sensitivity = field_data['sensitivity_level']
            risk_counts[sensitivity] = risk_counts.get(sensitivity, 0) + 1
            
            if sensitivity in ['TOP_SECRET', 'RESTRICTED']:
                high_risk_fields.append({
                    'field': field_name,
                    'type': field_data['data_type'],
                    'action': field_data['recommended_action']
                })
        
        narrative = "RISK ASSESSMENT SUMMARY:\n\n"
        
        if risk_counts.get('TOP_SECRET', 0) > 0:
            narrative += f"• {risk_counts['TOP_SECRET']} fields classified as TOP SECRET require immediate attention\n"
            narrative += "  - These contain highly sensitive data (SSN, credit cards, etc.)\n"
            narrative += "  - Immediate tokenization and access restriction required\n\n"
        
        if risk_counts.get('RESTRICTED', 0) > 0:
            narrative += f"• {risk_counts['RESTRICTED']} fields classified as RESTRICTED need enhanced security\n"
            narrative += "  - Contains personal or financial information\n"
            narrative += "  - Encryption and controlled access implementation required\n\n"
        
        if risk_counts.get('CONFIDENTIAL', 0) > 0:
            narrative += f"• {risk_counts['CONFIDENTIAL']} fields require standard security measures\n"
            narrative += "  - Selective masking and access controls sufficient\n\n"
        
        if high_risk_fields:
            narrative += "PRIORITY FIELDS REQUIRING IMMEDIATE ACTION:\n"
            for field in high_risk_fields[:5]:  # Top 5 most critical
                narrative += f"• {field['field']}: {field['action']}\n"
        
        return narrative

    def generate_automation_opportunities(self, field_classifications: Dict) -> str:
        """Generate narrative about automation opportunities"""
        
        automation_ready = []
        manual_review_needed = []
        
        for field_name, field_data in field_classifications.items():
            if field_data['automation_ready']:
                automation_ready.append({
                    'field': field_name,
                    'type': field_data['data_type'],
                    'confidence': field_data['confidence_score']
                })
            else:
                manual_review_needed.append(field_name)
        
        narrative = f"AUTOMATION READINESS ASSESSMENT:\n\n"
        narrative += f"• {len(automation_ready)} fields identified as safe for immediate automation\n"
        narrative += f"• {len(manual_review_needed)} fields require manual review before automation\n\n"
        
        if automation_ready:
            narrative += "RECOMMENDED FOR AUTOMATION:\n"
            for field in sorted(automation_ready, key=lambda x: x['confidence'], reverse=True)[:10]:
                narrative += f"• {field['field']} ({field['type']}) - Confidence: {field['confidence']:.0%}\n"
        
        narrative += f"\nESTIMATED MANUAL WORK REDUCTION: {len(automation_ready)/len(field_classifications)*100:.0f}%"
        
        return narrative

class ChartGenerator:
    """Generates chart data for visualization in presentations"""
    
    @staticmethod
    def create_risk_distribution_chart(field_classifications: Dict) -> ChartData:
        """Create risk distribution pie chart data"""
        
        risk_counts = {}
        for field_data in field_classifications.values():
            sensitivity = field_data['sensitivity_level']
            risk_counts[sensitivity] = risk_counts.get(sensitivity, 0) + 1
        
        chart_data = {
            'labels': list(risk_counts.keys()),
            'values': list(risk_counts.values()),
            'colors': {
                'TOP_SECRET': '#FF4444',
                'RESTRICTED': '#FF8800',
                'CONFIDENTIAL': '#FFBB00',
                'INTERNAL': '#88BB00',
                'PUBLIC': '#00BB44'
            }
        }
        
        return ChartData(
            chart_type='pie',
            title='Data Security Risk Distribution',
            data=chart_data,
            description=f'Distribution of {sum(risk_counts.values())} fields across security risk levels'
        )
    
    @staticmethod
    def create_automation_readiness_chart(field_classifications: Dict) -> ChartData:
        """Create automation readiness chart data"""
        
        ready_count = sum(1 for f in field_classifications.values() if f['automation_ready'])
        not_ready_count = len(field_classifications) - ready_count
        
        chart_data = {
            'labels': ['Ready for Automation', 'Requires Manual Review'],
            'values': [ready_count, not_ready_count],
            'colors': {
                'Ready for Automation': '#00BB44',
                'Requires Manual Review': '#FF8800'
            }
        }
        
        return ChartData(
            chart_type='donut',
            title='Automation Readiness Assessment',
            data=chart_data,
            description=f'{ready_count} of {len(field_classifications)} fields ready for automation'
        )
    
    @staticmethod
    def create_confidence_distribution_chart(field_classifications: Dict) -> ChartData:
        """Create confidence score distribution chart"""
        
        confidence_ranges = {
            'High (80-100%)': 0,
            'Medium (60-79%)': 0,
            'Low (40-59%)': 0,
            'Very Low (0-39%)': 0
        }
        
        for field_data in field_classifications.values():
            confidence = field_data['confidence_score']
            if confidence >= 0.8:
                confidence_ranges['High (80-100%)'] += 1
            elif confidence >= 0.6:
                confidence_ranges['Medium (60-79%)'] += 1
            elif confidence >= 0.4:
                confidence_ranges['Low (40-59%)'] += 1
            else:
                confidence_ranges['Very Low (0-39%)'] += 1
        
        chart_data = {
            'labels': list(confidence_ranges.keys()),
            'values': list(confidence_ranges.values()),
            'colors': {
                'High (80-100%)': '#00BB44',
                'Medium (60-79%)': '#88BB00',
                'Low (40-59%)': '#FFBB00',
                'Very Low (0-39%)': '#FF8800'
            }
        }
        
        return ChartData(
            chart_type='bar',
            title='Classification Confidence Distribution',
            data=chart_data,
            description='Distribution of confidence scores across all classified fields'
        )

class UniversalContentEngine:
    """Main engine that orchestrates content generation"""
    
    def __init__(self):
        self.narrative_engine = BusinessNarrativeEngine()
        self.chart_generator = ChartGenerator()
    
    def generate_presentation_content(self, classification_file: str, 
                                    presentation_title: str = "Data Classification Analysis",
                                    company_context: str = "Internal Analysis") -> PresentationStructure:
        """Generate complete presentation content from classification results"""
        
        # Load classification results
        with open(classification_file, 'r') as f:
            classification_data = json.load(f)
        
        field_classifications = classification_data['field_classifications']
        executive_summary_data = classification_data['executive_summary']
        
        # Generate narrative content
        exec_summary = self.narrative_engine.generate_executive_summary(classification_data)
        risk_narrative = self.narrative_engine.generate_risk_narrative(field_classifications)
        automation_narrative = self.narrative_engine.generate_automation_opportunities(field_classifications)
        
        # Generate charts
        risk_chart = self.chart_generator.create_risk_distribution_chart(field_classifications)
        automation_chart = self.chart_generator.create_automation_readiness_chart(field_classifications)
        confidence_chart = self.chart_generator.create_confidence_distribution_chart(field_classifications)
        
        # Create slides
        slides = []
        
        # Title slide
        slides.append(SlideContent(
            title=presentation_title,
            subtitle=f"{company_context} • {datetime.now().strftime('%B %Y')}",
            content_type='text',
            content=f"Automated analysis of {executive_summary_data['total_fields']} data fields",
            speaker_notes="Opening slide - introduce the scope and purpose of the analysis",
            priority=1
        ))
        
        # Executive summary slide
        slides.append(SlideContent(
            title="Executive Summary",
            subtitle="Key Findings and Business Impact",
            content_type='text',
            content=exec_summary,
            speaker_notes="Focus on business value and automation opportunities",
            priority=2
        ))
        
        # Risk distribution chart
        slides.append(SlideContent(
            title="Security Risk Assessment",
            subtitle="Distribution of Data Sensitivity Levels",
            content_type='chart',
            content=asdict(risk_chart),
            speaker_notes="Highlight any high-risk areas that need immediate attention",
            priority=3
        ))
        
        # Automation readiness chart
        slides.append(SlideContent(
            title="Automation Opportunities",
            subtitle="Fields Ready for Automated Processing",
            content_type='chart',
            content=asdict(automation_chart),
            speaker_notes="Emphasize the potential for manual work reduction",
            priority=4
        ))
        
        # Risk details slide
        slides.append(SlideContent(
            title="Risk Assessment Details",
            subtitle="Priority Areas and Required Actions",
            content_type='text',
            content=risk_narrative,
            speaker_notes="Detail the specific security measures needed",
            priority=5
        ))
        
        # Automation details slide
        slides.append(SlideContent(
            title="Automation Implementation Plan",
            subtitle="Recommended Fields and Expected Impact",
            content_type='text',
            content=automation_narrative,
            speaker_notes="Present the roadmap for automation deployment",
            priority=6
        ))
        
        # Confidence analysis
        slides.append(SlideContent(
            title="Analysis Quality Assessment",
            subtitle="Classification Confidence Levels",
            content_type='chart',
            content=asdict(confidence_chart),
            speaker_notes="Address any low-confidence areas that may need manual review",
            priority=7
        ))
        
        # Field details table (appendix style)
        field_details = []
        for field_name, field_data in field_classifications.items():
            field_details.append({
                'Field Name': field_name,
                'Data Type': field_data['data_type'],
                'Risk Level': field_data['sensitivity_level'],
                'Confidence': f"{field_data['confidence_score']:.0%}",
                'Automation Ready': 'Yes' if field_data['automation_ready'] else 'No',
                'Recommended Action': field_data['recommended_action'][:50] + '...' if len(field_data['recommended_action']) > 50 else field_data['recommended_action']
            })
        
        slides.append(SlideContent(
            title="Detailed Field Analysis",
            subtitle="Complete Classification Results",
            content_type='table',
            content={'headers': list(field_details[0].keys()), 'rows': field_details},
            speaker_notes="Reference slide - detailed breakdown of all classified fields",
            priority=8
        ))
        
        # Create presentation structure
        presentation = PresentationStructure(
            title=presentation_title,
            subtitle=f"{company_context} - Data Classification Analysis",
            executive_summary=exec_summary,
            slides=slides,
            appendix_data={
                'full_classification_data': classification_data,
                'generation_timestamp': datetime.now().isoformat(),
                'field_count': len(field_classifications)
            },
            metadata={
                'generated_by': 'Universal Content Engine v1.0',
                'source_file': classification_file,
                'slide_count': len(slides),
                'company_context': company_context
            }
        )
        
        return presentation
    
    def export_presentation_content(self, presentation: PresentationStructure, 
                                   output_file: str = "presentation_content.json") -> str:
        """Export presentation content to JSON for use with any presentation tool"""
        
        # Convert presentation to dictionary
        presentation_dict = asdict(presentation)
        
        # Add formatting hints for different output types
        presentation_dict['formatting_hints'] = {
            'powerpoint': {
                'slide_dimensions': '16:9',
                'font_family': 'Calibri',
                'title_size': 44,
                'content_size': 24,
                'color_scheme': 'corporate'
            },
            'web_presentation': {
                'framework': 'reveal.js',
                'theme': 'white',
                'transition': 'slide'
            },
            'pdf_report': {
                'page_size': 'letter',
                'margins': '1 inch',
                'font_family': 'Arial'
            }
        }
        
        # Save to file
        with open(output_file, 'w') as f:
            json.dump(presentation_dict, f, indent=2)
        
        return output_file

def main():
    """Demonstration of the Universal Content Engine"""
    
    print("Universal Content Engine - Presentation Generator")
    print("=" * 50)
    
    # Check if we have classification results
    try:
        # First, generate some classification data if it doesn't exist
        from enhanced_classifier import create_test_data
        
        classifier = AIDataClassifier()
        test_data = create_test_data()
        
        print("Generating fresh classification data...")
        results = classifier.classify_dataset(test_data, "customer_financial_data")
        classification_file = classifier.export_for_powerpoint(results, "sample_classification.json")
        print(f"Classification data saved to: {classification_file}")
        
    except FileNotFoundError:
        print("Error: No classification data found. Please run the enhanced_classifier.py first.")
        return
    
    # Generate presentation content
    print("\nGenerating presentation content...")
    content_engine = UniversalContentEngine()
    
    presentation = content_engine.generate_presentation_content(
        classification_file="sample_classification.json",
        presentation_title="Customer Data Security Analysis",
        company_context="Operations Team Analysis"
    )
    
    # Export presentation content
    output_file = content_engine.export_presentation_content(presentation)
    print(f"Presentation content exported to: {output_file}")
    
    # Summary
    print(f"\nContent Generation Complete!")
    print(f"• Generated {len(presentation.slides)} slides")
    print(f"• Analyzed {len(presentation.appendix_data['full_classification_data']['field_classifications'])} data            fields")
    print(f"• Ready for import into PowerPoint, Google Slides, or web presentation")
    print(f"• Structured content available in: {output_file}")
    
    # Show slide titles
    print(f"\nGenerated Slide Structure:")
    for i, slide in enumerate(presentation.slides, 1):
        print(f"{i}. {slide.title}")
    
    return output_file

if __name__ == "__main__":
    main()