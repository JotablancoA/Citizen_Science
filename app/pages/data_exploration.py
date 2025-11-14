"""
Data Exploration Page
=====================
Interactive data exploration with tables, summaries, and basic visualizations.
"""

import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster, HeatMap
try:
    from streamlit_folium import folium_static
except ImportError:
    # Fallback if streamlit_folium not installed
    def folium_static(map_obj, width=None, height=None):
        st.components.v1.html(map_obj._repr_html_(), width=width, height=height, scrolling=True)

from styles import create_section_header, create_highlight_box
from data_loader import (
    aggregate_by_species, aggregate_by_grid, aggregate_by_source,
    create_cameras_geodataframe, spatial_join_gbif_grid,
    load_html_map, check_generated_map
)
from visualizations import (
    plot_records_pie_by_source, plot_records_by_species,
    plot_records_by_grid
)
from config import MAP_CONFIG, PLATFORM_COLORS


def show_data_exploration_page(df: pd.DataFrame, data: dict):
    """
    Render the Data Exploration page with tabs organized by data source.
    
    Args:
        df: Filtered citizen science DataFrame
        data: Dictionary with all loaded datasets
    """
    
    # Page header
    st.markdown(create_section_header(
        "🔍 Data Exploration by Source",
        "Explore wildlife records from different data sources: Citizen Science, GBIF, UTM Grids, and Integrated Views"
    ), unsafe_allow_html=True)
    
    if df.empty:
        st.warning("⚠️ No data available with current filters. Please adjust your filters.")
        return
    
    st.markdown("---")
    
    # Tabs organized by data source
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Citizen Science Data",
        "🌍 GBIF Analysis", 
        "🗺️ UTM Grid Patterns",
        "🔗 Integrated Maps"
    ])
    
    # TAB 1: Citizen Science Data (dataset_CSsources_mod.csv)
    with tab1:
        show_citizen_science_tab(df, data)
    
    # TAB 2: GBIF Data (GBIFdata_CO.shp)
    with tab2:
        show_gbif_tab(df, data)
    
    # TAB 3: UTM Grid Analysis (CO_UTM2.shp)
    with tab3:
        show_utm_grid_tab(df, data)
    
    # TAB 4: Integrated Maps
    with tab4:
        show_integrated_maps_tab(df, data)


# ============================================================================
# TAB 1: CITIZEN SCIENCE DATA
# ============================================================================

def show_citizen_science_tab(df: pd.DataFrame, data: dict):
    """Display Citizen Science data exploration (dataset_CSsources_mod.csv)."""
    
    st.markdown("## 📊 Citizen Science Data Explorer")
    st.markdown("""
    This panel focuses on **citizen science records** aggregated from multiple platforms:
    - **Daily Record**: Daily presence/absence checks
    - **Sequences Record**: Detailed sequence observations from camera traps
    - **No Validation**: Community-contributed records (iMammalia, iNaturalist, Observation.org)
    """)
    
    # Data source breakdown
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📋 Raw Citizen Science Dataset")
        st.markdown("Browse the complete filtered citizen science dataset:")
        
        # Display options
        show_rows = st.selectbox("Show rows:", [10, 25, 50, 100, 500], index=1, key='cs_rows')
        
        # Display dataframe
        st.dataframe(
            df.head(show_rows),
            use_container_width=True,
            height=400
        )
        
        # Download button
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Citizen Science CSV",
            data=csv,
            file_name="citizen_science_data.csv",
            mime="text/csv",
            key='download_cs'
        )
    
    with col2:
        st.markdown("### 🎯 Data Source Distribution")
        st.plotly_chart(
            plot_records_pie_by_source(df),
            use_container_width=True,
            key='cs_pie'
        )
        
        # Summary by source
        source_summary = df.groupby('Data.Source').agg({
            'Records': 'sum',
            'Species.Name': 'nunique'
        }).reset_index()
        source_summary.columns = ['Source', 'Total Records', 'Unique Species']
        
        st.markdown("#### Source Statistics")
        st.dataframe(source_summary, use_container_width=True, hide_index=True)
    
    # Species analysis
    st.markdown("---")
    st.markdown("### 🦌 Species Composition Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Top Species by Records")
        species_agg = aggregate_by_species(df)
        st.plotly_chart(
            plot_records_by_species(species_agg),
            use_container_width=True,
            key='cs_species_chart'
        )
    
    with col2:
        st.markdown("#### Species Ranking Table")
        # Rename columns for display
        display_df = species_agg.rename(columns={
            'Species.Name': 'Species',
            'Total_Records': 'Total Records',
            'Num_Grids': 'Grids',
            'Num_Sources': 'Sources'
        })
        st.dataframe(
            display_df.head(15)[['Species', 'Total Records', 'Grids', 'Sources']],
            use_container_width=True,
            height=400,
            hide_index=True
        )


