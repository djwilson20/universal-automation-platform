#!/usr/bin/env python3
"""
Workflow Analysis Tool - Test the structure without external dependencies
Analyzes the universal automation platform codebase for quality issues
"""

import json
import re
import os
from typing import List, Dict, Any

class CodeQualityAnalyzer:
    """Analyzes code quality without requiring external dependencies"""

    def __init__(self):
        self.issues = []
        self.file_analysis = {}

    def analyze_file_structure(self, root_dir: str = ".") -> Dict[str, Any]:
        """Analyze repository file structure"""
        structure = {
            'total_files': 0,
            'python_files': 0,
            'test_files': 0,
            'doc_files': 0,
            'config_files': 0,
            'missing_files': [],
            'file_sizes': {}
        }

        expected_files = [
            'README.md',
            'requirements.txt',
            'src/__init__.py',
            'src/enhanced_classifier.py',
            'src/universal_content_engine.py',
            'src/sap_powerpoint_generator.py',
            'tests/__init__.py',
            'tests/test_classifier.py'
        ]

        # Check for expected files
        for expected_file in expected_files:
            file_path = os.path.join(root_dir, expected_file)
            if os.path.exists(file_path):
                structure['file_sizes'][expected_file] = os.path.getsize(file_path)
            else:
                structure['missing_files'].append(expected_file)

        # Count files by type
        for root, dirs, files in os.walk(root_dir):
            if '/.git' in root:
                continue

            for file in files:
                structure['total_files'] += 1

                if file.endswith('.py'):
                    structure['python_files'] += 1
                elif file.startswith('test_') or '/tests/' in root:
                    structure['test_files'] += 1
                elif file.endswith(('.md', '.txt', '.rst')):
                    structure['doc_files'] += 1
                elif file.endswith(('.json', '.yml', '.yaml', '.ini', '.cfg')):
                    structure['config_files'] += 1

        return structure

    def analyze_code_quality(self, file_path: str) -> Dict[str, Any]:
        """Analyze a Python file for quality issues"""

        if not os.path.exists(file_path):
            return {'error': f'File not found: {file_path}'}

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            return {'error': f'Cannot read file: {e}'}

        analysis = {
            'file_path': file_path,
            'line_count': len(content.split('\n')),
            'char_count': len(content),
            'issues': [],
            'metrics': {}
        }

        lines = content.split('\n')

        # Check for common quality issues
        issues = []

        # 1. Very long lines (over 120 characters)
        long_lines = []
        for i, line in enumerate(lines):
            if len(line) > 120:
                long_lines.append(f"Line {i+1}: {len(line)} chars")
        if long_lines:
            issues.append({
                'type': 'long_lines',
                'severity': 'medium',
                'count': len(long_lines),
                'details': long_lines[:5]  # Show first 5
            })

        # 2. Missing docstrings for classes/functions
        missing_docstrings = []
        in_class = False
        in_function = False

        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith('class '):
                in_class = True
                class_name = stripped.split()[1].split('(')[0].rstrip(':')
                # Check if next non-empty line has docstring
                for j in range(i+1, min(i+5, len(lines))):
                    next_line = lines[j].strip()
                    if next_line and not next_line.startswith('"""') and not next_line.startswith("'''"):
                        missing_docstrings.append(f"Class {class_name} at line {i+1}")
                        break
                    elif next_line.startswith('"""') or next_line.startswith("'''"):
                        break
            elif stripped.startswith('def '):
                func_name = stripped.split()[1].split('(')[0]
                if not func_name.startswith('_'):  # Skip private methods
                    # Check if next non-empty line has docstring
                    for j in range(i+1, min(i+5, len(lines))):
                        next_line = lines[j].strip()
                        if next_line and not next_line.startswith('"""') and not next_line.startswith("'''"):
                            missing_docstrings.append(f"Function {func_name} at line {i+1}")
                            break
                        elif next_line.startswith('"""') or next_line.startswith("'''"):
                            break

        if missing_docstrings:
            issues.append({
                'type': 'missing_docstrings',
                'severity': 'medium',
                'count': len(missing_docstrings),
                'details': missing_docstrings[:10]
            })

        # 3. Hardcoded values that should be configurable
        hardcoded_patterns = [
            (r'password\s*=\s*["\'][^"\']+["\']', 'hardcoded_password'),
            (r'api_key\s*=\s*["\'][^"\']+["\']', 'hardcoded_api_key'),
            (r'\.sleep\(\d+\)', 'hardcoded_sleep'),
            (r'\.jpg|\.png|\.pdf', 'hardcoded_file_extensions')
        ]

        hardcoded_issues = []
        for pattern, issue_type in hardcoded_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                line_num = content[:match.start()].count('\n') + 1
                hardcoded_issues.append(f"{issue_type} at line {line_num}")

        if hardcoded_issues:
            issues.append({
                'type': 'hardcoded_values',
                'severity': 'high',
                'count': len(hardcoded_issues),
                'details': hardcoded_issues
            })

        # 4. Error handling issues
        error_handling_issues = []

        # Check for bare except clauses
        bare_except_matches = re.finditer(r'except\s*:', content)
        for match in bare_except_matches:
            line_num = content[:match.start()].count('\n') + 1
            error_handling_issues.append(f"Bare except clause at line {line_num}")

        # Check for pass in except blocks
        pass_in_except = re.finditer(r'except.*?:\s*\n\s*pass', content, re.DOTALL)
        for match in pass_in_except:
            line_num = content[:match.start()].count('\n') + 1
            error_handling_issues.append(f"Empty except block at line {line_num}")

        if error_handling_issues:
            issues.append({
                'type': 'error_handling',
                'severity': 'high',
                'count': len(error_handling_issues),
                'details': error_handling_issues
            })

        # 5. Code complexity metrics
        function_count = len(re.findall(r'def\s+\w+', content))
        class_count = len(re.findall(r'class\s+\w+', content))

        analysis['metrics'] = {
            'function_count': function_count,
            'class_count': class_count,
            'lines_per_function': analysis['line_count'] / max(function_count, 1),
            'complexity_score': len(re.findall(r'\bif\b|\bfor\b|\bwhile\b|\btry\b', content))
        }

        analysis['issues'] = issues

        return analysis

    def analyze_workflow_completeness(self) -> Dict[str, Any]:
        """Analyze if the complete workflow can run end-to-end"""

        workflow_analysis = {
            'expected_workflow': [
                'enhanced_classifier.py - Data classification',
                'universal_content_engine.py - Content generation',
                'sap_powerpoint_generator.py - Presentation creation'
            ],
            'dependencies_satisfied': False,
            'workflow_issues': [],
            'integration_points': []
        }

        # Check if files can import each other
        src_files = [
            'src/enhanced_classifier.py',
            'src/universal_content_engine.py',
            'src/sap_powerpoint_generator.py'
        ]

        for file_path in src_files:
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r') as f:
                        content = f.read()

                    # Check imports
                    imports = re.findall(r'from\s+(\w+)\s+import|import\s+(\w+)', content)
                    external_deps = []

                    for imp in imports:
                        module = imp[0] or imp[1]
                        if module in ['pandas', 'numpy', 'pptx', 'openpyxl']:
                            external_deps.append(module)

                    if external_deps:
                        workflow_analysis['workflow_issues'].append({
                            'file': file_path,
                            'missing_dependencies': external_deps
                        })

                    # Check for main execution
                    has_main = '__name__' in content and '__main__' in content
                    if has_main:
                        workflow_analysis['integration_points'].append({
                            'file': file_path,
                            'runnable': True,
                            'dependencies': external_deps
                        })

                except Exception as e:
                    workflow_analysis['workflow_issues'].append({
                        'file': file_path,
                        'error': str(e)
                    })

        return workflow_analysis

    def generate_quality_report(self) -> Dict[str, Any]:
        """Generate comprehensive quality report"""

        print("Universal Automation Platform - Quality Analysis")
        print("=" * 60)

        # Analyze structure
        structure = self.analyze_file_structure()
        print(f"\nRepository Structure:")
        print(f"• Total files: {structure['total_files']}")
        print(f"• Python files: {structure['python_files']}")
        print(f"• Test files: {structure['test_files']}")
        print(f"• Documentation files: {structure['doc_files']}")

        if structure['missing_files']:
            print(f"• Missing expected files: {len(structure['missing_files'])}")
            for missing in structure['missing_files']:
                print(f"  - {missing}")

        # Analyze each source file
        source_files = [
            'src/enhanced_classifier.py',
            'src/universal_content_engine.py',
            'src/sap_powerpoint_generator.py'
        ]

        total_issues = 0
        critical_issues = 0

        print(f"\nCode Quality Analysis:")
        print("-" * 40)

        for src_file in source_files:
            if os.path.exists(src_file):
                analysis = self.analyze_code_quality(src_file)
                print(f"\n{src_file}:")
                print(f"  Lines: {analysis.get('line_count', 0)}")
                print(f"  Functions: {analysis.get('metrics', {}).get('function_count', 0)}")
                print(f"  Classes: {analysis.get('metrics', {}).get('class_count', 0)}")

                issues = analysis.get('issues', [])
                print(f"  Issues found: {len(issues)}")

                for issue in issues:
                    total_issues += issue['count']
                    if issue['severity'] == 'high':
                        critical_issues += issue['count']

                    print(f"    • {issue['type']}: {issue['count']} ({issue['severity']})")
                    if issue['details']:
                        for detail in issue['details'][:3]:
                            print(f"      - {detail}")
                        if len(issue['details']) > 3:
                            print(f"      - ... and {len(issue['details']) - 3} more")

        # Analyze workflow completeness
        workflow = self.analyze_workflow_completeness()
        print(f"\nWorkflow Analysis:")
        print("-" * 40)

        if workflow['workflow_issues']:
            print("Workflow cannot run end-to-end due to:")
            for issue in workflow['workflow_issues']:
                if 'missing_dependencies' in issue:
                    print(f"  • {issue['file']}: Missing {', '.join(issue['missing_dependencies'])}")
                elif 'error' in issue:
                    print(f"  • {issue['file']}: {issue['error']}")

        if workflow['integration_points']:
            print("Runnable components found:")
            for point in workflow['integration_points']:
                status = "✓ Ready" if not point['dependencies'] else f"⚠ Needs: {', '.join(point['dependencies'])}"
                print(f"  • {point['file']}: {status}")

        # Summary
        print(f"\nQUALITY SUMMARY:")
        print("=" * 60)
        print(f"Total issues found: {total_issues}")
        print(f"Critical issues: {critical_issues}")

        quality_score = max(0, 100 - (total_issues * 2) - (critical_issues * 5))
        print(f"Quality score: {quality_score}/100")

        if critical_issues > 0:
            print("❌ CRITICAL: Address high-severity issues before production")
        elif total_issues > 10:
            print("⚠️  WARNING: Consider addressing code quality issues")
        else:
            print("✅ GOOD: Code quality is acceptable")

        return {
            'structure': structure,
            'source_analysis': [self.analyze_code_quality(f) for f in source_files if os.path.exists(f)],
            'workflow': workflow,
            'summary': {
                'total_issues': total_issues,
                'critical_issues': critical_issues,
                'quality_score': quality_score
            }
        }

if __name__ == "__main__":
    analyzer = CodeQualityAnalyzer()
    report = analyzer.generate_quality_report()