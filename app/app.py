"""
Citizen Science Wildlife Dashboard - Main Application
======================================================
Interactive intelligence panel for Córdoba Province wildlife monitoring.

Author: Generated for Citizen Science Project
Date: 2024
"""

import streamlit as st
import pandas as pd
from pathlib import Path

# Import custom modules
from config import (
    PAGE_CONFIG, APP_TITLE, APP_SUBTITLE, SIDEBAR_TITLE,
    SECTION_TITLES, ABOUT_TEXT, DEFAULT_FILTERS
)
from data_loader import (
    load_citizen_science_data, load_gbif_data, load_utm_grid,
    load_camera_locations, get_species_list, get_grid_list,
    get_data_sources, filter_data, get_summary_stats
)

# Import page modules
from pages import (
    show_origin_page,
    show_data_exploration_page,
    show_eda_page,
    show_conclusions_page
)
from styles import apply_custom_css


# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(**PAGE_CONFIG)
apply_custom_css()


# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

def init_session_state():
    """Initialize session state variables."""
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'origin'
    if 'data_loaded' not in st.session_state:
        st.session_state.data_loaded = False


# ============================================================================
# DATA LOADING
# ============================================================================

@st.cache_resource
def load_all_data():
    """Load all datasets and cache for performance."""
    data = {
        'citizen_science': load_citizen_science_data(),
        'gbif': load_gbif_data(),
        'utm_grid': load_utm_grid(),
        'cameras': load_camera_locations()
    }
    return data


# ============================================================================
# SIDEBAR
# ============================================================================

def render_sidebar(df):
    """Render sidebar with filters and navigation."""
    
    with st.sidebar:
        st.title(SIDEBAR_TITLE)
        st.markdown("---")
        
        # Navigation
        st.subheader("📍 Navigation")
        page = st.radio(
            "Go to section:",
            options=['origin', 'data', 'eda', 'conclusions'],
            format_func=lambda x: SECTION_TITLES[x],
            key='navigation'
        )
        
        st.markdown("---")
        
        # Filters
        st.subheader("🔍 Data Filters")
        
        # Species filter
        species_list = ['All'] + get_species_list(df)
        selected_species = st.selectbox(
            "Select Species",
            options=species_list,
            index=0,
            key='species_filter'
        )
        
        # Grid filter
        grid_list = ['All'] + get_grid_list(df)
        selected_grid = st.selectbox(
            "Select UTM Grid",
            options=grid_list,
            index=0,
            key='grid_filter'
        )
        
        # Data source filter
        source_list = ['All'] + get_data_sources(df)
        selected_source = st.selectbox(
            "Select Data Source",
            options=source_list,
            index=0,
            key='source_filter'
        )
        
        # Minimum records filter
        min_records = st.slider(
            "Minimum Records",
            min_value=0,
            max_value=int(df['Records'].max()),
            value=0,
            step=1,
            key='min_records_filter'
        )
        
        # Apply filters button
        apply_filters = st.button("🔄 Apply Filters", use_container_width=True)
        
        st.markdown("---")
        
        # About section
        with st.expander("ℹ️ About"):
            st.markdown(ABOUT_TEXT)
        
        # Dataset info
        with st.expander("📊 Dataset Info"):
            stats = get_summary_stats(df)
            st.metric("Total Records", f"{stats['total_records']:,}")
            st.metric("Unique Species", stats['unique_species'])
            st.metric("UTM Grids", stats['unique_grids'])
            st.metric("Data Sources", stats['unique_sources'])
        
        # Data sources information
        with st.expander("🗂️ Data Sources"):
            st.markdown("""
            **Primary Datasets:**
            
            1. **Citizen Science** (`dataset_CSsources_mod.csv`)
               - Daily Record: Daily presence/absence
               - Sequences Record: Camera trap sequences
               - No Validation: Community platforms
            
            2. **GBIF Historical** (`GBIFdata_CO.shp`)
               - 2008-2023 occurrence records
               - Multiple taxonomic orders
               - iMammalia, iNaturalist, Observation.org
            
            3. **UTM Spatial Grid** (`CO_UTM2.shp`)
               - 10×10 km grid cells
               - Córdoba province coverage
               - Spatial reference layer
            
            4. **Camera Traps** (`locCam3.csv`)
               - Camera deployment locations
               - School-based monitoring sites
               - 2024 initiative (800 students, 11 schools)
            """)
        
        return page, selected_species, selected_grid, selected_source, min_records, apply_filters


# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Main application logic."""
    
    # Initialize session state
    init_session_state()
    
    # Header
    st.title(APP_TITLE)
    st.markdown(f"*{APP_SUBTITLE}*")
    st.markdown("---")
    
    # Load data
    with st.spinner("Loading datasets..."):
        data = load_all_data()
        df = data['citizen_science']
    
    # Check if data loaded successfully
    if df.empty:
        st.error("❌ Failed to load data. Please check data files.")
        return
    
    # Render sidebar and get filters
    page, species, grid, source, min_records, apply_filters = render_sidebar(df)
    
    # Apply filters if requested
    if apply_filters or st.session_state.get('filters_applied', False):
        df_filtered = filter_data(df, species, grid, source, min_records)
        st.session_state.filters_applied = True
        
        # Show filter summary
        if species != 'All' or grid != 'All' or source != 'All' or min_records > 0:
            filter_summary = []
            if species != 'All':
                filter_summary.append(f"Species: **{species}**")
            if grid != 'All':
                filter_summary.append(f"Grid: **{grid}**")
            if source != 'All':
                filter_summary.append(f"Source: **{source}**")
            if min_records > 0:
                filter_summary.append(f"Min Records: **{min_records}**")
            
            st.info(f"🔍 Active Filters: {' | '.join(filter_summary)}")
    else:
        df_filtered = df
    
    # Show filtered data stats
    col1, col2, col3, col4 = st.columns(4)
    stats = get_summary_stats(df_filtered)
    
    with col1:
        st.metric("📝 Total Records", f"{stats['total_records']:,}")
    with col2:
        st.metric("🦌 Unique Species", stats['unique_species'])
    with col3:
        st.metric("🗺️ UTM Grids", stats['unique_grids'])
    with col4:
        st.metric("📊 Data Sources", stats['unique_sources'])
    
    st.markdown("---")
    
    # Route to selected page
    if page == 'origin':
        show_origin_page()
    elif page == 'data':
        show_data_exploration_page(df_filtered, data)
    elif page == 'eda':
        show_eda_page(df_filtered, data)
    elif page == 'conclusions':
        show_conclusions_page(df_filtered)
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666; font-size: 0.9em;'>
            <p>Citizen Science Wildlife Dashboard | Córdoba Province, Spain</p>
            <p>Data sources: Camera Traps (2024) | GBIF (2008-2023) | Citizen Science Platforms</p>
            <p>© 2024 | Built with Streamlit & Python</p>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================================
# RUN APPLICATION
# ============================================================================

if __name__ == "__main__":
    main()
