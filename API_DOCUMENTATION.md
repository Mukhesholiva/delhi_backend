# Delhi Clinic Credit Balance API Documentation

## Base URL
```
http://localhost:8000
```

## Endpoints

### 1. Health Check
```bash
curl -X GET "http://localhost:8000/health"
```

### 2. Get All Credit Balances
```bash
# Get all records (default limit: 100)
curl -X GET "http://localhost:8000/credit-balances/"

# Get with pagination
curl -X GET "http://localhost:8000/credit-balances/?skip=0&limit=50"

# Filter by client code
curl -X GET "http://localhost:8000/credit-balances/?client_code=PB01C1321"

# Filter by center
curl -X GET "http://localhost:8000/credit-balances/?center=GK2"

# Combined filters
curl -X GET "http://localhost:8000/credit-balances/?client_code=PB&center=GK2&limit=25"
```

### 3. Get Credit Balance by ID
```bash
curl -X GET "http://localhost:8000/credit-balances/1"
```

### 4. Create New Credit Balance
```bash
curl -X POST "http://localhost:8000/credit-balances/" \
  -H "Content-Type: application/json" \
  -d '{
    "client_code": "TEST001",
    "client_name": "Test Client",
    "phone_no": "9876543210",
    "treatment_name": "Test Treatment",
    "package_amount": 5000.00,
    "amount_paid": 3000.00,
    "balance_amount": 2000.00,
    "prepaid_gift_card_balance": 0.00,
    "center": "GK2",
    "final_bucket": "Test Category",
    "sessions_paid": 5,
    "sessions_consumed": 2,
    "balance_sessions": 3
  }'
```

### 5. Update Credit Balance
```bash
curl -X PUT "http://localhost:8000/credit-balances/1" \
  -H "Content-Type: application/json" \
  -d '{
    "balance_amount": 1500.00,
    "sessions_consumed": 3
  }'
```

### 6. Delete Credit Balance
```bash
curl -X DELETE "http://localhost:8000/credit-balances/1"
```

### 7. Get Summary Statistics
```bash
curl -X GET "http://localhost:8000/credit-balances/stats/summary"
```

## Response Examples

### Credit Balance Object
```json
{
  "id": 1,
  "client_code": "PB01C1321",
  "client_name": "DT Deepanshi Kataria",
  "phone_no": "9871828279",
  "treatment_name": "Tan-Face-Reviving-15",
  "package_amount": 6600.0,
  "amount_paid": 0.0,
  "balance_amount": 0.0,
  "prepaid_gift_card_balance": 0.0,
  "center": "GK2",
  "final_bucket": "Peels",
  "sessions_paid": 1.0,
  "sessions_consumed": 0.0,
  "balance_sessions": 1.0,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": null
}
```

### Summary Statistics
```json
{
  "total_records": 4799,
  "total_balance_amount": 1250000.50,
  "total_balance_sessions": 1500,
  "centers": ["GK2", "PV", "HS"]
}
```

## Error Responses

### 404 Not Found
```json
{
  "detail": "Credit balance not found"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "client_code"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

## Data Model

### CreditBalance Fields
- `id` (integer): Primary key
- `client_code` (string): Unique client identifier
- `client_name` (string): Full client name
- `phone_no` (string, optional): Phone number
- `treatment_name` (string, optional): Treatment name
- `package_amount` (float): Total package amount
- `amount_paid` (float): Amount paid by client
- `balance_amount` (float): Outstanding balance
- `prepaid_gift_card_balance` (float): Prepaid/gift card balance
- `center` (string, optional): Center code (GK2, PV, HS)
- `final_bucket` (string, optional): Treatment category
- `sessions_paid` (float): Total sessions paid for
- `sessions_consumed` (float): Sessions used
- `balance_sessions` (float): Remaining sessions
- `created_at` (datetime): Record creation timestamp
- `updated_at` (datetime, optional): Last update timestamp

## Running the API

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Import Excel data:
```bash
python import_excel.py
```

3. Start the server:
```bash
python run.py
```

The API will be available at `http://localhost:8000`

## Interactive API Documentation

Visit `http://localhost:8000/docs` for Swagger UI documentation with interactive testing capabilities.



