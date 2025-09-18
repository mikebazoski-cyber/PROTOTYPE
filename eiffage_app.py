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
        --primary-red: #E63946;
        --light-white: #F1FAEE;
        --dark-black: #1D3557;
        --light-blue: #A8DADC;
        --medium-blue: #457B9D;
    }
    
    .main-header {
        font-size: 3rem;
        color: var(--primary-red);
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
        text-shadow: 1px 1px 2px var(--dark-black);
    }
    
    .sub-header {
        font-size: 2rem;
        color: var(--dark-black);
        margin-top: 2rem;
        margin-bottom: 1.5rem;
        font-weight: bold;
        border-bottom: 2px solid var(--primary-red);
        padding-bottom: 0.5rem;
    }
    
    .section-header {
        font-size: 1.8rem;
        color: var(--dark-black);
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    
    .info-text {
        font-size: 1.1rem;
        color: var(--dark-black);
        line-height: 1.6;
        margin-bottom: 1rem;
    }
    
    .card {
        background-color: var(--light-white);
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 5px solid var(--primary-red);
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .success-box {
        background-color: #D1FAE5;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #10B981;
        margin: 1rem 0;
    }
    
    .warning-box {
        background-color: #FEF3C7;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #F59E0B;
        margin: 1rem 0;
    }
    
    .info-box {
        background-color: #DBEAFE;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid var(--medium-blue);
        margin: 1rem 0;
    }
    
    .stButton>button {
        background-color: var(--primary-red);
        color: white;
        border: none;
        padding: 0.8rem 2rem;
        border-radius: 0.5rem;
        font-weight: bold;
        font-size: 1.1rem;
        margin: 0.5rem 0;
        width: 100%;
    }
    
    .stButton>button:hover {
        background-color: var(--dark-black);
        color: white;
    }
    
    .top-buttons {
        display: flex;
        justify-content: flex-end;
        margin-bottom: 2rem;
    }
    
    .top-buttons button {
        background-color: var(--dark-black);
        color: white;
        border: none;
        padding: 0.5rem 1.5rem;
        border-radius: 0.3rem;
        margin-left: 0.5rem;
        font-weight: bold;
    }
    
    .top-buttons button:hover {
        background-color: var(--primary-red);
        cursor: pointer;
    }
    
    .hero-section {
        background: linear-gradient(135deg, var(--dark-black) 0%, var(--medium-blue) 100%);
        padding: 4rem 2rem;
        border-radius: 1rem;
        text-align: center;
        margin-bottom: 3rem;
        color: white;
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: bold;
        margin-bottom: 1.5rem;
        color: white;
    }
    
    .hero-subtitle {
        font-size: 1.5rem;
        margin-bottom: 2rem;
        color: var(--light-white);
    }
    
    .step-container {
        display: flex;
        justify-content: space-between;
        margin: 2rem 0;
    }
    
    .step {
        flex: 1;
        padding: 1.5rem;
        margin: 0 1rem;
        background-color: var(--light-white);
        border-radius: 0.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        text-align: center;
    }
    
    .step-number {
        font-size: 2.5rem;
        font-weight: bold;
        color: var(--primary-red);
        margin-bottom: 1rem;
    }
    
    .step-title {
        font-size: 1.5rem;
        color: var(--dark-black);
        margin-bottom: 1rem;
        font-weight: bold;
    }
    
    .upload-box {
        background-color: var(--light-white);
        padding: 2rem;
        border-radius: 0.5rem;
        border: 2px dashed var(--primary-red);
        margin: 1rem 0;
        text-align: center;
    }
    
    .footer {
        text-align: center;
        margin-top: 3rem;
        padding: 1.5rem;
        background-color: var(--dark-black);
        color: white;
        border-radius: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Navigation functions
def go_to_home():
    st.session_state.current_page = "home"

def go_to_how_it_works():
    st.session_state.current_page = "how_it_works"

def go_to_launch():
    st.session_state.current_page = "launch"

# Initialize session state for navigation
if "current_page" not in st.session_state:
    st.session_state.current_page = "home"

def main():
    # Top navigation buttons
    col1, col2, col3, col4 = st.columns([5,1,1,1])
    
    with col2:
        if st.button("Home", key="home_btn"):
            go_to_home()
    with col3:
        if st.button("How it Works", key="how_it_works_btn"):
            go_to_how_it_works()
    with col4:
        if st.button("Launch", key="launch_btn"):
            go_to_launch()
    
    # Home section
    if st.session_state.current_page == "home":
        st.markdown('<div class="hero-section">', unsafe_allow_html=True)
        st.markdown('<h1 class="hero-title">Scope 3 Emissions:</h1>', unsafe_allow_html=True)
        st.markdown('<h2 class="hero-subtitle">The Missing Piece in Your Sustainability Strategy</h2>', unsafe_allow_html=True)
        
        if st.button("Launch Analysis Tool", key="hero_launch_btn"):
            go_to_launch()
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Brief introduction
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
    
    # How it works section
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
    
    # Launch section
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