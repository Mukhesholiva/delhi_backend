import pandas as pd

def check_excel_format():
    """Check the format of the Excel file."""
    excel_file_path = r"C:\Users\Oliva\Documents\Credit balance report Delhi - email iD's_updated_sheet.xlsx"
    
    try:
        # Read the Excel file
        df = pd.read_excel(excel_file_path)
        
        print(f"Shape: {df.shape}")
        print(f"Columns: {df.columns.tolist()}")
        print("\nFirst 10 rows:")
        print(df.head(10))
        
        # Check if there are multiple sheets
        xl_file = pd.ExcelFile(excel_file_path)
        print(f"\nSheet names: {xl_file.sheet_names}")
        
        # Try reading each sheet
        for sheet_name in xl_file.sheet_names:
            print(f"\n--- Sheet: {sheet_name} ---")
            sheet_df = pd.read_excel(excel_file_path, sheet_name=sheet_name)
            print(f"Shape: {sheet_df.shape}")
            print(f"Columns: {sheet_df.columns.tolist()}")
            print("First 5 rows:")
            print(sheet_df.head(5))
            
    except Exception as e:
        print(f"Error reading Excel file: {e}")

if __name__ == "__main__":
    check_excel_format()
