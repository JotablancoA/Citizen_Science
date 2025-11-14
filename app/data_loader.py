"""
Data Loader Module
==================
Handles all data loading, preprocessing, and caching operations.
Implements efficient data loading with Streamlit caching for performance.
"""

import pandas as pd
import geopandas as gpd
import streamlit as st
from pathlib import Path
from typing import Dict, Tuple, Optional
import numpy as np
import os

from config import DATA_FILES, GENERATED_IMAGES, GENERATED_MAPS


# ============================================================================
# DATA LOADING FUNCTIONS
# ============================================================================

@st.cache_data(ttl=3600)
def load_citizen_science_data() -> pd.DataFrame:
    """
    Load citizen science records from CSV file.
    
    Returns:
        pd.DataFrame: Citizen science records with species, grid, source, and counts
    """
    try:
        df = pd.read_csv(DATA_FILES['citizen_science'])
        
        # Ensure required columns exist
        required_cols = ['Species.Name', 'Grid', 'Data.Source', 'Records']
        if not all(col in df.columns for col in required_cols):
            st.error(f"Missing required columns in citizen science data")
            return pd.DataFrame()
        
        # Clean data
        df = df.dropna(subset=['Species.Name', 'Records'])
        df['Records'] = pd.to_numeric(df['Records'], errors='coerce').fillna(0)
        
        return df
    
    except Exception as e:
        st.error(f"Error loading citizen science data: {str(e)}")
        return pd.DataFrame()


@st.cache_data(ttl=3600)
def load_gbif_data() -> gpd.GeoDataFrame:
    """
    Load GBIF occurrence data from shapefile.
    
    Returns:
        gpd.GeoDataFrame: GBIF records with geometry and attributes
    """
    try:
        gdf = gpd.read_file(DATA_FILES['gbif_shapefile'])
        
        # Extract coordinates
        gdf['Longitude'] = gdf.geometry.x
        gdf['Latitude'] = gdf.geometry.y
        
        # Remove null coordinates
        gdf = gdf.dropna(subset=['Latitude', 'Longitude'])
        
        return gdf
    
    except Exception as e:
        st.error(f"Error loading GBIF data: {str(e)}")
        return gpd.GeoDataFrame()


@st.cache_data(ttl=3600)
def load_utm_grid() -> gpd.GeoDataFrame:
    """
    Load UTM grid polygons (10x10 km cells).
    
    Returns:
        gpd.GeoDataFrame: UTM grid cells with geometry
    """
    try:
        gdf = gpd.read_file(DATA_FILES['utm_grid'])
        return gdf
    
    except Exception as e:
        st.error(f"Error loading UTM grid: {str(e)}")
        return gpd.GeoDataFrame()


@st.cache_data(ttl=3600)
def load_camera_locations() -> pd.DataFrame:
    """
    Load camera trap location data.
    
    Returns:
        pd.DataFrame: Camera locations with coordinates and metadata
    """
    try:
        df = pd.read_csv(DATA_FILES['cameras'], sep=';')
        
        # Clean column names
        df.columns = df.columns.str.strip()
        
        # Ensure coordinate columns exist
        if 'Latitude' not in df.columns or 'Longitude' not in df.columns:
            st.error("Camera data missing coordinate columns")
            return pd.DataFrame()
        
        # Remove null coordinates
        df = df.dropna(subset=['Latitude', 'Longitude'])
        
        return df
    
    except Exception as e:
        st.error(f"Error loading camera data: {str(e)}")
        return pd.DataFrame()


@st.cache_data(ttl=3600)
def load_species_silhouettes() -> pd.DataFrame:
    """
    Load species silhouette URLs for visualization.
    
    Returns:
        pd.DataFrame: Species genus mapped to silhouette URLs
    """
    try:
        df = pd.read_csv(DATA_FILES['silhouettes'])
        return df
    
    except Exception as e:
        st.warning(f"Could not load silhouette data: {str(e)}")
        return pd.DataFrame()


# ============================================================================
# DATA PROCESSING FUNCTIONS
# ============================================================================

def get_species_list(df: pd.DataFrame) -> list:
    """
    Extract unique species names from dataset.
    
    Args:
        df: DataFrame with 'Species.Name' column
        
    Returns:
        list: Sorted list of unique species names
    """
    if 'Species.Name' in df.columns:
        species = df['Species.Name'].dropna().unique()
        return sorted(species.tolist())
    return []


def get_grid_list(df: pd.DataFrame) -> list:
    """
    Extract unique grid IDs from dataset.
    
    Args:
        df: DataFrame with 'Grid' column
        
    Returns:
        list: Sorted list of unique grid IDs
    """
    if 'Grid' in df.columns:
        grids = df['Grid'].dropna().unique()
        return sorted(grids.tolist())
    return []


