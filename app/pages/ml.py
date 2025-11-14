"""
Machine Learning Page
=====================
Placeholder for future ML models and predictive analytics.
"""

import streamlit as st
from styles import create_section_header, create_highlight_box


def show_ml_page():
    """Render the Machine Learning (Coming Soon) page."""
    
    # Page header
    st.markdown(create_section_header(
        "🤖 Machine Learning & Predictive Analytics",
        "Advanced modeling and AI-powered insights (In Development)"
    ), unsafe_allow_html=True)
    
    # Coming soon message
    st.info("""
    🚧 **This section is currently under development.**
    
    Future machine learning capabilities will enhance the dashboard with 
    predictive models, automated pattern recognition, and AI-powered insights.
    """)
    
    # Planned features
    st.markdown("## 🔮 Planned Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(create_highlight_box("""
        <h3>📊 Predictive Models</h3>
        
        <h4>Species Distribution Models (SDMs)</h4>
        <ul>
            <li>Predict species occurrence probability</li>
            <li>Identify suitable habitats</li>
            <li>Project climate change impacts</li>
            <li>Guide conservation prioritization</li>
        </ul>
        
        <h4>Occupancy Modeling</h4>
        <ul>
            <li>Estimate detection probability</li>
            <li>Account for imperfect detection</li>
            <li>Model site occupancy dynamics</li>
            <li>Assess sampling adequacy</li>
        </ul>
        
        <h4>Temporal Forecasting</h4>
        <ul>
            <li>Predict seasonal abundance patterns</li>
            <li>Forecast population trends</li>
            <li>Detect anomalies and early warnings</li>
            <li>Optimize sampling schedules</li>
        </ul>
        """, 'info'), unsafe_allow_html=True)
    
    with col2:
        st.markdown(create_highlight_box("""
        <h3>🤖 AI-Powered Tools</h3>
        
        <h4>Automated Species Identification</h4>
        <ul>
            <li>Deep learning image classification</li>
            <li>Real-time camera trap processing</li>
            <li>Confidence scoring and validation</li>
            <li>Reduce manual identification effort</li>
        </ul>
        
        <h4>Anomaly Detection</h4>
        <ul>
            <li>Identify unusual observation patterns</li>
            <li>Flag potential data quality issues</li>
            <li>Detect rare or unexpected species</li>
            <li>Monitor ecosystem health indicators</li>
        </ul>
        
        <h4>Clustering & Pattern Mining</h4>
        <ul>
            <li>Discover hidden data structures</li>
            <li>Group similar species/grids</li>
            <li>Identify community assemblages</li>
            <li>Reveal ecological relationships</li>
        </ul>
        """, 'success'), unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Technical approach
    st.markdown("## 🛠️ Technical Approach")
    
    tab1, tab2, tab3 = st.tabs(["Algorithms", "Data Requirements", "Validation"])
    
    with tab1:
        st.markdown("""
        ### Machine Learning Algorithms
        
        **Supervised Learning:**
        - **Random Forest**: Species presence/absence classification
        - **Gradient Boosting (XGBoost)**: Abundance prediction
        - **Neural Networks**: Image-based species identification
        - **Support Vector Machines**: Habitat suitability modeling
        
        **Unsupervised Learning:**
        - **K-means / DBSCAN**: Spatial clustering
        - **PCA / t-SNE**: Dimensionality reduction and visualization
        - **Hierarchical Clustering**: Species community analysis
        
        **Time Series:**
        - **ARIMA / SARIMA**: Temporal forecasting
        - **Prophet**: Seasonal trend decomposition
        - **LSTM Networks**: Long-term dependency modeling
        
        **Spatial Models:**
        - **MaxEnt**: Maximum entropy species distribution
        - **Spatial Autoregressive Models**: Account for spatial autocorrelation
        - **Gaussian Processes**: Flexible spatial prediction
        """)
    
    with tab2:
        st.markdown("""
        ### Data Requirements for ML
        
        **Environmental Predictors:**
        - Land cover / land use layers
        - Digital elevation model (DEM)
        - Distance to water sources
        - Temperature and precipitation data
        - Human population density
        - Protected area boundaries
        
        **Training Data Needs:**
        - Verified species occurrences (camera traps)
        - Pseudo-absences or background points
        - Environmental values at observation locations
        - Temporal metadata (season, time of day)
        
        **Data Preprocessing:**
        - Spatial resampling to consistent resolution
        - Normalization and scaling
        - Handling missing values
        - Balancing classes (for rare species)
        - Train/validation/test split strategies
        """)
    
    with tab3:
        st.markdown("""
        ### Model Validation & Evaluation
        
        **Performance Metrics:**
        - **Classification**: Accuracy, Precision, Recall, F1-score, AUC-ROC
        - **Regression**: RMSE, MAE, R², Adjusted R²
        - **Spatial**: True Skill Statistic (TSS), Boyce Index
        
        **Cross-Validation:**
        - k-fold cross-validation
        - Spatial block cross-validation (for spatial data)
        - Temporal validation (train on past, test on recent)
        
        **Interpretability:**
        - Variable importance plots
        - Partial dependence plots
        - SHAP values for feature attribution
        - Spatial prediction uncertainty maps
        
        **Validation Against Field Data:**
        - Compare predictions with held-out camera trap data
        - Expert review of flagged anomalies
        - Ground-truthing of predicted hotspots
        """)
    
    st.markdown("---")
    
    # Use cases
    st.markdown("## 🎯 Practical Use Cases")
    
    use_case1, use_case2, use_case3 = st.columns(3)
    
    with use_case1:
        st.markdown("""
        ### 🏞️ Conservation Planning
        
        **Scenario:** Identify priority areas for new protected areas
        
        **ML Approach:**
        - Train SDM for rare/threatened species
        - Predict suitable unprotected habitat
        - Overlay with land ownership/cost data
        - Rank sites by conservation value
        
        **Output:** Interactive map of recommended conservation zones
        """)
    
    with use_case2:
        st.markdown("""
        ### 📸 Smart Camera Placement
        
        **Scenario:** Optimize limited camera trap resources
        
        **ML Approach:**
        - Cluster analysis of species assemblages
        - Predict high-diversity areas
        - Model detectability by habitat
        - Suggest optimal grid cells
        
        **Output:** Camera deployment recommendations with expected yield
        """)
    
    with use_case3:
        st.markdown("""
        ### 🔔 Early Warning System
        
        **Scenario:** Detect population declines before critical
        
        **ML Approach:**
        - Time series forecasting of abundance
        - Anomaly detection on observation rates
        - Threshold-based alerts
        - Confidence intervals on predictions
        
        **Output:** Automated alerts when trends deviate from expected
        """)
    
    st.markdown("---")
    
    # Integration roadmap
    st.markdown(create_highlight_box("""
    <h2>🗓️ Implementation Roadmap</h2>
    
    <h3>Phase 1: Data Preparation (Months 1-2)</h3>
    <ul>
        <li>Acquire environmental raster layers</li>
        <li>Clean and validate training data</li>
        <li>Create model-ready datasets</li>
        <li>Document data provenance</li>
    </ul>
    
    <h3>Phase 2: Baseline Models (Months 3-4)</h3>
    <ul>
        <li>Develop initial SDMs for top 5 species</li>
        <li>Implement clustering for spatial patterns</li>
        <li>Create simple anomaly detection</li>
        <li>Validate with held-out data</li>
    </ul>
    
    <h3>Phase 3: Advanced Analytics (Months 5-6)</h3>
    <ul>
        <li>Integrate deep learning for images</li>
        <li>Build temporal forecasting models</li>
        <li>Develop ensemble predictions</li>
        <li>Add uncertainty quantification</li>
    </ul>
    
    <h3>Phase 4: Dashboard Integration (Months 7-8)</h3>
    <ul>
        <li>Embed interactive prediction maps</li>
        <li>Add model performance dashboards</li>
        <li>Create "what-if" scenario tools</li>
        <li>Enable automated report generation</li>
    </ul>
    
    <h3>Phase 5: Continuous Improvement (Ongoing)</h3>
    <ul>
        <li>Retrain models with new data</li>
        <li>Monitor prediction accuracy</li>
        <li>Expand to additional species/regions</li>
        <li>Incorporate user feedback</li>
    </ul>
    """, 'highlight'), unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Call to action
    st.success("""
    ### 🚀 Get Involved
    
    Interested in contributing to the ML development for this project?
    
    **We're looking for:**
    - Data scientists and ML engineers
    - Ecologists with modeling experience
    - GIS specialists for spatial data preparation
    - Software developers for integration
    
    Contact the project team to learn about collaboration opportunities.
    """)
    
    # Technical resources
    with st.expander("📚 Technical Resources & References"):
        st.markdown("""
        **Species Distribution Modeling:**
        - Elith, J., & Leathwick, J. R. (2009). Species distribution models: 
          Ecological explanation and prediction across space and time. *Annual Review 
          of Ecology, Evolution, and Systematics*, 40, 677-697.
        
        **Occupancy Modeling:**
        - MacKenzie, D. I., et al. (2017). *Occupancy Estimation and Modeling: 
          Inferring Patterns and Dynamics of Species Occurrence* (2nd ed.). 
          Academic Press.
        
        **Machine Learning in Ecology:**
        - Thessen, A. (2016). Adoption of machine learning techniques in ecology 
          and earth science. *One Ecosystem*, 1, e8621.
        
        **Camera Trap Image Classification:**
        - Norouzzadeh, M. S., et al. (2018). Automatically identifying, counting, 
          and describing wild animals in camera-trap images with deep learning. 
          *PNAS*, 115(25), E5716-E5725.
        
        **Python Libraries:**
        - **scikit-learn**: General-purpose ML algorithms
        - **TensorFlow / PyTorch**: Deep learning frameworks
        - **Prophet**: Time series forecasting
        - **geopandas / rasterio**: Spatial data handling
        - **SHAP**: Model interpretability
        """)
