import streamlit as st
import pandas as pd

# Streamlit app
st.title("File Upload and Data Processing App")

# File upload
uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

if uploaded_file:
    # Load the uploaded file into a DataFrame
    df = pd.read_csv(uploaded_file)
    
    # Process "pending" data for the summary
    col1, col2, col3, col4 = 'swap_status', 'check_status', 'child_swap_type', 'dealer'
    pending = df[(df[col1] == 'PENDING') & (df[col2] == 'PENDING')]
    pending_data = pending[
        ~pending[col3].str.contains('BULK', na=False) &
        ~pending[col4].str.contains('IS TEST', na=False)
    ]

    # Generate "summary" data
    dealer_counts = pending_data.groupby('dealer').size().reset_index(name='count')
    total_row = pd.DataFrame({'dealer': ['Grand Total'], 'count': [dealer_counts['count'].sum()]})
    summary = pd.concat([dealer_counts, total_row], ignore_index=True).reset_index()
    summary.rename(columns={"index": "S/N", "dealer": "SHOP", "count": "COUNT OF PENDING SWAPS"}, inplace=True)
    
    # Display the summary on the screen
    st.write("Summary of Pending Swaps:")
    st.dataframe(summary)

    # Save results to Excel
    output_file = "processed_results.xlsx"
    with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
        summary.to_excel(writer, sheet_name="summary", index=False)

    st.success(f"Summary processed successfully! File saved as '{output_file}'.")

    # Provide download link for the Excel file
    with open(output_file, "rb") as file:
        st.download_button(
            label="Download Summary Excel File",
            data=file,
            file_name=output_file,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
