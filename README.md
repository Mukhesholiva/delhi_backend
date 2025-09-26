# Delhi Clinic Backend API

A FastAPI-based backend service for managing Delhi Clinic's credit balance system.

## Features

- Credit Balance Management
- User Authentication & Authorization
- Center-based Access Control
- Voucher System
- API Logging
- SQL Server Database Integration

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment variables:
```bash
cp env.example .env
# Edit .env with your database credentials
```

3. Run the application:
```bash
python run.py
```

The API will be available at `http://localhost:8000`

## API Documentation

Once running, visit `http://localhost:8000/docs` for interactive API documentation.

## Database

The application uses SQL Server with the following main tables:
- `credit_balances` - Client credit balance records
- `users` - User authentication and profiles
- `centers` - Clinic center information
- `api_logs` - API usage tracking

## Environment Variables

- `DATABASE_URL` - SQL Server connection string
- `SECRET_KEY` - JWT secret key
- `ALGORITHM` - JWT algorithm (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES` - Token expiration time
