"""
Visualization Module
====================
Contains all visualization functions using Plotly for interactive charts.
Provides consistent styling and reusable plotting components.
"""

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import Optional, List, Dict

from config import DATA_SOURCE_COLORS, CHART_COLORS, CHART_CONFIG


# ============================================================================
# DISTRIBUTION VISUALIZATIONS
# ============================================================================

def plot_distribution_histogram(
    df: pd.DataFrame,
    column: str,
    title: str,
    color: str = '#4169E1',
    bins: int = 30
) -> go.Figure:
    """
    Create a histogram with KDE overlay.
    
    Args:
        df: Input DataFrame
        column: Column name for histogram
        title: Chart title
        color: Bar color
        bins: Number of bins
        
    Returns:
        plotly Figure object
    """
    fig = go.Figure()
    
    # Add histogram
    fig.add_trace(go.Histogram(
        x=df[column],
        nbinsx=bins,
        name='Frequency',
        marker_color=color,
        opacity=0.7
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title=column.replace('_', ' ').title(),
        yaxis_title='Frequency',
        template='plotly_white',
        height=CHART_CONFIG['default_height'],
        showlegend=False,
        font=dict(size=CHART_CONFIG['font_size'])
    )
    
    return fig


def plot_dual_histograms(
    df_sequences: pd.DataFrame,
    df_daily: pd.DataFrame,
    bins: int = 20
) -> go.Figure:
    """
    Create side-by-side histograms for Sequences vs Daily Records.
    
    Args:
        df_sequences: DataFrame filtered for sequence records
        df_daily: DataFrame filtered for daily records
        bins: Number of bins
        
    Returns:
        plotly Figure with subplots
    """
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Sequences Records Distribution', 'Daily Records Distribution')
    )
    
    # Sequences histogram
    fig.add_trace(
        go.Histogram(
            x=df_sequences['Records'],
            nbinsx=bins,
            name='Sequences',
            marker_color='#4169E1',
            opacity=0.7
        ),
        row=1, col=1
    )
    
    # Daily histogram
    fig.add_trace(
        go.Histogram(
            x=df_daily['Records'],
            nbinsx=bins,
            name='Daily',
            marker_color='#FFD700',
            opacity=0.7
        ),
        row=1, col=2
    )
    
    fig.update_layout(
        title_text='Record Count Distributions by Source Type',
        template='plotly_white',
        height=500,
        showlegend=False,
        font=dict(size=12)
    )
    
    fig.update_xaxes(title_text='Number of Records', row=1, col=1)
    fig.update_xaxes(title_text='Number of Records', row=1, col=2)
    fig.update_yaxes(title_text='Frequency', row=1, col=1)
    
    return fig


# ============================================================================
# CORRELATION VISUALIZATIONS
# ============================================================================

def plot_correlation_scatter(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    species_col: str,
    correlation: float,
    title: str = "Daily vs Sequences Records Correlation"
) -> go.Figure:
    """
    Create correlation scatter plot with trend line and labels.
    
    Args:
        df: Input DataFrame
        x_col: X-axis column name
        y_col: Y-axis column name
        species_col: Column with species names for labels
        correlation: Pearson correlation coefficient
        title: Chart title
        
    Returns:
        plotly Figure object
    """
    fig = px.scatter(
        df,
        x=x_col,
        y=y_col,
        text=species_col,
        trendline='ols',
        title=f"{title}<br><sub>Pearson r = {correlation:.3f}</sub>"
    )
    
    # Update traces
    fig.update_traces(
        marker=dict(size=10, opacity=0.7, color='#4169E1'),
        textposition='top center',
        textfont=dict(size=9)
    )
    
    fig.update_layout(
        template='plotly_white',
        height=CHART_CONFIG['default_height'],
        xaxis_title=x_col.replace('_', ' ').title(),
        yaxis_title=y_col.replace('_', ' ').title(),
        font=dict(size=CHART_CONFIG['font_size'])
    )
    
    return fig