# ============================================================================
# TAB 2: GBIF ANALYSIS
# ============================================================================

def show_gbif_tab(df: pd.DataFrame, data: dict):
    """Display GBIF data exploration (GBIFdata_CO.shp)."""
    
    st.markdown("## 🌍 GBIF Historical Records Analysis")
    st.markdown("""
    This panel analyzes **GBIF occurrence records** (2008-2023) from Córdoba province:
    - Historical biodiversity patterns over 15 years
    - Taxonomic composition (genus, family, order)
    - Temporal trends and accumulation curves
    - Spatial distribution across the study area
    """)
    
    gbif_df = data.get('gbif', pd.DataFrame())
    
    if gbif_df.empty:
        st.warning("⚠️ GBIF data not available")
        return
    
    # GBIF metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total GBIF Records", f"{len(gbif_df):,}")
    
    with col2:
        if 'genus' in gbif_df.columns:
            unique_genus = gbif_df['genus'].nunique()
            st.metric("Unique Genera", unique_genus)
        else:
            st.metric("Unique Genera", "N/A")
    
    with col3:
        if 'year' in gbif_df.columns:
            year_range = f"{gbif_df['year'].min()}-{gbif_df['year'].max()}"
            st.metric("Year Range", year_range)
        else:
            st.metric("Year Range", "N/A")
    
    with col4:
        if 'institut_1' in gbif_df.columns:
            unique_institutions = gbif_df['institut_1'].nunique()
            st.metric("Data Providers", unique_institutions)
        else:
            st.metric("Data Providers", "N/A")
    
    # GBIF data table
    st.markdown("### 📋 GBIF Records Sample")
    
    # Select relevant columns
    display_cols = []
    for col in ['genus', 'family', 'order', 'year', 'institut_1', 'CUADRICULA']:
        if col in gbif_df.columns:
            display_cols.append(col)
    
    if display_cols:
        show_rows_gbif = st.selectbox("Show rows:", [10, 25, 50, 100], index=1, key='gbif_rows')
        st.dataframe(
            gbif_df[display_cols].head(show_rows_gbif),
            use_container_width=True,
            height=400
        )
    else:
        st.warning("No display columns available in GBIF data")
    
    # Taxonomic composition
    st.markdown("---")
    st.markdown("### 🦁 Taxonomic Composition")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if 'order' in gbif_df.columns:
            st.markdown("#### Records by Taxonomic Order")
            order_counts = gbif_df['order'].value_counts().reset_index()
            order_counts.columns = ['Order', 'Records']
            st.dataframe(order_counts.head(10), use_container_width=True, hide_index=True)
    
    with col2:
        if 'genus' in gbif_df.columns:
            st.markdown("#### Top 10 Genera")
            genus_counts = gbif_df['genus'].value_counts().reset_index()
            genus_counts.columns = ['Genus', 'Records']
            st.dataframe(genus_counts.head(10), use_container_width=True, hide_index=True)
    
    # Temporal trends (if year available)
    if 'year' in gbif_df.columns:
        st.markdown("---")
        st.markdown("### 📅 Temporal Evolution")
        
        yearly_summary = gbif_df.groupby('year').size().reset_index(name='Records')
        yearly_summary['Cumulative'] = yearly_summary['Records'].cumsum()
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.line_chart(yearly_summary.set_index('year')[['Records', 'Cumulative']])
        
        with col2:
            st.markdown("#### Recent Years Summary")
            st.dataframe(yearly_summary.tail(5), use_container_width=True, hide_index=True)


# ============================================================================
# TAB 3: UTM GRID PATTERNS
# ============================================================================

