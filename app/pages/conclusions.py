"""
Conclusions Page
================
Key findings, recommendations, and actionable insights.
"""

import streamlit as st
import pandas as pd
from styles import create_section_header, create_highlight_box


def show_conclusions_page(df: pd.DataFrame):
    """
    Render the Conclusions & Recommendations page.
    
    Args:
        df: Filtered citizen science DataFrame
    """
    
    # Page header
    st.markdown(create_section_header(
        "💡 Key Findings & Recommendations",
        "Evidence-based insights and strategic recommendations"
    ), unsafe_allow_html=True)
    
    # Executive summary
    st.markdown("""
    ## Executive Summary
    
    This citizen science wildlife monitoring project demonstrates that **school-based 
    camera trapping** can generate high-quality biodiversity data comparable to 
    established monitoring platforms, while simultaneously promoting **scientific 
    literacy** and **environmental stewardship** among young students.
    """)
    
    st.markdown("---")
    
    # Key findings tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🔍 Data Patterns",
        "🌍 Spatial Insights",
        "📊 Platform Comparison",
        "🎯 Strategic Recommendations"
    ])
    
    # TAB 1: Data Patterns
    with tab1:
        st.markdown("## 📈 Data Distribution Patterns")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div style='background-color: #e3f2fd; padding: 20px; border-radius: 10px; border-left: 5px solid #1976d2;'>
                <h3 style='color: #1976d2; margin-top: 0;'>📊 Long-Tail Distributions</h3>
                <p>The data exhibits classic <strong>right-skewed distributions</strong>:</p>
                <ul>
                    <li>Many species with few records</li>
                    <li>Few species with very high record counts</li>
                    <li>Median significantly lower than mean</li>
                </ul>
                <p><strong>Interpretation:</strong> Observation effort naturally concentrates 
                on common, visible, or charismatic species. This is typical of citizen science 
                data and reflects both ecological reality and observer behavior.</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style='background-color: #e8f5e9; padding: 20px; border-radius: 10px; border-left: 5px solid #388e3c;'>
                <h3 style='color: #388e3c; margin-top: 0;'>🔗 Correlation Insights</h3>
                <p>Analysis of <strong>Daily vs Sequences Records</strong> reveals:</p>
                <ul>
                    <li>Generally positive correlation at species level</li>
                    <li>One or two hyper-abundant species strongly influence trends</li>
                    <li>Underlying pattern clearer when outliers excluded</li>
                </ul>
                <p><strong>Implication:</strong> Both recording methods capture similar 
                patterns, but sensitivity analysis (with/without top species) provides 
                more nuanced understanding.</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("### Statistical Recommendations")
        st.markdown("""
        When analyzing this type of data:
        - Use **log transformations** for visualization and modeling
        - Apply **robust statistics** (medians, MAD) alongside traditional means
        - Consider **negative binomial** or **zero-inflated** models for count data
        - Implement **outlier-aware metrics** in routine reporting
        - Always show both raw and transformed views
        """)
    
    # TAB 2: Spatial Insights
    with tab2:
        st.markdown("## 🗺️ Spatial Patterns & Hotspots")
        
        st.markdown(create_highlight_box("""
        <h3>Key Spatial Findings</h3>
        
        <h4>🔥 Hotspots Identified</h4>
        <ul>
            <li>Clustered observations tied to specific UTM grids</li>
            <li>Heat maps reveal recurring high-activity zones</li>
            <li>Certain grids show exceptional species richness</li>
        </ul>
        
        <h4>📍 Coverage Gaps</h4>
        <ul>
            <li>Several grids have minimal or no records</li>
            <li>Geographic sampling bias toward accessible areas</li>
            <li>Some habitat types under-represented</li>
        </ul>
        
        <h4>🎥 Camera Trap Value</h4>
        <ul>
            <li>Cameras provide strong local evidence</li>
            <li>Fill gaps in volunteer platform coverage</li>
            <li>Enable verification of rare species reports</li>
        </ul>
        """, 'info'), unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### Management Actions
            
            **Priority Actions:**
            1. **Validate hotspots** with additional surveys
            2. **Fill gaps** by deploying cameras in under-sampled grids
            3. **Cross-reference** with habitat/protection layers
            4. **Monitor trends** in high-value conservation areas
            5. **Engage communities** near hotspots for long-term stewardship
            """)
        
        with col2:
            st.markdown("""
            ### Optimization Strategy
            
            **Camera Placement:**
            - Target grids with <5 species detected
            - Focus on habitat transition zones
            - Balance effort across land cover types
            - Align with protected area boundaries
            
            **Volunteer Guidance:**
            - Provide grid-specific species checklists
            - Highlight rarities for validation
            - Encourage visits to under-sampled areas
            """)
    
    # TAB 3: Platform Comparison
    with tab3:
        st.markdown("## 📊 Data Source Complementarity")
        
        if not df.empty:
            richness = df.groupby('Data.Source')['Species.Name'].nunique().to_dict()
            
            st.markdown("### Species Richness by Platform")
            
            cols = st.columns(len(richness))
            for idx, (source, count) in enumerate(richness.items()):
                with cols[idx]:
                    st.metric(source, f"{count} species")
        
        st.markdown(create_highlight_box("""
        <h3>Platform Strengths & Use Cases</h3>
        
        <h4>🌍 Global Biodiversity (GBIF)</h4>
        <ul>
            <li><strong>Strength:</strong> Long-term historical coverage (2008-2023)</li>
            <li><strong>Use case:</strong> Baseline comparisons, trend analysis</li>
            <li><strong>Limitation:</strong> Variable data quality, sparse recent records</li>
        </ul>
        
        <h4>📸 Sequences Record (Camera Traps)</h4>
        <ul>
            <li><strong>Strength:</strong> Verified observations, temporal detail</li>
            <li><strong>Use case:</strong> Activity patterns, behavior studies</li>
            <li><strong>Limitation:</strong> Limited spatial coverage, equipment costs</li>
        </ul>
        
        <h4>📅 Daily Record (School Project)</h4>
        <ul>
            <li><strong>Strength:</strong> Rapid presence/absence data</li>
            <li><strong>Use case:</strong> Quick surveys, educational engagement</li>
            <li><strong>Limitation:</strong> Less temporal detail than sequences</li>
        </ul>
        
        <h4>🌐 No Validation (Citizen Science Platforms)</h4>
        <ul>
            <li><strong>Strength:</strong> Broad geographic reach, high volume</li>
            <li><strong>Use case:</strong> Exploration, preliminary patterns</li>
            <li><strong>Limitation:</strong> Requires validation for formal analyses</li>
        </ul>
        """, 'success'), unsafe_allow_html=True)
        
        st.markdown("### Integration Strategy")
        st.info("""
        **Recommendation:** Combine platforms for completeness. Use camera traps as 
        **ground truth** to validate citizen science observations, while leveraging 
        broad platform reach to identify new survey targets.
        
        Track **unique species per source** over time to monitor complementarity and 
        ensure no single platform dominates evidence base.
        """)
    
    # TAB 4: Strategic Recommendations
    with tab4:
        st.markdown("## 🎯 Strategic Recommendations")
        
        st.markdown("""
        Based on comprehensive data analysis, we propose the following evidence-based 
        actions to strengthen wildlife monitoring and conservation in Córdoba Province.
        """)
        
        # Recommendations organized by theme
        rec1, rec2 = st.columns(2)
        
        with rec1:
            st.markdown(create_highlight_box("""
            <h3>🔬 Research & Monitoring</h3>
            
            <h4>1. Balance Sampling Effort</h4>
            <ul>
                <li>Add cameras to under-sampled grids</li>
                <li>Relocate equipment from saturated areas</li>
                <li>Focus volunteer attention on gaps</li>
            </ul>
            
            <h4>2. Enhance Data Quality</h4>
            <ul>
                <li>Implement validation protocols</li>
                <li>Provide species ID training</li>
                <li>Use camera data as verification standard</li>
            </ul>
            
            <h4>3. Temporal Expansion</h4>
            <ul>
                <li>Extend beyond 4-month sampling window</li>
                <li>Capture seasonal variation</li>
                <li>Track year-to-year trends</li>
            </ul>
            """, 'info'), unsafe_allow_html=True)
        
        with rec2:
            st.markdown(create_highlight_box("""
            <h3>🌱 Education & Outreach</h3>
            
            <h4>4. Scale Up School Participation</h4>
            <ul>
                <li>Recruit additional educational centers</li>
                <li>Develop standardized curriculum materials</li>
                <li>Share success stories and results</li>
            </ul>
            
            <h4>5. Community Engagement</h4>
            <ul>
                <li>Host public data visualization events</li>
                <li>Create local species guides</li>
                <li>Establish citizen scientist recognition program</li>
            </ul>
            
            <h4>6. Policy Integration</h4>
            <ul>
                <li>Share findings with conservation authorities</li>
                <li>Inform protected area management plans</li>
                <li>Support evidence-based land use decisions</li>
            </ul>
            """, 'warning'), unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown(create_highlight_box("""
        <h3>📐 Technical Enhancements</h3>
        
        <h4>7. Analytical Sophistication</h4>
        <ul>
            <li>Implement mixed-effects models for nested data</li>
            <li>Use occupancy modeling for detection probability</li>
            <li>Apply spatial autocorrelation tests</li>
            <li>Develop predictive habitat suitability models</li>
        </ul>
        
        <h4>8. Environmental Integration</h4>
        <ul>
            <li>Overlay land cover data (agriculture, forest, urban)</li>
            <li>Incorporate elevation and water proximity</li>
            <li>Link to protected area boundaries</li>
            <li>Analyze anthropogenic disturbance factors</li>
        </ul>
        
        <h4>9. Temporal Refinement</h4>
        <ul>
            <li>Include timestamps for diel activity analysis</li>
            <li>Align camera events with weather data</li>
            <li>Track seasonal migration and breeding patterns</li>
            <li>Develop early warning systems for population declines</li>
        </ul>
        """, 'highlight'), unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Future directions
    st.markdown("## 🚀 Future Directions")
    
    future1, future2, future3 = st.columns(3)
    
    with future1:
        st.markdown("""
        ### Dashboard Evolution
        
        - Real-time data feeds
        - Automated species ID (AI/ML)
        - Mobile app integration
        - Public API access
        - Alert notifications
        """)
    
    with future2:
        st.markdown("""
        ### Research Extensions
        
        - Genetic sampling
        - Disease surveillance
        - Human-wildlife conflict mapping
        - Ecosystem service valuation
        - Climate change impacts
        """)
    
    with future3:
        st.markdown("""
        ### Institutional Growth
        
        - Regional network expansion
        - International collaborations
        - University partnerships
        - Funding diversification
        - Long-term data archiving
        """)
    
    # Closing statement
    st.markdown("---")
    st.success("""
    ### 🌟 Conclusion
    
    This project demonstrates that **citizen science**, when thoughtfully designed and 
    integrated with educational objectives, can generate **scientifically valuable data** 
    while fostering the next generation of **conservation champions**.
    
    The combination of camera traps, student engagement, and digital platforms provides 
    a **scalable model** for biodiversity monitoring that balances scientific rigor with 
    educational impact and community participation.
    
    By implementing the recommendations above, Córdoba Province can establish itself as 
    a **leader in participatory wildlife monitoring**, contributing both to scientific 
    knowledge and to a culture of environmental stewardship.
    """)