def plot_correlation_comparison(
    df_all: pd.DataFrame,
    df_filtered: pd.DataFrame,
    corr_all: float,
    corr_filtered: float,
    exclude_species: str = 'O. cuniculus'
) -> go.Figure:
    """
    Create side-by-side correlation plots (all species vs excluding outliers).
    
    Args:
        df_all: DataFrame with all species
        df_filtered: DataFrame excluding specified species
        corr_all: Correlation for all species
        corr_filtered: Correlation for filtered dataset
        exclude_species: Name of excluded species
        
    Returns:
        plotly Figure with subplots
    """
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=(
            f'All Species (r = {corr_all:.3f})',
            f'Excluding {exclude_species} (r = {corr_filtered:.3f})'
        )
    )
    
    # All species scatter
    fig.add_trace(
        go.Scatter(
            x=df_all['Daily_Sum'],
            y=df_all['Sequences_Sum'],
            mode='markers+text',
            text=df_all['Species.Name'],
            textposition='top center',
            textfont=dict(size=8),
            marker=dict(size=10, color='#4169E1', opacity=0.6),
            name='All Species'
        ),
        row=1, col=1
    )
    
    # Filtered scatter
    fig.add_trace(
        go.Scatter(
            x=df_filtered['Daily_Sum'],
            y=df_filtered['Sequences_Sum'],
            mode='markers+text',
            text=df_filtered['Species.Name'],
            textposition='top center',
            textfont=dict(size=8),
            marker=dict(size=10, color='#FF8C00', opacity=0.6),
            name='Filtered'
        ),
        row=1, col=2
    )
    
    fig.update_layout(
        title_text='Correlation Analysis: Daily vs Sequences Records',
        template='plotly_white',
        height=500,
        showlegend=False
    )
    
    fig.update_xaxes(title_text='Daily Records', row=1, col=1)
    fig.update_xaxes(title_text='Daily Records', row=1, col=2)
    fig.update_yaxes(title_text='Sequences Records', row=1, col=1)
    fig.update_yaxes(title_text='Sequences Records', row=1, col=2)
    
    return fig


# ============================================================================
# BAR CHARTS
# ============================================================================

def plot_species_richness_by_source(df: pd.DataFrame) -> go.Figure:
    """
    Create bar chart showing species richness per data source.
    
    Args:
        df: Aggregated DataFrame by source
        
    Returns:
        plotly Figure object
    """
    # Calculate richness
    richness = df.groupby('Data.Source')['Species.Name'].nunique().reset_index()
    richness.columns = ['Data Source', 'Number of Species']
    richness = richness.sort_values('Number of Species', ascending=False)
    
    # Map colors
    colors = [DATA_SOURCE_COLORS.get(src, '#808080') for src in richness['Data Source']]
    
    fig = go.Figure(data=[
        go.Bar(
            x=richness['Data Source'],
            y=richness['Number of Species'],
            marker_color=colors,
            text=richness['Number of Species'],
            textposition='outside'
        )
    ])
    
    fig.update_layout(
        title='Species Richness by Data Source',
        xaxis_title='Data Source',
        yaxis_title='Number of Unique Species',
        template='plotly_white',
        height=CHART_CONFIG['default_height'],
        font=dict(size=CHART_CONFIG['font_size'])
    )
    
    return fig


def plot_records_by_species(
    df: pd.DataFrame,
    top_n: int = 15,
    horizontal: bool = True
) -> go.Figure:
    """
    Create bar chart of records by species (top N).
    
    Args:
        df: Input DataFrame
        top_n: Number of top species to display
        horizontal: If True, create horizontal bar chart
        
    Returns:
        plotly Figure object
    """
    # Check if we need to aggregate or if data is already aggregated
    if 'Total_Records' in df.columns:
        # Data is already aggregated
        species_counts = df.nlargest(top_n, 'Total_Records')
        species_counts = species_counts.sort_values('Total_Records', ascending=True)
        records_col = 'Total_Records'
    else:
        # Need to aggregate
        species_counts = df.groupby('Species.Name')['Records'].sum().nlargest(top_n).reset_index()
        species_counts = species_counts.sort_values('Records', ascending=True)
        records_col = 'Records'
    
    if horizontal:
        fig = go.Figure(data=[
            go.Bar(
                y=species_counts['Species.Name'],
                x=species_counts[records_col],
                orientation='h',
                marker_color='#2ca02c',
                text=species_counts[records_col],
                textposition='outside'
            )
        ])
        fig.update_layout(
            xaxis_title='Total Records',
            yaxis_title='Species'
        )
    else:
        fig = go.Figure(data=[
            go.Bar(
                x=species_counts['Species.Name'],
                y=species_counts[records_col],
                marker_color='#2ca02c',
                text=species_counts[records_col],
                textposition='outside'
            )
        ])
        fig.update_layout(
            xaxis_title='Species',
            yaxis_title='Total Records'
        )
        fig.update_xaxes(tickangle=45)
    
    fig.update_layout(
        title=f'Top {top_n} Species by Total Records',
        template='plotly_white',
        height=CHART_CONFIG['default_height'],
        font=dict(size=CHART_CONFIG['font_size'])
    )
    
    return fig


