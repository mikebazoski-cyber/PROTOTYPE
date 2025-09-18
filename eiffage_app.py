#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import unicodedata
import os
import datetime
import re
import streamlit as st
from io import BytesIO
import time

# Set page configuration
st.set_page_config(
    page_title="Eiffage Scope 3 Emissions Analysis",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling with red, white, and black theme
st.markdown("""
<style>
    :root {
        --primary-red: #FF0000;
        --light-white: #FFFFFF;
        --dark-black: #000000;
    }
    
    /* Main container styling */
    .main {
        background-color: var(--light-white);
    }
    
    /* Black top bar */
    .black-top-bar {
        background-color: var(--dark-black);
        height: 60px;
        width: 100%;
        position: fixed;
        top: 0;
        left: 0;
        z-index: 999;
    }
    
    /* White content area */
    .white-content {
        background-color: var(--light-white);
        min-height: 100vh;
        padding-top: 80px; /* Space for fixed black bar */
    }
    
    /* Hero section with image and buttons */
    .hero-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 2rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    .hero-image {
        flex: 1;
        padding-right: 3rem;
    }
    
    .hero-image img {
        width: 100%;
        height: auto;
        border-radius: 10px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
    }
    
    .hero-buttons {
        flex: 1;
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
    }
    
    /* Custom button styling */
    .custom-button {
        background-color: var(--primary-red) !important;
        color: var(--light-white) !important;
        border: none !important;
        padding: 1.2rem 2rem !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        font-size: 1.2rem !important;
        text-align: center !important;
        width: 100% !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 8px rgba(255,0,0,0.2) !important;
    }
    
    .custom-button:hover {
        background-color: #CC0000 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 12px rgba(255,0,0,0.3) !important;
    }
    
    .custom-button:active {
        transform: translateY(0) !important;
    }
    
    /* Button container for consistent width */
    .button-container {
        width: 250px;
        margin: 0.5rem 0;
    }
    
    /* Remove default Streamlit button styles */
    .stButton > button {
        all: unset !important;
    }
    
    /* Content area styling */
    .content-section {
        max-width: 1200px;
        margin: 2rem auto;
        padding: 0 2rem;
    }
    
    /* Section headers */
    .section-header {
        font-size: 2.2rem;
        color: var(--dark-black);
        margin: 2rem 0 1.5rem 0;
        font-weight: bold;
        text-align: center;
        border-bottom: 3px solid var(--primary-red);
        padding-bottom: 0.5rem;
    }
    
    /* Footer styling */
    .footer {
        background-color: var(--dark-black);
        color: var(--light-white);
        text-align: center;
        padding: 2rem;
        margin-top: 3rem;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .hero-container {
            flex-direction: column;
            text-align: center;
        }
        
        .hero-image {
            padding-right: 0;
            padding-bottom: 2rem;
        }
        
        .hero-buttons {
            width: 100%;
        }
        
        .button-container {
            width: 100%;
        }
    }
</style>
""", unsafe_allow_html=True)

# Add black top bar
st.markdown('<div class="black-top-bar"></div>', unsafe_allow_html=True)

# White content area
st.markdown('<div class="white-content">', unsafe_allow_html=True)

# Hero section with image and buttons
st.markdown('<div class="hero-container">', unsafe_allow_html=True)

# Left side - Image
st.markdown('<div class="hero-image">', unsafe_allow_html=True)
try:
    st.image("/Users/mikemike/Downloads/eiffage pic for site.png", use_column_width=True)
except:
    st.warning("Image not found at the specified path. Using placeholder.")
    st.image("https://via.placeholder.com/400x300/FF0000/FFFFFF?text=Eiffage+Logo", use_column_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# Right side - Navigation buttons
st.markdown('<div class="hero-buttons">', unsafe_allow_html=True)

# Button container with consistent width
col1, col2, col3 = st.columns([1,1,1])

def go_to_home():
    st.session_state.current_page = "home"

def go_to_how_it_works():
    st.session_state.current_page = "how_it_works"

with col1:
    st.markdown('<div class="button-container">', unsafe_allow_html=True)
    if st.button("Home", key="home_btn_custom"):
        go_to_home()
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="button-container">', unsafe_allow_html=True)
    if st.button("How it Works", key="how_it_works_btn_custom"):
        go_to_how_it_works()
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="button-container">', unsafe_allow_html=True)
    def go_to_launch():
        st.session_state.current_page = "launch"
    if st.button("Launch", key="launch_btn_custom"):
        go_to_launch()
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # Close hero-buttons
st.markdown('</div>', unsafe_allow_html=True)  # Close hero-container

# Content sections
st.markdown('<div class="content-section">', unsafe_allow_html=True)

# Navigation callbacks
def go_to_home():
    st.session_state.current_page = "home"

def go_to_how_it_works():
    st.session_state.current_page = "how_it_works"

def go_to_launch():
    st.session_state.current_page = "launch"

# Brief introduction

def main():
    # Set up session state for navigation
    if "current_page" not in st.session_state:
        st.session_state.current_page = "home"

    # Hero section with navigation buttons
    col1, col2, col3 = st.columns([1,1,1])
    with col1:
        st.markdown('<div class="button-container">', unsafe_allow_html=True)
        if st.button("Home", key="home_btn_custom"):
            go_to_home()
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="button-container">', unsafe_allow_html=True)
        if st.button("How it Works", key="how_it_works_btn_custom"):
            go_to_how_it_works()
        st.markdown('</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="button-container">', unsafe_allow_html=True)
        if st.button("Launch", key="launch_btn_custom"):
            go_to_launch()
        st.markdown('</div>', unsafe_allow_html=True)

    # Main page logic
    if st.session_state.current_page == "home":
        st.markdown("""
            <div class="card">
                <h3>About This Tool</h3>
                <p class="info-text">
                    Our advanced Scope 3 emissions analysis tool helps organizations accurately measure and report 
                    their indirect greenhouse gas emissions across the entire value chain. By analyzing procurement data, 
                    supplier information, and industry-specific emission factors, we provide comprehensive insights 
                    into your carbon footprint.
                </p>
                <p class="info-text">
                    Understanding and managing Scope 3 emissions is crucial for developing effective sustainability strategies, 
                    meeting regulatory requirements, and demonstrating environmental responsibility to stakeholders.
                </p>
            </div>
            """, unsafe_allow_html=True)

    elif st.session_state.current_page == "how_it_works":
        st.markdown('<h2 class="sub-header">How It Works</h2>', unsafe_allow_html=True)
        st.markdown("""
            <div class="card">
                <p class="info-text">
                    Our three-step process simplifies Scope 3 emissions calculation, making complex sustainability 
                    reporting accessible and accurate for organizations of all sizes.
                </p>
            </div>
            """, unsafe_allow_html=True)
        # Steps
        st.markdown('<div class="step-container">', unsafe_allow_html=True)
        st.markdown("""
            <div class="step">
                <div class="step-number">1</div>
                <div class="step-title">Data Preparation</div>
                <p class="info-text">
                    The system starts by loading and validating your procurement data, official supplier registries, 
                    and industry emission factors. This ensures all inputs are standardized before analysis begins.
                </p>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("""
            <div class="step">
                <div class="step-number">2</div>
                <div class="step-title">Manual Code Entry</div>
                <p class="info-text">
                    When automatic matching fails, the system guides you to enter missing SIREN or NAF codes in the 
                    required format. This guarantees complete supplier coverage for accurate emissions calculation.
                </p>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("""
            <div class="step">
                <div class="step-number">3</div>
                <div class="step-title">Emissions Calculation & Reporting</div>
                <p class="info-text">
                    The system automatically computes your Scope 3 emissions using verified methodologies and 
                    generates a comprehensive report ready for disclosure or analysis.
                </p>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        # Bottom launch button
        if st.button("Launch Tool Now", key="how_to_launch_btn"):
            go_to_launch()

    elif st.session_state.current_page == "launch":
        st.markdown('<h2 class="sub-header">Launch Emissions Analysis</h2>', unsafe_allow_html=True)
        st.markdown("""
            <div class="card">
                <p class="info-text">
                    Upload the required files to begin your Scope 3 emissions analysis. The system will process your data, 
                    identify any missing information, and guide you through the completion process before generating 
                    your comprehensive emissions report.
                </p>
            </div>
            """, unsafe_allow_html=True)
        # File upload section
        st.markdown('<div class="upload-box">', unsafe_allow_html=True)
        st.markdown('<h3 class="section-header">Upload Required Files</h3>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            hl_file = st.file_uploader("HL_MATERIAUX.xlsx", type=["xlsx"], key="hl_upload")
        with col2:
            siren_file = st.file_uploader("SIREN_APE.xlsx", type=["xlsx"], key="siren_upload")
        with col3:
            naf_file = st.file_uploader("NAF Codes File", type=["xlsx"], key="naf_upload")
        st.markdown('</div>', unsafe_allow_html=True)
        # Process button
        if st.button("Process Data", key="process_btn"):
            if hl_file and siren_file and naf_file:
                with st.spinner("Processing data..."):
                    try:
                        # Read files
                        hl_df = pd.read_excel(hl_file)
                        siren_df = pd.read_excel(siren_file)
                        naf_df = pd.read_excel(naf_file)
                        # Define the name cleaning function
                        def clean_name(name):
                            if isinstance(name, str):
                                name = name.replace("(E)", "").strip().lower()
                                name = unicodedata.normalize('NFKD', name).encode('ASCII', 'ignore').decode('utf-8')
                                name = " ".join(name.split())
                                return name
                            return name
                        # Apply name cleaning
                        hl_df['Fournisseurs_Eiffage'] = hl_df['Fournisseur enfant panel'].apply(clean_name)
                        siren_df['Fournisseurs_Eiffage'] = siren_df['Fournisseur'].apply(clean_name)
                        # Merge datasets
                        merged_df = pd.merge(hl_df, siren_df[['Fournisseurs_Eiffage', 'Code SIREN', 'Code APE']],
                                           on='Fournisseurs_Eiffage', how='left')
                        # Cleaning function for codes
                        def clean_code(code):
                            if pd.isnull(code):
                                return code
                            return str(code).replace('\u00A0', '').replace('\u202F', '').replace(' ', '').strip()
                        merged_df['Code SIREN'] = merged_df['Code SIREN'].apply(clean_code)
                        merged_df['Code APE'] = merged_df['Code APE'].apply(clean_code)
                        # Check for missing codes
                        missing_suppliers = merged_df[(pd.isnull(merged_df['Code SIREN'])) | (pd.isnull(merged_df['Code APE']))]
                        if not missing_suppliers.empty:
                            st.markdown('<div class="warning-box">⚠️ Some suppliers are missing SIREN/APE codes</div>', unsafe_allow_html=True)
                            for idx, row in missing_suppliers.iterrows():
                                with st.expander(f"Missing codes for: {row['Fournisseur enfant panel']}"):
                                    col1, col2 = st.columns(2)
                                    with col1:
                                        code_siren = st.text_input(f"SIREN for {row['Fournisseur enfant panel']}", key=f"siren_{idx}")
                                    with col2:
                                        code_ape = st.text_input(f"APE for {row['Fournisseur enfant panel']}", key=f"ape_{idx}")
                                    if st.button(f"Save", key=f"save_{idx}"):
                                        merged_df.loc[idx, 'Code SIREN'] = code_siren
                                        merged_df.loc[idx, 'Code APE'] = code_ape
                                        st.success("Codes saved!")
                            # Continue processing if user has provided all missing codes
                            if st.button("Continue Processing", key="continue_btn"):
                                process_data(merged_df, naf_df)
                        else:
                            process_data(merged_df, naf_df)
                    except Exception as e:
                        st.error(f"An error occurred during processing: {str(e)}")
            else:
                st.error("Please upload all three required files to proceed.")

    # Footer
    st.markdown("""
    <div class="footer">
        <p>Eiffage Scope 3 Emissions Analysis Tool | Developed for Sustainability Reporting</p>
        <p>© 2023 Eiffage Group. All rights reserved.</p>
    </div>
    """, unsafe_allow_html=True)

def process_data(merged_df, naf_df):
    """Process the data and display results"""
    with st.spinner("Processing NAF codes and emissions data..."):
        # Build final output table
        final_columns = ['Panel parent', 'Panel enfant', 'Fournisseurs_Eiffage', 'Dépense N', 'Code SIREN', 'Code APE']
        final_df = merged_df[final_columns]
        
        # Clean NAF codes and merge with sector data
        merged_df['Code APE Clean'] = merged_df['Code APE'].str.replace('.', '', regex=False).str.strip()
        naf_df['Code NAF Clean'] = naf_df['Code NAF'].str.replace('.', '', regex=False).str.strip()
        
        merged_sector = pd.merge(
            merged_df[['Panel parent', 'Panel enfant', 'Fournisseur enfant panel', 'Code SIREN', 'Code APE', 'Code APE Clean', 'Dépense N']],
            naf_df[['Code NAF Clean', 'new best match sector', 'kg CO2-eq per EUR2024', 'm3 water eq per EUR2024']],
            left_on='Code APE Clean',
            right_on='Code NAF Clean',
            how='left'
        )
        
        # Calculate emissions
        def safe_multiply(x, y):
            try:
                return float(x) * float(y)
            except:
                return None
        
        merged_sector['GHG Emissions (kg CO2)'] = merged_sector.apply(
            lambda row: safe_multiply(row['Dépense N'], row['kg CO2-eq per EUR2024']), axis=1
        )
        
        merged_sector['Water Consumption (m³)'] = merged_sector.apply(
            lambda row: safe_multiply(row['Dépense N'], row['m3 water eq per EUR2024']), axis=1
        )
        
        # Create structured output
        structured_rows = []
        grouped = merged_sector.groupby(['Panel parent', 'Panel enfant'])
        
        for (panel_parent, panel_enfant), group in grouped:
            total_depenses = group['Dépense N'].sum(skipna=True)
            structured_rows.append({
                'Panel parent': panel_parent,
                'Panel enfant': panel_enfant,
                'Fournisseur': "",
                'DÉPENSES (€)': f"Total : {total_depenses:,.0f}".replace(",", " ").replace(".", ",") if pd.notna(total_depenses) else "",
                'Code APE': "",
                'Code SIREN': "",
                'Émissions CO2 (kg)': "",
                'Consommation eau (m³)': ""
            })
            
            for _, row in group.iterrows():
                structured_rows.append({
                    'Panel parent': panel_parent,
                    'Panel enfant': panel_enfant,
                    'Fournisseur': row['Fournisseur enfant panel'][:35],
                    'DÉPENSES (€)': f"{row['Dépense N']:,.0f}".replace(",", " ").replace(".", ",") if pd.notna(row['Dépense N']) else "",
                    'Code APE': row['Code APE'] if pd.notna(row['Code APE']) else "",
                    'Code SIREN': row['Code SIREN'] if pd.notna(row['Code SIREN']) else "",
                    'Émissions CO2 (kg)': f"{row['GHG Emissions (kg CO2)']:,.0f}".replace(",", " ").replace(".", ",") if pd.notna(row['GHG Emissions (kg CO2)']) else "",
                    'Consommation eau (m³)': f"{row['Water Consumption (m³)']:,.0f}".replace(",", " ").replace(".", ",") if pd.notna(row['Water Consumption (m³)']) else ""
                })
        
        final_structured_table = pd.DataFrame(structured_rows)
        
        # Display results
        st.markdown('<h2 class="sub-header">Analysis Results</h2>', unsafe_allow_html=True)
        
        # Summary statistics
        col1, col2, col3, col4 = st.columns(4)
        total_suppliers = len(final_structured_table[final_structured_table['Fournisseur'] != ""])
        total_spend = merged_sector['Dépense N'].sum()
        total_emissions = merged_sector['GHG Emissions (kg CO2)'].sum()
        total_water = merged_sector['Water Consumption (m³)'].sum()
        
        with col1:
            st.metric("Total Suppliers", f"{total_suppliers:,}")
        with col2:
            st.metric("Total Spend", f"€{total_spend:,.0f}")
        with col3:
            st.metric("Total CO2 Emissions", f"{total_emissions:,.0f} kg")
        with col4:
            st.metric("Total Water Consumption", f"{total_water:,.0f} m³")
        
        # Display data table
        st.dataframe(final_structured_table, use_container_width=True)
        
        # Download button
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f'HL_MATERIAUX_CODE_APE_SIREN_{timestamp}.xlsx'
        
        # Convert to Excel for download
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            final_structured_table.to_excel(writer, index=False, sheet_name='Results')
        output.seek(0)
        
        st.download_button(
            label="📥 Download Results as Excel",
            data=output,
            file_name=output_filename,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

if __name__ == "__main__":
    main()