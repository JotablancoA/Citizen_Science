"""
EDA (Exploratory Data Analysis) Page
=====================================
Comprehensive statistical analyses and advanced visualizations.
"""

import streamlit as st
import pandas as pd
import numpy as np
from styles import create_section_header, create_highlight_box
from data_loader import get_correlation_data, check_generated_image, get_generated_image_path
from visualizations import (
    plot_dual_histograms, plot_correlation_scatter, plot_correlation_comparison,
    plot_species_richness_by_source, plot_stacked_bar_by_source,
    plot_species_grid_heatmap, plot_records_boxplot_by_source,
    plot_hierarchical_sunburst, plot_temporal_trends
)


def show_eda_page(df: pd.DataFrame, data: dict):
    """
    Render the Exploratory Data Analysis page.
    
    Args:
        df: Filtered citizen science DataFrame
        data: Dictionary with all loaded datasets
    """
    
    # Page header
    st.markdown(create_section_header(
        "📊 Exploratory Data Analysis",
        "In-depth statistical analysis and pattern discovery"
    ), unsafe_allow_html=True)
    
    if df.empty:
        st.warning("⚠️ No data available with current filters. Please adjust your filters.")
        return
    
    # EDA Navigation
    st.markdown("### Analysis Sections")
    
    eda_section = st.selectbox(
        "Select analysis type:",
        options=[
            "Distribution Analysis",
            "Correlation Analysis",
            "Species Richness",
            "Spatial Patterns",
            "Temporal Trends",
            "Multi-dimensional Analysis"
        ]
    )
    
    st.markdown("---")
    
    # Route to selected analysis
    if eda_section == "Distribution Analysis":
        show_distribution_analysis(df)
    
    elif eda_section == "Correlation Analysis":
        show_correlation_analysis(df)
    
    elif eda_section == "Species Richness":
        show_species_richness_analysis(df)
    
    elif eda_section == "Spatial Patterns":
        show_spatial_analysis(df)
    
    elif eda_section == "Temporal Trends":
        show_temporal_analysis(df, data)
    
    elif eda_section == "Multi-dimensional Analysis":
        show_multidimensional_analysis(df)


# ============================================================================
# DISTRIBUTION ANALYSIS
# ============================================================================

def show_distribution_analysis(df):
    """Display distribution analysis section."""
    
    st.markdown("## 📈 Record Distribution Analysis")
    
    st.markdown("""
    Understanding the distribution of record counts helps identify:
    - **Data skewness**: Are records concentrated in few species/locations?
    - **Reporting patterns**: How do different sources report observations?
    - **Outliers**: Which species or grids show exceptional activity?
    """)
    
    # Check if generated image exists
    if check_generated_image('histogram_distributions'):
        st.markdown("### 📊 Generated Distribution Histograms (from EDA Notebook)")
        image_path = get_generated_image_path('histogram_distributions')
        st.image(image_path, caption="Distribution of Sequences vs Daily Records", use_container_width=True)
        
        st.markdown("""
        **From the EDA Analysis:**
        - The histograms reveal classic **right-skewed distributions**
        - Most species have few records, while a few have many
        - This pattern is typical of citizen science data where effort follows visibility
        """)
    else:
        st.info("💡 Run the EDA notebook to generate static histogram visualizations")
    
    # Interactive version
    st.markdown("### 🔄 Interactive Distribution Visualization")
    
    # Separate data by source type
    df_sequences = df[df['Data.Source'] == 'Sequences Record']
    df_daily = df[df['Data.Source'] == 'Daily Record']
    
    # Dual histogram
    if not df_sequences.empty and not df_daily.empty:
        st.plotly_chart(
            plot_dual_histograms(df_sequences, df_daily, bins=20),
            use_container_width=True
        )
    
    # Statistical summary
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Sequences Record Statistics")
        if not df_sequences.empty:
            stats_seq = df_sequences['Records'].describe()
            st.dataframe(stats_seq, use_container_width=True)
            
            # Additional metrics
            st.metric("Skewness", f"{df_sequences['Records'].skew():.2f}")
        else:
            st.info("No sequences records in filtered data")
    
    with col2:
        st.markdown("### Daily Record Statistics")
        if not df_daily.empty:
            stats_daily = df_daily['Records'].describe()
            st.dataframe(stats_daily, use_container_width=True)
            
            # Additional metrics
            st.metric("Skewness", f"{df_daily['Records'].skew():.2f}")
        else:
            st.info("No daily records in filtered data")
    
    # Key insights
    st.markdown(create_highlight_box("""
    <h3>📌 Key Insights from Distribution Analysis</h3>
    <ul>
        <li><strong>Right-skewed distributions:</strong> Confirm that most species have few records, 
        while a small number have many records - typical of citizen science data</li>
        <li><strong>Observation effort:</strong> Common, charismatic, or easily detected species 
        dominate the dataset</li>
        <li><strong>Statistical implications:</strong> Analyses should use robust statistics or 
        transformations (e.g., log scales)</li>
        <li><strong>Dashboard design:</strong> Highlight both common and rare species separately 
        to avoid masking patterns</li>
    </ul>
    
    <p><strong>See EDA Guide (eda.md):</strong> <code>img/histogram_distributions.png</code></p>
    """, 'info'), unsafe_allow_html=True)


