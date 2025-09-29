# API cURL Commands for Postman Testing

## Base URL: `http://localhost:8000`

## 1. Health Check
```bash
GET http://localhost:8000/health
```

## 2. Get All Credit Balances (with pagination)
```bash
GET http://localhost:8000/credit-balances/?skip=0&limit=10
```

## 3. Get Credit Balances with Filters
```bash
# Filter by client code
GET http://localhost:8000/credit-balances/?client_code=AD03C4403

# Filter by center
GET http://localhost:8000/credit-balances/?center=Punjabi%20Bagh

# Filter by client name
GET http://localhost:8000/credit-balances/?client_name=Anusha

# Combined filters
GET http://localhost:8000/credit-balances/?center=GK2&limit=5
```

## 4. Get Single Credit Balance by ID
```bash
GET http://localhost:8000/credit-balances/1
```

## 5. Get Summary Statistics
```bash
GET http://localhost:8000/credit-balances/stats/summary
```

## 6. Create New Credit Balance
```bash
POST http://localhost:8000/credit-balances/
Content-Type: application/json

{
  "client_code": "TEST001",
  "client_name": "Test Client",
  "phone_no": "9876543210",
  "email_id": "test@example.com",
  "treatment_name": "Test Treatment",
  "package_amount": 10000.0,
  "amount_paid": 5000.0,
  "balance_amount": 5000.0,
  "prepaid_gift_card_balance": 0.0,
  "center": "GK2",
  "final_bucket": "Test Bucket",
  "sessions_paid": 10.0,
  "sessions_consumed": 5.0,
  "balance_sessions": 5.0
}
```

## 7. Update Credit Balance
```bash
PUT http://localhost:8000/credit-balances/1
Content-Type: application/json

{
  "client_name": "Updated Client Name",
  "balance_amount": 3000.0,
  "email_id": "updated@example.com"
}
```

## 8. Delete Credit Balance
```bash
DELETE http://localhost:8000/credit-balances/1
```

## 9. Get Credit Balances by Center
```bash
GET http://localhost:8000/credit-balances/by-center/GK2?skip=0&limit=10
GET http://localhost:8000/credit-balances/by-center/Punjabi%20Bagh?skip=0&limit=10
GET http://localhost:8000/credit-balances/by-center/Preet%20Vihar?skip=0&limit=10
```

## 10. Search by Voucher Number
```bash
POST http://localhost:8000/credit-balances/by-voucher
Content-Type: application/json

{
  "user_name": "Test User",
  "voucher_id": "PBAD05349"
}
```

## 11. Get API Logs
```bash
GET http://localhost:8000/api-logs?skip=0&limit=10
```

## 12. Get API Logs by User
```bash
GET http://localhost:8000/api-logs/by-user/Test%20User?skip=0&limit=10
```

## 13. Get All Centers
```bash
GET http://localhost:8000/centers
```

## 14. Authentication Endpoints (if using auth)

### Login
```bash
POST http://localhost:8000/login
Content-Type: application/json

{
  "username": "your_username",
  "password": "your_password"
}
```

### OAuth2 Token
```bash
POST http://localhost:8000/token
Content-Type: application/x-www-form-urlencoded

username=your_username&password=your_password
```

### Get Current User (with Bearer token)
```bash
GET http://localhost:8000/users/me
Authorization: Bearer YOUR_ACCESS_TOKEN
```

## 15. Get Credit Balances by User's Center (requires auth)
```bash
GET http://localhost:8000/credit-balances/by-user-center?skip=0&limit=10
Authorization: Bearer YOUR_ACCESS_TOKEN
```

---

## Sample Test Data

Based on your imported data, here are some sample client codes and voucher numbers to test:

### Sample Client Codes:
- `AD03C4403` (Anusha Singh - Punjabi Bagh)
- `AN01C11235` (Minal Sharaff - Punjabi Bagh)
- `PV03C531` (Aadish Gupta - Preet Vihar)
- `GK04C139` (Praveen Chandravanshi - GK2)

### Sample Voucher Numbers (after update):
- `PBAD05349` (Punjabi Bagh - AD03C4403)
- `PBAN07827` (Punjabi Bagh - AN01C11235)
- `PVPV05310` (Preet Vihar - PV03C531)
- `GKGK04139` (GK2 - GK04C139)

### Sample Centers:
- `GK2`
- `Punjabi Bagh`
- `Preet Vihar`
- `Pitampura`

---

## Expected Response Format

### Credit Balance Object:
```json
{
  "id": 1,
  "client_code": "AD03C4403",
  "client_name": "Anusha Singh",
  "phone_no": "7985349490",
  "email_id": "anusha.singh.211@gmail.com",
  "treatment_name": "Hypertrichosis-Full Body-LHR-Female-4S",
  "package_amount": 40000.37,
  "amount_paid": 40000.37,
  "balance_amount": 32266.95,
  "prepaid_gift_card_balance": 0.0,
  "center": "Punjabi Bagh",
  "final_bucket": null,
  "sessions_paid": 80.0,
  "sessions_consumed": 13.0,
  "balance_sessions": 67.0,
  "voucher_number": "PBAD05349",
  "created_at": "2025-09-29T13:27:08.616667+00:00",
  "updated_at": null
}
```

### Summary Stats Response:
```json
{
  "total_records": 1353,
  "total_balance_amount": 12345678.90,
  "total_balance_sessions": 1234.0,
  "centers": ["GK2", "Punjabi Bagh", "Preet Vihar", "Pitampura"]
}
```
