"""
Solar Challenge Dashboard - Interactive Streamlit Application
Week 0/1 Project by Biruk Assamnew
"""
import streamlit as st
import pandas as pd
from pathlib import Path
import sys

# Add parent directory to path to import utils
sys.path.append(str(Path(__file__).parent))
from utils import (
    load_cleaned_data,
    create_boxplot,
    create_time_series,
    calculate_summary_stats,
    create_correlation_heatmap,
    create_wind_rose,
    create_ranking_chart
)

# Page configuration
st.set_page_config(
    page_title="Solar Challenge Dashboard",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and description
st.title("☀️ Solar Radiation Analysis Dashboard")
st.markdown("""
This interactive dashboard presents exploratory data analysis (EDA) and insights 
from solar radiation measurements across three West African countries: 
**Benin**, **Sierra Leone**, and **Togo**.
""")

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Select Analysis View",
    ["Overview", "Country Comparison", "Detailed Country Analysis", "Statistical Tests"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### About")
st.sidebar.info(
    "**Solar Challenge Dashboard**\n\n"
    "Week 0/1 Project\n\n"
    "Data: Solar radiation measurements from Benin, Sierra Leone, and Togo"
)

# Load data function with caching
@st.cache_data
def load_all_data():
    """Load all country data and combine into single DataFrame."""
    try:
        benin = load_cleaned_data('Benin')
        sierra_leone = load_cleaned_data('Sierra Leone')
        togo = load_cleaned_data('Togo')
        
        combined = pd.concat([benin, sierra_leone, togo], ignore_index=True)
        return combined, benin, sierra_leone, togo
    except FileNotFoundError as e:
        st.error(f"Error loading data: {e}")
        st.info("Please ensure you have run the EDA notebooks to generate cleaned data files.")
        st.stop()

# Load data
combined_data, benin_data, sierra_leone_data, togo_data = load_all_data()

# ==================== OVERVIEW PAGE ====================
if page == "Overview":
    st.header("📊 Project Overview")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Records", f"{len(combined_data):,}")
    with col2:
        st.metric("Countries Analyzed", "3")
    with col3:
        st.metric("Variables Tracked", "14")
    
    st.markdown("---")
    
    # Key metrics by country
    st.subheader("Key Metrics by Country")
    
    metrics_cols = st.columns(3)
    
    for i, (country, data) in enumerate([
        ("Benin", benin_data),
        ("Sierra Leone", sierra_leone_data),
        ("Togo", togo_data)
    ]):
        with metrics_cols[i]:
            st.markdown(f"### {country}")
            st.metric("Avg GHI (W/m²)", f"{data['GHI'].mean():.2f}")
            st.metric("Avg DNI (W/m²)", f"{data['DNI'].mean():.2f}")
            st.metric("Avg Temp (°C)", f"{data['Tamb'].mean():.2f}")
            st.metric("Records", f"{len(data):,}")
    
    st.markdown("---")
    
    # Country ranking
    st.subheader("☀️ Solar Potential Ranking")
    ranking_fig = create_ranking_chart(combined_data, 'GHI')
    st.plotly_chart(ranking_fig, use_container_width=True)
    
    st.markdown("---")
    
    # Summary statistics table
    st.subheader("📈 Summary Statistics")
    summary_df = calculate_summary_stats(combined_data, ['GHI', 'DNI', 'DHI', 'Tamb'])
    
    # Format the dataframe for better display
    display_df = summary_df.copy()
    display_df = display_df.round(2)
    st.dataframe(display_df, use_container_width=True)

# ==================== COUNTRY COMPARISON PAGE ====================
elif page == "Country Comparison":
    st.header("🌍 Cross-Country Comparison")
    
    st.markdown("""
    Compare solar radiation variables across Benin, Sierra Leone, and Togo to identify 
    regional patterns and optimal locations for solar energy deployment.
    """)
    
    # Variable selection
    comparison_vars = st.multiselect(
        "Select variables to compare:",
        ['GHI', 'DNI', 'DHI', 'ModA', 'ModB', 'Tamb', 'RH', 'WS'],
        default=['GHI', 'DNI', 'DHI']
    )
    
    if comparison_vars:
        # Boxplot comparison
        st.subheader("📦 Distribution Comparison")
        boxplot_fig = create_boxplot(combined_data, comparison_vars)
        st.plotly_chart(boxplot_fig, use_container_width=True)
        
        st.markdown("---")
        
        # Time series comparison
        st.subheader("📅 Time Series Comparison")
        selected_var = st.selectbox("Select variable for time series:", comparison_vars)
        
        # Sample data for faster rendering (every 10th point)
        sample_data = combined_data.iloc[::10]
        
        time_series_fig = create_time_series(sample_data, selected_var)
        st.plotly_chart(time_series_fig, use_container_width=True)
        
        st.markdown("---")
        
        # Statistical summary
        st.subheader("📊 Statistical Summary")
        stats_df = calculate_summary_stats(combined_data, comparison_vars)
        st.dataframe(stats_df.round(2), use_container_width=True)
        
        # Key insights
        st.markdown("### 🔍 Key Observations")
        
        # Calculate which country has highest mean for each variable
        for var in comparison_vars:
            country_means = combined_data.groupby('Country')[var].mean().sort_values(ascending=False)
            top_country = country_means.index[0]
            top_value = country_means.values[0]
            
            st.markdown(f"- **{var}**: {top_country} has the highest average ({top_value:.2f})")
    
    else:
        st.warning("Please select at least one variable to compare.")

# ==================== DETAILED COUNTRY ANALYSIS PAGE ====================
elif page == "Detailed Country Analysis":
    st.header("🔬 Detailed Country Analysis")
    
    # Country selection
    selected_country = st.selectbox(
        "Select a country for detailed analysis:",
        ["Benin", "Sierra Leone", "Togo"]
    )
    
    # Get country data
    country_data_map = {
        "Benin": benin_data,
        "Sierra Leone": sierra_leone_data,
        "Togo": togo_data
    }
    country_data = country_data_map[selected_country]
    
    # Display country metrics
    st.subheader(f"📊 {selected_country} - Key Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Avg GHI", f"{country_data['GHI'].mean():.2f} W/m²")
    with col2:
        st.metric("Avg DNI", f"{country_data['DNI'].mean():.2f} W/m²")
    with col3:
        st.metric("Avg Temperature", f"{country_data['Tamb'].mean():.2f} °C")
    with col4:
        st.metric("Avg Humidity", f"{country_data['RH'].mean():.2f} %")
    
    st.markdown("---")
    
    # Correlation heatmap
    st.subheader("🔗 Correlation Analysis")
    corr_fig = create_correlation_heatmap(combined_data, selected_country)
    st.plotly_chart(corr_fig, use_container_width=True)
    
    st.markdown("---")
    
    # Wind analysis
    st.subheader("💨 Wind Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        wind_rose_fig = create_wind_rose(combined_data, selected_country)
        st.plotly_chart(wind_rose_fig, use_container_width=True)
    
    with col2:
        st.markdown(f"### Wind Statistics - {selected_country}")
        st.metric("Average Wind Speed", f"{country_data['WS'].mean():.2f} m/s")
        st.metric("Max Wind Speed", f"{country_data['WS'].max():.2f} m/s")
        st.metric("Average Gust Speed", f"{country_data['WSgust'].mean():.2f} m/s")
        
        # Most common wind direction
        direction_bins = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
        country_data_copy = country_data.copy()
        country_data_copy['WD_binned'] = pd.cut(
            country_data_copy['WD'],
            bins=range(0, 361, 45),
            labels=direction_bins,
            include_lowest=True
        )
        most_common = country_data_copy['WD_binned'].mode()[0]
        st.metric("Prevailing Direction", most_common)
    
    st.markdown("---")
    
    # Time series for selected variable
    st.subheader("📈 Time Series Analysis")
    ts_variable = st.selectbox(
        "Select variable:",
        ['GHI', 'DNI', 'DHI', 'Tamb', 'RH', 'WS']
    )
    
    # Sample for performance
    sample_country_data = combined_data[combined_data['Country'] == selected_country].iloc[::10]
    
    ts_fig = create_time_series(sample_country_data, ts_variable, selected_country)
    st.plotly_chart(ts_fig, use_container_width=True)

# ==================== STATISTICAL TESTS PAGE ====================
elif page == "Statistical Tests":
    st.header("📊 Statistical Hypothesis Testing")
    
    st.markdown("""
    Perform statistical tests to determine if there are significant differences 
    in solar radiation measurements across the three countries.
    """)
    
    # Import scipy for tests
    from scipy import stats
    
    # Variable selection for testing
    test_var = st.selectbox(
        "Select variable for statistical testing:",
        ['GHI', 'DNI', 'DHI', 'Tamb', 'RH', 'WS']
    )
    
    # Prepare data for each country
    benin_vals = benin_data[test_var].dropna()
    sierra_leone_vals = sierra_leone_data[test_var].dropna()
    togo_vals = togo_data[test_var].dropna()
    
    st.markdown("---")
    
    # Display distributions
    st.subheader(f"Distribution of {test_var}")
    dist_fig = create_boxplot(combined_data, [test_var])
    st.plotly_chart(dist_fig, use_container_width=True)
    
    st.markdown("---")
    
    # ANOVA Test
    st.subheader("🧪 One-Way ANOVA Test")
    st.markdown("""
    **Null Hypothesis (H₀)**: The means of the three countries are equal.  
    **Alternative Hypothesis (H₁)**: At least one country mean is different.
    """)
    
    f_stat, p_value_anova = stats.f_oneway(benin_vals, sierra_leone_vals, togo_vals)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("F-statistic", f"{f_stat:.4f}")
    with col2:
        st.metric("p-value", f"{p_value_anova:.6f}")
    
    if p_value_anova < 0.05:
        st.success(f"✅ **Result**: Reject H₀ (p < 0.05). There are significant differences in {test_var} across countries.")
    else:
        st.info(f"ℹ️ **Result**: Fail to reject H₀ (p ≥ 0.05). No significant differences detected in {test_var} across countries.")
    
    st.markdown("---")
    
    # Kruskal-Wallis Test (non-parametric alternative)
    st.subheader("🧪 Kruskal-Wallis H Test")
    st.markdown("""
    **Non-parametric alternative** to ANOVA, used when data may not be normally distributed.  
    **Null Hypothesis (H₀)**: The distributions of the three countries are equal.  
    **Alternative Hypothesis (H₁)**: At least one country distribution is different.
    """)
    
    h_stat, p_value_kw = stats.kruskal(benin_vals, sierra_leone_vals, togo_vals)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("H-statistic", f"{h_stat:.4f}")
    with col2:
        st.metric("p-value", f"{p_value_kw:.6f}")
    
    if p_value_kw < 0.05:
        st.success(f"✅ **Result**: Reject H₀ (p < 0.05). There are significant differences in {test_var} distributions across countries.")
    else:
        st.info(f"ℹ️ **Result**: Fail to reject H₀ (p ≥ 0.05). No significant differences detected in {test_var} distributions across countries.")
    
    st.markdown("---")
    
    # Summary statistics comparison
    st.subheader("📊 Summary Statistics by Country")
    summary_stats = pd.DataFrame({
        'Country': ['Benin', 'Sierra Leone', 'Togo'],
        'Mean': [benin_vals.mean(), sierra_leone_vals.mean(), togo_vals.mean()],
        'Median': [benin_vals.median(), sierra_leone_vals.median(), togo_vals.median()],
        'Std Dev': [benin_vals.std(), sierra_leone_vals.std(), togo_vals.std()],
        'Min': [benin_vals.min(), sierra_leone_vals.min(), togo_vals.min()],
        'Max': [benin_vals.max(), sierra_leone_vals.max(), togo_vals.max()]
    })
    st.dataframe(summary_stats.round(2), use_container_width=True)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
        <p>Solar Challenge Dashboard | Week 0/1 Project | Built with Streamlit ☀️</p>
    </div>
    """,
    unsafe_allow_html=True
)
