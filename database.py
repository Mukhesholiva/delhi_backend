from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pyodbc
from urllib.parse import quote_plus
from config import settings

# Direct pyodbc connection string
db_config = {
    'server': '111.93.26.122',
    'database': 'Delhi',
    'username': 'sa',
    'password': 'Oliva@9876'
}

connection_string = (
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={db_config['server']};"
    f"DATABASE={db_config['database']};"
    f"UID={db_config['username']};"
    f"PWD={db_config['password']};"
    "ConnectRetryCount=5;"
    "ConnectRetryInterval=10;"
    "Connection Timeout=30;"
    "Command Timeout=60;"
    "TrustServerCertificate=yes;"
    "MultipleActiveResultSets=True;"
)

# Create SQLAlchemy engine with pyodbc and connection pooling
engine = create_engine(
    f"mssql+pyodbc:///?odbc_connect={quote_plus(connection_string)}",
    echo=False,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=3600,  # Recycle connections every hour
    pool_timeout=30
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()
