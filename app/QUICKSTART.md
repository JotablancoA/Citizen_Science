# Citizen Science Wildlife Dashboard - Quick Start Guide

## 🚀 Quick Start (5 Minutes)

### 1. Install Python Dependencies

```bash
cd app
pip install -r requirements.txt
```

### 2. Verify Data Files

Make sure these files exist in the `data/` directory:
- ✅ `dataset_CSsources_mod.csv`
- ✅ `GBIFdata_CO.shp` (+ .dbf, .shx, .prj)
- ✅ `CO_UTM2.shp` (+ .dbf, .shx, .prj)
- ✅ `locCam3.csv`
- ✅ `siluetas.csv` (optional)

### 3. Run the Dashboard

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

---

## 📱 Using the Dashboard

### Navigation Flow

1. **Start with "Origin"** to understand the project context
2. **Explore "Data Exploration"** to browse records and maps
3. **Dive into "EDA"** for statistical analyses
4. **Review "Conclusions"** for key findings
5. **Check "ML"** for future capabilities

### Key Features

- **Sidebar Filters**: Refine data by species, grid, source, minimum records
- **Interactive Charts**: Hover for details, click legends to toggle series
- **Download Options**: Export filtered data as CSV
- **Map Tools**: Zoom, pan, click markers for popups

---

## 🛠️ Troubleshooting

### Common Issues

**Problem**: "Module not found" error  
**Solution**: Make sure you're in the `app/` directory and ran `pip install -r requirements.txt`

**Problem**: "Data file not found" error  
**Solution**: Check that data files are in `../data/` relative to `app/`

**Problem**: Maps not displaying  
**Solution**: Install streamlit-folium: `pip install streamlit-folium`

**Problem**: Slow performance  
**Solution**: Reduce data size or increase Streamlit cache settings

---

## 🎨 Customization

### Change Colors

Edit `config.py`:

```python
DATA_SOURCE_COLORS = {
    'Global Biodiversity': '#YourColor',
    # ...
}
```

### Add New Page

1. Create `app/pages/your_page.py`
2. Define `show_your_page()` function
3. Import in `pages/__init__.py`
4. Add to navigation in `app.py`

### Modify Map Center

Edit `config.py`:

```python
MAP_CONFIG = {
    'center_lat': YOUR_LAT,
    'center_lon': YOUR_LON,
    'default_zoom': YOUR_ZOOM
}
```

---

## 📊 Example Workflows

### Workflow 1: Identify Hotspots

1. Go to **Data Exploration** → **By Grid** tab
2. Sort grids by total records
3. Select top grid in dropdown
4. View species composition
5. Switch to **Interactive Maps** → **Cluster Map**
6. Zoom to identified grid

### Workflow 2: Compare Platforms

1. Go to **EDA** → **Species Richness**
2. Review bar chart of unique species per source
3. Check stacked composition chart
4. Read platform strengths section
5. Visit **Conclusions** → **Platform Comparison** for recommendations

### Workflow 3: Export Filtered Data

1. Use sidebar to apply filters (e.g., specific species)
2. Go to **Data Exploration** → **Raw Data** tab
3. Review filtered records
4. Click **Download Full Dataset (CSV)**
5. Use exported CSV for external analysis

---

## 💡 Tips & Best Practices

### Performance
- Apply filters to reduce dataset size before creating visualizations
- Close unused browser tabs to free memory
- Use "Apply Filters" button to control when filters take effect

### Analysis
- Always check both raw and log-transformed views for skewed data
- Additionaly consider Negative binomial distribution (see paper)
- Consider outliers when interpreting correlation analyses
- Cross-reference spatial patterns with habitat data

### Interpretation
- Right-skewed distributions are normal in citizen science data
- High-abundance species can dominate patterns—look at filtered views
- Platform complementarity is key—no single source tells the full story

---

## 🔗 Additional Resources

- **Full Documentation**: See `README.md`
- **EDA Reference**: Review `../doc/eda.md` for analysis background
- **Project Info**: Read `../doc/info.md` for project details

---

**Need Help?** Open an issue or contact the project team.

**Ready to contribute?** See Contributing section in `README.md`.
