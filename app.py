import streamlit as st
import pandas as pd
import os
import re
from datetime import datetime
from io import BytesIO
import zipfile

# Streamlit page config must be first
st.set_page_config(
    page_title="Suggested Orders Files Converter",
    page_icon="📊",
    layout="wide"
)

# Page configuration
st.set_page_config(
    page_title="Suggested Orders Files Converter",
    page_icon="📊",
    layout="wide"
)

# Custom CSS to match Django app design
st.markdown("""
    <style>
    /* Import fonts */
    @import url('https://fonts.googleapis.com/css2?family=Segoe+UI:wght@400;600;700&display=swap');
    
    /* Global Styles */
    .stApp {
        background: linear-gradient(135deg, #e4d9f5 0%, #f0e8ff 50%, #e8f4f8 100%);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Remove default padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    .sub-header {
        font-size: 1.3rem;
        color: #6c757d;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    
    /* LabelFrame styling - only for the step sections */
    div[data-testid="stExpander"], .stTabs {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 8px 25px rgba(74, 0, 112, 0.08);
        border: 1px solid rgba(74, 0, 112, 0.05);
        margin-bottom: 20px;
    }
    
    /* Success Box */
    .success-box {
        padding: 1.2rem;
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        border-left: 5px solid #28a745;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(40, 167, 69, 0.2);
    }
    
    /* Info Box */
    .info-box {
        padding: 1.2rem;
        background: linear-gradient(135deg, #e4d9f5 0%, #d1ecf1 100%);
        border-left: 5px solid #4a0070;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(74, 0, 112, 0.2);
    }
    
    /* Warning Box */
    .warning-box {
        padding: 1.2rem;
        background: linear-gradient(135deg, #fff3cd 0%, #ffe69c 100%);
        border-left: 5px solid #ffc107;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(255, 193, 7, 0.2);
    }
    
    /* Buttons */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #4a0070, #2c5282) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 16px 32px !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        letter-spacing: 0.5px !important;
        box-shadow: 0 8px 25px rgba(74, 0, 112, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #370052, #1a365d) !important;
        transform: translateY(-2px);
        box-shadow: 0 12px 35px rgba(74, 0, 112, 0.4) !important;
    }
    
    .stButton>button[kind="primary"] {
        background: linear-gradient(135deg, #4a0070, #2c5282) !important;
    }
    
    /* Download Buttons */
    .stDownloadButton>button {
        background: linear-gradient(135deg, #28a745, #20c997) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        box-shadow: 0 6px 20px rgba(40, 167, 69, 0.3) !important;
    }
    
    .stDownloadButton>button:hover {
        background: linear-gradient(135deg, #218838, #17a2b8) !important;
        transform: translateY(-2px);
        box-shadow: 0 10px 30px rgba(40, 167, 69, 0.4) !important;
    }
    
    /* File Uploader */
    .stFileUploader {
        background: white;
        border-radius: 15px;
        padding: 20px;
        border: 2px dashed #4a0070;
        box-shadow: 0 4px 15px rgba(74, 0, 112, 0.1);
    }
    
    /* Progress Bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(135deg, #4a0070, #2c5282) !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: white;
        padding: 10px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(74, 0, 112, 0.08);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 10px;
        padding: 12px 24px;
        font-weight: 600;
        color: #4a0070;
        border: 2px solid transparent;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #4a0070, #2c5282) !important;
        color: white !important;
        border-color: transparent;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 10px;
        font-weight: 600;
        color: #3d005e;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: #3d005e;
    }
    
    /* Dataframe */
    .stDataFrame {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 8px 25px rgba(74, 0, 112, 0.1);
    }
    
    /* Divider */
    hr {
        margin: 2rem 0;
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #4a0070, transparent);
    }
    
    /* Selectbox */
    .stSelectbox {
        background: white;
        border-radius: 10px;
    }
    
    /* Text Input */
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #e9ecef;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #4a0070;
        box-shadow: 0 0 0 0.2rem rgba(74, 0, 112, 0.25);
    }
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: #4a0070 !important;
    }
    
    /* Section Headers */
    h1, h2, h3 {
        color: #3d005e;
        font-weight: 700;
    }
    
    h2 {
        font-size: 1.5rem;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
    
    h3 {
        font-size: 1.2rem;
        margin-top: 0.8rem;
        margin-bottom: 0.8rem;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Remove extra spacing */
    .element-container {
        margin-bottom: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'processed_files' not in st.session_state:
    st.session_state.processed_files = None
if 'codes_mapping' not in st.session_state:
    st.session_state.codes_mapping = {}

def product_flag(x):
    """Convert Product Flag to Material Type"""
    if x == 'Regular':
        return "01"
    elif x == "Suggested":
        return "02"
    return x

def detect_period(filename):
    """Detect period from filename"""
    match = re.search(r'(\d{6})_(\d{2})', filename)
    if match:
        year_month = match.group(1)
        year = year_month[:4]
        month = year_month[4:6]
        return f"{month}/{year}"
    return None

def load_mapping_file(file):
    """Load codes mapping from Excel/CSV file"""
    try:
        if file.name.endswith('.csv'):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)
        
        # Look for columns that might contain the mapping
        possible_old = ['Old_Code', 'old_code', 'Old Code', 'OldCode', 'Source', 'From']
        possible_new = ['New_Code', 'new_code', 'New Code', 'NewCode', 'Target', 'To']
        
        old_col = None
        new_col = None
        
        for col in df.columns:
            if col in possible_old:
                old_col = col
            if col in possible_new:
                new_col = col
        
        if old_col and new_col:
            mapping = dict(zip(
                df[old_col].astype(str).str.strip(),
                df[new_col].astype(str).str.strip()
            ))
            return mapping, len(mapping), None
        else:
            return {}, 0, "Could not find Old_Code/New_Code columns in the file"
    except Exception as e:
        return {}, 0, f"Error loading file: {str(e)}"

def process_csv_file(csv_file, codes_mapping):
    """Process a single CSV file"""
    try:
        # Read CSV
        df = pd.read_csv(csv_file)
        original_count = len(df)
        
        # Process Link Code
        if 'Link Code' in df.columns:
            df['Link Code'] = df['Link Code'].astype(str).str.strip()
            
            # Apply mapping if available
            if codes_mapping:
                df['Link Code'] = df['Link Code'].replace(codes_mapping)
        
        # Apply transformations
        df["Unit Sales"] = df["Unit Sales"].astype(str)
        df["Monthno"] = df["Monthno"].astype(str)
        
        # Product Flag conversion
        df["Material Type"] = df["Product Flag"].apply(product_flag)
        
        # Format Quantity
        df["Quantity"] = "0" + df["Unit Sales"]
        
        # Rename columns
        df.rename(columns={
            "Store code": "Customer",
            "Link Code": "Material",
            "yearno": "year",
            "Monthno": "Month"
        }, inplace=True)
        
        # Drop NaN Materials
        df.dropna(subset=["Material"], inplace=True)
        
        # Drop unnecessary columns
        columns_to_drop = ["Additional Info", "Priority", "Product Flag", "Unit Sales"]
        df.drop([col for col in columns_to_drop if col in df.columns], axis=1, inplace=True, errors='ignore')
        
        # Select final columns
        final_columns = ["Month", "year", "Customer", "Material", "Material Type", "Quantity"]
        df = df[[col for col in final_columns if col in df.columns]]
        
        final_count = len(df)
        
        return df, original_count, final_count, None
    except Exception as e:
        return None, 0, 0, str(e)

def create_excel_file(df):
    """Convert DataFrame to Excel file in memory"""
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    output.seek(0)
    return output

def create_zip_file(processed_files):
    """Create a ZIP file containing all Excel files"""
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for file_info in processed_files:
            excel_data = create_excel_file(file_info['dataframe'])
            excel_bytes = excel_data.getvalue()
            zip_file.writestr(file_info['excel_name'], excel_bytes)
    zip_buffer.seek(0)
    return zip_buffer.getvalue()

# Main UI
# Header with logo
st.markdown("""
    <div style="
        display: flex;
        align-items: center;
        background: linear-gradient(135deg, #390856 0%, #4a0070 50%, #2c5282 100%);
        padding: 25px 40px;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(74, 0, 112, 0.3);
        margin-bottom: 30px;
    ">
        <img src="https://toppng.com/uploads/preview/mondelez-international-logo-11530963807eftwuglptg.png" style="
            width: 90px;
            height: auto;
            margin-right: 25px;
            filter: drop-shadow(0 3px 6px rgba(255,255,255,0.1));
        ">
        <h1 style="
            font-size: 2.2rem;
            font-weight: 700;
            color: white;
            text-shadow: 0 3px 6px rgba(0,0,0,0.1);
            margin: 0;
        ">Suggested Orders Files Converter</h1>
    </div>
""", unsafe_allow_html=True)

st.markdown('<div class="sub-header">Process your suggested orders files with ease</div>', unsafe_allow_html=True)

# Create tabs for better organization
tab1, tab2, tab3 = st.tabs(["🔄 Process Files", "📖 Instructions", "ℹ️ About"])

with tab1:
    # Step 1: Mapping File (Optional)
    st.subheader("Step 1: Upload Codes Mapping File (Optional)")
    st.markdown('<div class="info-box">📝 Upload an Excel/CSV file with columns: <strong>Old_Code</strong> and <strong>New_Code</strong></div>', unsafe_allow_html=True)
    
    mapping_file = st.file_uploader(
        "Select mapping file",
        type=['csv', 'xlsx', 'xls'],
        key="mapping_uploader",
        help="This is optional. If not provided, no code mapping will be applied."
    )
    
    if mapping_file:
        mapping, count, error = load_mapping_file(mapping_file)
        if error:
            st.markdown(f'<div class="warning-box">⚠️ {error}</div>', unsafe_allow_html=True)
            st.session_state.codes_mapping = {}
        else:
            st.session_state.codes_mapping = mapping
            st.markdown(f'<div class="success-box">✅ Successfully loaded {count} code mappings</div>', unsafe_allow_html=True)
    
    st.divider()
    
    # Step 2: Upload CSV Files
    st.subheader("Step 2: Upload CSV Files")
    st.markdown('<div class="info-box">📁 Select all CSV files you want to process (you can select multiple files)</div>', unsafe_allow_html=True)
    
    uploaded_files = st.file_uploader(
        "Choose CSV files",
        type=['csv'],
        accept_multiple_files=True,
        key="csv_uploader"
    )
    
    if uploaded_files:
        st.markdown(f'<div class="success-box">✅ {len(uploaded_files)} files uploaded</div>', unsafe_allow_html=True)
        
        # Detect period from first file
        first_file_name = uploaded_files[0].name
        detected_period = detect_period(first_file_name)
        
        if detected_period:
            st.markdown(f'<div class="info-box"><strong>🗓️ Detected Period:</strong> {detected_period}</div>', 
                       unsafe_allow_html=True)
        
        # Show uploaded files
        with st.expander("📋 View uploaded files"):
            for i, file in enumerate(uploaded_files, 1):
                st.text(f"{i}. {file.name}")
        
        st.divider()
        
        # Step 3: Process Files
        st.subheader("Step 3: Process Files")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚀 Process All Files", type="primary", use_container_width=True):
                with st.spinner("Processing files... Please wait"):
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    processed_files = []
                    total_original = 0
                    total_final = 0
                    errors = []
                    
                    for idx, csv_file in enumerate(uploaded_files):
                        status_text.text(f"Processing: {csv_file.name}")
                        
                        df, original_count, final_count, error = process_csv_file(
                            csv_file, 
                            st.session_state.codes_mapping
                        )
                        
                        if error:
                            errors.append({
                                'file': csv_file.name,
                                'error': error
                            })
                        else:
                            excel_name = csv_file.name.replace('.csv', '.xlsx')
                            processed_files.append({
                                'csv_name': csv_file.name,
                                'excel_name': excel_name,
                                'original_count': original_count,
                                'final_count': final_count,
                                'dataframe': df
                            })
                            total_original += original_count
                            total_final += final_count
                        
                        progress_bar.progress((idx + 1) / len(uploaded_files))
                    
                    status_text.empty()
                    progress_bar.empty()
                    
                    # Store results in session state
                    st.session_state.processed_files = {
                        'files': processed_files,
                        'total_original': total_original,
                        'total_final': total_final,
                        'errors': errors,
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
        
        # Display Results
        if st.session_state.processed_files:
            results = st.session_state.processed_files
            
            st.divider()
            st.subheader("✅ Processing Complete!")
            
            # Summary metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Files Processed", len(results['files']))
            with col2:
                st.metric("Original Records", f"{results['total_original']:,}")
            with col3:
                st.metric("Final Records", f"{results['total_final']:,}")
            with col4:
                records_dropped = results['total_original'] - results['total_final']
                st.metric("Records Dropped", f"{records_dropped:,}")
            
            st.markdown(f"**Processed at:** {results['timestamp']}")
            
            # File details
            st.subheader("📄 File Details")
            
            file_data = []
            for file_info in results['files']:
                file_data.append({
                    'Excel File': file_info['excel_name'],
                    'Original Records': file_info['original_count'],
                    'Final Records': file_info['final_count'],
                    'Dropped': file_info['original_count'] - file_info['final_count']
                })
            
            st.dataframe(pd.DataFrame(file_data), use_container_width=True)
            
            # Errors (if any)
            if results['errors']:
                st.error("⚠️ Some files encountered errors:")
                for error in results['errors']:
                    st.text(f"❌ {error['file']}: {error['error']}")
            
            st.divider()
            
            # Download Section
            st.subheader("💾 Download Processed Files")
            
            # Option 1: Download All Files as ZIP
            st.markdown("### Option 1: Download All Files (ZIP)")
            
            try:
                zip_data = create_zip_file(results['files'])
                
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.download_button(
                        label="📦 Download All Files as ZIP",
                        data=zip_data,
                        file_name=f"processed_files_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip",
                        mime="application/zip",
                        use_container_width=True,
                        type="primary",
                        key="download_zip"
                    )
                with col2:
                    st.metric("Total Size", f"{len(zip_data) / 1024:.1f} KB")
                
                st.caption("💡 Click the button above to download all files in one ZIP archive")
            except Exception as e:
                st.error(f"Error creating ZIP file: {str(e)}")
                st.info("Please download files individually below")
            
            st.markdown("---")
            
            # Option 2: Download Individual Files
            st.markdown("### Option 2: Download Individual Files")
            st.caption("Click the download button next to each file")
            
            for idx, file_info in enumerate(results['files']):
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.text(f"📄 {file_info['excel_name']}")
                with col2:
                    st.text(f"{file_info['final_count']} records")
                with col3:
                    excel_data = create_excel_file(file_info['dataframe'])
                    st.download_button(
                        label="⬇️",
                        data=excel_data,
                        file_name=file_info['excel_name'],
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        key=f"download_{idx}",
                        use_container_width=True
                    )

with tab2:
    st.subheader("📖 How to Use This Tool")
    
    st.markdown("""
    ### Step-by-Step Instructions:
    
    #### 1️⃣ **Upload Codes Mapping File (Optional)**
    - Prepare an Excel or CSV file with two columns: `Old_Code` and `New_Code`
    - This file maps old product codes to new ones
    - If you don't have a mapping file, skip this step
    
    #### 2️⃣ **Upload CSV Files**
    - Click on "Browse files" or drag and drop your CSV files
    - You can select multiple files at once
    - The tool will automatically detect the period from filenames
    - Supported filename format: `Suggestedorders_YYYYMM_DD.csv`
    
    #### 3️⃣ **Process Files**
    - Review the detected period and file list
    - Click "Process All Files" to start conversion
    - Wait for the processing to complete (usually takes a few seconds)
    
    #### 4️⃣ **Download Results**
    - **Option A:** Download all files as a ZIP archive
    - **Option B:** Download individual Excel files one by one
    - Review the summary to ensure all records were processed correctly
    
    ### ⚙️ What This Tool Does:
    
    - ✅ Converts CSV files to Excel format (.xlsx)
    - ✅ Applies code mapping (if provided)
    - ✅ Transforms columns and data formats
    - ✅ Removes invalid records (empty Material codes)
    - ✅ Provides detailed processing summary
    - ✅ Tracks record counts (original vs. final)
    
    ### 🔒 Data Security:
    
    - All processing happens in your browser session
    - Files are not stored on any server
    - Data is automatically cleared when you close the browser
    """)

with tab3:
    st.subheader("ℹ️ About This Tool")
    
    st.markdown("""
    ### Suggested Orders Files Converter
    
    **Version:** 1.0.0  
    **Last Updated:** December 2024
    
    This tool helps you convert suggested orders CSV files to Excel format with automatic data transformation and validation.
    
    ### Features:
    - 📊 Batch processing of multiple CSV files
    - 🔄 Optional code mapping support
    - 📈 Real-time processing progress
    - 📉 Detailed record tracking
    - 💾 Multiple download options (ZIP or individual)
    - 🎯 Automatic period detection
    
    ### Technical Details:
    - Built with Streamlit and Pandas
    - Uses openpyxl for Excel file generation
    - Processes files in-memory for security
    - No data storage or logging
    
    ### Support:
    If you encounter any issues or have questions, please contact your IT administrator.
    
    ---
    
    **Developed for internal use**
    """)

# Footer
st.divider()
st.markdown("""
    <div style="
        text-align: center;
        padding: 30px 20px;
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 15px;
        margin-top: 40px;
    ">
        <p style="color: #6c757d; font-size: 0.9rem; margin: 0;">
            Suggested Orders Files Converter | Process your files securely and efficiently
        </p>
    </div>
""", unsafe_allow_html=True)