def show_utm_grid_tab(df: pd.DataFrame, data: dict):
    """Display UTM Grid spatial analysis (CO_UTM2.shp)."""
    
    st.markdown("## 🗺️ UTM Grid Spatial Patterns")
    st.markdown("""
    This panel analyzes **spatial distribution** across UTM 10×10 km grid cells:
    - Species richness per grid
    - Record density and sampling effort
    - Hotspots and sampling gaps
    - Grid-level species composition
    """)
    
    # Grid-level aggregation
    grid_agg = aggregate_by_grid(df)
    
    if grid_agg.empty:
        st.warning("⚠️ No grid data available")
        return
    
    # Grid metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total UTM Grids", len(grid_agg))
    
    with col2:
        avg_species = grid_agg['Num_Species'].mean()
        st.metric("Avg Species/Grid", f"{avg_species:.1f}")
    
    with col3:
        avg_records = grid_agg['Total_Records'].mean()
        st.metric("Avg Records/Grid", f"{avg_records:.0f}")
    
    with col4:
        top_grid = grid_agg.nlargest(1, 'Total_Records')['Grid'].values[0]
        st.metric("Richest Grid", top_grid)
    
    # Grid visualization
    st.markdown("### 📊 Grid Activity Ranking")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.plotly_chart(
            plot_records_by_grid(grid_agg),
            use_container_width=True,
            key='grid_chart'
        )
    
    with col2:
        st.markdown("#### 🏆 Top 10 Hotspot Grids")
        # Rename columns for display
        top_grids = grid_agg.nlargest(10, 'Total_Records')[['Grid', 'Total_Records', 'Num_Species']].copy()
        top_grids.columns = ['Grid', 'Total Records', 'Species Count']
        st.dataframe(top_grids, use_container_width=True, hide_index=True)
    
    # Detailed grid table
    st.markdown("---")
    st.markdown("### 📋 Complete Grid Summary")
    
    st.dataframe(
        grid_agg.sort_values('Total_Records', ascending=False),
        use_container_width=True,
        height=400,
        hide_index=True
    )
    
    # Download button
    csv_grid = grid_agg.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Grid Summary CSV",
        data=csv_grid,
        file_name="utm_grid_summary.csv",
        mime="text/csv",
        key='download_grid'
    )
    
    # Sampling gaps analysis
    st.markdown("---")
    st.markdown("### 🎯 Sampling Coverage Analysis")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        high_coverage = len(grid_agg[grid_agg['Total_Records'] > grid_agg['Total_Records'].quantile(0.75)])
        st.metric("High Coverage Grids", high_coverage, help="Grids in top 25% for records")
    
    with col2:
        low_coverage = len(grid_agg[grid_agg['Total_Records'] < grid_agg['Total_Records'].quantile(0.25)])
        st.metric("Low Coverage Grids", low_coverage, help="Grids in bottom 25% for records")
    
    with col3:
        single_species = len(grid_agg[grid_agg['Num_Species'] == 1])
        st.metric("Single-Species Grids", single_species, help="Grids with only 1 species recorded")


# ============================================================================
# TAB 4: INTEGRATED MAPS
# ============================================================================

