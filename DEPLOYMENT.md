# Deployment Guide

## Prerequisites

- Python 3.8+
- Node.js 16+
- PostgreSQL 12+
- Stellar SDK
- Docker (optional)

## Backend Setup

### 1. Environment Configuration

```bash
cp .env.example .env
```

Edit `.env` with your configuration:
```
STELLAR_SERVER=https://horizon-testnet.stellar.org
STELLAR_NETWORK=Test SDF Network ; September 2015
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 2. Database Migration

```bash
cd backend
python manage.py migrate
python manage.py createsuperuser
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Development Server

```bash
python manage.py runserver
```

## Frontend Setup

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Configure API Endpoint

Edit `frontend/src/api/client.js`:
```javascript
const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000';
```

### 3. Run Development Server

```bash
npm start
```

## Docker Deployment

### 1. Build Images

```bash
docker-compose build
```

### 2. Start Services

```bash
docker-compose up -d
```

### 3. Run Migrations

```bash
docker-compose exec backend python manage.py migrate
```

## Production Deployment

### 1. Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### 2. Configure Gunicorn

```bash
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

### 3. Setup Nginx

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location /api/ {
        proxy_pass http://localhost:8000;
    }

    location / {
        proxy_pass http://localhost:3000;
    }
}
```

### 4. Enable HTTPS

```bash
certbot certonly --standalone -d your-domain.com
```

## Stellar Testnet Setup

### 1. Fund Account

```bash
curl "https://friendbot.stellar.org?addr=YOUR_PUBLIC_KEY"
```

### 2. Verify Account

```bash
curl "https://horizon-testnet.stellar.org/accounts/YOUR_PUBLIC_KEY"
```

## Database Backup

```bash
pg_dump forex_db > backup.sql
```

## Monitoring

### 1. Application Logs

```bash
tail -f /var/log/gunicorn.log
```

### 2. Database Logs

```bash
tail -f /var/log/postgresql/postgresql.log
```

## Troubleshooting

### Port Already in Use

```bash
lsof -i :8000
kill -9 <PID>
```

### Database Connection Error

```bash
psql -U postgres -h localhost -d forex_db
```

### Stellar Network Issues

Check network status: https://status.stellar.org/

## Maintenance

### Regular Backups

```bash
0 2 * * * pg_dump forex_db > /backups/backup_$(date +\%Y\%m\%d).sql
```

### Update Dependencies

```bash
pip install --upgrade -r requirements.txt
npm update
```

### Clear Cache

```bash
python manage.py clear_cache
```
