# Artisan CRM Setup Guide

## Environment Configuration

### 1. Environment Variables Setup

Copy the example environment file:

```bash
cp .env.example .env
```

Update `.env` with your actual values:

#### Required Configuration

```bash
# Database
DB_PASSWORD=your-actual-password
SECRET_KEY=your-unique-secret-key

# CRM Database
artisan_NAME=artisan

# AI Integration (Optional)
OPENAI_API_KEY=your-openai-api-key
```

#### Mode Configuration

```bash
# For StoreLoop (artisan e-commerce)
CRM_MODE=STORELOOP

# For AioTap (AI consulting)
CRM_MODE=AIO
```

### 2. Start AT Identity Service

```bash
# Start AT Identity on port 8001
python manage.py runserver 8001
```

### 3. Database Setup

Create CRM database:

```sql
CREATE DATABASE artisan;
```

Run migrations:

```bash
python manage.py migrate --database=artisan
```

### 4. Sample Data

Seed with test data:

```bash
# StoreLoop mode
python manage.py seed_crm_data --customers 10

# AioTap mode
CRM_MODE=AIO python manage.py seed_crm_data --customers 10
```

### 5. AI Features

Generate AI follow-ups:

```bash
python manage.py generate_followups --days 7 --limit 20
```

## Quick Start URLs

- **Login**: http://localhost:8000/crm/login/
- **Customer List**: http://localhost:8000/crm/
- **Lead Pipeline**: http://localhost:8000/crm/pipeline/
- **Admin**: http://localhost:8000/admin/

## Environment Variables Reference

| Variable          | Default                      | Description                    |
| ----------------- | ---------------------------- | ------------------------------ |
| `CRM_MODE`        | `STORELOOP`                  | `STORELOOP` or `AIO`           |
| `artisan_NAME`    | `artisan`                    | CRM database name              |
| `OPENAI_API_KEY`  | -                            | OpenAI API key for AI features |
| `AI_MODEL`        | `gpt-3.5-turbo`              | AI model to use                |
| `USE_AT_IDENTITY` | `True`                       | Enable AT Identity integration |
| `AT_IDENTITY_URL` | `http://localhost:8001/api/` | AT Identity service URL        |

## Security Notes

- Never commit `.env` file to version control
- Use strong, unique `SECRET_KEY` in production
- Rotate API keys regularly
- Use environment-specific configurations