def show_integrated_maps_tab(df: pd.DataFrame, data: dict):
    """Display integrated interactive maps combining all data sources."""
    
    st.markdown("## 🌍 Integrated Interactive Maps")
    st.markdown("""
    Visualize **combined data sources** on interactive maps:
    - **Cluster Map**: GBIF points clustered by UTM grid
    - **Heat Map**: Species occurrence density with camera trap locations
    - **Create Custom Map**: Build your own map with selected layers
    """)
    
    # Map selection
    map_type = st.radio(
        "Select Map Type:",
        options=[
            "📍 Cluster Map (Generated)",
            "🌡️ Heat Map with Cameras (Generated)",
            "🛠️ Create Custom Map"
        ],
        horizontal=True
    )
    
    st.markdown("---")
    
    # OPTION 1: Cluster Map (Generated)
    if map_type == "📍 Cluster Map (Generated)":
        st.markdown("### 📍 Cluster Map: GBIF Records by UTM Grid")
        st.markdown("""
        Pre-generated interactive map showing **GBIF occurrence points** clustered by UTM grid.
        Each cluster expands to show individual observation markers with species and source information.
        """)
        
        if check_generated_map('clusters_by_grid'):
            html_content = load_html_map('clusters_by_grid')
            st.components.v1.html(html_content, width=1200, height=600, scrolling=True)
            
            with st.container():
                st.info("🗺️ **How to Use This Map:**")
                st.markdown("""
                - **Cluster numbers** show count of observations in that area
                - **Click clusters** to zoom in and expand to individual markers
                - **Click markers** to see species, source, and grid information
                - **Purple grid overlay** shows UTM 10×10 km cells
                - **Color coding:** Orange (iMammalia), Green (iNaturalist), Blue (Observation.org)
                
                **File:** `html/mapa_clusters_por_grid.html`
                """)
        else:
            st.warning("⚠️ Cluster map not found. Run the EDA notebook to generate `mapa_clusters_por_grid.html`")
    
    # OPTION 2: Heat Map (Generated)
    elif map_type == "🌡️ Heat Map with Cameras (Generated)":
        st.markdown("### 🌡️ Heat Map: Species Density with Camera Locations")
        st.markdown("""
        Pre-generated heat map showing **species occurrence density** (blue → lime → yellow → red) 
        overlaid with **camera trap locations** (black markers) and UTM grid boundaries.
        """)
        
        if check_generated_map('heatmap_cameras'):
            html_content = load_html_map('heatmap_cameras')
            st.components.v1.html(html_content, width=1200, height=600, scrolling=True)
            
            with st.container():
                st.success("🔥 **Heat Map Interpretation:**")
                st.markdown("""
                - **Color gradient:** Blue (low density) → Red (high density)
                - **Black camera icons:** Camera trap deployment locations
                - **Purple grid overlay:** UTM 10×10 km grid cells
                - **Hotspots (red zones):** High biodiversity or high sampling effort
                - **Cool zones (blue):** Low detection or sampling gaps
                
                **Conservation Use:** Prioritize camera relocation to cool zones to balance spatial coverage
                
                **File:** `html/mapa_calor_con_utm_y_camaras.html`
                """)
        else:
            st.warning("⚠️ Heat map not found. Run the EDA notebook to generate `mapa_calor_con_utm_y_camaras.html`")
    
    # OPTION 3: Create Custom Map
    elif map_type == "🛠️ Create Custom Map":
        st.markdown("### 🛠️ Build Your Own Interactive Map")
        st.markdown("Customize map layers and filters to create a personalized view.")
        
        # Map customization options
        col1, col2 = st.columns(2)
        
        with col1:
            show_gbif = st.checkbox("Show GBIF Points", value=True)
            show_cameras = st.checkbox("Show Camera Traps", value=True)
            show_grid = st.checkbox("Show UTM Grid", value=True)
        
        with col2:
            show_heat = st.checkbox("Show Heat Layer", value=False)
            cluster_points = st.checkbox("Cluster Points", value=True)
        
        # Build custom map
        if st.button("🗺️ Generate Custom Map"):
            st.info("🔄 Generating custom map...")
            
            try:
                # Create base map
                center_lat = MAP_CONFIG['center_lat']
                center_lon = MAP_CONFIG['center_lon']
                zoom = MAP_CONFIG['zoom_start']
                
                custom_map = folium.Map(location=[center_lat, center_lon], zoom_start=zoom)
                
                # Add UTM grid if selected
                if show_grid and 'utm_grid' in data:
                    folium.GeoJson(
                        data['utm_grid'].__geo_interface__,
                        name="UTM Grid",
                        style_function=lambda x: {
                            'color': 'purple',
                            'weight': 2,
                            'opacity': 0.3,
                            'fillOpacity': 0.05
                        }
                    ).add_to(custom_map)
                
                # Add GBIF points
                if show_gbif and 'gbif' in data:
                    gbif_df = data['gbif']
                    
                    if not gbif_df.empty and hasattr(gbif_df, 'geometry'):
                        if cluster_points:
                            marker_cluster = MarkerCluster(name="GBIF Records")
                            
                            for idx, row in gbif_df.iterrows():
                                if row.geometry is not None:
                                    folium.Marker(
                                        location=[row.geometry.y, row.geometry.x],
                                        popup=f"Species: {row.get('genus', 'Unknown')}",
                                        icon=folium.Icon(color='green', icon='paw', prefix='fa')
                                    ).add_to(marker_cluster)
                            
                            marker_cluster.add_to(custom_map)
                        else:
                            for idx, row in gbif_df.iterrows():
                                if row.geometry is not None:
                                    folium.CircleMarker(
                                        location=[row.geometry.y, row.geometry.x],
                                        radius=3,
                                        color='green',
                                        fill=True,
                                        popup=f"Species: {row.get('genus', 'Unknown')}"
                                    ).add_to(custom_map)
                
                # Add heat layer
                if show_heat and 'gbif' in data:
                    gbif_df = data['gbif']
                    if not gbif_df.empty and hasattr(gbif_df, 'geometry'):
                        heat_data = [[row.geometry.y, row.geometry.x] for idx, row in gbif_df.iterrows() if row.geometry is not None]
                        if heat_data:
                            HeatMap(heat_data, radius=15, blur=20, max_zoom=10).add_to(custom_map)
                
                # Add cameras
                if show_cameras and 'cameras' in data:
                    cameras_gdf = create_cameras_geodataframe(data['cameras'])
                    if not cameras_gdf.empty:
                        for idx, row in cameras_gdf.iterrows():
                            folium.Marker(
                                location=[row.geometry.y, row.geometry.x],
                                popup=f"<b>Camera Trap</b><br>{row.get('Nombre.Loc', 'Camera')}",
                                icon=folium.Icon(color='black', icon='camera', prefix='fa')
                            ).add_to(custom_map)
                
                # Add layer control
                folium.LayerControl().add_to(custom_map)
                
                # Display map
                folium_static(custom_map, width=800, height=600)
                
                st.success("✅ Custom map generated successfully!")
                
            except Exception as e:
                st.error(f"❌ Error generating custom map: {str(e)}")
                st.info("💡 Ensure all data sources are properly loaded and contain valid geometry.")
