import pandas as pd
import streamlit as st
from io import BytesIO

def generate_excel_files(file):
    try:
        # Read the uploaded Excel file
        df = pd.read_excel(file)
    except Exception as e:
        st.error(f"Error reading the Excel file: {e}")
        return None, None, None, None

    # Optional: Remove any leading/trailing spaces from column names
    df.columns = df.columns.str.strip()

    # Check if the 'MARKS' column exists
    if 'MARKS' not in df.columns:
        st.error("Error: Column 'MARKS' not found in Excel file.")
        st.write("Available columns:", df.columns.tolist())
        return None, None, None, None

    # Filtering data based on the criteria
    pass_df = df[df['MARKS'].apply(lambda x: isinstance(x, (int, float)) and x > 21)]
    fail_df = df[df['MARKS'].apply(lambda x: isinstance(x, (int, float)) and x < 22)]
    absent_df = df[df['MARKS'] == 'A']
    detained_df = df[df['MARKS'] == 'D']

    # Create BytesIO objects for each DataFrame
    pass_buffer = BytesIO()
    fail_buffer = BytesIO()
    absent_buffer = BytesIO()
    detained_buffer = BytesIO()

    # Write dataframes to these BytesIO objects
    pass_df.to_excel(pass_buffer, index=False)
    fail_df.to_excel(fail_buffer, index=False)
    absent_df.to_excel(absent_buffer, index=False)
    detained_df.to_excel(detained_buffer, index=False)

    # Seek to the start of each BytesIO object
    pass_buffer.seek(0)
    fail_buffer.seek(0)
    absent_buffer.seek(0)
    detained_buffer.seek(0)

    return pass_buffer, fail_buffer, absent_buffer, detained_buffer

def main():
    st.title("Excel File Processor")

    uploaded_file = st.file_uploader("UPLOAD YOUR FILE HERE", type=["xlsx"])

    if uploaded_file is not None:
        pass_buffer, fail_buffer, absent_buffer, detained_buffer = generate_excel_files(uploaded_file)
        
        if pass_buffer and fail_buffer and absent_buffer and detained_buffer:
            st.success("Excel files have been generated successfully!")

            # Provide download links
            st.download_button(label="Download Pass.xlsx", data=pass_buffer, file_name='pass.xlsx')
            st.download_button(label="Download Fail.xlsx", data=fail_buffer, file_name='fail.xlsx')
            st.download_button(label="Download Absent.xlsx", data=absent_buffer, file_name='absent.xlsx')
            st.download_button(label="Download Detained.xlsx", data=detained_buffer, file_name='detained.xlsx')

if __name__ == "__main__":
    main()
