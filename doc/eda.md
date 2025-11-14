# Citizen Science Wildlife EDA: Storytelling Guide

This document narrates the exploratory data analysis (EDA) performed on wildlife records from Córdoba province, integrating citizen science submissions, GBIF occurrences, UTM grid geometry, and camera-trap locations. It aims to communicate insights clearly to non-technical readers while preserving technical rigor for analysts and decision-makers. It also outlines a blueprint for a future intelligence dashboard.

## Executive Summary

- Popular species and locations dominate the data (right-skewed distributions). Many species are recorded rarely, while a few are recorded very often.
- Daily Records and Sequences Record generally align at the species level (positive association), but one or two very common species can disproportionately drive the trend.
- Spatial hotspots appear around specific UTM grids; interactive maps reveal clusters of observations and areas with low coverage.
- Platforms differ in breadth and focus: some bring higher species richness, others provide dense records for a subset of species.
- Camera-trap sites provide strong local evidence and can complement broader volunteer platforms by filling gaps.

## Data Landscape

- `data/dataset_CSsources_mod.csv`: Tabular species records by species (Species.Name), UTM grid (Grid), platform (`Data.Source`), and `Records` count.
- `data/GBIFdata_CO.shp`: GBIF occurrence points with attributes such as year, taxonomic information, and source.
- `data/CO_UTM2.shp`: 10×10 km UTM grid polygons that provide spatial context.
- `data/locCam3.csv`: Camera-trap sites (latitude/longitude) with per-guild/species tallies.
- `data/siluetas.csv`: Species silhouettes used as icons in some map popups.

Outputs generated during the EDA:

- Static images in `img/`:
	- `histogram_distributions.png` — Distributions of Sequences vs Daily record counts.
	- `correlation_daily_sequences.png` — Species-level correlation between Daily and Sequences records.
	- `species_richness_by_source.png` — Number of species detected per data source.
	- `records_by_species_grid.png` — Faceted bar chart: species × grid × source.
	- `panel_mapps_heat.png` (panel of KDE maps by genus, if available).
	- Optional: `accumulated_curves_orders.png` (temporal trends by order, when year/order available).
- Interactive maps in `html/`:
	- `mapa_clusters_por_grid.html` — Clustered GBIF points over UTM grids.
	- `mapa_calor_con_utm_y_camaras.html` — Heat map of occurrences with camera locations.

## Story Arc: Questions We Set Out to Answer

1. Which species and locations are most frequently recorded, and how is observation effort distributed?
2. Do Sequences Record and Daily Record tell a consistent story about species presence?
3. Where are the spatial hotspots and gaps when records are overlaid with UTM grids and cameras?
4. Which platforms contribute most to species richness and coverage?
5. How are records changing over time (if year is available), and do trends differ by taxa or platform?

## Methods in Brief

- Standardized platform labels into `Data.Source` and species into `Species.Name`.
- Aggregated records by species and source for comparability (e.g., `Daily_Sum`, `Sequences_Sum`).
- Built histograms to characterize count distributions and inspect skewness.
- Computed Pearson correlation between `Daily_Sum` and `Sequences_Sum` and visualized with regression lines.
- Mapped GBIF points with UTM overlays; used cluster layers and heat maps to surface hotspots.
- Faceted bar plots highlighted grid-level species composition by source.
- Where available, plotted temporal trends by `year` and taxonomic `order`.

## Key Findings

### 1) Distributions: Long Tails and Rare Species

- The histograms show a classic right-skew: many species with few records, few species with many records.
- Interpretation: Citizen science data often follow effort and visibility—common, charismatic, or easily detected species dominate.
- Implication: Analyses should use robust statistics or transformations, and dashboards should highlight both common and rare species separately.

See: `img/histogram_distributions.png`.

### 2) Daily vs Sequences: Alignment with Influential Outliers

- At the species level, Daily Records and Sequences Record tend to rise together (positive correlation).
- One or two hyper-abundant species can pull the regression line; excluding them typically reveals the underlying pattern for the majority.
- Recommendation: In dashboards, show the overall correlation plus a sensitivity view excluding the top outlier species.