# ============================================================================
# CORRELATION ANALYSIS
# ============================================================================

def show_correlation_analysis(df):
    """Display correlation analysis section."""
    
    st.markdown("## 🔗 Daily vs Sequences Correlation Analysis")
    
    st.markdown("""
    Examining the relationship between **Daily Records** and **Sequences Records** 
    reveals consistency across observation methods and helps identify outlier species.
    """)
    
    # Interactive analysis - PRIMARY visualization
    st.markdown("### 🔄 Interactive Correlation Visualization")
    
    # Get correlation data
    corr_df, corr_value = get_correlation_data(df)
    
    if corr_df.empty or len(corr_df) < 2:
        st.warning("Insufficient data for correlation analysis")
        return
    
    # All species correlation
    st.markdown("#### All Species Correlation")
    st.plotly_chart(
        plot_correlation_scatter(
            corr_df,
            'Daily_Sum',
            'Sequences_Sum',
            'Species.Name',
            corr_value
        ),
        use_container_width=True
    )
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Pearson Correlation", f"{corr_value:.3f}")
    with col2:
        st.metric("Number of Species", len(corr_df))
    with col3:
        relationship = "Strong" if abs(corr_value) > 0.7 else "Moderate" if abs(corr_value) > 0.4 else "Weak"
        st.metric("Relationship Strength", relationship)
    
    # Outlier analysis
    st.markdown("#### Outlier Sensitivity Analysis")
    
    # Identify top species
    top_species = corr_df.nlargest(1, 'Daily_Sum')['Species.Name'].values[0]
    
    st.info(f"**Most abundant species (Daily Records):** {top_species}")
    
    # Correlation without outlier
    corr_df_filtered = corr_df[corr_df['Species.Name'] != top_species]
    
    if len(corr_df_filtered) > 1:
        corr_value_filtered = corr_df_filtered[['Daily_Sum', 'Sequences_Sum']].corr(method='pearson').iloc[0, 1]
        
        st.plotly_chart(
            plot_correlation_comparison(corr_df, corr_df_filtered, corr_value, corr_value_filtered, top_species),
            use_container_width=True
        )
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Correlation (All)", f"{corr_value:.3f}")
        with col2:
            st.metric(f"Correlation (Excluding {top_species})", f"{corr_value_filtered:.3f}")
        with col3:
            change = corr_value_filtered - corr_value
            st.metric("Change", f"{change:+.3f}")
    
    # Insights
    st.markdown(create_highlight_box("""
    <h3>📌 Interpretation Guidelines for Conservation & Education</h3>
    <ul>
        <li><strong>Positive correlation:</strong> Daily and Sequences records generally align, 
        suggesting consistent detection across methods - validates both approaches</li>
        <li><strong>Influential species (O. cuniculus):</strong> One or two hyper-abundant species can 
        disproportionately drive the overall trend - important for statistical modeling</li>
        <li><strong>Outlier effects:</strong> Excluding top species typically reveals the 
        underlying pattern for the majority of species - shows ecological reality for rare taxa</li>
        <li><strong>Dashboard recommendation:</strong> Always show both views (with/without outliers) 
        for complete understanding of biodiversity patterns</li>
        <li><strong>Management implication:</strong> Both daily checks and sequence analysis capture 
        similar biodiversity signals, but each method has unique value</li>
        <li><strong>Student education:</strong> This demonstrates the importance of robust statistics 
        when dealing with skewed ecological data</li>
    </ul>
    
    <p><strong>See EDA Guide (eda.md):</strong> <code>img/correlation_comparison.png</code>, 
    <code>img/correlation_daily_sequences.png</code>, 
    <code>img/correlation_daily_sequences_no_ocuniculus.png</code></p>
    """, 'info'), unsafe_allow_html=True)


