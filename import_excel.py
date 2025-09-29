import pandas as pd
from sqlalchemy.orm import sessionmaker
from database import engine, Base
from models import CreditBalance
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def import_excel_data(excel_file_path: str):
    """Import data from Excel file to database."""
    
    # Create session
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Create tables
        logger.info("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        
        # Read Excel file
        logger.info(f"Reading Excel file: {excel_file_path}")
        df = pd.read_excel(excel_file_path)
        
        # Clean column names (remove extra spaces)
        df.columns = df.columns.str.strip()
        
        logger.info(f"Found {len(df)} rows in Excel file")
        logger.info(f"Columns: {df.columns.tolist()}")
        
        # Clear existing data
        logger.info("Clearing existing data...")
        db.query(CreditBalance).delete()
        db.commit()
        
        # Import data
        imported_count = 0
        for index, row in df.iterrows():
            try:
                # Create CreditBalance object
                credit_balance = CreditBalance(
                    client_code=str(row.get('Client Code', '')),
                    client_name=str(row.get('Client name', '')),
                    phone_no=str(row.get('Phone No', '')) if pd.notna(row.get('Phone No')) else None,
                    treatment_name=str(row.get('Treatment Name', '')) if pd.notna(row.get('Treatment Name')) else None,
                    package_amount=float(str(row.get('Package Amount (₹)', 0)).replace(',', '')) if pd.notna(row.get('Package Amount (₹)')) else 0.0,
                    amount_paid=float(str(row.get('Amount Paid by the client', 0)).replace(',', '')) if pd.notna(row.get('Amount Paid by the client')) else 0.0,
                    balance_amount=float(str(row.get('Balance Amount (₹)', 0)).replace(',', '')) if pd.notna(row.get('Balance Amount (₹)')) else 0.0,
                    prepaid_gift_card_balance=float(str(row.get('Prepaid / Gift Card Balance', 0)).replace(',', '')) if pd.notna(row.get('Prepaid / Gift Card Balance')) else 0.0,
                    center=str(row.get('Center', '')) if pd.notna(row.get('Center')) else None,
                    final_bucket=str(row.get('Final Bucket', '')) if pd.notna(row.get('Final Bucket')) else None,
                    sessions_paid=float(row.get('Sessions Paid', 0)) if pd.notna(row.get('Sessions Paid')) else 0.0,
                    sessions_consumed=float(row.get('Sessions Consumed', 0)) if pd.notna(row.get('Sessions Consumed')) else 0.0,
                    balance_sessions=float(row.get('Balance Sessions', 0)) if pd.notna(row.get('Balance Sessions')) else 0.0,
                )
                
                db.add(credit_balance)
                imported_count += 1
                
                # Commit in batches of 100
                if imported_count % 100 == 0:
                    db.commit()
                    logger.info(f"Imported {imported_count} records...")
                    
            except Exception as e:
                logger.error(f"Error importing row {index}: {e}")
                continue
        
        # Final commit
        db.commit()
        logger.info(f"Successfully imported {imported_count} records")
        
        return imported_count
        
    except Exception as e:
        logger.error(f"Error importing Excel data: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    excel_file_path = r"C:\Users\Oliva\Downloads\Credit balance report Delhi - Copy.xlsx"
    try:
        count = import_excel_data(excel_file_path)
        print(f"Import completed successfully. {count} records imported.")
    except Exception as e:
        print(f"Import failed: {e}")
