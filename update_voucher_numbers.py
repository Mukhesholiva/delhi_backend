import pyodbc
from urllib.parse import quote_plus
from sqlalchemy.orm import sessionmaker
from database import engine
from models import CreditBalance
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def update_voucher_numbers():
    """Update all voucher numbers in the database with correct prefixes."""
    
    # Create session
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Get all records
        records = db.query(CreditBalance).all()
        logger.info(f"Found {len(records)} records to update")
        
        updated_count = 0
        for record in records:
            # Generate new voucher number
            new_voucher = record.generate_voucher_number()
            
            # Update the record
            record.voucher_number = new_voucher
            updated_count += 1
            
            if updated_count % 100 == 0:
                db.commit()
                logger.info(f"Updated {updated_count} records...")
        
        # Final commit
        db.commit()
        logger.info(f"Successfully updated {updated_count} voucher numbers")
        
        return updated_count
        
    except Exception as e:
        logger.error(f"Error updating voucher numbers: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    try:
        count = update_voucher_numbers()
        print(f"Voucher number update completed successfully. {count} records updated.")
    except Exception as e:
        print(f"Voucher number update failed: {e}")
