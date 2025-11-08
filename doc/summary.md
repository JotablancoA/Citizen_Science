## Explanation of Distribution and Correlation Visualizations

### 1. Data Sources and Aggregation

The dataset combines species occurrence coming from two anlytical different approaches: (a) **Daily Record** for each camera trap device if a specie was recorded or nor by each specie and day.  and (b) **Sequences Record** are clusters of images sequences of related images). After cleaning, the platform labels were harmonized and the data were aggregated per species: we summed counts of records independently for Daily and Sequence sources to obtain `Daily_Sum` and `Sequences_Sum` for each species. These aggregated values form the basis of the exploratory plots.


### 2. Distribution Histograms

Two histograms display the frequency distribution of record counts (`Records`) for each source type: one for Sequences Record and one for Daily Record. Key points typically inspected in these plots include:

- **Skewness**: Citizen science data often show right-skew (many species with few records, few species with many records).

- **Zero / Low Inflation**: A concentration near zero suggests many species are rarely reported in a given mode.

- **Tail Behavior**: A long tail may indicate a handful of very commonly recorded species.

- **Comparative Spread**: Differences in spread between the two histograms can hint at contrasting engagement or detectability patterns between daily single-image submissions and multi-image sequence uploads.



If the Sequences histogram appears more concentrated at low counts while the Daily histogram has a broader tail, that could mean daily observations capture common species more redundantly, whereas sequences might be used selectively. Conversely, similar shapes would suggest both modes sample species with comparable intensity.


### 3. Correlation Scatter Plot

The scatter plot relates `Daily_Sum` (x-axis) to `Sequences_Sum` (y-axis) at the species level, with a fitted regression line (red) and semi-transparent points to mitigate overplotting. This visualization helps assess whether species recorded frequently in one mode are also frequent in the other.


### 4. Pearson Correlation Interpretation

The printed correlation matrix above includes the Pearson coefficient between `Daily_Sum` and `Sequences_Sum`. Interpretation guidelines:

- **Positive and High (e.g., > 0.6)**: Species popular in daily submissions tend also to generate many sequence records (shared drivers like abundance, conspicuousness, or observer interest).

- **Near Zero (≈ 0)**: Little linear association; each mode might capture distinct ecological or user behavior niches.

- **Moderate (0.3–0.5)**: Partial overlap—some joint popularity, yet mode-specific factors remain.

- **Negative** (unlikely here): Would imply substitution (species recorded heavily in one mode are underrepresented in the other).



Because counts can be highly skewed, the Pearson correlation may be influenced by a few high-count species. A log or square-root transform (after handling zeros) could be explored to stabilize variance and reassess the relationship.


### 5. Potential Data Characteristics and Caveats

- **Sampling Bias**: Volunteer interest and ease of photographing certain taxa may inflate counts independently of true abundance.

- **Detection Probability**: Some species are easier to record via sequences (behavioral patterns) versus daily single sightings.

- **Data Quality**: The distinction between validated and non-validated records (mentioned earlier) could affect reliability; merging sources without considering validation status may introduce noise.

- **Outliers**: Species with extremely high counts should be inspected to ensure they are not artifacts (e.g., mislabeling or duplicated submissions).


### 6. Suggestions for Further Analysis

- Apply log-transforms to both sums and recompute Pearson and Spearman correlations.

- Examine residuals of the regression line for heteroscedasticity (variance increasing with mean).

- Consider species-level metadata (e.g., taxonomy, habitat) to explain differential mode popularity.

- Partition analyses by grid cell to see if spatial patterns alter correlation strength.


### 7. Summary

The histograms contextualize the overall reporting intensity and its distribution, while the scatter plot and correlation quantify the alignment between daily and sequence reporting behaviors across species. Together they provide an initial quantitative lens on how different citizen science submission modes complement or overlap in documenting biodiversity.