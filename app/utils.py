"""
Utility functions for the Solar Challenge Dashboard
"""
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path


def load_cleaned_data(country: str) -> pd.DataFrame:
    """
    Load cleaned data for a specific country.
    
    Args:
        country: Name of the country ('Benin', 'Sierra Leone', or 'Togo')
    
    Returns:
        DataFrame with cleaned data
    """
    country_file_map = {
        'Benin': 'benin_clean.csv',
        'Sierra Leone': 'sierraleone_clean.csv',
        'Togo': 'togo_clean.csv'
    }
    
    data_dir = Path(__file__).parent.parent / 'data'
    file_path = data_dir / country_file_map[country]
    
    if not file_path.exists():
        raise FileNotFoundError(f"Data file not found: {file_path}")
    
    df = pd.read_csv(file_path)
    
    # Convert Timestamp to datetime if it exists
    if 'Timestamp' in df.columns:
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    
    # Add country column for easy filtering
    df['Country'] = country
    
    return df


def create_boxplot(data: pd.DataFrame, variables: list) -> go.Figure:
    """
    Create interactive boxplots for selected variables across countries.
    
    Args:
        data: Combined DataFrame with data from all countries
        variables: List of column names to plot
    
    Returns:
        Plotly figure with boxplots
    """
    fig = go.Figure()
    
    countries = data['Country'].unique()
    colors = px.colors.qualitative.Plotly
    
    for i, var in enumerate(variables):
        for j, country in enumerate(countries):
            country_data = data[data['Country'] == country][var].dropna()
            
            fig.add_trace(go.Box(
                y=country_data,
                name=f"{country}",
                legendgroup=country,
                showlegend=(i == 0),  # Only show legend for first variable
                marker_color=colors[j % len(colors)],
                xaxis=f'x{i+1}' if i > 0 else 'x'
            ))
    
    # Update layout with subplots
    n_vars = len(variables)
    fig.update_layout(
        title="Distribution Comparison Across Countries",
        height=400,
        boxmode='group',
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis=dict(domain=[0, 0.30], title=variables[0] if n_vars > 0 else ""),
        xaxis2=dict(domain=[0.35, 0.65], title=variables[1] if n_vars > 1 else ""),
        xaxis3=dict(domain=[0.70, 1.0], title=variables[2] if n_vars > 2 else "")
    )
    
    return fig


def create_time_series(data: pd.DataFrame, variable: str, country: str = None) -> go.Figure:
    """
    Create time series plot for a variable.
    
    Args:
        data: DataFrame with Timestamp and variable columns
        variable: Column name to plot
        country: Optional country filter
    
    Returns:
        Plotly figure with time series
    """
    if country:
        plot_data = data[data['Country'] == country]
    else:
        plot_data = data
    
    fig = px.line(
        plot_data,
        x='Timestamp',
        y=variable,
        color='Country' if not country else None,
        title=f"{variable} Over Time" + (f" - {country}" if country else ""),
        labels={variable: f"{variable} (W/m²)" if variable in ['GHI', 'DNI', 'DHI'] else variable}
    )
    
    fig.update_layout(
        height=400,
        hovermode='x unified'
    )
    
    return fig


def calculate_summary_stats(data: pd.DataFrame, variables: list) -> pd.DataFrame:
    """
    Calculate summary statistics by country.
    
    Args:
        data: Combined DataFrame with Country column
        variables: List of variables to summarize
    
    Returns:
        DataFrame with summary statistics
    """
    summary_list = []
    
    for country in data['Country'].unique():
        country_data = data[data['Country'] == country][variables]
        
        stats = {
            'Country': country,
        }
        
        for var in variables:
            stats[f'{var}_mean'] = country_data[var].mean()
            stats[f'{var}_median'] = country_data[var].median()
            stats[f'{var}_std'] = country_data[var].std()
            stats[f'{var}_min'] = country_data[var].min()
            stats[f'{var}_max'] = country_data[var].max()
        
        summary_list.append(stats)
    
    return pd.DataFrame(summary_list)


def create_correlation_heatmap(data: pd.DataFrame, country: str) -> go.Figure:
    """
    Create correlation heatmap for a specific country.
    
    Args:
        data: DataFrame with country data
        country: Name of the country
    
    Returns:
        Plotly figure with correlation heatmap
    """
    country_data = data[data['Country'] == country]
    
    # Select numeric columns
    numeric_cols = ['GHI', 'DNI', 'DHI', 'ModA', 'ModB', 'Tamb', 'RH', 'WS', 'WSgust', 'BP']
    available_cols = [col for col in numeric_cols if col in country_data.columns]
    
    corr_matrix = country_data[available_cols].corr()
    
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.columns,
        colorscale='RdBu',
        zmid=0,
        text=corr_matrix.values.round(2),
        texttemplate='%{text}',
        textfont={"size": 10},
        colorbar=dict(title="Correlation")
    ))
    
    fig.update_layout(
        title=f"Correlation Heatmap - {country}",
        height=500,
        xaxis={'side': 'bottom'}
    )
    
    return fig


def create_wind_rose(data: pd.DataFrame, country: str) -> go.Figure:
    """
    Create wind rose plot for wind direction and speed.
    
    Args:
        data: DataFrame with WD and WS columns
        country: Name of the country
    
    Returns:
        Plotly figure with wind rose
    """
    country_data = data[data['Country'] == country].copy()
    
    # Define wind direction bins
    direction_bins = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE',
                     'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
    
    # Bin the wind directions (using list instead of range for float step)
    bin_edges = [i * 22.5 for i in range(17)]  # 0, 22.5, 45, ..., 360
    country_data['WD_binned'] = pd.cut(
        country_data['WD'],
        bins=bin_edges,
        labels=direction_bins,
        include_lowest=True
    )
    
    # Calculate mean wind speed for each direction
    wind_summary = country_data.groupby('WD_binned')['WS'].mean().reset_index()
    
    fig = go.Figure(go.Barpolar(
        r=wind_summary['WS'],
        theta=wind_summary['WD_binned'],
        marker_color='lightblue',
        marker_line_color='darkblue',
        marker_line_width=1,
        opacity=0.8
    ))
    
    fig.update_layout(
        title=f"Wind Rose - {country}",
        polar=dict(
            radialaxis=dict(visible=True, range=[0, wind_summary['WS'].max() * 1.1]),
            angularaxis=dict(direction='clockwise')
        ),
        height=500
    )
    
    return fig


def create_ranking_chart(data: pd.DataFrame, variable: str = 'GHI') -> go.Figure:
    """
    Create bar chart ranking countries by average of a variable.
    
    Args:
        data: Combined DataFrame with Country column
        variable: Variable to rank by (default: GHI)
    
    Returns:
        Plotly figure with ranking bar chart
    """
    avg_values = data.groupby('Country')[variable].mean().sort_values(ascending=False)
    
    # Use valid CSS colors: gold, silver, and bronze equivalents
    colors = ['#FFD700', '#C0C0C0', '#CD7F32'][:len(avg_values)]
    
    fig = go.Figure(go.Bar(
        x=avg_values.index,
        y=avg_values.values,
        marker_color=colors,
        text=avg_values.values.round(2),
        textposition='auto',
    ))
    
    fig.update_layout(
        title=f"Countries Ranked by Average {variable}",
        xaxis_title="Country",
        yaxis_title=f"Average {variable} (W/m²)" if variable in ['GHI', 'DNI', 'DHI'] else f"Average {variable}",
        height=400
    )
    
    return fig