def get_data_sources(df: pd.DataFrame) -> list:
    """
    Extract unique data sources from dataset.
    
    Args:
        df: DataFrame with 'Data.Source' column
        
    Returns:
        list: List of unique data sources
    """
    if 'Data.Source' in df.columns:
        sources = df['Data.Source'].dropna().unique()
        return sorted(sources.tolist())
    return []


def filter_data(
    df: pd.DataFrame,
    species: Optional[str] = None,
    grid: Optional[str] = None,
    source: Optional[str] = None,
    min_records: int = 0
) -> pd.DataFrame:
    """
    Apply filters to the dataset.
    
    Args:
        df: Input DataFrame
        species: Filter by species name (None or 'All' for no filter)
        grid: Filter by grid ID (None or 'All' for no filter)
        source: Filter by data source (None or 'All' for no filter)
        min_records: Minimum number of records threshold
        
    Returns:
        pd.DataFrame: Filtered DataFrame
    """
    filtered = df.copy()
    
    # Apply species filter
    if species and species != 'All':
        filtered = filtered[filtered['Species.Name'] == species]
    
    # Apply grid filter
    if grid and grid != 'All':
        filtered = filtered[filtered['Grid'] == grid]
    
    # Apply source filter
    if source and source != 'All':
        filtered = filtered[filtered['Data.Source'] == source]
    
    # Apply minimum records filter
    if min_records > 0:
        filtered = filtered[filtered['Records'] >= min_records]
    
    return filtered


# ============================================================================
# AGGREGATION FUNCTIONS
# ============================================================================

