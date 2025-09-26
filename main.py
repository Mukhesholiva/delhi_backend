from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
import models
import schemas
from database import get_db, engine

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Delhi Clinic Credit Balance API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Authentication configuration
SECRET_KEY = "your-secret-key-change-this-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Authentication helper functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(db, username=username)
    if user is None:
        raise credentials_exception
    return user

@app.get("/")
async def root():
    return {"message": "Delhi Clinic Credit Balance API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# CRUD operations for CreditBalance
@app.post("/credit-balances/", response_model=schemas.CreditBalance)
async def create_credit_balance(credit_balance: schemas.CreditBalanceCreate, db: Session = Depends(get_db)):
    db_credit_balance = models.CreditBalance(**credit_balance.dict())
    # Generate voucher number
    db_credit_balance.voucher_number = db_credit_balance.generate_voucher_number()
    db.add(db_credit_balance)
    db.commit()
    db.refresh(db_credit_balance)
    return db_credit_balance

@app.get("/credit-balances/", response_model=List[schemas.CreditBalance])
async def get_credit_balances(
    skip: int = 0, 
    limit: Optional[int] = None, 
    client_code: Optional[str] = None,
    client_name: Optional[str] = None,
    center: Optional[str] = None,
    db: Session = Depends(get_db)
):
    from sqlalchemy.exc import OperationalError
    
    try:
        query = db.query(models.CreditBalance)
        
        if client_code:
            query = query.filter(models.CreditBalance.client_code.ilike(f"%{client_code}%"))
        if client_name:
            query = query.filter(models.CreditBalance.client_name.ilike(f"%{client_name}%"))
        if center:
            query = query.filter(models.CreditBalance.center.ilike(f"%{center}%"))
        
        # SQL Server requires ORDER BY for OFFSET/LIMIT
        query = query.order_by(models.CreditBalance.id).offset(skip)
        
        # If limit is provided, apply it; otherwise return all records
        if limit is not None:
            print(f"API: Returning {limit} records (limit provided)")
            return query.limit(limit).all()
        else:
            print(f"API: Returning ALL records (no limit provided)")
            return query.all()
    except OperationalError as e:
        print(f"Database connection error: {e}")
        # Return empty list if database is unavailable
        return []

@app.get("/credit-balances/{credit_balance_id}", response_model=schemas.CreditBalance)
async def get_credit_balance(credit_balance_id: int, db: Session = Depends(get_db)):
    credit_balance = db.query(models.CreditBalance).filter(models.CreditBalance.id == credit_balance_id).first()
    if credit_balance is None:
        raise HTTPException(status_code=404, detail="Credit balance not found")
    return credit_balance

@app.put("/credit-balances/{credit_balance_id}", response_model=schemas.CreditBalance)
async def update_credit_balance(
    credit_balance_id: int, 
    credit_balance_update: schemas.CreditBalanceUpdate, 
    db: Session = Depends(get_db)
):
    credit_balance = db.query(models.CreditBalance).filter(models.CreditBalance.id == credit_balance_id).first()
    if credit_balance is None:
        raise HTTPException(status_code=404, detail="Credit balance not found")
    
    update_data = credit_balance_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(credit_balance, field, value)
    
    # Regenerate voucher number if relevant fields were updated
    if any(field in update_data for field in ['center', 'client_code', 'phone_no']):
        credit_balance.voucher_number = credit_balance.generate_voucher_number()
    
    db.commit()
    db.refresh(credit_balance)
    return credit_balance

@app.delete("/credit-balances/{credit_balance_id}")
async def delete_credit_balance(credit_balance_id: int, db: Session = Depends(get_db)):
    credit_balance = db.query(models.CreditBalance).filter(models.CreditBalance.id == credit_balance_id).first()
    if credit_balance is None:
        raise HTTPException(status_code=404, detail="Credit balance not found")
    
    db.delete(credit_balance)
    db.commit()
    return {"message": "Credit balance deleted successfully"}

@app.get("/credit-balances/stats/summary")
async def get_summary_stats(db: Session = Depends(get_db)):
    from sqlalchemy import func
    from sqlalchemy.exc import OperationalError
    
    try:
        total_records = db.query(models.CreditBalance).count()
        total_balance = db.query(func.sum(models.CreditBalance.balance_amount)).scalar() or 0
        total_sessions = db.query(func.sum(models.CreditBalance.balance_sessions)).scalar() or 0
        
        centers = db.query(models.CreditBalance.center).distinct().all()
        center_list = [center[0] for center in centers if center[0]]
        
        return {
            "total_records": total_records,
            "total_balance_amount": total_balance,
            "total_balance_sessions": total_sessions,
            "centers": center_list
        }
    except OperationalError as e:
        # Handle database connection errors
        print(f"Database connection error: {e}")
        # Return default values if database is unavailable
        return {
            "total_records": 0,
            "total_balance_amount": 0,
            "total_balance_sessions": 0,
            "centers": []
        }

# Authentication endpoints
@app.post("/login", response_model=schemas.LoginResponse)
async def login(login_data: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, login_data.username, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }

@app.post("/token", response_model=schemas.LoginResponse)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }

