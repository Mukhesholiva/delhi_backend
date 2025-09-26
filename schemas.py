from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CreditBalanceBase(BaseModel):
    client_code: str
    client_name: str
    phone_no: Optional[str] = None
    treatment_name: Optional[str] = None
    package_amount: Optional[float] = 0.0
    amount_paid: Optional[float] = 0.0
    balance_amount: Optional[float] = 0.0
    prepaid_gift_card_balance: Optional[float] = 0.0
    center: Optional[str] = None
    final_bucket: Optional[str] = None
    sessions_paid: Optional[float] = 0.0
    sessions_consumed: Optional[float] = 0.0
    balance_sessions: Optional[float] = 0.0
    voucher_number: Optional[str] = None

class CreditBalanceCreate(CreditBalanceBase):
    pass

class CreditBalanceUpdate(BaseModel):
    client_code: Optional[str] = None
    client_name: Optional[str] = None
    phone_no: Optional[str] = None
    treatment_name: Optional[str] = None
    package_amount: Optional[float] = None
    amount_paid: Optional[float] = None
    balance_amount: Optional[float] = None
    prepaid_gift_card_balance: Optional[float] = None
    center: Optional[str] = None
    final_bucket: Optional[str] = None
    sessions_paid: Optional[float] = None
    sessions_consumed: Optional[float] = None
    balance_sessions: Optional[float] = None
    voucher_number: Optional[str] = None

class CreditBalance(CreditBalanceBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# Center Schemas
class CenterBase(BaseModel):
    name: str
    code: str
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = True

class CenterCreate(CenterBase):
    pass

class CenterUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = None

class Center(CenterBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# User Schemas
class UserBase(BaseModel):
    username: str
    email: str
    full_name: str
    role: str = "USER"
    role_id: Optional[int] = None
    center_id: Optional[int] = None
    is_active: Optional[bool] = True
    is_verified: Optional[bool] = False

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    full_name: Optional[str] = None
    role: Optional[str] = None
    role_id: Optional[int] = None
    center_id: Optional[int] = None
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None
    password: Optional[str] = None

class User(UserBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# Authentication Schemas
class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: User


# API Log Schemas
class ApiLogBase(BaseModel):
    user_name: str
    voucher_id: str
    api_endpoint: str
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None

class ApiLogCreate(ApiLogBase):
    pass

class ApiLog(ApiLogBase):
    id: int
    request_timestamp: datetime
    
    class Config:
        from_attributes = True


# Voucher Search Schemas
class VoucherSearchRequest(BaseModel):
    voucher_id: str
    user_name: str