# ============================================================================
# SPECIES RICHNESS ANALYSIS
# ============================================================================

def show_species_richness_analysis(df):
    """Display species richness analysis section."""
    
    st.markdown("## 🦌 Species Richness by Data Source")
    
    st.markdown("""
    Different data sources may contribute varying levels of species diversity. 
    Understanding these patterns helps optimize data collection strategies.
    """)
    
    # Display the comprehensive generated image (more informative than interactive)
    if check_generated_image('species_richness_by_source'):
        st.markdown("### 📊 Species Richness Analysis by Data Source")
        image_path = get_generated_image_path('species_richness_by_source')
        st.image(image_path, caption="Species Richness by Source - Comprehensive View from EDA Analysis", use_container_width=True)
        
        st.markdown("""
        **Key Findings from Richness Analysis:**
        - **Global Biodiversity (GBIF)** provides the broadest species coverage with historical depth (2008-2023)
        - **Sequences Record** (camera traps) detects species difficult to observe through citizen science platforms
        - **Daily Record** offers rapid validation and real-time monitoring
        - **Citizen Science platforms** (iMammalia, iNaturalist, Observation.org) bring complementary geographic reach
        - **Combined dataset** maximizes species representation and spatial coverage
        """)
    else:
        st.info("💡 Run the EDA notebook to generate species richness visualizations")
        # Fallback: show interactive version only if generated image unavailable
        st.markdown("### 🔄 Interactive Species Richness Comparison (Fallback)")
        st.plotly_chart(
            plot_species_richness_by_source(df),
            use_container_width=True
        )
    
    # Detailed breakdown
    st.markdown("### 📋 Source Contribution Details")
    
    richness_data = df.groupby('Data.Source').agg({
        'Species.Name': 'nunique',
        'Records': 'sum',
        'Grid': 'nunique'
    }).reset_index()
    richness_data.columns = ['Data Source', 'Unique Species', 'Total Records', 'Grids Covered']
    
    st.dataframe(richness_data, use_container_width=True)
    
    # Stacked bar for species composition
    st.markdown("### Species Composition by Source")
    st.plotly_chart(
        plot_stacked_bar_by_source(df, top_n=12),
        use_container_width=True
    )
    
    # Platform comparison
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(create_highlight_box("""
<h3>📊 Platform Strengths</h3>
<ul>
    <li><strong>GBIF:</strong> Comprehensive historical coverage (2008-2023)</li>
    <li><strong>Sequences Record:</strong> Detailed temporal data from camera traps</li>
    <li><strong>Daily Record:</strong> Rapid presence/absence data</li>
    <li><strong>Citizen Science Platforms:</strong> Broad geographic reach (iMammalia, iNaturalist, Observation.org)</li>
</ul>
""", 'success'), unsafe_allow_html=True)
    
    with col2:
        st.markdown(create_highlight_box("""
<h3>💡 Conservation & Education Recommendations</h3>
<ul>
    <li><strong>Combine platforms</strong> for maximum species coverage</li>
    <li><strong>Track unique species per source</strong> to identify complementarity</li>
    <li><strong>Focus student efforts</strong> on under-represented taxa</li>
    <li><strong>Validate high-value observations</strong> across multiple sources</li>
    <li><strong>Leverage camera traps</strong> for nocturnal/elusive species detection</li>
</ul>
<p><strong>See EDA Guide (eda.md):</strong> <code>img/species_richness_by_source.png</code></p>
""", 'warning'), unsafe_allow_html=True)