def plot_records_by_grid(df: pd.DataFrame, top_n: int = 10) -> go.Figure:
    """
    Create bar chart of records by UTM grid (top N).
    
    Args:
        df: Input DataFrame
        top_n: Number of top grids to display
        
    Returns:
        plotly Figure object
    """
    # Get top grids (df already aggregated with Total_Records column)
    grid_counts = df.nlargest(top_n, 'Total_Records').sort_values('Total_Records', ascending=True)
    
    fig = go.Figure(data=[
        go.Bar(
            y=grid_counts['Grid'],
            x=grid_counts['Total_Records'],
            orientation='h',
            marker_color='#9467bd',
            text=grid_counts['Total_Records'],
            textposition='outside'
        )
    ])
    
    fig.update_layout(
        title=f'Top {top_n} UTM Grids by Total Records',
        xaxis_title='Total Records',
        yaxis_title='UTM Grid',
        template='plotly_white',
        height=CHART_CONFIG['default_height'],
        font=dict(size=CHART_CONFIG['font_size'])
    )
    
    return fig


def plot_stacked_bar_by_source(df: pd.DataFrame, top_n: int = 10) -> go.Figure:
    """
    Create stacked bar chart showing species composition by data source.
    
    Args:
        df: Input DataFrame
        top_n: Number of top species to display
        
    Returns:
        plotly Figure object
    """
    # Get top species
    top_species = df.groupby('Species.Name')['Records'].sum().nlargest(top_n).index
    df_filtered = df[df['Species.Name'].isin(top_species)]
    
    # Pivot for stacked bar
    pivot_df = df_filtered.pivot_table(
        values='Records',
        index='Species.Name',
        columns='Data.Source',
        aggfunc='sum',
        fill_value=0
    )
    
    fig = go.Figure()
    
    for source in pivot_df.columns:
        color = DATA_SOURCE_COLORS.get(source, '#808080')
        fig.add_trace(go.Bar(
            name=source,
            x=pivot_df.index,
            y=pivot_df[source],
            marker_color=color
        ))
    
    fig.update_layout(
        title=f'Records by Species and Data Source (Top {top_n})',
        xaxis_title='Species',
        yaxis_title='Records',
        barmode='stack',
        template='plotly_white',
        height=CHART_CONFIG['default_height'],
        font=dict(size=CHART_CONFIG['font_size'])
    )
    
    fig.update_xaxes(tickangle=45)
    
    return fig


# ============================================================================
# PIE & DONUT CHARTS
# ============================================================================

def plot_records_pie_by_source(df: pd.DataFrame) -> go.Figure:
    """
    Create pie chart showing distribution of records by data source.
    
    Args:
        df: Input DataFrame
        
    Returns:
        plotly Figure object
    """
    source_counts = df.groupby('Data.Source')['Records'].sum().reset_index()
    
    colors = [DATA_SOURCE_COLORS.get(src, '#808080') for src in source_counts['Data.Source']]
    
    fig = go.Figure(data=[
        go.Pie(
            labels=source_counts['Data.Source'],
            values=source_counts['Records'],
            marker=dict(colors=colors),
            hole=0.3,
            textinfo='label+percent',
            textposition='outside'
        )
    ])
    
    fig.update_layout(
        title='Records Distribution by Data Source',
        template='plotly_white',
        height=CHART_CONFIG['default_height'],
        font=dict(size=CHART_CONFIG['font_size'])
    )
    
    return fig


# ============================================================================
# LINE CHARTS
# ============================================================================

