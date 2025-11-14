"""
Configuration Module
====================
Central configuration file for the Citizen Science Wildlife Dashboard.
Contains all constants, paths, color schemes, and application settings.
"""

import os
from pathlib import Path

# ============================================================================
# PROJECT PATHS
# ============================================================================

# Get the base directory (parent of 'app' folder)
BASE_DIR = Path(__file__).parent.parent

# Data directory
DATA_DIR = BASE_DIR / "data"

# Output directories
IMG_DIR = BASE_DIR / "img"
HTML_DIR = BASE_DIR / "html"

# Documentation directory
DOC_DIR = BASE_DIR / "doc"

# Generated visualization files
GENERATED_IMAGES = {
    'correlation_daily_sequences': IMG_DIR / 'correlation_daily_sequences.png',
    'correlation_comparison': IMG_DIR / 'correlation_comparison.png',
    'correlation_daily_sequences_no_ocuniculus': IMG_DIR / 'correlation_daily_sequences_no_ocuniculus.png',
    'species_richness_by_source': IMG_DIR / 'species_richness_by_source.png',
    'records_by_species_grid': IMG_DIR / 'records_by_species_grid.png',
    'panel_mapps_heat': IMG_DIR / 'panel_mapps_heat.png',
    'accumulated_curves_orders': IMG_DIR / 'accumulated_curves_orders.png',
    'tendencias_ordenes': IMG_DIR / 'tendencias_ordenes.png',
    'violin_log_records_platform': IMG_DIR / 'violin_log_records_platform.png'
}

GENERATED_MAPS = {
    'clusters_by_grid': HTML_DIR / 'mapa_clusters_por_grid.html',
    'heatmap_cameras': HTML_DIR / 'mapa_calor_con_utm_y_camaras.html'
}


# ============================================================================
# DATA FILES
# ============================================================================

DATA_FILES = {
    'citizen_science': DATA_DIR / 'dataset_CSsources_mod.csv',
    'gbif_shapefile': DATA_DIR / 'GBIFdata_CO.shp',
    'utm_grid': DATA_DIR / 'CO_UTM2.shp',
    'cameras': DATA_DIR / 'locCam3.csv',
    'silhouettes': DATA_DIR / 'siluetas.csv'
}


# ============================================================================
# COLOR PALETTES
# ============================================================================

# Data source color mapping
DATA_SOURCE_COLORS = {
    'Global Biodiversity': '#228B22',  # Forest Green
    'No Validation': '#C71585',         # Medium Violet Red
    'Sequences Record': '#4169E1',      # Royal Blue
    'Daily Record': '#FFD700'           # Gold
}

# Platform color mapping for GBIF sources
PLATFORM_COLORS = {
    'iMammalia': '#FF8C00',   # Dark Orange
    'iNaturalist': '#32CD32',  # Lime Green
    'Observation': '#4169E1',  # Royal Blue
}

# General palette for charts
CHART_COLORS = [
    '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
    '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'
]

# Heat map gradient
HEATMAP_GRADIENT = {
    0.0: 'blue',
    0.5: 'lime',
    0.7: 'yellow',
    1.0: 'red'
}


# ============================================================================
# APPLICATION SETTINGS
# ============================================================================

# Page configuration
PAGE_CONFIG = {
    'page_title': 'Citizen Science Wildlife Dashboard',
    'page_icon': '🦌',
    'layout': 'wide',
    'initial_sidebar_state': 'expanded'
}

# Map settings
MAP_CONFIG = {
    'center_lat': 37.6,
    'center_lon': -4.5,
    'default_zoom': 9,
    'tile_layer': 'OpenStreetMap'
}

# Chart settings
CHART_CONFIG = {
    'default_height': 500,
    'default_width': 800,
    'dpi': 300,
    'font_size': 12
}


# ============================================================================
# TEXT CONTENT
# ============================================================================

# Application header
APP_TITLE = "🦌 Citizen Science Wildlife Dashboard"
APP_SUBTITLE = "Interactive Intelligence Panel for Córdoba Province Wildlife Monitoring"

# Sidebar header
SIDEBAR_TITLE = "🎛️ Control Panel"

# Section titles
SECTION_TITLES = {
    'origin': '📚 Project Origin & Context',
    'data': '🔍 Data Exploration',
    'eda': '📊 Exploratory Data Analysis',
    'conclusions': '💡 Key Findings & Recommendations'
}

# About text
ABOUT_TEXT = """
### About This Dashboard

This interactive dashboard presents comprehensive analyses of wildlife monitoring data 
from the Córdoba province citizen science project. It integrates multiple data sources:

- **Camera Trap Records**: Direct observations from educational centers
- **GBIF Database**: Historical occurrences (2008-2023)
- **Citizen Science Platforms**: iMammalia, iNaturalist, Observation.org

The dashboard enables stakeholders to explore biodiversity patterns, identify hotspots, 
assess data quality, and make evidence-based conservation decisions.
"""


# ============================================================================
# FILTER OPTIONS
# ============================================================================

# Default filter values
DEFAULT_FILTERS = {
    'species': 'All',
    'grid': 'All',
    'source': 'All',
    'min_records': 0
}


# ============================================================================
# METRICS CONFIGURATION
# ============================================================================

# KPI card configuration
KPI_CONFIG = {
    'icon_size': 24,
    'delta_color': 'normal',
    'show_delta': True
}


# ============================================================================
# EXPORT SETTINGS
# ============================================================================

EXPORT_CONFIG = {
    'figure_format': 'png',
    'figure_dpi': 300,
    'csv_encoding': 'utf-8',
    'excel_engine': 'openpyxl'
}
