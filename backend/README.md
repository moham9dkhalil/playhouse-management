# Play House Management System - Backend

## Overview
Full-featured backend API for managing PlayStation gaming cafe/playhouse operations.

## Features

### 🎮 Device Management
- Track all PlayStation devices
- Monitor device status (active, maintenance, inactive)
- Maintenance logging and scheduling

### 👥 Customer Management
- Customer profiles and contact information
- Loyalty card system with points tracking
- Customer statistics and spending history

### 🎯 Session Management
- Start/pause/resume/end play sessions
- Automatic billing calculation
- Session history and analytics

### 🛒 Sales Management
- Cafeteria product sales
- Multiple payment methods
- Sales analytics and reports

### 📊 Reports & Analytics
- Daily/monthly revenue summaries
- Top customers analysis
- Session and sales statistics

### 🔐 Security
- JWT-based authentication
- Role-based access control (Admin, Manager, Staff)
- Password hashing with bcrypt

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations (when ready)
alembic upgrade head

# Start the server
uvicorn app.main:app --reload
```

## API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Project Structure

```
backend/
├── app/
│   ├── api/v1/           # API endpoints
│   ├── core/             # Configuration and utilities
│   ├── models/           # SQLAlchemy models
│   ├── schemas/          # Pydantic validators
│   ├── services/         # Business logic
│   └── main.py          # FastAPI app
├── requirements.txt      # Dependencies
└── Dockerfile           # Container configuration
```

## Key Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login

### Devices
- `GET /api/v1/devices/` - List devices
- `POST /api/v1/devices/` - Create device
- `POST /api/v1/devices/{id}/maintenance` - Mark for maintenance

### Sessions
- `POST /api/v1/sessions/` - Start session
- `POST /api/v1/sessions/{id}/pause` - Pause session
- `POST /api/v1/sessions/{id}/resume` - Resume session
- `POST /api/v1/sessions/{id}/end` - End session

### Customers
- `GET /api/v1/customers/` - List customers
- `POST /api/v1/customers/` - Create customer
- `GET /api/v1/customers/{id}/loyalty-card` - Get loyalty card
- `GET /api/v1/customers/{id}/stats` - Customer statistics

### Sales
- `POST /api/v1/sales/` - Create sale
- `GET /api/v1/sales/` - List sales

### Reports
- `GET /api/v1/reports/daily-summary` - Daily summary
- `GET /api/v1/reports/monthly-summary` - Monthly summary
- `GET /api/v1/reports/top-customers` - Top customers

## Database Models

- **Users** - System users with roles
- **PlaystationDevice** - Gaming devices
- **PlaySession** - Gaming sessions
- **Customer** - Customer profiles
- **LoyaltyCard** - Customer loyalty cards
- **CafeteriaProduct** - Shop products
- **Sale** - Sales transactions
- **Game** - Available games
- **SystemSettings** - Configuration settings

## Technologies

- FastAPI - Modern Python web framework
- SQLAlchemy - ORM
- PostgreSQL - Database
- Redis - Caching/Sessions
- Pydantic - Data validation
- JWT - Authentication

## Development

```bash
# Install dev dependencies
pip install -r requirements.txt

# Run with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run tests
pytest
```

## Docker

```bash
# Build image
docker build -t playhouse-backend .

# Run container
docker run -p 8000:8000 playhouse-backend
```

## Contributing

Please create a new branch for each feature and submit a pull request.

## License

MIT License - See LICENSE file for details