# Center-based API endpoints
@app.get("/credit-balances/by-center/{center_name}", response_model=List[schemas.CreditBalance])
async def get_credit_balances_by_center(
    center_name: str,
    skip: int = 0,
    limit: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Get all credit balance records for a specific center."""
    from sqlalchemy.exc import OperationalError
    
    try:
        query = db.query(models.CreditBalance).filter(
            models.CreditBalance.center.ilike(f"%{center_name}%")
        )
        
        # SQL Server requires ORDER BY for OFFSET/LIMIT
        query = query.order_by(models.CreditBalance.id).offset(skip)
        
        # If limit is provided, apply it; otherwise return all records
        if limit is not None:
            print(f"API: Returning {limit} records for center '{center_name}' (limit provided)")
            return query.limit(limit).all()
        else:
            print(f"API: Returning ALL records for center '{center_name}' (no limit provided)")
            return query.all()
    except OperationalError as e:
        print(f"Database connection error: {e}")
        return []

@app.get("/credit-balances/by-user-center", response_model=List[schemas.CreditBalance])
async def get_credit_balances_by_user_center(
    skip: int = 0,
    limit: Optional[int] = None,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all credit balance records for the current user's center."""
    from sqlalchemy.exc import OperationalError
    
    try:
        # Get user's center
        if not current_user.center_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is not associated with any center"
            )
        
        # Get center name from center_id
        center = db.query(models.Center).filter(models.Center.id == current_user.center_id).first()
        if not center:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Center not found"
            )
        
        # Get credit balances for this center
        query = db.query(models.CreditBalance).filter(
            models.CreditBalance.center.ilike(f"%{center.name}%")
        )
        
        # SQL Server requires ORDER BY for OFFSET/LIMIT
        query = query.order_by(models.CreditBalance.id).offset(skip)
        
        # If limit is provided, apply it; otherwise return all records
        if limit is not None:
            print(f"API: Returning {limit} records for user's center '{center.name}' (limit provided)")
            return query.limit(limit).all()
        else:
            print(f"API: Returning ALL records for user's center '{center.name}' (no limit provided)")
            return query.all()
    except OperationalError as e:
        print(f"Database connection error: {e}")
        return []

# User management endpoints
@app.get("/users/me", response_model=schemas.User)
async def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user

@app.get("/centers", response_model=List[schemas.Center])
async def get_centers(db: Session = Depends(get_db)):
    """Get all centers."""
    return db.query(models.Center).filter(models.Center.is_active == True).all()

# Voucher-based API endpoint
@app.post("/credit-balances/by-voucher", response_model=List[schemas.CreditBalance])
async def get_credit_balances_by_voucher(
    request: schemas.VoucherSearchRequest,
    db: Session = Depends(get_db)
):
    """Get all credit balance records for a specific voucher ID and log the API usage."""
    from sqlalchemy.exc import OperationalError
    from fastapi import Request
    
    try:
        # Search for records with the given voucher ID
        query = db.query(models.CreditBalance).filter(
            models.CreditBalance.voucher_number.ilike(f"%{request.voucher_id}%")
        )
        
        # Get all matching records
        records = query.order_by(models.CreditBalance.id).all()
        
        # Log the API usage
        api_log = models.ApiLog(
            user_name=request.user_name,
            voucher_id=request.voucher_id,
            api_endpoint="/credit-balances/by-voucher",
            ip_address=None,  # Could be extracted from request if needed
            user_agent=None   # Could be extracted from request if needed
        )
        
        db.add(api_log)
        db.commit()
        
        print(f"API: User '{request.user_name}' searched for voucher '{request.voucher_id}' and found {len(records)} records")
        
        return records
        
    except OperationalError as e:
        print(f"Database connection error: {e}")
        return []
    except Exception as e:
        print(f"Error in voucher search: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing voucher search: {str(e)}"
        )

@app.get("/api-logs", response_model=List[schemas.ApiLog])
async def get_api_logs(
    skip: int = 0,
    limit: Optional[int] = 100,
    db: Session = Depends(get_db)
):
    """Get API usage logs."""
    from sqlalchemy.exc import OperationalError
    
    try:
        query = db.query(models.ApiLog).order_by(models.ApiLog.request_timestamp.desc())
        query = query.offset(skip)
        
        if limit is not None:
            return query.limit(limit).all()
        else:
            return query.all()
    except OperationalError as e:
        print(f"Database connection error: {e}")
        return []

@app.get("/api-logs/by-user/{user_name}", response_model=List[schemas.ApiLog])
async def get_api_logs_by_user(
    user_name: str,
    skip: int = 0,
    limit: Optional[int] = 100,
    db: Session = Depends(get_db)
):
    """Get API usage logs for a specific user."""
    from sqlalchemy.exc import OperationalError
    
    try:
        query = db.query(models.ApiLog).filter(
            models.ApiLog.user_name.ilike(f"%{user_name}%")
        ).order_by(models.ApiLog.request_timestamp.desc())
        
        query = query.offset(skip)
        
        if limit is not None:
            return query.limit(limit).all()
        else:
            return query.all()
    except OperationalError as e:
        print(f"Database connection error: {e}")
        return []

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
