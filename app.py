# Import libraries
import streamlit as st
import pandas as pd
import datetime
import os
import xlsxwriter

# Set up page configuration
st.set_page_config(page_title="SIM SWAP Report App", page_icon="📱")

# Create a rolling text animation using CSS
st.markdown(
    """
    <style>
    @keyframes rolling {
        0% { transform: translateX(100%); }
        100% { transform: translateX(-100%); }
    }

    .rolling-title {
        overflow: hidden;
        white-space: nowrap;
        display: inline-block;
        animation: rolling 15s linear infinite;
        font-size: 32px;
        font-weight: bold;
        color: #4A8D3E;
    }

    .title-container {
        overflow: hidden;
        width: 100%;
    }
    </style>

    <div class="title-container">
        <div class="rolling-title">Pending SIM SWAP Report App 📱</div>
    </div>
    """,
    unsafe_allow_html=True
)

# Sidebar
st.sidebar.write("**App Information**")
st.sidebar.write(
    """
    This app allows you to upload **`Pending SIM Swap Report`** file for processing. 
    Once you've uploaded your file, the app will analyze and combine the results into an Excel Spreadsheet.
    """
)

st.sidebar.write("#### Usage Guide")
st.sidebar.write(
    """
    1. Click the **Browse files** button on the main page to upload a `csv` file or drag and drop.
    2. The app will process the file, download to your local computer and display the results. 
    3. You can preview results by selecting the tabs.
    """
)

st.sidebar.write("#### Developer: [Yusuf Okunlola](https://www.linkedin.com/in/yusufokunlola/)")
st.sidebar.write("#### `v0.1, Dec 2024`")

uploaded_file = st.file_uploader("**Upload CSV File**", type=["csv"])

if uploaded_file:
    # Load the uploaded file into a DataFrame
    df = pd.read_csv(uploaded_file)

    # Ensure MSISDN is treated as a string
    if 'msisdn' in df.columns:
        df['msisdn'] = df['msisdn'].astype(str)

    # Process "checked" data
    col1, col2 = 'swap_status', 'check_status'
    checked_data = df[(df[col1] == 'PENDING') & (df[col2] == 'CHECKED')]

    # Process "pending" data
    col3, col4 = 'child_swap_type', 'dealer'
    pending = df[(df[col1] == 'PENDING') & (df[col2] == 'PENDING')]
    pending_data = pending[
        ~pending[col3].str.contains('BULK', na=False) &
        ~pending[col4].str.contains('IS TEST', na=False)
    ]

    # Generate "summary" data
    dealer_counts = pending_data.groupby('dealer').size().reset_index(name='count')
    summary = dealer_counts.copy()
    summary.reset_index(drop=True, inplace=True)
    summary.index += 1  # Start S/N from 1
    summary.insert(0, "S/N", summary.index)  # Add S/N as the first column

    summary.rename(columns={"dealer": "SHOP", "count": "COUNT OF PENDING SWAPS"}, inplace=True)
    grand_total = pd.DataFrame({
        "S/N": [pd.NA],  # Set S/N for GRAND TOTAL to NA
        "SHOP": ['GRAND TOTAL'],
        "COUNT OF PENDING SWAPS": [summary["COUNT OF PENDING SWAPS"].sum()]
    })
    summary = pd.concat([summary, grand_total], ignore_index=True)

    # Ensure S/N column is numeric for all rows except the GRAND TOTAL
    summary["S/N"] = pd.to_numeric(summary["S/N"], errors='coerce')

    # Set today's date and timezone to GMT+1
    gmt_plus_one = datetime.timezone(datetime.timedelta(hours=1))
    today_date = datetime.datetime.now(gmt_plus_one).strftime('%Y-%m-%d_%H-%M-%S')

    # Save results to Excel Spreadsheet in the user's Downloads directory
    downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
    output_file = os.path.join(downloads_folder, f"{today_date}_Pending_SIM_Swaps.xlsx")
    with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
        pending_data.to_excel(writer, sheet_name="pending", index=False)
        checked_data.to_excel(writer, sheet_name="checked", index=False)
        summary.to_excel(writer, sheet_name="summary", index=False)

    st.success(f"Data processed successfully! The file has been saved to your Downloads folder: {output_file}")

    st.write("#### Processed Data Overview")
    # Create tabs for data preview
    tab1, tab2, tab3, tab4 = st.tabs(["Uploaded Data", "Pending Data", "Checked Data", "Summary Data"])
    with tab1:
        st.write("**Uploaded Data**")
        st.dataframe(df)

    with tab2:
        st.write("**Pending Data**")
        st.dataframe(pending_data)

    with tab3:
        st.write("**Checked Data**")
        st.dataframe(checked_data)

    with tab4:
        st.write("**Summary Data**")
        st.dataframe(summary)
else:
    st.warning("Please upload a CSV file.")