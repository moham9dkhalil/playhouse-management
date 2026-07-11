# Development Guide

## Environment Setup

### Requirements
- Python 3.11+
- PostgreSQL 14+
- Redis 6+
- Docker & Docker Compose (optional but recommended)

### Quick Start with Docker

```bash
# Clone the repository
git clone https://github.com/moham9dkhalil/playhouse-management.git
cd playhouse-management

# Start services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f backend
```

### Manual Setup

```bash
# Clone
git clone https://github.com/moham9dkhalil/playhouse-management.git
cd playhouse-management

# Virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
cd backend
pip install -r requirements.txt

# Setup database
psql -U postgres -c "CREATE DATABASE playhouse_db"
psql -U postgres -d playhouse_db -c "CREATE USER playhouse WITH PASSWORD 'playhouse123'"
psql -U postgres -d playhouse_db -c "GRANT ALL PRIVILEGES ON DATABASE playhouse_db to playhouse"

# Run migrations (when ready)
alembic upgrade head

# Start server
uvicorn app.main:app --reload
```

---

## API Testing

### Using Swagger UI
```
http://localhost:8000/docs
```

### Using cURL

```bash
# Health check
curl http://localhost:8000/health

# Register
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "user@example.com",
    "password": "password123",
    "full_name": "Ahmed",
    "role": "staff"
  }'

# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "user@example.com",
    "password": "password123"
  }'

# Use token in requests
curl http://localhost:8000/api/v1/devices/ \
  -H "Authorization: Bearer <your_token>"
```

### Using Postman
1. Import the API endpoints
2. Set BASE_URL variable: `http://localhost:8000/api/v1`
3. Use Pre-request Script to set token

---

## Database

### Accessing Database

```bash
# Connect to PostgreSQL
psql -h localhost -U playhouse -d playhouse_db

# Common commands
\dt                 # List tables
\d table_name       # Describe table
\l                  # List databases
\q                  # Quit
```

### Creating Sample Data

```bash
cd backend
python -m scripts.seed_data
```

### Resetting Database

```bash
# With Docker
docker-compose down -v
docker-compose up -d

# Manual
psql -U postgres -d playhouse_db -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
python -m scripts.seed_data
```

---

## Debugging

### Using print statements
```python
from app.main import app

@app.get("/debug")
def debug():
    print("Debug info here")
    return {"status": "ok"}
```

### Using logging
```python
import logging
logger = logging.getLogger(__name__)

logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
```

### Using debugger
```bash
# Install debugger
pip install debugpy

# Add to code
import debugpy
debugpy.listen(("0.0.0.0", 5678))
debugpy.wait_for_client()
```

---

## Testing

### Run all tests
```bash
pytest
```

### Run specific test
```bash
pytest tests/test_devices.py::test_list_devices
```

### Run with coverage
```bash
pytest --cov=app --cov-report=html tests/
open htmlcov/index.html
```

### Write a test
```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
```

---

## Code Quality

### Format code
```bash
black app/
isort app/
```

### Lint
```bash
flake8 app/ --max-line-length=100
```

### Type checking
```bash
mypy app/
```

### All together
```bash
pytest && black app/ && flake8 app/ && mypy app/
```

---

## Performance

### Profiling
```python
from cProfile import run
run('your_function()')
```

### Load testing
```bash
pip install locust
locust -f tests/locustfile.py --host=http://localhost:8000
```

---

## Deployment

### Production with Gunicorn
```bash
cd backend
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker
```

### Using Docker
```bash
# Build
docker build -t playhouse-backend:latest ./backend

# Run
docker run -p 8000:8000 playhouse-backend:latest
```

### Environment Setup
```bash
# Copy and update .env
cp .env.example .env
# Edit .env with production values
```

---

## Troubleshooting

### Port already in use
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9
```

### Database connection issues
```bash
# Check PostgreSQL
psql -h localhost -U playhouse -d playhouse_db -c "SELECT 1"
```

### Redis issues
```bash
# Check Redis
redis-cli ping
```

### Import errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

---

## Resources

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)
- [PostgreSQL Docs](https://www.postgresql.org/docs/)
- [Pydantic Docs](https://docs.pydantic.dev/)
- [Docker Docs](https://docs.docker.com/)

---

## Tips & Tricks

1. **Use VS Code REST Client**
   ```
   Extension: REST Client
   Create file: .vscode/requests.http
   ```

2. **Environment variables**
   ```bash
   source venv/bin/activate
   export PYTHONPATH="${PWD}/backend"
   ```

3. **Database backup**
   ```bash
   pg_dump -U playhouse playhouse_db > backup.sql
   ```

4. **Database restore**
   ```bash
   psql -U playhouse playhouse_db < backup.sql
   ```

---

Need help? Check GitHub Issues or contact the team!