def plot_temporal_trends(
    df: pd.DataFrame,
    time_col: str = 'year',
    group_col: str = 'order'
) -> go.Figure:
    """
    Create line chart showing temporal trends by taxonomic group.
    
    Args:
        df: Input DataFrame with temporal column
        time_col: Column name for time axis
        group_col: Column for grouping (e.g., 'order', 'genus')
        
    Returns:
        plotly Figure object
    """
    if time_col not in df.columns or group_col not in df.columns:
        return go.Figure()
    
    # Aggregate by time and group
    temporal = df.groupby([time_col, group_col]).size().reset_index(name='records')
    
    # Calculate cumulative
    temporal['cumulative'] = temporal.groupby(group_col)['records'].cumsum()
    
    fig = px.line(
        temporal,
        x=time_col,
        y='cumulative',
        color=group_col,
        markers=True,
        title=f'Cumulative Records Over Time by {group_col.title()}'
    )
    
    fig.update_layout(
        xaxis_title=time_col.title(),
        yaxis_title='Cumulative Records',
        template='plotly_white',
        height=CHART_CONFIG['default_height'],
        font=dict(size=CHART_CONFIG['font_size'])
    )
    
    return fig


# ============================================================================
# HEATMAPS
# ============================================================================

def plot_species_grid_heatmap(df: pd.DataFrame, top_n: int = 15) -> go.Figure:
    """
    Create heatmap showing species presence across grids.
    
    Args:
        df: Input DataFrame
        top_n: Number of top species to include
        
    Returns:
        plotly Figure object
    """
    # Get top species
    top_species = df.groupby('Species.Name')['Records'].sum().nlargest(top_n).index
    df_filtered = df[df['Species.Name'].isin(top_species)]
    
    # Create pivot table
    heatmap_data = df_filtered.pivot_table(
        values='Records',
        index='Species.Name',
        columns='Grid',
        aggfunc='sum',
        fill_value=0
    )
    
    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data.values,
        x=heatmap_data.columns,
        y=heatmap_data.index,
        colorscale='YlOrRd',
        text=heatmap_data.values,
        texttemplate='%{text}',
        textfont={"size": 10},
        colorbar=dict(title="Records")
    ))
    
    fig.update_layout(
        title=f'Species × Grid Heatmap (Top {top_n} Species)',
        xaxis_title='UTM Grid',
        yaxis_title='Species',
        template='plotly_white',
        height=600,
        font=dict(size=CHART_CONFIG['font_size'])
    )
    
    return fig


# ============================================================================
# BOX & VIOLIN PLOTS
# ============================================================================

def plot_records_boxplot_by_source(df: pd.DataFrame) -> go.Figure:
    """
    Create box plot showing distribution of records by data source.
    
    Args:
        df: Input DataFrame
        
    Returns:
        plotly Figure object
    """
    fig = px.box(
        df,
        x='Data.Source',
        y='Records',
        color='Data.Source',
        color_discrete_map=DATA_SOURCE_COLORS,
        title='Record Distribution by Data Source',
        points='all'
    )
    
    fig.update_layout(
        xaxis_title='Data Source',
        yaxis_title='Records (log scale)',
        yaxis_type='log',
        template='plotly_white',
        height=CHART_CONFIG['default_height'],
        showlegend=False,
        font=dict(size=CHART_CONFIG['font_size'])
    )
    
    return fig


# ============================================================================
# SUNBURST CHART
# ============================================================================

def plot_hierarchical_sunburst(df: pd.DataFrame) -> go.Figure:
    """
    Create sunburst chart showing hierarchical data structure.
    
    Args:
        df: Input DataFrame with Grid, Species.Name, Data.Source
        
    Returns:
        plotly Figure object
    """
    # Aggregate data
    sunburst_data = df.groupby(['Grid', 'Species.Name', 'Data.Source'])['Records'].sum().reset_index()
    
    fig = px.sunburst(
        sunburst_data,
        path=['Grid', 'Species.Name', 'Data.Source'],
        values='Records',
        title='Hierarchical View: Grid → Species → Source'
    )
    
    fig.update_layout(
        template='plotly_white',
        height=600,
        font=dict(size=CHART_CONFIG['font_size'])
    )
    
    return fig