See: `img/correlation_daily_sequences.png`.

### 3) Spatial Patterns: Hotspots and Gaps

- Clustered map overlays indicate recurring hotspots tied to particular grids.
- Heat maps (with grids and camera locations) reveal where effort concentrates and where to expand coverage.
- Implication: Target new or under-sampled grids to balance spatial evidence; cross-check with habitat/protection layers in future iterations.

See: `html/mapa_clusters_por_grid.html`, `html/mapa_calor_con_utm_y_camaras.html`.

### 4) Platform Contributions: Complementary Strengths

- Species richness varies by platform. Some sources contribute broader species lists, others add depth for a subset.
- Use cases: Platforms may be optimized for certain taxa or contexts (e.g., rapid daily checks vs curated sequences).
- Recommendation: Combine platforms for completeness; track unique species per source to monitor complementarity over time.

See: `img/species_richness_by_source.png`.

### 5) Species × Grid × Source: Where to Focus

- Faceted bar charts by top grids show contrasting species composition and source dominance across space.
- Implication: Management actions and volunteer guidance can be grid-specific (e.g., “Grid UG18 needs more non-daily sources to validate rarities”).

See: `img/records_by_species_grid.png`.

### 6) Temporal Trends (When Available)

- If `year` and `order` are present, accumulated curves suggest how observation pressure and biodiversity signals evolve by taxonomic groups.
- Implication: Tracking trajectories by group helps detect early warnings (declines) and positive signals (recoveries).

See: `img/accumulated_curves_orders.png` (when generated).

## Data Quality and Caveats

- Observation bias: Visibility, accessibility, and observer interest skew the data.
- Validation status: Non-validated records may include misidentifications; consider quality flags in summaries.
- Outliers: Extremely high counts for a few species can mask typical patterns; include with-/without-outlier views.
- Spatial CRS and joins: Ensure consistent coordinate reference systems when layering points and grids.

## From EDA to Dashboard: Intelligence Blueprint

Design a dashboard that balances discovery for non-experts with analytical depth for practitioners.

### Core KPIs

- Total records, unique species, unique grids covered.
- Records and species per data source; share of unique species per source.
- Correlation (Daily vs Sequences) with toggle to exclude top outliers.
- Hotspot count and under-sampled grid count.

### Visual Building Blocks

- Distribution panel: Histograms of Sequences vs Daily record counts.
- Correlation card: Scatter with regression; outlier toggle.
- Richness panel: Bar chart of species by source; optional Venn/pairwise overlaps.
- Spatial view: Interactive map with UTM overlay, clusters, heat map, camera markers.
- Grid detail: Faceted species × grid chart with filters for taxa and source.
- Trends panel: Lines by year and taxonomic order (when available).

### Interactions and Filters

- Filters: Species/Genus, Data Source, Grid, Year, Validation status.
- Map-driven drill-down: Click a grid to populate species list, source breakdown, and recent records.
- Export: Snapshot PNG/CSV for reporting; link back to underlying evidence.

## Recommendations and Next Steps

1. Balance effort by adding/relocating cameras or volunteer focus to under-sampled grids.
2. Track platform complementarity with periodic species overlap summaries (unique vs shared species).
3. Incorporate validation flags into KPIs and provide separate quality-filtered views.
4. Add environmental layers (land cover, elevation, water) to explain hotspots and guide site selection.
5. Implement outlier-aware metrics (log scales, medians, robust correlations) in routine reporting.
6. If possible, include timestamps to analyze diel/seasonal activity and to align with camera-trap event times.

## Reproducibility and Assets

- Primary EDA notebooks: `notebooks/eda.ipynb`, `notebooks/visualizations.ipynb`.
- Data folder: `data/` (see files listed above).
- Static outputs: `img/` (PNG figures referenced in this guide).
- Interactive outputs: `html/` (open in a browser).

This guide will evolve as the dataset grows and the analysis matures. Use it as a foundation to brief stakeholders, prioritize field actions, and seed a production-grade intelligence dashboard.