# ============================================================================
# SPATIAL ANALYSIS
# ============================================================================

def show_spatial_analysis(df):
    """Display spatial patterns analysis section."""
    
    st.markdown("## 🗺️ Spatial Patterns Analysis")
    
    st.markdown("""
    Spatial analysis reveals **hotspots** (high-activity areas) and **gaps** 
    (under-sampled regions) that inform field work prioritization.
    """)
    
    # Check if generated images exist - ALL spatial visualizations
    has_spatial_images = (
        check_generated_image('records_by_species_grid') or 
        check_generated_image('panel_mapps_heat') or
        check_generated_image('panel_mapas_calor')
    )
    
    if has_spatial_images:
        st.markdown("### 📊 Generated Spatial Analysis (from EDA Notebook)")
        
        # Multi-panel heat maps for individual species
        if check_generated_image('panel_mapps_heat') or check_generated_image('panel_mapas_calor'):
            st.markdown("#### 🌡️ Multi-Panel Heat Maps by Species (KDE Density)")
            
            if check_generated_image('panel_mapps_heat'):
                image_path = get_generated_image_path('panel_mapps_heat')
                st.image(image_path, caption="Kernel Density Estimation (KDE) Heat Maps by Genus - UTM Grid Overlay", use_container_width=True)
            elif check_generated_image('panel_mapas_calor'):
                image_path = get_generated_image_path('panel_mapas_calor')
                st.image(image_path, caption="Panel de Mapas de Calor por Especie", use_container_width=True)
            
            st.markdown("""
            **Interpretation of Multi-Species Heat Maps:**
            - Each panel shows **spatial density** for a different genus/species using KDE
            - **Red hotspots** indicate areas with highest concentration of observations
            - **Purple UTM grid overlay** provides spatial reference (10×10 km cells)
            - **Contextily basemap** (OpenStreetMap) shows habitat context (urban, forest, water)
            - **Species-specific patterns** reveal habitat preferences and range distribution
            - **Empty grids** indicate sampling gaps or true species absence
            
            **Conservation Applications:**
            - Identify **core habitat areas** (persistent red zones) for priority species
            - Detect **corridor needs** between isolated hotspots
            - Guide **camera trap placement** to fill spatial gaps
            - Validate **student observation patterns** against known species distributions
            """)
        
        # Records by species and grid faceted view
        if check_generated_image('records_by_species_grid'):
            st.markdown("#### 📊 Records by Species and UTM Grid (Top 12 Grids)")
            image_path = get_generated_image_path('records_by_species_grid')
            st.image(image_path, caption="Faceted Bar Plot: Species × Grid × Data Source", use_container_width=True)
            
            st.markdown("""
            **Grid-Level Species Composition:**
            - Each panel represents **one UTM grid** (10×10 km)
            - Bars show **record counts** for each species
            - Colors distinguish **data sources** (GBIF, No Validation, Daily, Sequences)
            - Reveals **grid-specific species assemblages** and sampling biases
            """)
        
        st.markdown("""
        ---
        **Combined Spatial Insights:**
        - Heat maps show **where** species occur (continuous density)
        - Bar plots show **what** species are in each grid (discrete counts)
        - Together they provide both **macro** and **micro** spatial perspectives
        """)
    else:
        st.info("💡 Run the EDA notebook to generate multi-panel heat maps and grid-level species visualizations")
    
    # Interactive species × Grid heatmap
    st.markdown("### 🔄 Interactive Species Distribution Across UTM Grids")
    st.plotly_chart(
        plot_species_grid_heatmap(df, top_n=15),
        use_container_width=True
    )
    
    # Grid ranking
    st.markdown("### 📊 Grid Activity Ranking")
    
    grid_summary = df.groupby('Grid').agg({
        'Records': 'sum',
        'Species.Name': 'nunique',
        'Data.Source': 'nunique'
    }).reset_index()
    grid_summary.columns = ['Grid', 'Total Records', 'Species Count', 'Sources']
    grid_summary = grid_summary.sort_values('Total Records', ascending=False)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.dataframe(grid_summary, use_container_width=True, height=400)
    
    with col2:
        st.markdown("#### 🏆 Top 3 Hotspots")
        for idx, row in grid_summary.head(3).iterrows():
            st.metric(
                f"Grid {row['Grid']}",
                f"{int(row['Total Records'])} records",
                f"{int(row['Species Count'])} species"
            )
    
    # Insights
    st.markdown(create_highlight_box("""
    <h3>🎯 Spatial Conservation Strategy</h3>
    <ul>
        <li><strong>Hotspot validation:</strong> High-activity grids need quality control and detailed monitoring 
        to ensure data accuracy</li>
        <li><strong>Gap filling:</strong> Target low-coverage grids for new student surveys and camera deployments 
        to balance spatial representation</li>
        <li><strong>Habitat correlation:</strong> Link spatial patterns to land cover (forests, urban areas, 
        agricultural zones, water bodies) using GIS layers</li>
        <li><strong>Camera placement optimization:</strong> Use heat map hotspots to guide future trap locations 
        for maximum detection efficiency</li>
        <li><strong>School allocation:</strong> Assign student groups to grids based on accessibility and 
        biodiversity potential revealed by heat maps</li>
        <li><strong>Connectivity analysis:</strong> Identify corridors between high-richness grids for wildlife 
        movement studies and conservation planning</li>
        <li><strong>Species-specific management:</strong> Use individual species heat maps to define critical 
        habitat zones for rare or threatened taxa</li>
        <li><strong>Seasonal adjustments:</strong> Combine heat maps with temporal data to optimize survey timing 
        for elusive species</li>
    </ul>
    
    <p><strong>See EDA Guide (eda.md):</strong> <code>img/panel_mapps_heat.png</code>, 
    <code>img/panel_mapas_calor.png</code>, <code>img/records_by_species_grid.png</code></p>
    """, 'highlight'), unsafe_allow_html=True)


