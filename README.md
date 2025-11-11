# Solar Radiation Analysis - Week 1 Challenge

## Project Overview
This project analyzes solar radiation data from three African countries (Benin, Sierra Leone, and Togo) to identify optimal locations for solar panel installations. The analysis includes comprehensive exploratory data analysis (EDA), data cleaning, statistical analysis, and visualization.

## Table of Contents
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Environment Setup](#environment-setup)
- [Usage](#usage)
- [Data Description](#data-description)
- [Analysis Workflow](#analysis-workflow)
- [CI/CD Pipeline](#cicd-pipeline)
- [Contributing](#contributing)

## Installation

### Prerequisites
- Python 3.9 or higher
- Git
- pip (Python package manager)

### Clone the Repository
```bash
git clone https://github.com/Biruk7479/solar-challenge-week1.git
cd solar-challenge-week1
```

## Environment Setup

### Option 1: Using venv (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### Option 2: Using Conda
```bash
# Create conda environment
conda create -n solar-analysis python=3.10

# Activate environment
conda activate solar-analysis

# Install dependencies
pip install -r requirements.txt
```

## Project Structure
```
solar-challenge-week1/
├── .github/
│   └── workflows/
│       └── unittests.yml          # CI/CD pipeline configuration
├── .vscode/
│   └── settings.json              # VS Code settings
├── data/                          # Data directory (excluded from git)
│   ├── benin-malanville.csv
│   ├── sierraleone-bumbuna.csv
│   ├── togo-dapaong_qc.csv
│   └── *_clean.csv               # Cleaned datasets
├── notebooks/
│   ├── __init__.py
│   ├── README.md
│   ├── benin_eda.ipynb           # Benin EDA notebook
│   ├── sierraleone_eda.ipynb     # Sierra Leone EDA notebook
│   └── togo_eda.ipynb            # Togo EDA notebook
├── src/
│   └── __init__.py               # Source code modules
├── scripts/
│   ├── __init__.py
│   └── README.md                 # Utility scripts
├── tests/
│   └── __init__.py               # Unit tests
├── .gitignore
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## Data Description

The project analyzes solar radiation data with the following key measurements:

### Solar Radiation Metrics
- **GHI** (Global Horizontal Irradiance): Total solar radiation received on a horizontal surface
- **DNI** (Direct Normal Irradiance): Direct solar radiation perpendicular to the sun
- **DHI** (Diffuse Horizontal Irradiance): Scattered solar radiation on a horizontal surface

### Environmental Measurements
- **TModA, TModB**: Temperature readings from Module A and Module B
- **Tamb**: Ambient temperature
- **RH**: Relative Humidity
- **BP**: Barometric Pressure
- **WS**: Wind Speed
- **WSgust**: Wind Gust Speed
- **WD**: Wind Direction

### Module Measurements
- **ModA, ModB**: Sensor readings from solar modules

## Analysis Workflow

### Task 1: Git & Environment Setup ✅
- [x] Initialize GitHub repository
- [x] Set up Python virtual environment
- [x] Create branch structure (setup-task)
- [x] Configure .gitignore
- [x] Add requirements.txt
- [x] Set up GitHub Actions CI/CD
- [x] Document environment reproduction

### Task 2: Data Profiling, Cleaning & EDA
For each country (Benin, Sierra Leone, Togo):

#### 2.1 Summary Statistics & Missing Values
- Generate descriptive statistics using `df.describe()`
- Identify missing values and columns with >5% nulls
- Document data quality issues

#### 2.2 Outlier Detection & Cleaning
- Compute Z-scores for key variables (GHI, DNI, DHI, ModA, ModB, WS, WSgust)
- Flag outliers with |Z| > 3
- Apply appropriate cleaning strategies (drop/impute)
- Export cleaned data to `data/<country>_clean.csv`

#### 2.3 Time Series Analysis
- Visualize trends in GHI, DNI, DHI, and Tamb over time
- Identify seasonal patterns and daily cycles
- Detect anomalies in solar irradiance

#### 2.4 Correlation Analysis
- Generate correlation heatmaps
- Create scatter plots for key variable relationships
- Analyze wind effects on solar radiation

#### 2.5 Wind & Distribution Analysis
- Create wind rose diagrams
- Generate histograms for key variables
- Analyze wind direction patterns

#### 2.6 Temperature & Humidity Analysis
- Examine RH influence on temperature and solar radiation
- Create bubble charts (GHI vs Tamb with RH as bubble size)

## Usage

### Running EDA Notebooks
```bash
# Activate your virtual environment first
source venv/bin/activate  # or: conda activate solar-analysis

# Start Jupyter Notebook
jupyter notebook

# Navigate to notebooks/ directory and open the desired notebook
```

### Running Tests
```bash
# Run all tests
pytest tests/ --verbose

# Run with coverage report
pytest tests/ --cov=src --cov-report=html
```

### Running Scripts
```bash
python scripts/your_script.py
```

## CI/CD Pipeline

The project uses GitHub Actions for continuous integration:

### Workflow Features
- **Multi-version Testing**: Tests against Python 3.9, 3.10, and 3.11
- **Automated Linting**: Flake8 checks for code quality
- **Dependency Caching**: Speeds up subsequent builds
- **Test Execution**: Runs pytest with coverage reports

### Trigger Events
- Push to `main`, `master`, or `setup-task` branches
- Pull requests to `main` or `master`

## Key Performance Indicators (KPIs)

### Task 1: Development Environment Setup
- ✅ Repository properly initialized with version control
- ✅ Virtual environment configured and documented
- ✅ CI/CD pipeline functional
- ✅ Proper branching strategy implemented

### Task 2: EDA Excellence
- 📊 Comprehensive statistical analysis
- 🧹 Robust data cleaning methodology
- 📈 Insightful visualizations
- 🔍 Actionable insights from correlation analysis
- 📝 Clear documentation of findings

## Contributing

### Branching Strategy
- `main/master`: Production-ready code
- `setup-task`: Initial setup and configuration
- `eda-<country>`: Country-specific EDA work

### Commit Message Convention
- `init:` Initial setup
- `chore:` Maintenance tasks
- `ci:` CI/CD changes
- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation updates
- `test:` Test additions/modifications

## References & Resources

### Statistical Analysis
- [Scipy Documentation](https://docs.scipy.org/doc/scipy/)
- [Pandas User Guide](https://pandas.pydata.org/docs/user_guide/index.html)
- [Outlier Detection Methods](https://towardsdatascience.com/5-ways-to-detect-outliers-that-every-data-scientist-should-know-python-code-70a54335a623)

### Visualization
- [Matplotlib Tutorials](https://matplotlib.org/stable/tutorials/index.html)
- [Seaborn Documentation](https://seaborn.pydata.org/)
- [Plotly Python](https://plotly.com/python/)

### Solar Energy
- [Solar Radiation Basics](https://www.energy.gov/eere/solar/solar-radiation-basics)
- [Understanding GHI, DNI, and DHI](https://www.solar.com/learn/solar-panel-glossary/)

## License
This project is part of the 10 Academy AI/ML training program.

## Contact
- **Repository**: https://github.com/Biruk7479/solar-challenge-week1
- **Author**: Biruk7479

## Acknowledgments
- 10 Academy for providing the challenge and datasets
- Solar radiation data providers for the African regions analyzed
