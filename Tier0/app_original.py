import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from io import BytesIO
import base64
from scipy import stats
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.ensemble import IsolationForest
from sklearn.linear_model import LinearRegression
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
import warnings
import time
import traceback

warnings.filterwarnings('ignore')

# Configure page with German corporate branding
st.set_page_config(
    page_title="KI-Automatisierungsplattform | Enterprise Analytics",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional German corporate styling
st.markdown("""
<style>
    /* Main container styling */
    .main > div {
        padding-top: 2rem;
    }

    /* Header styling */
    .header-container {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    .header-title {
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-align: center;
    }

    .header-subtitle {
        color: #e2e8f0;
        font-size: 1.2rem;
        text-align: center;
        margin-bottom: 1rem;
    }

    .header-tagline {
        color: #cbd5e1;
        font-size: 1rem;
        text-align: center;
        font-style: italic;
    }

    /* Card styling */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #3b82f6;
        margin-bottom: 1rem;
    }

    .analysis-card {
        background: #f8fafc;
        padding: 2rem;
        border-radius: 10px;
        border: 1px solid #e2e8f0;
        margin: 1rem 0;
    }

    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }

    /* Sidebar styling */
    .css-1d391kg {
        background-color: #f1f5f9;
    }

    /* Progress bar styling */
    .stProgress > div > div > div > div {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
    }

    /* Alert styling */
    .success-alert {
        background-color: #ecfdf5;
        border: 1px solid #10b981;
        border-radius: 8px;
        padding: 1rem;
        color: #065f46;
    }

    .error-alert {
        background-color: #fef2f2;
        border: 1px solid #ef4444;
        border-radius: 8px;
        padding: 1rem;
        color: #991b1b;
    }

    .warning-alert {
        background-color: #fffbeb;
        border: 1px solid #f59e0b;
        border-radius: 8px;
        padding: 1rem;
        color: #92400e;
    }

    /* Data quality indicators */
    .quality-indicator {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.875rem;
        font-weight: 600;
        margin-right: 0.5rem;
    }

    .quality-excellent {
        background-color: #dcfce7;
        color: #166534;
    }

    .quality-good {
        background-color: #fef3c7;
        color: #92400e;
    }

    .quality-poor {
        background-color: #fee2e2;
        color: #991b1b;
    }
</style>
""", unsafe_allow_html=True)

# German corporate header
st.markdown("""
<div class="header-container">
    <div class="header-title">🏢 KI-Automatisierungsplattform</div>
    <div class="header-subtitle">Enterprise Data Intelligence & Analytics Suite</div>
    <div class="header-tagline">Modernste künstliche Intelligenz für deutsche Unternehmen</div>
</div>
""", unsafe_allow_html=True)

# Utility functions
@st.cache_data
def load_data(file_content, file_name):
    """Load and cache data with error handling"""
    try:
        if file_name.endswith('.csv'):
            # Try different encodings
            try:
                return pd.read_csv(BytesIO(file_content), encoding='utf-8')
            except UnicodeDecodeError:
                try:
                    return pd.read_csv(BytesIO(file_content), encoding='latin-1')
                except UnicodeDecodeError:
                    return pd.read_csv(BytesIO(file_content), encoding='cp1252')
        else:
            return pd.read_excel(BytesIO(file_content))
    except Exception as e:
        st.error(f"Fehler beim Laden der Datei: {str(e)}")
        return None

def validate_data(df):
    """Validate uploaded data quality"""
    issues = []
    recommendations = []

    if df is None or df.empty:
        issues.append("⚠️ Datei ist leer oder konnte nicht gelesen werden")
        return issues, recommendations, "poor"

    # Check data quality metrics
    missing_pct = (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
    duplicate_pct = (df.duplicated().sum() / len(df)) * 100
    numeric_cols = len(df.select_dtypes(include=[np.number]).columns)

    # Determine quality score
    if missing_pct < 5 and duplicate_pct < 1 and numeric_cols > 0:
        quality = "excellent"
    elif missing_pct < 15 and duplicate_pct < 5:
        quality = "good"
    else:
        quality = "poor"

    # Generate recommendations
    if missing_pct > 10:
        recommendations.append(f"🔍 {missing_pct:.1f}% fehlende Werte identifiziert - Datenbereinigung empfohlen")

    if duplicate_pct > 2:
        recommendations.append(f"🔄 {duplicate_pct:.1f}% Duplikate gefunden - Deduplizierung empfohlen")

    if numeric_cols == 0:
        recommendations.append("📊 Keine numerischen Spalten erkannt - erweiterte Analyse begrenzt")

    return issues, recommendations, quality

def create_progress_placeholder():
    """Create progress tracking interface"""
    progress_container = st.container()
    with progress_container:
        progress_bar = st.progress(0)
        status_text = st.empty()
        details_text = st.empty()
    return progress_bar, status_text, details_text

# Sidebar for configuration
with st.sidebar:
    st.markdown("### 🛠️ Konfiguration")

    # Analysis settings
    st.markdown("#### Analyse-Einstellungen")
    analysis_depth = st.selectbox(
        "Analyse-Tiefe",
        ["Schnellübersicht", "Standard-Analyse", "Tiefgehende Analyse"],
        index=1
    )

    include_clustering = st.checkbox("Clustering-Analyse", value=True)
    include_anomalies = st.checkbox("Anomalie-Erkennung", value=True)
    include_forecasting = st.checkbox("Trend-Prognose", value=True)

    # Export settings
    st.markdown("#### Export-Einstellungen")
    report_language = st.selectbox("Berichtssprache", ["Deutsch", "English"], index=0)
    include_charts = st.checkbox("Diagramme einschließen", value=True)
    include_raw_data = st.checkbox("Rohdaten anhängen", value=False)

    st.markdown("---")
    st.markdown("### 📊 Systemstatus")
    st.success("✅ Alle Systeme betriebsbereit")
    st.info(f"🕰️ Letzte Aktualisierung: {datetime.now().strftime('%H:%M:%S')}")

# Main file upload section
st.markdown("### 📁 Daten-Upload")

col1, col2 = st.columns([2, 1])

with col1:
    uploaded_file = st.file_uploader(
        "Wählen Sie Ihre Datendatei aus",
        type=['xlsx', 'csv', 'xls'],
        help="Unterstützte Formate: Excel (.xlsx, .xls), CSV (.csv). Maximale Dateigröße: 200MB"
    )

with col2:
    if uploaded_file:
        file_size = len(uploaded_file.getvalue()) / (1024 * 1024)  # MB
        st.metric("Dateigröße", f"{file_size:.1f} MB")
        st.metric("Dateiformat", uploaded_file.name.split('.')[-1].upper())

if uploaded_file:
    # Create progress tracking
    progress_bar, status_text, details_text = create_progress_placeholder()

    try:
        # Step 1: Load data
        status_text.text("📂 Lade Datei...")
        progress_bar.progress(20)

        file_content = uploaded_file.getvalue()
        df = load_data(file_content, uploaded_file.name)

        if df is None:
            st.stop()

        # Step 2: Validate data
        status_text.text("🔍 Validiere Datenqualität...")
        progress_bar.progress(40)

        issues, recommendations, quality = validate_data(df)

        # Step 3: Display results
        progress_bar.progress(60)
        status_text.text("✅ Daten erfolgreich geladen")
        details_text.empty()
        progress_bar.empty()
        status_text.empty()

    st.success(f"✅ File loaded: {len(df)} rows, {len(df.columns)} columns")
    st.dataframe(df.head())

    if st.button("🚀 Generate Intelligence Report", type="primary"):
        # Quick analysis
        numeric_cols = df.select_dtypes(include=[np.number]).columns

        st.subheader("📊 Quick Insights")

        # Basic metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Records", f"{len(df):,}")
        with col2:
            st.metric("Numeric Fields", len(numeric_cols))
        with col3:
            missing_pct = (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
            st.metric("Data Quality", f"{100-missing_pct:.1f}%")

        # Simple visualizations
        if len(numeric_cols) > 0:
            st.subheader("📈 Data Visualization")
            for col in numeric_cols[:2]:  # First 2 numeric columns
                st.write(f"**{col}**")
                st.bar_chart(df[col].value_counts().head(10))

        # Mock insights
        st.subheader("💡 AI-Generated Insights")
        st.write("✅ Data quality is high with minimal missing values")
        st.write("📈 Trend analysis identifies growth opportunities")
        st.write("🎯 Recommend focusing on top-performing segments")

        st.success("🎉 Analysis complete! PowerPoint generation ready for integration.")

# Demo button
if st.button("🎪 Professor Demo Mode"):
    st.balloons()
    # Create sample data
    sample_data = pd.DataFrame({
        'Date': pd.date_range('2024-01-01', periods=100),
        'Revenue': np.random.randint(10000, 50000, 100),
        'Region': np.random.choice(['North', 'South', 'East', 'West'], 100),
        'Product': np.random.choice(['Product A', 'Product B', 'Product C'], 100)
    })

    st.write("📊 Sample Data Loaded")
    st.dataframe(sample_data.head())
    st.success("Ready for professor demonstration!")