# ============================================================================
# TEMPORAL ANALYSIS
# ============================================================================

def show_temporal_analysis(df, data):
    """Display temporal trends analysis section."""
    
    st.markdown("## ⏱️ Temporal Trends Analysis")
    
    gbif_df = data['gbif']
    
    # Check if temporal data available
    if 'year' not in gbif_df.columns:
        st.warning("⚠️ Temporal data (year) not available in current dataset")
        return
    
    st.markdown("""
    Temporal analysis reveals how observation effort and species detection 
    have changed over time, highlighting trends by taxonomic groups.
    """)
    
    # Interactive temporal trends plot - PRIMARY visualization
    st.markdown("### 🔄 Interactive Temporal Trends by Taxonomic Order")
    st.markdown("""
    **Understanding Temporal Dynamics (2008-2023):**
    - **2008-2015**: Initial phase with sporadic GBIF observations
    - **2016-2020**: Gradual increase in citizen science participation  
    - **2021-2023**: Exponential growth through platform expansion (iMammalia, iNaturalist, Observation.org)
    - **2024**: Camera trap project generates volumes comparable to entire GBIF historical record
    - **Seasonal patterns**: Some taxonomic orders show seasonal peaks (breeding, migration, detectability)
    """)
    if 'order' in gbif_df.columns:
        st.plotly_chart(
            plot_temporal_trends(gbif_df, 'year', 'order'),
            use_container_width=True
        )
    
    # Year-by-year summary
    st.markdown("### 📅 Records by Year - Detailed Breakdown")
    
    yearly_summary = gbif_df.groupby('year').size().reset_index(name='Records')
    yearly_summary['Cumulative'] = yearly_summary['Records'].cumsum()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.line_chart(yearly_summary.set_index('year')[['Records']])
    
    with col2:
        st.markdown("#### Recent Years (Last 5)")
        st.dataframe(yearly_summary.tail(5), use_container_width=True)
    
    # Project context and conservation implications
    st.markdown(create_highlight_box("""
    <h3>📅 Citizen Science Impact & Conservation Implications</h3>
    <ul>
        <li><strong>Camera trap project (2024):</strong> Generated data volumes comparable to 15 years of GBIF 
        historical records - demonstrates the power of focused, school-based initiatives</li>
        <li><strong>Student engagement:</strong> 800 students from 11 schools contributed to 2024 data collection, 
        representing a massive increase in observation effort</li>
        <li><strong>Temporal complementarity:</strong> Recent camera trap data fills gaps in historical GBIF coverage, 
        particularly for nocturnal and elusive species</li>
        <li><strong>Observation effort evolution:</strong> Increased dramatically post-2020, likely due to enhanced 
        citizen science platforms and COVID-19 outdoor activity surge</li>
        <li><strong>Species accumulation patterns:</strong> Curves suggest ongoing species discovery for rare taxa, 
        particularly Carnivora and Chiroptera</li>
        <li><strong>Taxonomic bias detection:</strong> Some orders (Rodentia, Insectivora) show early saturation, 
        indicating either true rarity or detection bias favoring larger mammals</li>
        <li><strong>Long-term monitoring value:</strong> 15-year time series enables detection of population trends, 
        range shifts, and conservation status changes</li>
    </ul>
    
    <p><strong>See EDA Guide (eda.md):</strong> <code>img/accumulated_curves_orders.png</code>, 
    <code>img/temporal_trends.png</code>, <code>img/tendencias_ordenes.png</code></p>
    """, 'info'), unsafe_allow_html=True)


