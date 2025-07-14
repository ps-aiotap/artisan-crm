# Artisan CRM - AI-Powered Customer Relationship Management

A modular, AI-powered CRM system built for both StoreLoop (artisan e-commerce) and AioTap (AI consulting) businesses.

## Quick Start

### 1. Environment Setup

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your configuration
# Required: DB_PASSWORD, SECRET_KEY, CRM_DB_NAME
```

### 2. Database Setup

```bash
# Create CRM database
psql -c "CREATE DATABASE artisan_crm;"

# Run migrations
python manage.py migrate
python manage.py migrate --database=artisan_crm
```

### 3. Start Server

```bash
python manage.py runserver
```

### 4. Access CRM Interface

- **Customer List**: http://localhost:8000/crm/
- **Lead Pipeline**: http://localhost:8000/crm/pipeline/
- **Login**: http://localhost:8000/crm/login/

## Features

### 🤖 AI-Powered Workflows

- Conversation Summarization
- Reply Suggestions
- Intent Classification
- Follow-up Generation

### 📊 Customer Management

- Customer Profiles with interaction history
- Tag Management
- Lead Scoring
- Timeline tracking

### 🎯 Lead Pipeline

- Kanban Board interface
- Stage Tracking
- Progress Monitoring

### 🔄 Mode-Aware Operation

- **StoreLoop Mode**: Artisan WhatsApp sales
- **AioTap Mode**: AI consulting workflows
- Dynamic UI per mode

## Environment Configuration

### Required Variables

```bash
# Essential settings
CRM_MODE=STORELOOP          # or AIO
CRM_DB_NAME=artisan_crm
DB_PASSWORD=your-password
SECRET_KEY=your-secret-key

# Optional AI features
OPENAI_API_KEY=your-openai-key
```

### Database Configuration

- Uses PostgreSQL with separate CRM database
- Auto-creates databases if they don't exist
- Cross-database integration with StoreLoop users

## API Endpoints

### Customer Management

- `GET /crm/customers/` - Customer list with filters
- `GET /crm/customers/<id>/` - Customer detail with timeline
- `POST /crm/customers/<id>/interaction/` - Add interaction

### AI Features

- `POST /crm/customers/<id>/summary/` - Generate AI summary
- `POST /crm/customers/<id>/reply/` - Get reply suggestion

### Pipeline Management

- `GET /crm/pipeline/` - Kanban pipeline view
- `POST /crm/pipeline/move/` - Move lead between stages

## AT Identity Integration

### Prerequisites

1. **AT Identity Service** must be running on `http://localhost:8001`
2. Set `AT_IDENTITY_URL=http://localhost:8001` in `.env`
3. Set `APP_NAME=artisan_crm` in `.env`

### Authentication Flow

1. User visits `/crm/login/`
2. Redirected to AT Identity service at `http://localhost:8001/accounts/login/`
3. After successful login, AT Identity redirects back with user ID
4. Middleware fetches user data from AT Identity API
5. User is authenticated in CRM system

## Architecture

- **Separate Database**: Uses `artisan_crm` PostgreSQL database
- **AT Identity Integration**: Centralized authentication service
- **Database Router**: Automatic routing for CRM models
- **Mode-Specific Features**: StoreLoop vs AioTap workflows

## Development

### Seed Sample Data

```bash
# For StoreLoop mode (default)
python manage.py seed_crm_data --customers 10

# For AioTap mode
CRM_MODE=AIO python manage.py seed_crm_data --customers 10
```

### Mock Channel Integration

The system includes mock message connectors for testing WhatsApp, Email, and Upwork interactions.

## Security

- Never commit `.env` to version control
- Uses AT Identity for authentication
- Cross-database security with user ID references
- Session-based authentication with timeout
