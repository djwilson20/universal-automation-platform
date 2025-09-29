import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
from io import BytesIO
import warnings
import traceback
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.dml import MSO_THEME_COLOR
from docx import Document
import re

warnings.filterwarnings('ignore')

# Configure page with SAP-style branding
st.set_page_config(
    page_title="Universal Automation Platform - SAP Edition",
    page_icon="<�",
    layout="wide",
    initial_sidebar_state="expanded"
)

# SAP Corporate CSS Styling
st.markdown("""
<style>
    /* SAP Color Palette */
    :root {
        --sap-blue: #0070f2;
        --sap-dark-blue: #0854a0;
        --sap-light-blue: #d1efff;
        --sap-gray: #6a6d70;
        --sap-light-gray: #f7f7f7;
        --sap-green: #30914c;
        --sap-orange: #ff6600;
        --sap-red: #cc1919;
    }

    /* Main container styling */
    .main > div {
        padding-top: 1rem;
    }

    /* SAP Header styling */
    .sap-header {
        background: linear-gradient(135deg, var(--sap-blue) 0%, var(--sap-dark-blue) 100%);
        padding: 2rem;
        border-radius: 8px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 12px rgba(0, 112, 242, 0.15);
        border-left: 4px solid var(--sap-orange);
    }

    .sap-title {
        color: white;
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-align: left;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    .sap-subtitle {
        color: var(--sap-light-blue);
        font-size: 1.1rem;
        text-align: left;
        margin-bottom: 0.5rem;
    }

    .sap-tagline {
        color: #e8f4ff;
        font-size: 0.95rem;
        text-align: left;
        font-style: italic;
    }

    /* SAP Card styling */
    .sap-card {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #e5e5e5;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        border-left: 4px solid var(--sap-blue);
    }

    /* SAP Button styling */
    .stButton > button {
        background: var(--sap-blue);
        color: white;
        border: none;
        border-radius: 4px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        transition: all 0.2s ease;
        box-shadow: 0 2px 4px rgba(0, 112, 242, 0.2);
    }

    .stButton > button:hover {
        background: var(--sap-dark-blue);
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0, 112, 242, 0.3);
    }

    /* SAP Status indicators */
    .sap-status-success {
        background-color: #e8f5e8;
        color: var(--sap-green);
        padding: 0.5rem 1rem;
        border-radius: 4px;
        border-left: 4px solid var(--sap-green);
        margin: 0.5rem 0;
    }

    .sap-status-warning {
        background-color: #fff3e0;
        color: var(--sap-orange);
        padding: 0.5rem 1rem;
        border-radius: 4px;
        border-left: 4px solid var(--sap-orange);
        margin: 0.5rem 0;
    }

    .sap-status-error {
        background-color: #ffebee;
        color: var(--sap-red);
        padding: 0.5rem 1rem;
        border-radius: 4px;
        border-left: 4px solid var(--sap-red);
        margin: 0.5rem 0;
    }

    /* SAP Metrics */
    .sap-metric {
        background: var(--sap-light-gray);
        padding: 1rem;
        border-radius: 4px;
        text-align: center;
        border: 1px solid #e0e0e0;
    }

    .sap-metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: var(--sap-blue);
        margin-bottom: 0.25rem;
    }

    .sap-metric-label {
        font-size: 0.9rem;
        color: var(--sap-gray);
        font-weight: 500;
    }

    /* SAP Sidebar styling */
    .css-1d391kg {
        background-color: var(--sap-light-gray);
    }

    /* SAP File uploader */
    .stFileUploader > div > div > div > div {
        border: 2px dashed var(--sap-blue);
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# SAP Corporate Header
st.markdown("""
<div class="sap-header">
    <div class="sap-title"><� Universal Automation Platform</div>
    <div class="sap-subtitle">SAP Edition - Enterprise Data Processing Suite</div>
    <div class="sap-tagline">Professional data processing and reporting for modern enterprises</div>
</div>
""", unsafe_allow_html=True)

class SAPTemplateAnalyzer:
    """SAP PowerPoint template analysis and learning system"""

    def __init__(self):
        self.template_data = None
        self.learned_styles = {}
        self.layout_patterns = []

    def analyze_template(self, pptx_file):
        """Analyze template PowerPoint to extract patterns and styles"""
        try:
            prs = Presentation(BytesIO(pptx_file))
            template_info = {
                'slide_count': len(prs.slides),
                'layouts': [],
                'colors': [],
                'fonts': [],
                'slide_patterns': [],
                'master_layouts': [],
                'content_patterns': {
                    'title_positions': [],
                    'content_areas': [],
                    'bullet_styles': [],
                    'shape_arrangements': []
                }
            }

            # Extract slide layouts and patterns
            for i, slide in enumerate(prs.slides):
                slide_info = {
                    'slide_number': i + 1,
                    'layout_type': slide.slide_layout.name if hasattr(slide.slide_layout, 'name') else 'Unknown',
                    'layout_index': slide.slide_layout.element.get('idx') if hasattr(slide.slide_layout.element, 'get') else 0,
                    'shapes': [],
                    'colors': [],
                    'fonts': [],
                    'title_shape': None,
                    'content_shapes': [],
                    'background_info': {},
                    'spacing_patterns': {}
                }

                # Analyze shapes and their properties
                for shape in slide.shapes:
                    shape_info = {
                        'type': shape.shape_type,
                        'left': shape.left.inches if hasattr(shape.left, 'inches') else None,
                        'top': shape.top.inches if hasattr(shape.top, 'inches') else None,
                        'width': shape.width.inches if hasattr(shape.width, 'inches') else None,
                        'height': shape.height.inches if hasattr(shape.height, 'inches') else None,
                        'is_title': False,
                        'is_placeholder': hasattr(shape, 'is_placeholder') and shape.is_placeholder,
                        'placeholder_format': None,
                        'text_alignment': None,
                        'indent_level': 0
                    }

                    # Identify title shapes
                    if hasattr(shape, 'is_placeholder') and shape.is_placeholder:
                        try:
                            if shape.placeholder_format.type == 1:  # Title placeholder
                                shape_info['is_title'] = True
                                slide_info['title_shape'] = shape_info.copy()
                                template_info['content_patterns']['title_positions'].append({
                                    'left': shape_info['left'],
                                    'top': shape_info['top'],
                                    'width': shape_info['width'],
                                    'height': shape_info['height']
                                })
                        except:
                            pass

                    # Check if it's a title shape by position (fallback)
                    if not shape_info['is_title'] and shape_info['top'] and shape_info['top'] < 2:
                        shape_info['is_title'] = True
                        slide_info['title_shape'] = shape_info.copy()

                    # Extract text formatting if available
                    if hasattr(shape, 'text_frame') and shape.text_frame:
                        try:
                            for para_idx, paragraph in enumerate(shape.text_frame.paragraphs):
                                # Capture paragraph-level formatting
                                bullet_info = {
                                    'level': paragraph.level,
                                    'alignment': paragraph.alignment,
                                    'space_before': getattr(paragraph.space_before, 'pt', None) if paragraph.space_before else None,
                                    'space_after': getattr(paragraph.space_after, 'pt', None) if paragraph.space_after else None,
                                    'line_spacing': getattr(paragraph.line_spacing, 'pt', None) if paragraph.line_spacing else None
                                }
                                template_info['content_patterns']['bullet_styles'].append(bullet_info)

                                for run in paragraph.runs:
                                    if run.font.name:
                                        slide_info['fonts'].append(run.font.name)
                                    if hasattr(run.font, 'color') and run.font.color.rgb:
                                        color_hex = f"#{run.font.color.rgb}"
                                        slide_info['colors'].append(color_hex)

                            # Store content area information
                            if not shape_info['is_title']:
                                content_area = {
                                    'left': shape_info['left'],
                                    'top': shape_info['top'],
                                    'width': shape_info['width'],
                                    'height': shape_info['height'],
                                    'paragraph_count': len(shape.text_frame.paragraphs)
                                }
                                template_info['content_patterns']['content_areas'].append(content_area)
                                slide_info['content_shapes'].append(shape_info.copy())

                        except:
                            pass

                    slide_info['shapes'].append(shape_info)

                template_info['slide_patterns'].append(slide_info)

            # Extract dominant colors and fonts
            all_fonts = []
            all_colors = []
            for slide in template_info['slide_patterns']:
                all_fonts.extend(slide['fonts'])
                all_colors.extend(slide['colors'])

            # Get most common fonts and colors
            from collections import Counter
            template_info['fonts'] = [font for font, count in Counter(all_fonts).most_common(5)]
            template_info['colors'] = [color for color, count in Counter(all_colors).most_common(5)]

            self.template_data = template_info
            self.learned_styles = {
                'primary_font': template_info['fonts'][0] if template_info['fonts'] else 'Calibri',
                'primary_colors': template_info['colors'][:3] if template_info['colors'] else ['#0070f2', '#ff6600', '#30914c'],
                'layout_patterns': template_info['slide_patterns'],
                'title_positioning': self._calculate_average_position(template_info['content_patterns']['title_positions']),
                'content_positioning': self._calculate_average_position(template_info['content_patterns']['content_areas']),
                'bullet_formatting': self._analyze_bullet_patterns(template_info['content_patterns']['bullet_styles']),
                'slide_sequencing': self._analyze_slide_sequence(template_info['slide_patterns'])
            }

            return template_info

        except Exception as e:
            st.error(f"Error analyzing template: {str(e)}")
            return None

    def _calculate_average_position(self, positions):
        """Calculate average position from a list of position dictionaries"""
        if not positions:
            return None

        avg_pos = {
            'left': sum(pos['left'] for pos in positions if pos['left']) / len([pos for pos in positions if pos['left']]),
            'top': sum(pos['top'] for pos in positions if pos['top']) / len([pos for pos in positions if pos['top']]),
            'width': sum(pos['width'] for pos in positions if pos['width']) / len([pos for pos in positions if pos['width']]),
            'height': sum(pos['height'] for pos in positions if pos['height']) / len([pos for pos in positions if pos['height']])
        }
        return avg_pos

    def _analyze_bullet_patterns(self, bullet_styles):
        """Analyze bullet formatting patterns"""
        if not bullet_styles:
            return {}

        from collections import Counter
        levels = [style['level'] for style in bullet_styles if style['level'] is not None]
        alignments = [style['alignment'] for style in bullet_styles if style['alignment'] is not None]

        return {
            'common_levels': Counter(levels).most_common(3),
            'common_alignments': Counter(alignments).most_common(2),
            'avg_space_before': sum(style['space_before'] for style in bullet_styles if style['space_before']) / max(1, len([s for s in bullet_styles if s['space_before']])),
            'avg_space_after': sum(style['space_after'] for style in bullet_styles if style['space_after']) / max(1, len([s for s in bullet_styles if s['space_after']]))
        }

    def _analyze_slide_sequence(self, slide_patterns):
        """Analyze slide sequencing patterns"""
        if not slide_patterns:
            return []

        sequence = []
        for slide in slide_patterns:
            slide_type = 'title' if slide['slide_number'] == 1 else 'content'
            if slide['title_shape'] and len(slide['content_shapes']) > 0:
                slide_type = 'title_and_content'
            elif slide['title_shape']:
                slide_type = 'title_only'
            elif len(slide['content_shapes']) > 0:
                slide_type = 'content_only'

            sequence.append({
                'slide_number': slide['slide_number'],
                'type': slide_type,
                'layout_type': slide['layout_type'],
                'shape_count': len(slide['shapes'])
            })

        return sequence

    def get_template_summary(self):
        """Get a summary of the learned template"""
        if not self.template_data:
            return None

        return {
            'total_slides': self.template_data['slide_count'],
            'unique_layouts': len(set([slide['layout_type'] for slide in self.template_data['slide_patterns']])),
            'dominant_fonts': self.template_data['fonts'][:3],
            'dominant_colors': self.template_data['colors'][:3],
            'avg_shapes_per_slide': sum(len(slide['shapes']) for slide in self.template_data['slide_patterns']) / max(1, len(self.template_data['slide_patterns'])),
            'content_areas_detected': len(self.template_data['content_patterns']['content_areas']),
            'bullet_styles_found': len(set([str(style) for style in self.template_data['content_patterns']['bullet_styles']]))
        }

    def apply_template_structure(self, slide, slide_type='content'):
        """Apply learned template structure to a new slide"""
        if not self.learned_styles:
            return slide

        try:
            # Apply title positioning if available
            if slide_type in ['title', 'title_and_content'] and self.learned_styles.get('title_positioning'):
                title_pos = self.learned_styles['title_positioning']
                if slide.shapes.title:
                    title_shape = slide.shapes.title
                    if title_pos['left']:
                        title_shape.left = Inches(title_pos['left'])
                    if title_pos['top']:
                        title_shape.top = Inches(title_pos['top'])
                    if title_pos['width']:
                        title_shape.width = Inches(title_pos['width'])
                    if title_pos['height']:
                        title_shape.height = Inches(title_pos['height'])

            # Apply content positioning for content slides
            if slide_type in ['content', 'title_and_content'] and self.learned_styles.get('content_positioning'):
                content_pos = self.learned_styles['content_positioning']

                # Find content placeholders
                for shape in slide.shapes:
                    if hasattr(shape, 'is_placeholder') and shape.is_placeholder:
                        try:
                            if shape.placeholder_format.type == 2:  # Content placeholder
                                if content_pos['left']:
                                    shape.left = Inches(content_pos['left'])
                                if content_pos['top']:
                                    shape.top = Inches(content_pos['top'])
                                if content_pos['width']:
                                    shape.width = Inches(content_pos['width'])
                                if content_pos['height']:
                                    shape.height = Inches(content_pos['height'])
                        except:
                            pass

            # Apply bullet formatting
            bullet_format = self.learned_styles.get('bullet_formatting', {})
            for shape in slide.shapes:
                if hasattr(shape, 'text_frame') and shape.text_frame:
                    for paragraph in shape.text_frame.paragraphs:
                        # Apply spacing patterns
                        if 'avg_space_before' in bullet_format and bullet_format['avg_space_before']:
                            try:
                                paragraph.space_before = Pt(bullet_format['avg_space_before'])
                            except:
                                pass
                        if 'avg_space_after' in bullet_format and bullet_format['avg_space_after']:
                            try:
                                paragraph.space_after = Pt(bullet_format['avg_space_after'])
                            except:
                                pass

        except Exception as e:
            # Silently continue if template application fails
            pass

        return slide

    def get_recommended_slide_order(self, content_sections):
        """Get recommended slide order based on template patterns"""
        if not self.learned_styles or not self.learned_styles.get('slide_sequencing'):
            return content_sections

        template_sequence = self.learned_styles['slide_sequencing']

        # Analyze template patterns
        title_slides = [s for s in template_sequence if s['type'] in ['title', 'title_only']]
        content_slides = [s for s in template_sequence if s['type'] in ['title_and_content', 'content']]

        # Recommend structure based on template
        recommended_order = []

        # Always start with title slide
        recommended_order.append({'type': 'title', 'content': 'title_slide'})

        # If template has early summary/overview slides
        if len(template_sequence) > 1 and template_sequence[1]['type'] in ['title_and_content']:
            recommended_order.append({'type': 'overview', 'content': 'executive_summary'})

        # Add content sections based on template pattern
        for section in content_sections:
            if section == 'data_quality' and any(s['shape_count'] > 5 for s in content_slides):
                recommended_order.append({'type': 'detailed_content', 'content': section})
            else:
                recommended_order.append({'type': 'standard_content', 'content': section})

        # If template ends with summary/recommendations
        if len(template_sequence) > 2 and template_sequence[-1]['shape_count'] < 4:
            recommended_order.append({'type': 'summary', 'content': 'recommendations'})

        return recommended_order

class SAPDataProcessor:
    """SAP-style data processing engine"""

    def __init__(self):
        self.supported_formats = ['csv', 'xlsx', 'xls', 'pptx', 'docx']

    def extract_word_document_data(self, docx_file):
        """Extract comprehensive content from Word documents including text, tables, and metadata"""
        try:
            doc = Document(BytesIO(docx_file))
            extracted_data = {
                'document_structure': {
                    'paragraphs': [],
                    'tables': [],
                    'headers': [],
                    'footers': [],
                    'metadata': {}
                },
                'processed_content': {
                    'text_content': [],
                    'data_tables': [],
                    'key_points': [],
                    'decisions': [],
                    'metrics': []
                },
                'document_stats': {
                    'total_paragraphs': 0,
                    'total_tables': 0,
                    'total_words': 0,
                    'bullet_points': 0,
                    'numbered_lists': 0
                }
            }

            # Extract document metadata
            try:
                core_props = doc.core_properties
                extracted_data['document_structure']['metadata'] = {
                    'title': core_props.title or '',
                    'author': core_props.author or '',
                    'subject': core_props.subject or '',
                    'created': core_props.created.strftime('%Y-%m-%d %H:%M:%S') if core_props.created else '',
                    'modified': core_props.modified.strftime('%Y-%m-%d %H:%M:%S') if core_props.modified else '',
                    'last_modified_by': core_props.last_modified_by or ''
                }
            except:
                extracted_data['document_structure']['metadata'] = {}

            # Extract headers and footers
            for section in doc.sections:
                # Headers
                if section.header:
                    for paragraph in section.header.paragraphs:
                        if paragraph.text.strip():
                            extracted_data['document_structure']['headers'].append({
                                'text': paragraph.text.strip(),
                                'style': paragraph.style.name if paragraph.style else 'Normal'
                            })

                # Footers
                if section.footer:
                    for paragraph in section.footer.paragraphs:
                        if paragraph.text.strip():
                            extracted_data['document_structure']['footers'].append({
                                'text': paragraph.text.strip(),
                                'style': paragraph.style.name if paragraph.style else 'Normal'
                            })

            # Extract paragraphs with detailed analysis
            word_count = 0
            bullet_count = 0
            numbered_count = 0

            for para_idx, paragraph in enumerate(doc.paragraphs):
                if not paragraph.text.strip():
                    continue

                para_text = self._clean_paragraph_text(paragraph.text)
                word_count += len(para_text.split())

                para_data = {
                    'index': para_idx,
                    'text': para_text,
                    'style': paragraph.style.name if paragraph.style else 'Normal',
                    'level': getattr(paragraph, 'level', 0),
                    'is_bullet': self._is_bullet_point(paragraph),
                    'is_numbered': self._is_numbered_list(paragraph),
                    'is_heading': self._is_heading(paragraph),
                    'formatting': self._extract_paragraph_formatting(paragraph),
                    'content_type': self._classify_paragraph_content(para_text)
                }

                # Count bullet points and numbered lists
                if para_data['is_bullet']:
                    bullet_count += 1
                if para_data['is_numbered']:
                    numbered_count += 1

                extracted_data['document_structure']['paragraphs'].append(para_data)

                # Classify content for processing
                if para_data['content_type'] in ['key_point', 'decision']:
                    extracted_data['processed_content'][para_data['content_type'] + 's'].append(para_text)
                elif para_data['content_type'] == 'metric':
                    extracted_data['processed_content']['metrics'].append(para_text)
                else:
                    extracted_data['processed_content']['text_content'].append(para_text)

            # Extract tables with sophisticated parsing
            for table_idx, table in enumerate(doc.tables):
                table_data = []
                has_header = False

                for row_idx, row in enumerate(table.rows):
                    row_data = []
                    for cell_idx, cell in enumerate(row.cells):
                        cell_text = self._clean_cell_text(cell.text)
                        row_data.append(cell_text)

                    table_data.append(row_data)

                # Detect if first row is header
                if table_data and len(table_data) > 1:
                    first_row = table_data[0]
                    if self._likely_table_header(first_row):
                        has_header = True

                # Process table into DataFrame if it contains data
                df_table = None
                if table_data and len(table_data) > (1 if has_header else 0):
                    try:
                        if has_header and len(table_data) > 1:
                            df_table = pd.DataFrame(table_data[1:], columns=table_data[0])
                        else:
                            df_table = pd.DataFrame(table_data)

                        # Clean and process DataFrame
                        df_table = self._clean_dataframe(df_table)

                        # Only add if it has meaningful data
                        if not df_table.empty and df_table.shape[1] > 1:
                            extracted_data['processed_content']['data_tables'].append({
                                'table_index': table_idx,
                                'dataframe': df_table,
                                'has_header': has_header,
                                'shape': df_table.shape,
                                'numeric_columns': len(df_table.select_dtypes(include=[np.number]).columns)
                            })

                    except Exception as e:
                        # If DataFrame creation fails, store as raw table
                        pass

                table_info = {
                    'table_index': table_idx,
                    'raw_data': table_data,
                    'rows': len(table_data),
                    'columns': len(table_data[0]) if table_data else 0,
                    'has_header': has_header,
                    'has_dataframe': df_table is not None and not df_table.empty
                }

                extracted_data['document_structure']['tables'].append(table_info)

            # Update document statistics
            extracted_data['document_stats'].update({
                'total_paragraphs': len(extracted_data['document_structure']['paragraphs']),
                'total_tables': len(extracted_data['document_structure']['tables']),
                'total_words': word_count,
                'bullet_points': bullet_count,
                'numbered_lists': numbered_count,
                'data_tables_found': len(extracted_data['processed_content']['data_tables']),
                'key_points_found': len(extracted_data['processed_content']['key_points']),
                'decisions_found': len(extracted_data['processed_content']['decisions']),
                'metrics_found': len(extracted_data['processed_content']['metrics'])
            })

            return extracted_data

        except Exception as e:
            st.error(f"Error extracting Word document data: {str(e)}")
            return None

    def _clean_paragraph_text(self, text):
        """Clean paragraph text by removing track changes and comments"""
        # Remove common track changes markers
        text = re.sub(r'\[.*?\]', '', text)  # Remove tracked deletions
        text = re.sub(r'\{.*?\}', '', text)  # Remove comments
        text = re.sub(r'<.*?>', '', text)    # Remove any XML-like tags

        # Clean up whitespace
        text = ' '.join(text.split())
        return text.strip()

    def _clean_cell_text(self, text):
        """Clean table cell text"""
        text = self._clean_paragraph_text(text)
        # Remove table-specific artifacts
        text = text.replace('\a', ' ')  # Remove vertical tab characters
        return text.strip()

    def _is_bullet_point(self, paragraph):
        """Detect if paragraph is a bullet point"""
        text = paragraph.text.strip()
        if not text:
            return False

        # Check for common bullet markers
        bullet_markers = ['•', '●', '○', '▪', '▫', '■', '□', '-', '*']
        if any(text.startswith(marker) for marker in bullet_markers):
            return True

        # Check paragraph style
        style_name = paragraph.style.name.lower() if paragraph.style else ''
        if 'bullet' in style_name or 'list' in style_name:
            return True

        return False

    def _is_numbered_list(self, paragraph):
        """Detect if paragraph is a numbered list item"""
        text = paragraph.text.strip()
        if not text:
            return False

        # Check for numbered patterns
        numbered_patterns = [
            r'^\d+\.',     # 1. 2. 3.
            r'^\d+\)',     # 1) 2) 3)
            r'^\(\d+\)',   # (1) (2) (3)
            r'^[a-z]\.',   # a. b. c.
            r'^[A-Z]\.',   # A. B. C.
            r'^[ivx]+\.',  # i. ii. iii.
            r'^[IVX]+\.'   # I. II. III.
        ]

        for pattern in numbered_patterns:
            if re.match(pattern, text):
                return True

        return False

    def _is_heading(self, paragraph):
        """Detect if paragraph is a heading"""
        if paragraph.style:
            style_name = paragraph.style.name.lower()
            if 'heading' in style_name or 'title' in style_name:
                return True
        return False

    def _extract_paragraph_formatting(self, paragraph):
        """Extract formatting information from paragraph"""
        formatting = {
            'is_bold': False,
            'is_italic': False,
            'font_size': None,
            'font_name': None
        }

        try:
            if paragraph.runs:
                first_run = paragraph.runs[0]
                formatting['is_bold'] = first_run.bold or False
                formatting['is_italic'] = first_run.italic or False
                if first_run.font.size:
                    formatting['font_size'] = first_run.font.size.pt
                formatting['font_name'] = first_run.font.name
        except:
            pass

        return formatting

    def _classify_paragraph_content(self, text):
        """Classify paragraph content type for better processing"""
        text_lower = text.lower()

        # Key point indicators
        key_indicators = ['key point', 'important', 'note:', 'remember', 'action item', 'takeaway']
        if any(indicator in text_lower for indicator in key_indicators):
            return 'key_point'

        # Decision indicators
        decision_indicators = ['decision', 'agreed', 'decided', 'resolved', 'concluded', 'approved']
        if any(indicator in text_lower for indicator in decision_indicators):
            return 'decision'

        # Metric indicators
        metric_patterns = [
            r'\d+%',           # Percentages
            r'\$[\d,]+',       # Dollar amounts
            r'\d+\.\d+',       # Decimal numbers
            r'\d{1,3}(,\d{3})*' # Large numbers with commas
        ]
        if any(re.search(pattern, text) for pattern in metric_patterns):
            return 'metric'

        return 'general_text'

    def _likely_table_header(self, row):
        """Determine if a table row is likely a header"""
        if not row:
            return False

        # Check if all cells have content
        if all(cell.strip() for cell in row):
            # Check for common header patterns
            header_indicators = ['name', 'date', 'amount', 'type', 'status', 'description', 'value', 'total']
            if any(any(indicator in cell.lower() for indicator in header_indicators) for cell in row):
                return True

        return False

    def _clean_dataframe(self, df):
        """Clean and optimize DataFrame from Word table"""
        if df.empty:
            return df

        # Remove completely empty rows and columns
        df = df.dropna(how='all').dropna(axis=1, how='all')

        # Try to convert numeric columns
        for col in df.columns:
            try:
                # Remove common non-numeric characters
                df[col] = df[col].astype(str).str.replace('$', '').str.replace(',', '').str.replace('%', '')
                # Try to convert to numeric
                df[col] = pd.to_numeric(df[col], errors='ignore')
            except:
                pass

        return df

    def extract_powerpoint_data(self, pptx_file):
        """Extract text and table data from PowerPoint presentations"""
        try:
            prs = Presentation(BytesIO(pptx_file))
            extracted_data = {
                'slides': [],
                'text_content': [],
                'tables': [],
                'slide_count': len(prs.slides)
            }

            for i, slide in enumerate(prs.slides):
                slide_data = {
                    'slide_number': i + 1,
                    'title': '',
                    'text_content': [],
                    'tables': []
                }

                # Extract text from shapes
                for shape in slide.shapes:
                    if hasattr(shape, "text") and shape.text.strip():
                        if shape == slide.shapes.title:
                            slide_data['title'] = shape.text.strip()
                        else:
                            slide_data['text_content'].append(shape.text.strip())

                    # Extract tables
                    if shape.shape_type == 19:  # Table shape
                        try:
                            table_data = []
                            table = shape.table
                            for row_idx, row in enumerate(table.rows):
                                row_data = []
                                for cell in row.cells:
                                    row_data.append(cell.text.strip())
                                table_data.append(row_data)

                            if table_data:
                                slide_data['tables'].append(table_data)
                                extracted_data['tables'].append({
                                    'slide': i + 1,
                                    'data': table_data
                                })
                        except:
                            pass

                extracted_data['slides'].append(slide_data)
                extracted_data['text_content'].extend(slide_data['text_content'])

            return extracted_data

        except Exception as e:
            st.error(f"Error extracting PowerPoint data: {str(e)}")
            return None

    def process_csv_excel(self, file_content, file_name):
        """Process CSV and Excel files"""
        try:
            if file_name.lower().endswith('.csv'):
                # Try different encodings for CSV
                encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
                for encoding in encodings:
                    try:
                        df = pd.read_csv(BytesIO(file_content), encoding=encoding)
                        return df
                    except UnicodeDecodeError:
                        continue
                raise ValueError("Could not decode CSV file with any supported encoding")
            else:
                # Excel files
                df = pd.read_excel(BytesIO(file_content))
                return df

        except Exception as e:
            st.error(f"Error processing file: {str(e)}")
            return None

    def analyze_data_quality(self, df):
        """Analyze data quality with SAP-style metrics"""
        if df is None or df.empty:
            return None

        total_cells = len(df) * len(df.columns)
        missing_cells = df.isnull().sum().sum()
        duplicate_rows = df.duplicated().sum()

        quality_metrics = {
            'total_records': len(df),
            'total_columns': len(df.columns),
            'completeness_pct': ((total_cells - missing_cells) / total_cells * 100) if total_cells > 0 else 0,
            'duplicate_pct': (duplicate_rows / len(df) * 100) if len(df) > 0 else 0,
            'numeric_columns': len(df.select_dtypes(include=[np.number]).columns),
            'text_columns': len(df.select_dtypes(include=['object', 'string']).columns),
            'date_columns': len(df.select_dtypes(include=['datetime64']).columns)
        }

        # Quality assessment
        if quality_metrics['completeness_pct'] >= 95 and quality_metrics['duplicate_pct'] <= 1:
            quality_metrics['quality_level'] = 'Excellent'
            quality_metrics['quality_color'] = 'success'
        elif quality_metrics['completeness_pct'] >= 85 and quality_metrics['duplicate_pct'] <= 5:
            quality_metrics['quality_level'] = 'Good'
            quality_metrics['quality_color'] = 'warning'
        else:
            quality_metrics['quality_level'] = 'Needs Improvement'
            quality_metrics['quality_color'] = 'error'

        return quality_metrics

    def generate_basic_insights(self, df):
        """Generate basic data insights"""
        if df is None or df.empty:
            return None

        insights = {
            'summary_stats': {},
            'column_insights': [],
            'data_types': df.dtypes.to_dict()
        }

        # Numeric column analysis
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            insights['summary_stats'] = df[numeric_cols].describe().round(2)

        # Column-level insights
        for col in df.columns:
            col_insight = {
                'column': col,
                'type': str(df[col].dtype),
                'missing_count': df[col].isnull().sum(),
                'missing_pct': (df[col].isnull().sum() / len(df) * 100),
                'unique_values': df[col].nunique()
            }

            if df[col].dtype in ['object', 'string']:
                col_insight['top_values'] = df[col].value_counts().head(3).to_dict()
            elif np.issubdtype(df[col].dtype, np.number):
                col_insight['min_value'] = df[col].min()
                col_insight['max_value'] = df[col].max()
                col_insight['mean_value'] = df[col].mean()

            insights['column_insights'].append(col_insight)

        return insights

# Initialize SAP processor and template analyzer
sap_processor = SAPDataProcessor()
template_analyzer = SAPTemplateAnalyzer()

# Sidebar configuration
with st.sidebar:
    st.markdown("### � SAP Configuration Panel")

    # File processing options
    st.markdown("#### File Processing")
    auto_detect_types = st.checkbox("Auto-detect data types", value=True)
    remove_duplicates = st.checkbox("Remove duplicate records", value=False)
    handle_missing = st.selectbox(
        "Missing data handling",
        ["Keep as-is", "Remove rows", "Fill with mean", "Fill with median"],
        index=0
    )

    # Visualization options
    st.markdown("#### Visualization")
    chart_theme = st.selectbox("Chart theme", ["SAP Corporate", "Modern", "Classic"], index=0)
    include_charts = st.checkbox("Include charts in report", value=True)
    max_categories = st.slider("Maximum categories in charts", 5, 20, 10)

    # Template learning section
    st.markdown("#### 🎨 Template Learning")
    use_template = st.checkbox("Enable template matching", value=False, help="Use a custom PowerPoint template for report generation")

    template_file = None
    if use_template:
        template_file = st.file_uploader(
            "Upload template PowerPoint",
            type=['pptx'],
            help="Upload a sample PowerPoint with your preferred layout and styling",
            key="template_uploader"
        )

        if template_file and st.button("🔍 Learn from Template", key="learn_template"):
            with st.spinner("Analyzing template..."):
                template_data = template_analyzer.analyze_template(template_file.getvalue())
                if template_data:
                    st.success(f"✅ Template learned! Found {template_data['slide_count']} slides")
                    st.session_state['template_learned'] = True
                    st.session_state['template_data'] = template_data

    # Report options
    st.markdown("#### Report Generation")
    report_title = st.text_input("Report title", value="SAP Data Analysis Report")
    include_summary = st.checkbox("Include executive summary", value=True)
    include_quality_assessment = st.checkbox("Include quality assessment", value=True)

    st.markdown("---")
    st.markdown("### =� SAP System Status")
    st.markdown('<div class="sap-status-success"> All systems operational</div>', unsafe_allow_html=True)
    st.markdown(f"=P **Last update:** {datetime.now().strftime('%H:%M:%S')}")

# Main content area
st.markdown("### =� File Upload & Processing")

# File upload section
col1, col2 = st.columns([3, 1])

with col1:
    uploaded_file = st.file_uploader(
        "Upload your business data file",
        type=['csv', 'xlsx', 'xls', 'pptx', 'docx'],
        help="Supported formats: CSV, Excel (.xlsx, .xls), PowerPoint (.pptx), Word (.docx)"
    )

with col2:
    if uploaded_file:
        file_size = len(uploaded_file.getvalue()) / (1024 * 1024)  # MB
        file_extension = uploaded_file.name.split('.')[-1].upper()

        st.markdown('<div class="sap-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="sap-metric-value">{file_size:.1f} MB</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="sap-metric-label">File Size</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="sap-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="sap-metric-value">{file_extension}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="sap-metric-label">Format</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# Template preview section
if 'template_learned' in st.session_state and st.session_state['template_learned']:
    st.markdown("### 🎨 Template Preview")

    # Get template summary
    template_summary = template_analyzer.get_template_summary()

    if template_summary:
        st.markdown('<div class="sap-card">', unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown('<div class="sap-metric">', unsafe_allow_html=True)
            st.markdown(f'<div class="sap-metric-value">{template_summary["total_slides"]}</div>', unsafe_allow_html=True)
            st.markdown('<div class="sap-metric-label">Template Slides</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="sap-metric">', unsafe_allow_html=True)
            st.markdown(f'<div class="sap-metric-value">{template_summary["unique_layouts"]}</div>', unsafe_allow_html=True)
            st.markdown('<div class="sap-metric-label">Layout Types</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col3:
            st.markdown('<div class="sap-metric">', unsafe_allow_html=True)
            st.markdown(f'<div class="sap-metric-value">{len(template_summary["dominant_fonts"])}</div>', unsafe_allow_html=True)
            st.markdown('<div class="sap-metric-label">Font Styles</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col4:
            st.markdown('<div class="sap-metric">', unsafe_allow_html=True)
            st.markdown(f'<div class="sap-metric-value">{template_summary["avg_shapes_per_slide"]:.1f}</div>', unsafe_allow_html=True)
            st.markdown('<div class="sap-metric-label">Avg Shapes/Slide</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # Show template details
        with st.expander("🔍 Template Analysis Details", expanded=False):
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**Dominant Fonts:**")
                for font in template_summary['dominant_fonts']:
                    st.write(f"• {font}")

            with col2:
                st.markdown("**Color Scheme:**")
                for color in template_summary['dominant_colors']:
                    st.markdown(f'<span style="color: {color}; font-weight: bold;">● {color}</span>', unsafe_allow_html=True)

        # Show additional template analysis
        if template_summary.get('content_areas_detected', 0) > 0:
            st.markdown("**Template Structure Analysis:**")
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"📍 Content Areas Detected: {template_summary['content_areas_detected']}")
            with col2:
                st.write(f"🎯 Bullet Styles Found: {template_summary['bullet_styles_found']}")

            # Show slide sequencing if available
            if hasattr(template_analyzer, 'learned_styles') and template_analyzer.learned_styles.get('slide_sequencing'):
                sequence = template_analyzer.learned_styles['slide_sequencing']
                st.markdown("**Template Slide Sequence:**")
                sequence_text = " → ".join([f"{s['type']}" for s in sequence[:5]])
                if len(sequence) > 5:
                    sequence_text += f" ... ({len(sequence)} total slides)"
                st.write(sequence_text)

        st.info("🎯 **Template Active:** Generated reports will match this template's styling and layout patterns.")

def create_sap_visualization(df, chart_type="overview"):
    """Create SAP-style visualizations"""
    if df is None or df.empty:
        return None

    numeric_cols = df.select_dtypes(include=[np.number]).columns

    if chart_type == "overview" and len(numeric_cols) > 0:
        # Create overview dashboard
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Data Distribution', 'Correlation Matrix', 'Missing Values', 'Data Types'),
            specs=[[{"type": "histogram"}, {"type": "heatmap"}],
                   [{"type": "bar"}, {"type": "pie"}]]
        )

        # Data distribution (first numeric column)
        if len(numeric_cols) > 0:
            fig.add_trace(
                go.Histogram(x=df[numeric_cols[0]], name=numeric_cols[0], marker_color='#0070f2'),
                row=1, col=1
            )

        # Correlation matrix
        if len(numeric_cols) > 1:
            corr_matrix = df[numeric_cols].corr()
            fig.add_trace(
                go.Heatmap(
                    z=corr_matrix.values,
                    x=corr_matrix.columns,
                    y=corr_matrix.columns,
                    colorscale='RdBu',
                    zmid=0
                ),
                row=1, col=2
            )

        # Missing values
        missing_data = df.isnull().sum()
        missing_data = missing_data[missing_data > 0]
        if len(missing_data) > 0:
            fig.add_trace(
                go.Bar(x=missing_data.values, y=missing_data.index,
                       orientation='h', marker_color='#ff6600'),
                row=2, col=1
            )

        # Data types
        type_counts = df.dtypes.value_counts()
        fig.add_trace(
            go.Pie(labels=type_counts.index.astype(str), values=type_counts.values,
                   marker_colors=['#0070f2', '#30914c', '#ff6600', '#cc1919'][:len(type_counts)]),
            row=2, col=2
        )

        fig.update_layout(
            height=600,
            showlegend=False,
            title_text="SAP Data Overview Dashboard",
            title_font_size=16
        )

        return fig

    return None

def generate_sap_powerpoint_report(df, insights, pptx_data=None, docx_data=None):
    """Generate professional SAP-style PowerPoint report"""
    try:
        # Check if template should be used
        use_template_styling = ('template_learned' in st.session_state and
                              st.session_state['template_learned'] and
                              hasattr(template_analyzer, 'learned_styles') and
                              template_analyzer.learned_styles)

        prs = Presentation()

        # Define colors (use template colors if available, otherwise SAP defaults)
        if use_template_styling and template_analyzer.learned_styles['primary_colors']:
            try:
                # Convert hex colors to RGB
                def hex_to_rgb(hex_color):
                    hex_color = hex_color.lstrip('#')
                    return RGBColor(*tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4)))

                primary_colors = template_analyzer.learned_styles['primary_colors']
                primary_color = hex_to_rgb(primary_colors[0]) if primary_colors else RGBColor(0, 112, 242)
                secondary_color = hex_to_rgb(primary_colors[1]) if len(primary_colors) > 1 else RGBColor(255, 102, 0)
                accent_color = hex_to_rgb(primary_colors[2]) if len(primary_colors) > 2 else RGBColor(106, 109, 112)
            except:
                # Fallback to SAP colors if template colors can't be parsed
                primary_color = RGBColor(0, 112, 242)
                secondary_color = RGBColor(255, 102, 0)
                accent_color = RGBColor(106, 109, 112)
        else:
            # Use SAP default colors
            primary_color = RGBColor(0, 112, 242)
            secondary_color = RGBColor(255, 102, 0)
            accent_color = RGBColor(106, 109, 112)

        # Define primary font (use template font if available)
        primary_font = (template_analyzer.learned_styles['primary_font']
                       if use_template_styling and template_analyzer.learned_styles['primary_font']
                       else 'Calibri')

        # Title slide
        title_slide_layout = prs.slide_layouts[0]
        slide = prs.slides.add_slide(title_slide_layout)

        # Apply template structure to title slide
        if use_template_styling:
            slide = template_analyzer.apply_template_structure(slide, 'title')

        title = slide.shapes.title
        subtitle = slide.placeholders[1]

        title.text = report_title
        if use_template_styling:
            subtitle.text = f"Generated on {datetime.now().strftime('%B %d, %Y')}\nTemplate-based SAP Analysis"
        else:
            subtitle.text = f"Generated on {datetime.now().strftime('%B %d, %Y')}\nSAP Universal Automation Platform"

        # Format title with template styling
        title_paragraph = title.text_frame.paragraphs[0]
        title_paragraph.font.color.rgb = primary_color
        title_paragraph.font.size = Pt(44)
        title_paragraph.font.bold = True
        title_paragraph.font.name = primary_font

        # Executive Summary slide
        if include_summary and insights:
            bullet_slide_layout = prs.slide_layouts[1]
            slide = prs.slides.add_slide(bullet_slide_layout)

            # Apply template structure
            if use_template_styling:
                slide = template_analyzer.apply_template_structure(slide, 'title_and_content')

            title = slide.shapes.title
            body = slide.placeholders[1]

            title.text = "Executive Summary"
            title_paragraph = title.text_frame.paragraphs[0]
            title_paragraph.font.color.rgb = primary_color
            title_paragraph.font.name = primary_font

            tf = body.text_frame
            tf.text = "Data Processing Results"

            if df is not None:
                p = tf.add_paragraph()
                p.text = f"• Total Records: {len(df):,}"
                p.level = 1

                p = tf.add_paragraph()
                p.text = f"• Data Columns: {len(df.columns)}"
                p.level = 1

                quality_metrics = sap_processor.analyze_data_quality(df)
                if quality_metrics:
                    p = tf.add_paragraph()
                    p.text = f"• Data Quality: {quality_metrics['quality_level']}"
                    p.level = 1

                    p = tf.add_paragraph()
                    p.text = f"• Completeness: {quality_metrics['completeness_pct']:.1f}%"
                    p.level = 1

        # Data Quality slide
        if include_quality_assessment and df is not None:
            quality_metrics = sap_processor.analyze_data_quality(df)
            if quality_metrics:
                bullet_slide_layout = prs.slide_layouts[1]
                slide = prs.slides.add_slide(bullet_slide_layout)

                # Apply template structure
                if use_template_styling:
                    slide = template_analyzer.apply_template_structure(slide, 'title_and_content')

                title = slide.shapes.title
                body = slide.placeholders[1]

                title.text = "Data Quality Assessment"
                title_paragraph = title.text_frame.paragraphs[0]
                title_paragraph.font.color.rgb = primary_color
                title_paragraph.font.name = primary_font

                tf = body.text_frame
                tf.text = f"Overall Quality: {quality_metrics['quality_level']}"

                metrics_text = [
                    f"Data Completeness: {quality_metrics['completeness_pct']:.1f}%",
                    f"Duplicate Records: {quality_metrics['duplicate_pct']:.1f}%",
                    f"Numeric Columns: {quality_metrics['numeric_columns']}",
                    f"Text Columns: {quality_metrics['text_columns']}",
                    f"Total Records: {quality_metrics['total_records']:,}"
                ]

                for metric in metrics_text:
                    p = tf.add_paragraph()
                    p.text = f"• {metric}"
                    p.level = 1

        # PowerPoint Data slide (if PowerPoint was uploaded)
        if pptx_data:
            bullet_slide_layout = prs.slide_layouts[1]
            slide = prs.slides.add_slide(bullet_slide_layout)

            # Apply template structure
            if use_template_styling:
                slide = template_analyzer.apply_template_structure(slide, 'title_and_content')

            title = slide.shapes.title
            body = slide.placeholders[1]

            title.text = "PowerPoint Analysis Results"
            title_paragraph = title.text_frame.paragraphs[0]
            title_paragraph.font.color.rgb = primary_color
            title_paragraph.font.name = primary_font

            tf = body.text_frame
            tf.text = f"Processed {pptx_data['slide_count']} slides"

            p = tf.add_paragraph()
            p.text = f"• Text blocks extracted: {len(pptx_data['text_content'])}"
            p.level = 1

            p = tf.add_paragraph()
            p.text = f"• Tables found: {len(pptx_data['tables'])}"
            p.level = 1

            # Show sample text content
            if pptx_data['text_content']:
                p = tf.add_paragraph()
                p.text = "• Sample content:"
                p.level = 1

                for i, text in enumerate(pptx_data['text_content'][:3]):
                    if text.strip():
                        p = tf.add_paragraph()
                        p.text = f"  - {text[:100]}{'...' if len(text) > 100 else ''}"
                        p.level = 2

        # Word Document Data slide (if Word document was uploaded)
        if docx_data:
            bullet_slide_layout = prs.slide_layouts[1]
            slide = prs.slides.add_slide(bullet_slide_layout)

            # Apply template structure
            if use_template_styling:
                slide = template_analyzer.apply_template_structure(slide, 'title_and_content')

            title = slide.shapes.title
            body = slide.placeholders[1]

            title.text = "Word Document Analysis Results"
            title_paragraph = title.text_frame.paragraphs[0]
            title_paragraph.font.color.rgb = primary_color
            title_paragraph.font.name = primary_font

            tf = body.text_frame
            doc_stats = docx_data['document_stats']
            tf.text = f"Processed document with {doc_stats['total_words']:,} words"

            p = tf.add_paragraph()
            p.text = f"• Tables extracted: {doc_stats['total_tables']}"
            p.level = 1

            p = tf.add_paragraph()
            p.text = f"• Data tables found: {doc_stats['data_tables_found']}"
            p.level = 1

            p = tf.add_paragraph()
            p.text = f"• Key points identified: {doc_stats['key_points_found']}"
            p.level = 1

            p = tf.add_paragraph()
            p.text = f"• Decisions captured: {doc_stats['decisions_found']}"
            p.level = 1

            p = tf.add_paragraph()
            p.text = f"• Metrics found: {doc_stats['metrics_found']}"
            p.level = 1

            # Document metadata slide
            if docx_data['document_structure']['metadata']:
                bullet_slide_layout = prs.slide_layouts[1]
                slide = prs.slides.add_slide(bullet_slide_layout)

                # Apply template structure
                if use_template_styling:
                    slide = template_analyzer.apply_template_structure(slide, 'title_and_content')

                title = slide.shapes.title
                body = slide.placeholders[1]

                title.text = "Document Information"
                title_paragraph = title.text_frame.paragraphs[0]
                title_paragraph.font.color.rgb = primary_color
                title_paragraph.font.name = primary_font

                tf = body.text_frame
                metadata = docx_data['document_structure']['metadata']

                tf.text = "Document Properties"

                if metadata.get('title'):
                    p = tf.add_paragraph()
                    p.text = f"• Title: {metadata['title']}"
                    p.level = 1

                if metadata.get('author'):
                    p = tf.add_paragraph()
                    p.text = f"• Author: {metadata['author']}"
                    p.level = 1

                if metadata.get('created'):
                    p = tf.add_paragraph()
                    p.text = f"• Created: {metadata['created']}"
                    p.level = 1

                if metadata.get('subject'):
                    p = tf.add_paragraph()
                    p.text = f"• Subject: {metadata['subject']}"
                    p.level = 1

            # Key findings slide from Word document
            if docx_data['processed_content']['key_points'] or docx_data['processed_content']['decisions']:
                bullet_slide_layout = prs.slide_layouts[1]
                slide = prs.slides.add_slide(bullet_slide_layout)

                # Apply template structure
                if use_template_styling:
                    slide = template_analyzer.apply_template_structure(slide, 'title_and_content')

                title = slide.shapes.title
                body = slide.placeholders[1]

                title.text = "Key Findings from Document"
                title_paragraph = title.text_frame.paragraphs[0]
                title_paragraph.font.color.rgb = primary_color
                title_paragraph.font.name = primary_font

                tf = body.text_frame
                tf.text = "Important Points and Decisions"

                # Add key points
                key_points = docx_data['processed_content']['key_points'][:5]
                if key_points:
                    p = tf.add_paragraph()
                    p.text = "Key Points:"
                    p.level = 1

                    for point in key_points:
                        p = tf.add_paragraph()
                        p.text = f"• {point[:150]}{'...' if len(point) > 150 else ''}"
                        p.level = 2

                # Add decisions
                decisions = docx_data['processed_content']['decisions'][:3]
                if decisions:
                    p = tf.add_paragraph()
                    p.text = "Decisions Made:"
                    p.level = 1

                    for decision in decisions:
                        p = tf.add_paragraph()
                        p.text = f"• {decision[:150]}{'...' if len(decision) > 150 else ''}"
                        p.level = 2

            # Data tables slide from Word document
            if docx_data['processed_content']['data_tables']:
                bullet_slide_layout = prs.slide_layouts[1]
                slide = prs.slides.add_slide(bullet_slide_layout)

                # Apply template structure
                if use_template_styling:
                    slide = template_analyzer.apply_template_structure(slide, 'title_and_content')

                title = slide.shapes.title
                body = slide.placeholders[1]

                title.text = "Extracted Data Tables"
                title_paragraph = title.text_frame.paragraphs[0]
                title_paragraph.font.color.rgb = primary_color
                title_paragraph.font.name = primary_font

                tf = body.text_frame
                data_tables = docx_data['processed_content']['data_tables']
                tf.text = f"Found {len(data_tables)} analyzable data tables"

                for i, table_info in enumerate(data_tables[:3]):  # Show first 3 tables
                    p = tf.add_paragraph()
                    shape = table_info['shape']
                    numeric_cols = table_info['numeric_columns']
                    p.text = f"• Table {i+1}: {shape[0]} rows × {shape[1]} columns ({numeric_cols} numeric)"
                    p.level = 1

                    # Show sample data from largest table
                    if i == 0 and table_info['dataframe'] is not None:
                        df_sample = table_info['dataframe']
                        if not df_sample.empty:
                            p = tf.add_paragraph()
                            p.text = "Sample columns:"
                            p.level = 1

                            for col in list(df_sample.columns)[:4]:  # Show first 4 columns
                                p = tf.add_paragraph()
                                p.text = f"  - {col}"
                                p.level = 2

        # Data Overview slide
        if df is not None and insights:
            bullet_slide_layout = prs.slide_layouts[1]
            slide = prs.slides.add_slide(bullet_slide_layout)

            # Apply template structure
            if use_template_styling:
                slide = template_analyzer.apply_template_structure(slide, 'title_and_content')

            title = slide.shapes.title
            body = slide.placeholders[1]

            title.text = "Data Structure Overview"
            title_paragraph = title.text_frame.paragraphs[0]
            title_paragraph.font.color.rgb = primary_color
            title_paragraph.font.name = primary_font

            tf = body.text_frame
            tf.text = "Column Analysis"

            # Show top columns with insights
            for col_insight in insights['column_insights'][:8]:
                p = tf.add_paragraph()
                p.text = f"• {col_insight['column']} ({col_insight['type']})"
                p.level = 1

                if col_insight['missing_pct'] > 0:
                    p = tf.add_paragraph()
                    p.text = f"  Missing: {col_insight['missing_pct']:.1f}%"
                    p.level = 2

        # Recommendations slide
        recommendations_layout = prs.slide_layouts[1]
        slide = prs.slides.add_slide(recommendations_layout)

        # Apply template structure
        if use_template_styling:
            slide = template_analyzer.apply_template_structure(slide, 'title_and_content')

        title = slide.shapes.title
        body = slide.placeholders[1]

        title.text = "SAP Recommendations"
        title_paragraph = title.text_frame.paragraphs[0]
        title_paragraph.font.color.rgb = primary_color
        title_paragraph.font.name = primary_font

        tf = body.text_frame
        tf.text = "Next Steps for Data Processing"

        recommendations = [
            "Implement data quality monitoring",
            "Establish automated data validation",
            "Create standardized reporting templates",
            "Set up regular data governance reviews",
            "Consider SAP integration opportunities"
        ]

        for rec in recommendations:
            p = tf.add_paragraph()
            p.text = f"• {rec}"
            p.level = 1

        # Save to buffer
        ppt_buffer = BytesIO()
        prs.save(ppt_buffer)
        ppt_buffer.seek(0)

        return ppt_buffer

    except Exception as e:
        st.error(f"Error generating PowerPoint report: {str(e)}")
        return None

# Main processing logic
if uploaded_file:
    file_content = uploaded_file.getvalue()
    file_extension = uploaded_file.name.split('.')[-1].lower()

    with st.spinner("Processing file..."):
        if file_extension == 'docx':
            # Process Word document file
            st.markdown("### 📄 Word Document Analysis Results")

            docx_data = sap_processor.extract_word_document_data(file_content)

            if docx_data:
                # Display Word document analysis
                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.markdown('<div class="sap-card">', unsafe_allow_html=True)
                    st.markdown(f'<div class="sap-metric-value">{docx_data["document_stats"]["total_words"]:,}</div>', unsafe_allow_html=True)
                    st.markdown('<div class="sap-metric-label">Total Words</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                with col2:
                    st.markdown('<div class="sap-card">', unsafe_allow_html=True)
                    st.markdown(f'<div class="sap-metric-value">{docx_data["document_stats"]["total_tables"]}</div>', unsafe_allow_html=True)
                    st.markdown('<div class="sap-metric-label">Tables</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                with col3:
                    st.markdown('<div class="sap-card">', unsafe_allow_html=True)
                    st.markdown(f'<div class="sap-metric-value">{docx_data["document_stats"]["data_tables_found"]}</div>', unsafe_allow_html=True)
                    st.markdown('<div class="sap-metric-label">Data Tables</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                with col4:
                    st.markdown('<div class="sap-card">', unsafe_allow_html=True)
                    st.markdown(f'<div class="sap-metric-value">{docx_data["document_stats"]["key_points_found"]}</div>', unsafe_allow_html=True)
                    st.markdown('<div class="sap-metric-label">Key Points</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                # Additional stats row
                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.markdown('<div class="sap-card">', unsafe_allow_html=True)
                    st.markdown(f'<div class="sap-metric-value">{docx_data["document_stats"]["bullet_points"]}</div>', unsafe_allow_html=True)
                    st.markdown('<div class="sap-metric-label">Bullet Points</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                with col2:
                    st.markdown('<div class="sap-card">', unsafe_allow_html=True)
                    st.markdown(f'<div class="sap-metric-value">{docx_data["document_stats"]["decisions_found"]}</div>', unsafe_allow_html=True)
                    st.markdown('<div class="sap-metric-label">Decisions</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                with col3:
                    st.markdown('<div class="sap-card">', unsafe_allow_html=True)
                    st.markdown(f'<div class="sap-metric-value">{docx_data["document_stats"]["metrics_found"]}</div>', unsafe_allow_html=True)
                    st.markdown('<div class="sap-metric-label">Metrics</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                with col4:
                    st.markdown('<div class="sap-card">', unsafe_allow_html=True)
                    metadata = docx_data['document_structure']['metadata']
                    author = metadata.get('author', 'Unknown')[:10] + ('...' if len(metadata.get('author', '')) > 10 else '')
                    st.markdown(f'<div class="sap-metric-value">{author}</div>', unsafe_allow_html=True)
                    st.markdown('<div class="sap-metric-label">Author</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                # Document metadata section
                if docx_data['document_structure']['metadata']:
                    st.markdown("#### 📋 Document Metadata")
                    metadata = docx_data['document_structure']['metadata']

                    col1, col2 = st.columns(2)
                    with col1:
                        if metadata.get('title'):
                            st.write(f"**Title:** {metadata['title']}")
                        if metadata.get('author'):
                            st.write(f"**Author:** {metadata['author']}")
                        if metadata.get('subject'):
                            st.write(f"**Subject:** {metadata['subject']}")

                    with col2:
                        if metadata.get('created'):
                            st.write(f"**Created:** {metadata['created']}")
                        if metadata.get('modified'):
                            st.write(f"**Modified:** {metadata['modified']}")
                        if metadata.get('last_modified_by'):
                            st.write(f"**Last Modified By:** {metadata['last_modified_by']}")

                # Show extracted data tables as DataFrames
                if docx_data['processed_content']['data_tables']:
                    st.markdown("#### 📊 Extracted Data Tables")

                    for i, table_data in enumerate(docx_data['processed_content']['data_tables']):
                        df_table = table_data['dataframe']
                        st.markdown(f"**Table {i+1}** (Shape: {table_data['shape']}, Numeric columns: {table_data['numeric_columns']})")
                        st.dataframe(df_table, use_container_width=True)

                        # Add option to use this table for analysis
                        if st.button(f"📈 Analyze Table {i+1}", key=f"analyze_table_{i}"):
                            # Analyze the extracted DataFrame using existing pipeline
                            quality_metrics = sap_processor.analyze_data_quality(df_table)
                            insights = sap_processor.generate_basic_insights(df_table)

                            if quality_metrics:
                                st.markdown("##### Data Quality Assessment")
                                col1, col2, col3 = st.columns(3)

                                with col1:
                                    st.metric("Completeness", f"{quality_metrics['completeness_pct']:.1f}%")
                                with col2:
                                    st.metric("Quality Level", quality_metrics['quality_level'])
                                with col3:
                                    st.metric("Numeric Columns", quality_metrics['numeric_columns'])

                            if insights and 'summary_stats' in insights and not insights['summary_stats'].empty:
                                st.markdown("##### Summary Statistics")
                                st.dataframe(insights['summary_stats'], use_container_width=True)

                # Show content analysis
                st.markdown("#### 🔍 Content Analysis")

                tab1, tab2, tab3, tab4 = st.tabs(["Key Points", "Decisions", "Metrics", "All Text"])

                with tab1:
                    if docx_data['processed_content']['key_points']:
                        for i, point in enumerate(docx_data['processed_content']['key_points'][:10]):
                            st.write(f"• {point}")
                    else:
                        st.info("No key points automatically identified.")

                with tab2:
                    if docx_data['processed_content']['decisions']:
                        for i, decision in enumerate(docx_data['processed_content']['decisions'][:10]):
                            st.write(f"• {decision}")
                    else:
                        st.info("No decisions automatically identified.")

                with tab3:
                    if docx_data['processed_content']['metrics']:
                        for i, metric in enumerate(docx_data['processed_content']['metrics'][:10]):
                            st.write(f"• {metric}")
                    else:
                        st.info("No metrics automatically identified.")

                with tab4:
                    if docx_data['processed_content']['text_content']:
                        for i, text in enumerate(docx_data['processed_content']['text_content'][:20]):
                            if text.strip():
                                st.write(f"{i+1}. {text}")
                    else:
                        st.info("No text content found.")

                # Headers and footers
                if docx_data['document_structure']['headers'] or docx_data['document_structure']['footers']:
                    with st.expander("📑 Headers & Footers", expanded=False):
                        if docx_data['document_structure']['headers']:
                            st.markdown("**Headers:**")
                            for header in docx_data['document_structure']['headers']:
                                st.write(f"- {header['text']} ({header['style']})")

                        if docx_data['document_structure']['footers']:
                            st.markdown("**Footers:**")
                            for footer in docx_data['document_structure']['footers']:
                                st.write(f"- {footer['text']} ({footer['style']})")

                # Document structure details
                with st.expander("🏗️ Document Structure Analysis", expanded=False):
                    st.markdown("**Paragraph Analysis:**")

                    # Group paragraphs by type
                    headings = [p for p in docx_data['document_structure']['paragraphs'] if p['is_heading']]
                    bullets = [p for p in docx_data['document_structure']['paragraphs'] if p['is_bullet']]
                    numbered = [p for p in docx_data['document_structure']['paragraphs'] if p['is_numbered']]

                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Headings", len(headings))
                    with col2:
                        st.metric("Bullet Lists", len(bullets))
                    with col3:
                        st.metric("Numbered Lists", len(numbered))

                    if headings:
                        st.markdown("**Document Headings:**")
                        for heading in headings[:10]:
                            st.write(f"- {heading['text']} ({heading['style']})")

                # Generate report button for Word document
                if st.button("📊 Generate SAP Analysis Report", type="primary", key="word_report"):
                    with st.spinner("Generating comprehensive SAP report from Word document..."):
                        # Create a combined dataset for reporting
                        combined_data = None

                        # If we have data tables, use the largest one as primary data
                        if docx_data['processed_content']['data_tables']:
                            largest_table = max(docx_data['processed_content']['data_tables'],
                                              key=lambda x: x['dataframe'].shape[0] * x['dataframe'].shape[1])
                            combined_data = largest_table['dataframe']

                        # Generate insights from document content
                        doc_insights = {
                            'document_type': 'Word Document',
                            'total_words': docx_data['document_stats']['total_words'],
                            'key_findings': docx_data['processed_content']['key_points'][:5],
                            'decisions_made': docx_data['processed_content']['decisions'][:5],
                            'metrics_identified': docx_data['processed_content']['metrics'][:5],
                            'data_tables_count': docx_data['document_stats']['data_tables_found'],
                            'metadata': docx_data['document_structure']['metadata']
                        }

                        report_buffer = generate_sap_powerpoint_report(combined_data, doc_insights, None, docx_data)

                        if report_buffer:
                            st.success("✅ SAP report generated successfully!")
                            st.download_button(
                                label="📎 Download SAP Word Analysis Report",
                                data=report_buffer.getvalue(),
                                file_name=f"SAP_Word_Analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pptx",
                                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
                            )

        elif file_extension == 'pptx':
            # Process PowerPoint file
            st.markdown("### =� PowerPoint Analysis Results")

            pptx_data = sap_processor.extract_powerpoint_data(file_content)

            if pptx_data:
                # Display PowerPoint analysis
                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.markdown('<div class="sap-card">', unsafe_allow_html=True)
                    st.markdown(f'<div class="sap-metric-value">{pptx_data["slide_count"]}</div>', unsafe_allow_html=True)
                    st.markdown('<div class="sap-metric-label">Slides</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                with col2:
                    st.markdown('<div class="sap-card">', unsafe_allow_html=True)
                    st.markdown(f'<div class="sap-metric-value">{len(pptx_data["text_content"])}</div>', unsafe_allow_html=True)
                    st.markdown('<div class="sap-metric-label">Text Blocks</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                with col3:
                    st.markdown('<div class="sap-card">', unsafe_allow_html=True)
                    st.markdown(f'<div class="sap-metric-value">{len(pptx_data["tables"])}</div>', unsafe_allow_html=True)
                    st.markdown('<div class="sap-metric-label">Tables</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                with col4:
                    total_words = sum(len(text.split()) for text in pptx_data["text_content"])
                    st.markdown('<div class="sap-card">', unsafe_allow_html=True)
                    st.markdown(f'<div class="sap-metric-value">{total_words}</div>', unsafe_allow_html=True)
                    st.markdown('<div class="sap-metric-label">Total Words</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                # Show slide summaries
                if st.checkbox("Show slide details", value=False):
                    for slide_data in pptx_data['slides']:
                        with st.expander(f"Slide {slide_data['slide_number']}: {slide_data['title'] or 'Untitled'}", expanded=False):
                            if slide_data['text_content']:
                                st.markdown("**Text Content:**")
                                for text in slide_data['text_content']:
                                    if text.strip():
                                        st.write(f"- {text}")

                            if slide_data['tables']:
                                st.markdown("**Tables:**")
                                for i, table in enumerate(slide_data['tables']):
                                    st.markdown(f"Table {i+1}:")
                                    try:
                                        df_table = pd.DataFrame(table[1:], columns=table[0])
                                        st.dataframe(df_table, width='stretch')
                                    except:
                                        st.write("Table structure could not be parsed")

                # Generate report button for PowerPoint
                if st.button("=� Generate Analysis Report", type="primary"):
                    with st.spinner("Generating SAP report..."):
                        report_buffer = generate_sap_powerpoint_report(None, None, pptx_data)

                        if report_buffer:
                            st.success(" Report generated successfully!")
                            st.download_button(
                                label="=� Download SAP Report",
                                data=report_buffer.getvalue(),
                                file_name=f"SAP_PowerPoint_Analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pptx",
                                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
                            )

        else:
            # Process CSV/Excel files
            df = sap_processor.process_csv_excel(file_content, uploaded_file.name)

            if df is not None:
                # Data processing options
                if handle_missing == "Remove rows":
                    df = df.dropna()
                elif handle_missing == "Fill with mean":
                    numeric_cols = df.select_dtypes(include=[np.number]).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                elif handle_missing == "Fill with median":
                    numeric_cols = df.select_dtypes(include=[np.number]).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())

                if remove_duplicates:
                    df = df.drop_duplicates()

                # Analyze data
                quality_metrics = sap_processor.analyze_data_quality(df)
                insights = sap_processor.generate_basic_insights(df)

                # Display results
                st.markdown("### =� SAP Data Analysis Dashboard")

                # Quality metrics
                if quality_metrics:
                    col1, col2, col3, col4 = st.columns(4)

                    with col1:
                        st.markdown('<div class="sap-card">', unsafe_allow_html=True)
                        st.markdown(f'<div class="sap-metric-value">{quality_metrics["total_records"]:,}</div>', unsafe_allow_html=True)
                        st.markdown('<div class="sap-metric-label">Records</div>', unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)

                    with col2:
                        st.markdown('<div class="sap-card">', unsafe_allow_html=True)
                        st.markdown(f'<div class="sap-metric-value">{quality_metrics["completeness_pct"]:.1f}%</div>', unsafe_allow_html=True)
                        st.markdown('<div class="sap-metric-label">Complete</div>', unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)

                    with col3:
                        st.markdown('<div class="sap-card">', unsafe_allow_html=True)
                        st.markdown(f'<div class="sap-metric-value">{quality_metrics["numeric_columns"]}</div>', unsafe_allow_html=True)
                        st.markdown('<div class="sap-metric-label">Numeric Cols</div>', unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)

                    with col4:
                        quality_status = f'sap-status-{quality_metrics["quality_color"]}'
                        st.markdown(f'<div class="{quality_status}">{quality_metrics["quality_level"]}</div>', unsafe_allow_html=True)

                # Data preview
                st.markdown("#### =� Data Preview")
                st.dataframe(df.head(10), width='stretch')

                # Summary statistics
                if insights and 'summary_stats' in insights and not insights['summary_stats'].empty:
                    st.markdown("#### =� Summary Statistics")
                    st.dataframe(insights['summary_stats'], width='stretch')

                # Visualizations
                if include_charts:
                    st.markdown("#### =� Data Visualizations")

                    fig = create_sap_visualization(df)
                    if fig:
                        st.plotly_chart(fig, width='stretch')

                # Column insights
                st.markdown("#### 🔍 Column Analysis")

                col_df = pd.DataFrame(insights['column_insights'])
                col_display = col_df[['column', 'type', 'missing_pct', 'unique_values']].round(2)
                st.dataframe(col_display, width='stretch')

                # Generate report button
                if st.button("=� Generate SAP Report", type="primary"):
                    with st.spinner("Generating professional SAP report..."):
                        report_buffer = generate_sap_powerpoint_report(df, insights)

                        if report_buffer:
                            st.success(" SAP report generated successfully!")
                            st.download_button(
                                label="=� Download SAP Report",
                                data=report_buffer.getvalue(),
                                file_name=f"SAP_Data_Analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pptx",
                                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
                            )



# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6a6d70; font-size: 0.9rem; padding: 1rem;">
    🚀 <strong>Universal Automation Platform - SAP Edition</strong> |
    Enterprise Data Processing & Analytics |
    Powered by SAP Corporate Standards
</div>
""", unsafe_allow_html=True)
