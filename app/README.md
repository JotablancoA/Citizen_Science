# Citizen Science Wildlife Dashboard

🦌 **Interactive Intelligence Panel for Córdoba Province Wildlife Monitoring**

A comprehensive Streamlit-based dashboard for exploring, analyzing, and visualizing wildlife monitoring data from the Córdoba province citizen science project. This application integrates camera trap records, GBIF occurrences, and citizen science platform data to provide actionable insights for conservation and education.

---

## 📋 Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Data Requirements](#data-requirements)
- [Dashboard Sections](#dashboard-sections)
- [Architecture](#architecture)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [Citation](#citation)
- [License](#license)

---

## ✨ Features

### Core Capabilities

- **📊 Interactive Data Exploration**: Filter and explore wildlife records by species, UTM grid, and data source
- **📈 Advanced EDA**: Comprehensive statistical analyses including distributions, correlations, and patterns
- **🗺️ Spatial Visualization**: Interactive maps with clustering, heat maps, and camera trap locations
- **💡 Evidence-Based Insights**: Key findings and strategic recommendations for conservation
- **🎨 Professional UI/UX**: Custom CSS styling with intuitive navigation and responsive design
- **⚡ High Performance**: Data caching and optimized loading for smooth user experience

### Analysis Types

1. **Distribution Analysis**: Histogram visualizations and statistical summaries
2. **Correlation Analysis**: Daily vs Sequences records with outlier handling
3. **Species Richness**: Platform comparison and contribution analysis
4. **Spatial Patterns**: Hotspot identification and coverage gap detection
5. **Temporal Trends**: Year-over-year changes by taxonomic groups
6. **Multi-dimensional Views**: Hierarchical and sunburst visualizations

---

## 📁 Project Structure

```
app/
│
├── app.py                      # Main application entry point
├── config.py                   # Configuration settings and constants
├── data_loader.py              # Data loading and preprocessing functions
├── visualizations.py           # Plotly chart generation functions
├── styles.py                   # Custom CSS and styling utilities
│
├── pages/                      # Page modules
│   ├── __init__.py            # Package initialization
│   ├── origin.py              # Project origin and context page
│   ├── data_exploration.py    # Interactive data exploration page
│   ├── eda.py                 # Exploratory data analysis page
│   ├── conclusions.py         # Key findings and recommendations
│   └── ml.py                  # Machine learning (coming soon)
│
└── README.md                   # This file
```

---

## 🚀 Installation

### Prerequisites

- **Python 3.8+**
- **pip** package manager

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd Citizen_Science
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Verify Data Files

Ensure the following data files exist in the `data/` directory:

- `dataset_CSsources_mod.csv` - Citizen science records
- `GBIFdata_CO.shp` (and associated .dbf, .shx, .prj files) - GBIF occurrences
- `CO_UTM2.shp` (and associated files) - UTM grid polygons
- `locCam3.csv` - Camera trap locations
- `siluetas.csv` - Species silhouette URLs (optional)

---

## 💻 Usage

### Running the Dashboard

From the project root directory:

```bash
cd app
streamlit run app.py
```

The dashboard will open automatically in your default web browser at `http://localhost:8501`.

### Navigation

1. **Sidebar**: Use the control panel to filter data and navigate between sections
2. **Filters**: Apply species, grid, source, and minimum record filters
3. **Sections**: Explore different pages using the radio button navigation
4. **Interactive Charts**: Hover, zoom, and click on visualizations for details
5. **Download**: Export filtered data and summaries as CSV files

---

## 📊 Data Requirements

### Input Data Format

#### Citizen Science Records (`dataset_CSsources_mod.csv`)

| Column       | Type   | Description                           |
|-------------|--------|---------------------------------------|
| Species.Name| string | Species scientific name abbreviation  |
| Grid        | string | UTM grid ID (10×10 km)                |
| Data.Source | string | Data source platform                   |
| Records     | integer| Number of records                      |

**Accepted Data Sources:**
- `Global Biodiversity` (GBIF)
- `Sequences Record` (Camera traps)
- `Daily Record` (School observations)
- `No Validation` (Citizen science platforms)

#### GBIF Shapefile (`GBIFdata_CO.shp`)

Must include:
- Geometry (point locations)
- `genus` - Taxonomic genus
- `institut_1` - Institution/platform
- `year` - Observation year (optional, for temporal analysis)
- `order` - Taxonomic order (optional)

#### UTM Grid Shapefile (`CO_UTM2.shp`)

- Polygon geometries representing 10×10 km grid cells
- `CUADRICULA` - Grid ID field

#### Camera Locations (`locCam3.csv`)

| Column      | Type   | Description              |
|------------|--------|--------------------------|
| Nombre.Loc | string | Camera location name      |
| Latitude   | float  | Latitude (decimal degrees)|
| Longitude  | float  | Longitude (decimal degrees)|

---

## 📖 Dashboard Sections

### 1️⃣ Project Origin & Context

- Project background and objectives
- Participants and study area description
- Methodology and data sources
- Key statistics and impact
- Scientific reference

### 2️⃣ Data Exploration

- **Raw Data**: Browse and download complete dataset
- **By Species**: Species-level aggregations and rankings
- **By Grid**: UTM grid analysis and detail explorer
- **By Source**: Data source comparison and richness
- **Interactive Maps**: Cluster, heat, and camera location maps

### 3️⃣ Exploratory Data Analysis (EDA)

- **Distribution Analysis**: Histograms and statistical summaries
- **Correlation Analysis**: Daily vs Sequences with outlier sensitivity
- **Species Richness**: Platform contribution and complementarity
- **Spatial Patterns**: Heatmaps and hotspot identification
- **Temporal Trends**: Year-over-year accumulation curves
- **Multi-dimensional**: Sunburst charts and hierarchical views

### 4️⃣ Key Findings & Recommendations

- Executive summary of main findings
- Data pattern insights and interpretations
- Spatial strategy and management actions
- Platform comparison and integration recommendations
- Strategic roadmap for program enhancement

### 5️⃣ Machine Learning (Coming Soon)

- Planned predictive modeling capabilities
- Species distribution models (SDMs)
- Automated species identification
- Anomaly detection and early warning systems
- Implementation roadmap and technical approach

---

## 🏗️ Architecture

### Design Principles

1. **Modularity**: Separate concerns into distinct modules (data, visualization, styling)
2. **Reusability**: Functions designed for flexible reuse across pages
3. **Performance**: Streamlit caching for expensive operations
4. **Maintainability**: Clear documentation and consistent naming conventions
5. **Extensibility**: Easy to add new analyses and visualizations

### Key Components

#### `config.py`
- Centralized configuration management
- File paths, color schemes, application settings
- Easy customization without code changes

#### `data_loader.py`
- Data loading with error handling
- Filtering and aggregation functions
- Caching decorators for performance
- Geospatial data processing

#### `visualizations.py`
- Plotly-based interactive charts
- Consistent styling and theming
- Reusable plotting functions
- Support for various chart types

#### `styles.py`
- Custom CSS for professional appearance
- Utility functions for styled components
- Responsive design elements
- Color scheme management

#### `pages/`
- Modular page components
- Independent sections with clear responsibilities
- Easy to extend with new pages

---

## ⚙️ Configuration

### Customizing Settings

Edit `config.py` to customize:

```python
# Change color scheme
DATA_SOURCE_COLORS = {
    'Global Biodiversity': '#YOUR_COLOR',
    # ...
}

# Adjust map center
MAP_CONFIG = {
    'center_lat': YOUR_LAT,
    'center_lon': YOUR_LON,
    'default_zoom': YOUR_ZOOM
}

# Modify chart defaults
CHART_CONFIG = {
    'default_height': YOUR_HEIGHT,
    'dpi': YOUR_DPI
}
```

### Adding New Data Sources

1. Update `DATA_SOURCE_COLORS` in `config.py`
2. Ensure source name matches exactly in CSV file
3. Restart the application

---

## 🤝 Contributing

We welcome contributions! To contribute:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Add docstrings to all functions
- Include type hints where applicable
- Test thoroughly before submitting
- Update documentation as needed

---

## 📚 Citation

If you use this dashboard or methodology in your work, please cite:

> Jiménez, T. M., Ferrando, D. F., Collado, C. O., Casado, J. G., & Blanco-Aguiar, J. A. (2025). 
> Camera Trapping in Classrooms: Opportunities for Citizen Science to Contribute to Knowledge 
> of Wild Mammal Distribution. *Ecosistemas*, 34(1), 2848-2848.

---

## 📄 License

This project is part of the **IncluScience-Me** and **ConCiencia-2** initiatives.

For academic and non-commercial use. Please contact project authors for commercial licensing.

---

## 👥 Authors & Acknowledgments

**Project Team:**
- T. M. Jiménez
- D. F. Ferrando
- C. O. Collado
- J. G. Casado
- J. A. Blanco-Aguiar

**Dashboard Development:**
- Built for the Citizen Science Wildlife Monitoring Project
- Universidad de Castilla-La Mancha

**Special Thanks:**
- 11 participating educational centers
- 800 student citizen scientists
- Teachers and coordinators
- Local communities in Córdoba Province

---

## 📞 Contact & Support

For questions, bug reports, or collaboration inquiries:

- **Project Website**: [Link to project page]
- **Email**: [Project contact email]
- **GitHub Issues**: [Link to issue tracker]

---

## 🔄 Version History

### Version 1.0.0 (Current)
- Initial release
- Core dashboard functionality
- Five main sections (Origin, Data, EDA, Conclusions, ML placeholder)
- Interactive maps and visualizations
- Data filtering and export capabilities

### Planned Updates
- Machine learning integration
- Real-time data feeds
- Mobile app companion
- Additional languages support
- Enhanced spatial analysis tools

---

**Built with ❤️ for wildlife conservation and education**
