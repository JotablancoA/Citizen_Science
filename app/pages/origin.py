"""
Origin Page
===========
Displays project context, objectives, and methodology.
"""

import streamlit as st
from styles import create_section_header, create_highlight_box


def show_origin_page():
    """Render the Origin & Context page."""
    
    # Page header
    st.markdown(create_section_header(
        "📚 Project Origin & Context",
        "Understanding the Citizen Science Wildlife Monitoring Initiative"
    ), unsafe_allow_html=True)
    
    # Introduction
    st.markdown("""
    ## Overview
    
    This dashboard presents comprehensive analyses of wildlife monitoring data from the 
    **Córdoba province citizen science project**. The initiative combines educational 
    outreach with scientific research to improve our understanding of wild mammal 
    distribution in Spain.
    """)
    
    # Project background
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div style='background-color: #e3f2fd; padding: 20px; border-radius: 10px; border-left: 5px solid #1976d2;'>
            <h3 style='color: #1976d2; margin-top: 0;'>🎯 Main Objective</h3>
            <p>
            To assess whether school participation can generate a significant volume of 
            reliable data on the distribution of wild mammals, comparable to historical 
            records available on platforms such as GBIF.
            </p>
            <p>
            The results demonstrate that over a four-month period, camera trapping produced 
            a large number of records, documenting previously unconfirmed species and 
            suggesting this approach is a viable strategy for updating distribution atlases 
            and promoting scientific literacy in education.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background-color: #e8f5e9; padding: 20px; border-radius: 10px; border-left: 5px solid #388e3c;'>
            <h3 style='color: #388e3c; margin-top: 0;'>📊 Key Statistics</h3>
            <ul>
                <li><strong>11 educational centers</strong> participated</li>
                <li><strong>800 students</strong> aged 4-12 years</li>
                <li><strong>11 UTM grids</strong> (10×10 km) surveyed</li>
                <li><strong>1,605 sequence records</strong> generated</li>
                <li><strong>589 daily records</strong> over 4 months</li>
                <li><strong>15 wild mammal species</strong> documented</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Project design
    st.markdown("""
    ## 🗺️ Project Design & Geographical Context
    
    The study was conceived as an educational and citizen science experience carried out 
    between **January and April 2024** in the province of Córdoba, Spain.
    """)
    
    tab1, tab2, tab3 = st.tabs(["🎓 Participants", "📍 Study Area", "🎯 Activities"])
    
    with tab1:
        st.markdown("""
        ### Participants and Scope
        
        A total of **11 educational centers** and **800 schoolchildren** aged between 
        four and twelve participated in the **IncluScience-Me** and **ConCiencia-2** projects.
        
        **Role of Students:**
        - Actively participated in hypothesis design
        - Conducted field observations
        - Collected and processed data
        - Analyzed results
        - Disseminated findings
        - Placed and monitored camera traps
        
        The aim was to promote **scientific, participatory, and social dimensions**, 
        stimulating interest in science and conservation among young students.
        """)
    
    with tab2:
        st.markdown("""
        ### Study Area
        
        Sampling covered **11 UTM grids of 10×10 km** near educational centers in Córdoba, 
        encompassing various habitats:
        
        - **Agricultural areas**: Primarily olive groves
        - **Pastures**: Open grasslands and meadows
        - **Dense scrubland**: Mediterranean vegetation
        - **Mixed landscapes**: Habitat mosaics
        
        This diversity of habitats allowed for comprehensive species detection across 
        different ecological contexts.
        """)
    
    with tab3:
        st.markdown("""
        ### Key Activities
        
        Students engaged in multiple aspects of the scientific process:
        
        1. **Hypothesis Formation**: Discussed predictions about local wildlife
        2. **Camera Trap Deployment**: Strategically placed monitoring equipment
        3. **Data Collection**: Retrieved and organized camera trap images
        4. **Species Identification**: Learned to identify local mammals
        5. **Data Analysis**: Explored patterns and trends
        6. **Result Communication**: Presented findings to peers and community
        
        This hands-on approach fostered **scientific literacy** and **environmental awareness**.
        """)
    
    st.markdown("---")
    
    # Methodology
    st.markdown("""
    ## 🔬 Methodology
    
    A crucial part of the methodology was comparing data generated by the school project 
    with historical data from multiple sources.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### Data Sources
        
        **Camera Trap Records (2024)**
        - 4-month sampling period
        - 11 educational centers
        - Standardized protocols
        - Verified observations
        
        **GBIF Database (2008-2023)**
        - Historical occurrences
        - 15-year time span
        - Multiple contributors
        - Quality-controlled records
        """)
    
    with col2:
        st.markdown("""
        ### Citizen Science Platforms
        
        **Non-validated Records (up to 2023)**
        - **Observation.org**: General biodiversity
        - **iNaturalist**: Photo-based observations
        - **iMammalia**: Mammal-specific platform
        
        **Comparison Standard**
        - 10×10 km UTM grid system
        - Aligned with Spanish distribution atlases
        - Spatial consistency across sources
        """)
    
    st.markdown("---")
    
    # Impact and significance
    st.markdown(create_highlight_box("""
    <h2>💡 Impact & Significance</h2>
    
    <h3>Educational Impact</h3>
    <ul>
        <li>Enhanced scientific literacy among 800 students</li>
        <li>Hands-on experience with real research methods</li>
        <li>Increased environmental awareness and conservation values</li>
        <li>Development of critical thinking and data analysis skills</li>
    </ul>
    
    <h3>Scientific Contribution</h3>
    <ul>
        <li>Generated data volume comparable to 15 years of GBIF records</li>
        <li>Documented species previously unconfirmed in specific grids</li>
        <li>Provided reliable, verifiable wildlife distribution data</li>
        <li>Demonstrated viability of school-based citizen science</li>
    </ul>
    
    <h3>Conservation Value</h3>
    <ul>
        <li>Updated distribution information for conservation planning</li>
        <li>Identified biodiversity hotspots and gaps</li>
        <li>Created baseline data for long-term monitoring</li>
        <li>Engaged local communities in wildlife conservation</li>
    </ul>
    """, 'highlight'), unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Reference
    st.markdown("""
    ## 📖 Reference
    
    **Citation:**
    
    > Murillo Jiménez, T., Ferrer Ferrando, D., Olivares Collado, C., Guerrero Casado, J., & Blanco-Aguiar, J. A. (2025, April 8). 
    > *Fototrampeo en las Aulas: Oportunidades de la Ciencia Ciudadana para Contribuir al Conocimiento de la Distribución de los Mamíferos Silvestres* 
    > (Camera Trapping in Classrooms: Opportunities for Citizen Science to Contribute to Knowledge of Wild Mammal Distribution). 
    > Ecosistemas, 34(1), 2848-2848. Asociacion Espanola de Ecologia Terrestre (AEET). 
    > http://doi.org/10.7818/ecos.2848
    
    ---
    
    **Projects:**
    - **IncluScience-Me**: Inclusive science education initiative
    - **ConCiencia-2**: Consciousness and science awareness program
    - **Momentum CSIC**: Desarrolla tu Talento Digital - https://momentum.csic.es/
    """)
    
    # Call to action
    st.info("""
    🔍 **Explore Further**: Use the navigation menu to explore the data, analyses, and findings 
    from this groundbreaking citizen science initiative.
    """)
