"""
Styles Module
=============
Custom CSS styling for the Streamlit dashboard.
Provides professional UI/UX with consistent design patterns.
"""

import streamlit as st


def apply_custom_css():
    """Apply custom CSS styles to the Streamlit app."""
    
    custom_css = """
    <style>
        /* Hide Streamlit page navigation menu */
        [data-testid="stSidebarNav"] {
            display: none;
        }
        
        /* Main container styling */
        .main {
            padding: 2rem;
        }
        
        /* Header styling */
        h1 {
            color: #2C5F2D;
            font-family: 'Helvetica Neue', sans-serif;
            font-weight: 700;
            padding-bottom: 0.5rem;
            border-bottom: 3px solid #97BC62;
        }
        
        h2 {
            color: #4A7C59;
            font-weight: 600;
            margin-top: 2rem;
        }
        
        h3 {
            color: #5A8F6A;
            font-weight: 500;
        }
        
        /* Sidebar styling */
        .css-1d391kg {
            background-color: #F5F7F5;
        }
        
        [data-testid="stSidebar"] {
            background-color: #F5F7F5;
            padding: 2rem 1rem;
        }
        
        [data-testid="stSidebar"] h1 {
            color: #2C5F2D;
            font-size: 1.5rem;
            border-bottom: 2px solid #97BC62;
        }
        
        /* Metric cards styling */
        [data-testid="stMetricValue"] {
            font-size: 2rem;
            font-weight: 700;
            color: #2C5F2D;
        }
        
        [data-testid="stMetricLabel"] {
            font-size: 1rem;
            color: #5A8F6A;
            font-weight: 500;
        }
        
        /* Button styling */
        .stButton > button {
            background-color: #4A7C59;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.5rem 1.5rem;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .stButton > button:hover {
            background-color: #2C5F2D;
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
            transform: translateY(-2px);
        }
        
        /* Info boxes */
        .stAlert {
            border-radius: 8px;
            padding: 1rem;
        }
        
        /* Expander styling */
        .streamlit-expanderHeader {
            background-color: #E8F5E9;
            border-radius: 8px;
            font-weight: 600;
            color: #2C5F2D;
        }
        
        /* Dataframe styling */
        .dataframe {
            font-size: 0.9rem;
            border-radius: 8px;
            overflow: hidden;
        }
        
        .dataframe th {
            background-color: #4A7C59;
            color: white;
            font-weight: 600;
            text-align: left;
            padding: 0.75rem;
        }
        
        .dataframe td {
            padding: 0.5rem 0.75rem;
            border-bottom: 1px solid #E0E0E0;
        }
        
        .dataframe tr:hover {
            background-color: #F5F7F5;
        }
        
        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 1rem;
        }
        
        .stTabs [data-baseweb="tab"] {
            border-radius: 8px 8px 0 0;
            padding: 0.75rem 1.5rem;
            background-color: #E8F5E9;
            color: #2C5F2D;
            font-weight: 600;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: #4A7C59;
            color: white;
        }
        
        /* Select box styling */
        .stSelectbox > div > div {
            border-radius: 8px;
            border: 2px solid #97BC62;
        }
        
        /* Slider styling */
        .stSlider > div > div > div {
            background-color: #97BC62;
        }
        
        /* Card styling for content sections */
        .content-card {
            background-color: white;
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            margin-bottom: 1.5rem;
            border-left: 4px solid #4A7C59;
        }
        
        /* KPI card styling */
        .kpi-card {
            background: linear-gradient(135deg, #E8F5E9 0%, #F5F7F5 100%);
            border-radius: 12px;
            padding: 1.5rem;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }
        
        .kpi-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        }
        
        .kpi-value {
            font-size: 2.5rem;
            font-weight: 700;
            color: #2C5F2D;
            margin: 0.5rem 0;
        }
        
        .kpi-label {
            font-size: 1rem;
            color: #5A8F6A;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        /* Section divider */
        .section-divider {
            height: 3px;
            background: linear-gradient(90deg, #4A7C59 0%, #97BC62 50%, #4A7C59 100%);
            margin: 2rem 0;
            border-radius: 2px;
        }
        
        /* Highlight box */
        .highlight-box {
            background-color: #FFF9E6;
            border-left: 4px solid #FFD700;
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
        }
        
        /* Success box */
        .success-box {
            background-color: #E8F5E9;
            border-left: 4px solid #4A7C59;
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
        }
        
        /* Warning box */
        .warning-box {
            background-color: #FFF3E0;
            border-left: 4px solid #FF8C00;
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
        }
        
        /* Footer styling */
        .footer {
            text-align: center;
            color: #666;
            font-size: 0.9rem;
            padding: 2rem 0;
            border-top: 2px solid #E0E0E0;
            margin-top: 3rem;
        }
        
        /* Loading spinner */
        .stSpinner > div {
            border-top-color: #4A7C59 !important;
        }
        
        /* Plotly chart container */
        .js-plotly-plot {
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        
        /* Radio button styling */
        .stRadio > div {
            gap: 0.5rem;
        }
        
        .stRadio > div > label {
            background-color: #E8F5E9;
            padding: 0.5rem 1rem;
            border-radius: 8px;
            transition: all 0.3s ease;
        }
        
        .stRadio > div > label:hover {
            background-color: #C8E6C9;
        }
        
        /* Download button */
        .stDownloadButton > button {
            background-color: #2C5F2D;
            color: white;
            border-radius: 8px;
            font-weight: 600;
        }
        
        /* Progress bar */
        .stProgress > div > div {
            background-color: #4A7C59;
        }
    </style>
    """
    
    st.markdown(custom_css, unsafe_allow_html=True)


def create_metric_card(label: str, value: str, icon: str = "📊") -> str:
    """
    Create HTML for a custom metric card.
    
    Args:
        label: Metric label
        value: Metric value
        icon: Emoji icon
        
    Returns:
        HTML string for metric card
    """
    return f"""
    <div class="kpi-card">
        <div style="font-size: 2rem;">{icon}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-label">{label}</div>
    </div>
    """


def create_section_header(title: str, subtitle: str = "") -> str:
    """
    Create HTML for a styled section header.
    
    Args:
        title: Section title
        subtitle: Optional subtitle
        
    Returns:
        HTML string for section header
    """
    subtitle_html = f"<p style='color: #666; font-size: 1.1rem; margin-top: 0.5rem;'>{subtitle}</p>" if subtitle else ""
    
    return f"""
    <div style="margin: 2rem 0 1rem 0;">
        <h2 style="color: #2C5F2D; margin-bottom: 0;">{title}</h2>
        {subtitle_html}
        <div class="section-divider"></div>
    </div>
    """


def create_highlight_box(content: str, box_type: str = "info") -> str:
    """
    Create HTML for a highlighted content box.
    
    Args:
        content: Content to display
        box_type: Type of box ('info', 'success', 'warning', 'highlight')
        
    Returns:
        HTML string for highlight box
    """
    box_classes = {
        'info': 'content-card',
        'success': 'success-box',
        'warning': 'warning-box',
        'highlight': 'highlight-box'
    }
    
    box_class = box_classes.get(box_type, 'content-card')
    
    return f"""
    <div class="{box_class}">
        {content}
    </div>
    """
