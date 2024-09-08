import streamlit as st
import pandas as pd
from io import BytesIO

# Function to process the uploaded Excel file
def process_excel_file(file):
    # Load the Excel file
    df = pd.read_excel(file)
    
    # Define column names (adjust if necessary)
    marks_column = 'MARKS'
    
    # Ensure the column exists
    if marks_column not in df.columns:
        st.error(f"Column '{marks_column}' not found in the Excel file.")
        return None, None, None, None
    
    # Categorize data
    pass_df = df[df[marks_column].apply(lambda x: isinstance(x, (int, float)) and x > 21)]
    fail_df = df[df[marks_column].apply(lambda x: isinstance(x, (int, float)) and x < 22)]
    absent_df = df[df[marks_column].astype(str).str.upper() == 'A']
    detained_df = df[df[marks_column].astype(str).str.upper() == 'D']
    
    return pass_df, fail_df, absent_df, detained_df

# Streamlit UI
def main():
    st.title("Student Data Processing App")
    
    uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx")
    
    if uploaded_file is not None:
        st.write("Processing file...")
        
        # Process the uploaded Excel file
        pass_df, fail_df, absent_df, detained_df = process_excel_file(uploaded_file)
        
        if pass_df is None:
            st.write("Error processing the file. Please check the column names and file format.")
        else:
            # Create downloadable Excel files
            def create_excel_buffer(df, sheet_name):
                output = BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
                output.seek(0)
                return output
            
            if not pass_df.empty:
                pass_buffer = create_excel_buffer(pass_df, "Passed Students")
                st.download_button(
                    label="Download Passed Students Excel file",
                    data=pass_buffer,
                    file_name="pass.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            
            if not fail_df.empty:
                fail_buffer = create_excel_buffer(fail_df, "Failed Students")
                st.download_button(
                    label="Download Failed Students Excel file",
                    data=fail_buffer,
                    file_name="fail.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
                
            if not absent_df.empty:
                absent_buffer = create_excel_buffer(absent_df, "Absent Students")
                st.download_button(
                    label="Download Absent Students Excel file",
                    data=absent_buffer,
                    file_name="absent.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
                
            if not detained_df.empty:
                detained_buffer = create_excel_buffer(detained_df, "Detained Students")
                st.download_button(
                    label="Download Detained Students Excel file",
                    data=detained_buffer,
                    file_name="detained.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

if __name__ == "__main__":
    main()
