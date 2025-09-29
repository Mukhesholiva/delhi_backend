# Delhi Clinic Credit Balance Management System

A comprehensive backend API for managing credit balance data for Delhi Clinic with multiple centers.

## Features

- **Credit Balance Management**: Full CRUD operations for client credit balance records
- **Multi-Center Support**: Support for GK2, Punjabi Bagh, Preet Vihar, and Pitampura centers
- **Voucher Generation**: Automatic voucher number generation based on center, client code, and phone number
- **Email Integration**: Client email addresses for communication
- **Session Tracking**: Package sessions, consumed sessions, and balance sessions
- **API Logging**: Track API usage and voucher searches
- **Authentication**: JWT-based authentication system
- **SQL Server Integration**: Connected to SQL Server database

## Database Schema

### Credit Balance Table
- `id`: Primary key
- `client_code`: Unique client identifier
- `client_name`: Client full name
- `phone_no`: Client phone number
- `email_id`: Client email address
- `treatment_name`: Treatment/service name
- `package_amount`: Total package amount
- `amount_paid`: Amount paid by client
- `balance_amount`: Outstanding balance
- `prepaid_gift_card_balance`: Prepaid/gift card balance
- `center`: Clinic center (GK2, Punjabi Bagh, Preet Vihar, Pitampura)
- `final_bucket`: Treatment category
- `sessions_paid`: Total sessions purchased
- `sessions_consumed`: Sessions used
- `balance_sessions`: Remaining sessions
- `voucher_number`: Auto-generated voucher number
- `created_at`: Record creation timestamp
- `updated_at`: Last update timestamp

## Voucher Number Format

Voucher numbers are generated using the following format:
- **Prefix**: Based on center
  - `GK` for GK2/Greater Kailash
  - `PV` for Preet Vihar
  - `PB` for Punjabi Bagh
  - `PT` for Pitampura
- **Client Code**: First 3 characters
- **Phone Number**: Middle 4 digits

Example: `PBAD05349` (Punjabi Bagh, AD03C4403, phone 7985349490)

## API Endpoints

### Core Endpoints
- `GET /credit-balances/` - List all credit balances with filtering
- `GET /credit-balances/{id}` - Get specific credit balance
- `POST /credit-balances/` - Create new credit balance
- `PUT /credit-balances/{id}` - Update credit balance
- `DELETE /credit-balances/{id}` - Delete credit balance
- `GET /credit-balances/stats/summary` - Get summary statistics

### Center-Based Endpoints
- `GET /credit-balances/by-center/{center_name}` - Get records by center
- `GET /credit-balances/by-user-center` - Get records for user's center (requires auth)

### Voucher Endpoints
- `POST /credit-balances/by-voucher` - Search by voucher number
- `GET /api-logs` - Get API usage logs
- `GET /api-logs/by-user/{user_name}` - Get logs by user

### Authentication Endpoints
- `POST /login` - User login
- `POST /token` - OAuth2 token generation
- `GET /users/me` - Get current user info

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Environment Configuration
Copy `env.example` to `.env` and update the database connection:
```
DATABASE_URL=mssql+pyodbc://sa:Oliva@9876@111.93.26.122/Delhi?driver=ODBC+Driver+17+for+SQL+Server
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 3. Database Setup
The system will automatically create tables on first run. To import data:
```bash
python import_updated_excel.py
```

### 4. Run the Server
```bash
python run.py
```

The API will be available at `http://localhost:8000`

## Data Import

### Excel Import
The system supports importing data from Excel files with the following format:
- Client Code
- Client Name
- Phone No
- Treatment Name
- Center
- Package Amount (₹)
- Amount Paid by the client
- Balance Amount (₹)
- Prepaid / Gift Card Balance
- Sessions Paid
- Sessions Consumed
- Balance Sessions
- Email ID's

### Import Scripts
- `import_updated_excel.py` - Import from updated Excel format
- `update_voucher_numbers.py` - Update existing voucher numbers
- `add_email_column.py` - Add email column to database

## Testing

### API Testing
Use the provided cURL commands in `API_CURL_COMMANDS.md` for Postman testing.

### Test Scripts
- `test_api.py` - Basic API functionality tests
- `test_connection.py` - Database connection test

## Current Data Status
- **Total Records**: 1,353 credit balance entries
- **Total Balance**: ₹21,942,400.57
- **Centers**: Pitampura, Punjabi Bagh, GK2, Preet Vihar
- **Database**: SQL Server at 111.93.26.122

## Technology Stack
- **Backend**: FastAPI, SQLAlchemy, PyODBC
- **Database**: SQL Server
- **Authentication**: JWT with OAuth2
- **Data Processing**: Pandas, OpenPyXL
- **API Documentation**: Automatic OpenAPI/Swagger docs

## File Structure
```
delhi_backend/
├── main.py                 # FastAPI application
├── models.py              # SQLAlchemy models
├── schemas.py             # Pydantic schemas
├── database.py            # Database connection
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── run.py                 # Server startup script
├── import_updated_excel.py # Excel data import
├── update_voucher_numbers.py # Voucher update script
├── test_api.py            # API testing
└── API_CURL_COMMANDS.md   # API documentation
```

## Support
For issues or questions, refer to the API documentation at `http://localhost:8000/docs` when the server is running.