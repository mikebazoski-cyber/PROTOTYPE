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
import base64

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
        --dark-black: #010B13;
    }

    html, body { overflow-x: hidden !important; }  /* prevent horizontal scroll from 100vw */
    /* Black top bar (used above) */
    .black-top-bar {
        background-color: #010B13;
        height: 8px;
        width: 100%;
        position: fixed;
        top: 0;
        left: 0;
        z-index: 1001;
    }

    /* Red top bar */
    .red-top-bar {
        background-color: var(--primary-red);
        height: 60px;
        width: 100%;
        position: fixed;
        top: 0;
        left: 0;
        z-index: 1000;
    }

    /* White content area (actually red) */
    .white-content {
        background-color: #FF0000;
        min-height: 40px;
        padding-top: 40px;
    }

    /* Hero section with image and buttons */
    .hero-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.34rem 2rem;
        min-height: 40px;
        max-width: 700px;
        margin-left: auto;
        margin-right: auto;
    }
    .card {
        max-width: 700px;
        margin-left: auto;
        margin-right: auto;
    }

    .hero-image {
        flex: 1;
        padding-right: 3rem;
    }

    /* Target only the hero image rendered by st.image */
    .hero-image .stImage img {
        width: auto !important;
        height: 50px !important;  /* was 80px */
        border-radius: 10px;
        box-shadow: 0 8px 16px rgba(1,11,19,0.1);
        object-fit: cover;
        display: block;
        margin: 0;                /* keep left-aligned */
    }
            

    /* Force all nav buttons in the hero section to black with white text */
    .white-content .stButton > button, .white-content button[data-testid="baseButton"] {
        background-color: #010B13 !important;
        color: #fff !important;
        border: none !important;
        border-radius: 5px !important;
        font-weight: bold !important;
        font-size: 1.35rem !important;
        padding: 0.5rem 1.2rem !important;
        box-shadow: 0 2px 6px rgba(1,11,19,0.08) !important;
        text-align: center !important;
        outline: none !important;
        cursor: pointer !important;
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
        padding: 0.25rem;
        margin-top: 3rem;
        height: 5rem;
        font-size: 1rem;
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
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Add black top bar
    st.markdown('<div class="black-top-bar"></div>', unsafe_allow_html=True)
    # Add red top bar
    st.markdown('<div class="red-top-bar"></div>', unsafe_allow_html=True)

    # --- HERO SECTION (red box, image and buttons in one row) ---
    st.markdown('<div class="white-content">', unsafe_allow_html=True)
    
    # Add padding above the buttons with a spacer
    st.markdown('<div style="height: 8px;"></div>', unsafe_allow_html=True)
    
    # Create a container for the row with logo and buttons
    row1 = st.container()
    
    # Use columns with carefully chosen ratios to place buttons right of logo
    with row1:
        logo_col, btn1_col, btn2_col, btn3_col = st.columns([1.5, 1, 1.2, 1])
        
        # Logo in first column
        with logo_col:
            try:
                with open("eiffage pic for site .png", "rb") as f:
                    logo_b64 = base64.b64encode(f.read()).decode()
                st.markdown(f'<img src="data:image/png;base64,{logo_b64}" style="height: 50px; width: auto; border-radius: 10px;" alt="Eiffage Logo">', unsafe_allow_html=True)
            except Exception as e:
                st.warning(f"Could not load logo: {e}")
                st.markdown('<img src="https://via.placeholder.com/200x50/010B13/FFFFFF?text=Eiffage+Logo" style="height: 50px; width: auto;" alt="Eiffage Logo">', unsafe_allow_html=True)
        
        # Navigation buttons in next columns with top padding via CSS
        with btn1_col:
            st.markdown('<div style="padding-top: 4px;">', unsafe_allow_html=True)
            if st.button("Home", key="nav_home", help="Go to Home", use_container_width=True):
                st.session_state.current_page = "home"
            st.markdown('</div>', unsafe_allow_html=True)
                
        with btn2_col:
            st.markdown('<div style="padding-top: 4px;">', unsafe_allow_html=True)
            if st.button("How it Works", key="nav_how", help="How it Works", use_container_width=True):
                st.session_state.current_page = "how_it_works"
            st.markdown('</div>', unsafe_allow_html=True)
                
        with btn3_col:
            st.markdown('<div style="padding-top: 4px;">', unsafe_allow_html=True)
            if st.button("Launch", key="nav_launch", help="Launch Tool", use_container_width=True):
                st.session_state.current_page = "launch"
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Close the white-content container
    st.markdown('</div>', unsafe_allow_html=True)

    # --- PAGE CONTENT ---
    st.markdown('<div class="content-section">', unsafe_allow_html=True)
    if "current_page" not in st.session_state:
        st.session_state.current_page = "home"
    if st.session_state.current_page == "home":
        st.markdown("""
            <div class="card" style="text-align: center;">
                <h3 style='font-size: 3em;'>Eiffage, a leading player in a low-carbon Europe</h3>
                <p class="info-text">
                    Your comprehensive solution for Scope 3 emissions calculation and reporting
                </p>
                <p class="info-text">
                    Understanding and managing Scope 3 emissions is crucial for developing effective sustainability strategies, 
                    meeting regulatory requirements, and demonstrating environmental responsibility to stakeholders.
                </p>
            </div>
            """, unsafe_allow_html=True)
    elif st.session_state.current_page == "how_it_works":
        # Removed background image. Plain centered content.
        st.markdown('<h2 class="sub-header" style="text-align: center;">How It Works</h2>', unsafe_allow_html=True)
        st.markdown("""
            <div class="card" style="text-align: center;">
                <p class="info-text">
                    Our three-step process simplifies Scope 3 emissions calculation, making complex sustainability 
                    reporting accessible and accurate for organizations of all sizes.
                </p>
            </div>
            <div class="step" style="text-align: center;">
                <div class="step-number">1</div>
                <div class="step-title">Upload Data</div>
                <p class="info-text">Upload your procurement and supplier data files to begin the analysis.</p>
            </div>
            <div class="step" style="text-align: center;">
                <div class="step-number">2</div>
                <div class="step-title">Manual Code Entry</div>
                <p class="info-text">When automatic matching fails, the system guides you to enter missing SIREN or NAF codes in the required format. 
                    
                    This guarantees complete supplier coverage for accurate emissions calculation.</p>
            </div>
            <div class="step" style="text-align: center;">
                <div class="step-number">3</div>
                <div class="step-title">Emissions Calculation & Reporting</div>
                <p class="info-text">The system automatically computes your Scope 3 emissions using verified methodologies and generates a comprehensive report ready for disclosure or analysis.</p>
            </div>
            """, unsafe_allow_html=True)
    elif st.session_state.current_page == "launch":
        st.markdown('<h2 class="sub-header" style="text-align: center;">Launch Emissions Analysis</h2>', unsafe_allow_html=True)
        st.markdown("""
            <div class="card" style="text-align: center;">
                <p class="info-text">
                    Upload the required files to begin your Scope 3 emissions analysis. 
                </p>  
                <p class="info-text">
                    The system will process your data and generate your comprehensive emissions report.
                </p>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('<div class="upload-box" style="text-align: center;">', unsafe_allow_html=True)
        st.markdown('<h3 class="section-header">Upload Required Files</h3>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            hl_file = st.file_uploader("HL_MATERIAUX.xlsx", type=["xlsx"], key="hl_upload")
        with col2:
            siren_file = st.file_uploader("SIREN_APE.xlsx", type=["xlsx"], key="siren_upload")
        with col3:
            naf_file = st.file_uploader("NAF Codes File", type=["xlsx"], key="naf_upload")
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
                            if st.button("Continue Processing", key="continue_btn"):
                                process_data(merged_df, naf_df)
                        else:
                            process_data(merged_df, naf_df)
                    except Exception as e:
                        st.error(f"An error occurred during processing: {str(e)}")
            else:
                st.error("Please upload all three required files to proceed.")
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