from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class CreditBalance(Base):
    """Credit Balance model for storing client credit balance data."""
    
    __tablename__ = "credit_balances"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Client information
    client_code = Column(String(50), nullable=False, index=True)
    client_name = Column(String(255), nullable=False, index=True)
    phone_no = Column(String(20), nullable=True)
    
    # Treatment information
    treatment_name = Column(String(255), nullable=True)
    package_amount = Column(Float, nullable=True, default=0.0)
    amount_paid = Column(Float, nullable=True, default=0.0)
    balance_amount = Column(Float, nullable=True, default=0.0)
    prepaid_gift_card_balance = Column(Float, nullable=True, default=0.0)
    
    # Center and category information
    center = Column(String(50), nullable=True)
    final_bucket = Column(String(100), nullable=True)
    
    # Session information
    sessions_paid = Column(Float, nullable=True, default=0.0)
    sessions_consumed = Column(Float, nullable=True, default=0.0)
    balance_sessions = Column(Float, nullable=True, default=0.0)
    
    # Voucher information
    voucher_number = Column(String(20), nullable=True, index=True)
    
    # Audit fields
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def generate_voucher_number(self):
        """Generate voucher number based on center, client code, and phone number."""
        if not self.center or not self.client_code or not self.phone_no:
            return None
            
        # Determine prefix based on center
        prefix = "GK" if self.center.upper() == "GK2" else "PV"
        
        # Get first 3 digits of client code
        client_code_digits = ''.join(filter(str.isdigit, self.client_code))[:3]
        
        # Get middle 4 digits of phone number
        phone_digits = ''.join(filter(str.isdigit, self.phone_no))
        if len(phone_digits) >= 4:
            middle_phone = phone_digits[2:6] if len(phone_digits) > 6 else phone_digits[:4]
        else:
            middle_phone = phone_digits.zfill(4)
        
        return f"{prefix}{client_code_digits.zfill(3)}{middle_phone}"
    
    def __repr__(self):
        return f"<CreditBalance(id={self.id}, client_code='{self.client_code}', client_name='{self.client_name}')>"


class Center(Base):
    """Center model for storing clinic center information."""
    
    __tablename__ = "centers"
    __table_args__ = {'schema': 'delhi'}
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    code = Column(String(10), nullable=False, unique=True)
    address = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationship with users
    users = relationship("User", back_populates="center")
    
    def __repr__(self):
        return f"<Center(id={self.id}, name='{self.name}', code='{self.code}')>"


class User(Base):
    """User model for storing user authentication and profile information."""
    
    __tablename__ = "users"
    __table_args__ = {'schema': 'delhi'}
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), nullable=False, unique=True, index=True)
    email = Column(String(100), nullable=False, unique=True, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    role = Column(String(50), nullable=False, default="USER")
    role_id = Column(Integer, nullable=True)
    center_id = Column(Integer, ForeignKey("delhi.centers.id"), nullable=True)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationship with center
    center = relationship("Center", back_populates="users")
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}', role='{self.role}')>"


class ApiLog(Base):
    """API Log model for storing API usage logs."""
    
    __tablename__ = "api_logs"
    __table_args__ = {'schema': 'delhi'}
    
    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String(100), nullable=False)
    voucher_id = Column(String(50), nullable=False)
    api_endpoint = Column(String(100), nullable=False)
    request_timestamp = Column(DateTime(timezone=True), server_default=func.now())
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(500), nullable=True)
    
    def __repr__(self):
        return f"<ApiLog(id={self.id}, user_name='{self.user_name}', voucher_id='{self.voucher_id}', timestamp='{self.request_timestamp}')>"
