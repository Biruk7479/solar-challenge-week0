# Solar Challenge Streamlit Dashboard

An interactive dashboard for exploring solar radiation data from Benin, Sierra Leone, and Togo.

## Features

- **Overview**: High-level metrics and country rankings
- **Country Comparison**: Side-by-side comparisons of solar radiation variables
- **Detailed Analysis**: In-depth exploration of individual countries with correlation heatmaps and wind roses
- **Statistical Tests**: ANOVA and Kruskal-Wallis tests to identify significant differences

## Running Locally

1. Ensure you have the cleaned data files in the `data/` directory:
   - `benin_clean.csv`
   - `sierraleone_clean.csv`
   - `togo_clean.csv`

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Streamlit app:
   ```bash
   streamlit run app/main.py
   ```

4. Open your browser to `http://localhost:8501`

## Deployment

This app can be deployed to [Streamlit Community Cloud](https://streamlit.io/cloud) for free.

### Steps:
1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Select `app/main.py` as the main file
5. Click "Deploy"

**Note**: Make sure to include the cleaned CSV files in your repository or configure the app to generate them on startup.

## Project Structure

```
app/
├── __init__.py          # Package initialization
├── main.py              # Main Streamlit application
├── utils.py             # Helper functions for data loading and visualization
└── README.md            # This file
```

## Technologies Used

- **Streamlit**: Interactive web application framework
- **Plotly**: Interactive visualizations
- **Pandas**: Data manipulation
- **SciPy**: Statistical tests