# ============================================================================
# MULTI-DIMENSIONAL ANALYSIS
# ============================================================================

def show_multidimensional_analysis(df):
    """Display multi-dimensional analysis section."""
    
    st.markdown("## 🔀 Multi-dimensional Analysis")
    
    st.markdown("""
    Hierarchical and multi-variate visualizations reveal complex relationships 
    between grids, species, and data sources.
    """)
    
    # Check if generated image exists
    if check_generated_image('violin_log_records_platform'):
        st.markdown("### 📊 Generated Multi-dimensional Analysis (from EDA Notebook)")
        image_path = get_generated_image_path('violin_log_records_platform')
        st.image(image_path, caption="Violin Plot of Log-transformed Records by Platform", use_container_width=True)
        
        st.markdown("""
        **Key Multi-dimensional Patterns:**
        - Violin plots reveal distribution shapes for each platform
        - Log transformation handles right-skewed record counts
        - Width of violin indicates density of observations at each value
        - Combined with box plot elements for quartile information
        """)
    else:
        st.info("💡 Run the EDA notebook to generate violin plots with log-transformed distributions")
    
    # Interactive sunburst chart
    st.markdown("### 🔄 Interactive Hierarchical View: Grid → Species → Source")
    st.plotly_chart(
        plot_hierarchical_sunburst(df),
        use_container_width=True
    )
    
    # Box plot by source
    st.markdown("### 📦 Record Distribution by Source (Log Scale)")
    st.plotly_chart(
        plot_records_boxplot_by_source(df),
        use_container_width=True
    )
    
    # Statistical tests info
    st.markdown(create_highlight_box("""
    <h3>📐 Statistical Considerations for Ecological Data</h3>
    <p>
    The visualizations above use <strong>log transformations</strong> to handle 
    right-skewed distributions typical of ecological count data. For formal hypothesis testing and modeling:
    </p>
    <ul>
        <li><strong>Mixed-effects models (GLMM):</strong> Account for nested structure (species within grids, 
        grids within regions) and handle random effects appropriately</li>
        <li><strong>Negative binomial models:</strong> Handle over-dispersed count data where variance exceeds mean 
        (common in wildlife observations)</li>
        <li><strong>Zero-inflated models:</strong> Address excess zeros in datasets (grids with no detections)</li>
        <li><strong>Robust statistics:</strong> Minimize influence of extreme values (hyper-abundant species like rabbits)</li>
        <li><strong>Rarefaction curves:</strong> Compare species richness across sampling efforts of different intensities</li>
        <li><strong>Permutation tests:</strong> Non-parametric alternatives when distributional assumptions violated</li>
    </ul>
    <p>
    <strong>Dashboard Recommendation:</strong> These approaches provide more reliable inference than traditional 
    parametric methods (t-tests, ANOVA) when dealing with ecological count data characterized by non-normality, 
    heteroscedasticity, and hierarchical structure.
    </p>
    
    <p><strong>See EDA Guide (eda.md):</strong> <code>img/violin_log_records_platform.png</code></p>
    """, 'info'), unsafe_allow_html=True)