def aggregate_by_species(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate records by species.
    
    Args:
        df: Input DataFrame with Records column
        
    Returns:
        pd.DataFrame: Aggregated data by species
    """
    if df.empty:
        return pd.DataFrame()
    
    agg_df = df.groupby('Species.Name')['Records'].agg([
        ('Total_Records', 'sum'),
        ('Num_Grids', lambda x: df.loc[x.index, 'Grid'].nunique()),
        ('Num_Sources', lambda x: df.loc[x.index, 'Data.Source'].nunique())
    ]).reset_index()
    
    return agg_df.sort_values('Total_Records', ascending=False)


def aggregate_by_grid(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate records by UTM grid.
    
    Args:
        df: Input DataFrame with Records column
        
    Returns:
        pd.DataFrame: Aggregated data by grid
    """
    if df.empty:
        return pd.DataFrame()
    
    agg_df = df.groupby('Grid')['Records'].agg([
        ('Total_Records', 'sum'),
        ('Num_Species', lambda x: df.loc[x.index, 'Species.Name'].nunique()),
        ('Num_Sources', lambda x: df.loc[x.index, 'Data.Source'].nunique())
    ]).reset_index()
    
    return agg_df.sort_values('Total_Records', ascending=False)


def aggregate_by_source(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate records by data source.
    
    Args:
        df: Input DataFrame with Records column
        
    Returns:
        pd.DataFrame: Aggregated data by source
    """
    if df.empty:
        return pd.DataFrame()
    
    agg_df = df.groupby('Data.Source')['Records'].agg([
        ('Total_Records', 'sum'),
        ('Num_Species', lambda x: df.loc[x.index, 'Species.Name'].nunique()),
        ('Num_Grids', lambda x: df.loc[x.index, 'Grid'].nunique())
    ]).reset_index()
    
    return agg_df.sort_values('Total_Records', ascending=False)


def get_correlation_data(df: pd.DataFrame) -> Tuple[pd.DataFrame, float]:
    """
    Prepare data for Daily vs Sequences correlation analysis.
    
    Args:
        df: Input DataFrame with species and records
        
    Returns:
        Tuple of (correlation DataFrame, Pearson r coefficient)
    """
    # Separate by source type
    df_daily = df[df['Data.Source'] == 'Daily Record'].groupby('Species.Name')['Records'].sum().reset_index()
    df_daily.rename(columns={'Records': 'Daily_Sum'}, inplace=True)
    
    df_sequences = df[df['Data.Source'] == 'Sequences Record'].groupby('Species.Name')['Records'].sum().reset_index()
    df_sequences.rename(columns={'Records': 'Sequences_Sum'}, inplace=True)
    
    # Merge datasets
    corr_df = pd.merge(df_daily, df_sequences, on='Species.Name', how='outer').fillna(0)
    
    # Calculate Pearson correlation
    if len(corr_df) > 1:
        correlation = corr_df[['Daily_Sum', 'Sequences_Sum']].corr(method='pearson').iloc[0, 1]
    else:
        correlation = 0.0
    
    return corr_df, correlation


# ============================================================================
# SUMMARY STATISTICS
# ============================================================================

def get_summary_stats(df: pd.DataFrame) -> Dict:
    """
    Calculate comprehensive summary statistics.
    
    Args:
        df: Input DataFrame
        
    Returns:
        Dict: Dictionary with summary statistics
    """
    if df.empty:
        return {
            'total_records': 0,
            'unique_species': 0,
            'unique_grids': 0,
            'unique_sources': 0,
            'species_richness_by_source': {}
        }
    
    stats = {
        'total_records': int(df['Records'].sum()),
        'unique_species': df['Species.Name'].nunique(),
        'unique_grids': df['Grid'].nunique() if 'Grid' in df.columns else 0,
        'unique_sources': df['Data.Source'].nunique(),
        'species_richness_by_source': df.groupby('Data.Source')['Species.Name'].nunique().to_dict(),
        'top_species': df.groupby('Species.Name')['Records'].sum().nlargest(5).to_dict(),
        'top_grids': df.groupby('Grid')['Records'].sum().nlargest(5).to_dict() if 'Grid' in df.columns else {}
    }
    
    return stats


# ============================================================================
# GEOSPATIAL FUNCTIONS
# ============================================================================

def create_cameras_geodataframe(cameras_df: pd.DataFrame) -> gpd.GeoDataFrame:
    """
    Convert camera DataFrame to GeoDataFrame.
    
    Args:
        cameras_df: DataFrame with Latitude/Longitude columns
        
    Returns:
        gpd.GeoDataFrame: Camera locations as GeoDataFrame
    """
    from shapely.geometry import Point
    
    geometry = [Point(xy) for xy in zip(cameras_df['Longitude'], cameras_df['Latitude'])]
    gdf = gpd.GeoDataFrame(cameras_df, geometry=geometry, crs="EPSG:4326")
    
    return gdf


def spatial_join_gbif_grid(gbif_gdf: gpd.GeoDataFrame, utm_gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """
    Perform spatial join between GBIF points and UTM grid.
    
    Args:
        gbif_gdf: GBIF occurrence GeoDataFrame
        utm_gdf: UTM grid GeoDataFrame
        
    Returns:
        gpd.GeoDataFrame: GBIF data with grid assignments
    """
    # Ensure same CRS
    if gbif_gdf.crs != utm_gdf.crs:
        gbif_gdf = gbif_gdf.to_crs(utm_gdf.crs)
    
    # Spatial join
    joined = gpd.sjoin(gbif_gdf, utm_gdf, how="left", predicate="within")
    
    return joined


# ============================================================================
# VISUALIZATION ASSETS MANAGEMENT
# ============================================================================

def check_generated_image(image_key: str) -> bool:
    """
    Check if a generated image exists.
    
    Args:
        image_key: Key from GENERATED_IMAGES dict
        
    Returns:
        bool: True if image exists
    """
    if image_key not in GENERATED_IMAGES:
        return False
    
    image_path = GENERATED_IMAGES[image_key]
    return os.path.exists(image_path)


def get_generated_image_path(image_key: str) -> Optional[str]:
    """
    Get path to generated image if it exists.
    
    Args:
        image_key: Key from GENERATED_IMAGES dict
        
    Returns:
        Optional[str]: Path to image or None
    """
    if check_generated_image(image_key):
        return str(GENERATED_IMAGES[image_key])
    return None


def check_generated_map(map_key: str) -> bool:
    """
    Check if a generated HTML map exists.
    
    Args:
        map_key: Key from GENERATED_MAPS dict
        
    Returns:
        bool: True if map exists
    """
    if map_key not in GENERATED_MAPS:
        return False
    
    map_path = GENERATED_MAPS[map_key]
    return os.path.exists(map_path)


def load_html_map(map_key: str) -> Optional[str]:
    """
    Load HTML map content for embedding.
    
    Args:
        map_key: Key from GENERATED_MAPS dict
        
    Returns:
        Optional[str]: HTML content or None
    """
    if not check_generated_map(map_key):
        return None
    
    try:
        with open(GENERATED_MAPS[map_key], 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return None


def get_available_visualizations() -> Dict[str, Dict[str, bool]]:
    """
    Get status of all generated visualizations.
    
    Returns:
        Dict: Status of images and maps
    """
    return {
        'images': {key: check_generated_image(key) for key in GENERATED_IMAGES},
        'maps': {key: check_generated_map(key) for key in GENERATED_MAPS}
    }
