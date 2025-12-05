# SupportMax Pro v1 - MVP System

## Overview

Version 1 builds on v0.5 to create a complete vertical slice with end-to-end ticket processing, persistent storage, multi-turn conversations, and enterprise integrations. This is a production-ready MVP system.

## Key Features

### New in v1
- **Persistent Storage**: PostgreSQL for tickets, sessions, and user data
- **Multi-turn Conversations**: Track conversation history and context
- **Vector Database**: Chroma for semantic FAQ search
- **Message Queue**: Redis for asynchronous processing
- **Email Integration**: IMAP/SMTP for ticket intake
- **Chat Integration**: Web chat widget
- **CRM Integration**: Basic Salesforce sync
- **Dashboard**: Real-time metrics and monitoring
- **Advanced Classification**: Intent and urgency detection

### From v0.5
- LLM-powered responses (OpenAI GPT-4, Anthropic Claude)
- Production constraints enforcement
- FAQ knowledge base
- Automated ticket creation
- Comprehensive metrics tracking

## Technology Stack

- **LLM**: OpenAI GPT-4, Anthropic Claude Sonnet
- **Framework**: LangChain (basic chains)
- **Vector DB**: Chroma (embedded mode)
- **Queue**: Redis
- **Storage**: PostgreSQL
- **API**: FastAPI
- **Frontend**: React dashboard
- **Deployment**: Docker Compose (multi-container)

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend (React)                      │
│                  Dashboard + Chat Widget                     │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                     API Gateway (FastAPI)                    │
│              /chat, /tickets, /sessions, /metrics            │
└─────┬───────────────┬──────────────┬────────────────────────┘
      │               │              │
┌─────▼─────┐  ┌─────▼─────┐  ┌────▼──────┐
│  Intake   │  │Classification│ │  Response │
│  Agent    │  │   Agent    │  │   Agent   │
└─────┬─────┘  └─────┬──────┘  └────┬──────┘
      │              │              │
┌─────▼──────────────▼──────────────▼─────────┐
│          Vector Store (Chroma)               │
│         Knowledge + Embeddings               │
└──────────────────────────────────────────────┘
      │              │              │
┌─────▼─────┐  ┌────▼──────┐  ┌────▼──────┐
│PostgreSQL │  │   Redis   │  │   Email   │
│  Tickets  │  │   Queue   │  │   IMAP    │
│  Sessions │  │   Tasks   │  │   SMTP    │
└───────────┘  └───────────┘  └───────────┘
```

## Prerequisites

- Python 3.11+
- Docker and Docker Compose
- PostgreSQL 15+
- Redis 7+
- OpenAI or Anthropic API key
- Node.js 18+ (for frontend)
- Email account (for email integration)

## Quick Start

### 1. Clone and Setup

```bash
cd implementation/src/v1-mvp
cp .env.example .env
# Edit .env with your configuration
```

### 2. Start Services with Docker Compose

```bash
docker-compose up --build
```

This starts:
- API server (port 8000)
- PostgreSQL database (port 5432)
- Redis (port 6379)
- Frontend dashboard (port 3000)

### 3. Initialize Database

```bash
# Run migrations
docker-compose exec api python -m alembic upgrade head

# Load sample data
docker-compose exec api python scripts/load_sample_data.py
```

### 4. Access the System

- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Dashboard**: http://localhost:3000
- **Health Check**: http://localhost:8000/health

## API Endpoints

### Tickets
- `POST /tickets` - Create new ticket
- `GET /tickets/{id}` - Get ticket details
- `PUT /tickets/{id}` - Update ticket
- `GET /tickets` - List tickets (with filters)
- `POST /tickets/{id}/respond` - Add response to ticket

### Chat
- `POST /chat` - Process chat message (multi-turn)
- `GET /sessions/{id}` - Get conversation session
- `DELETE /sessions/{id}` - End conversation

### Integrations
- `POST /integrations/email/sync` - Sync email tickets
- `POST /integrations/salesforce/sync` - Sync with Salesforce
- `GET /integrations/status` - Integration health

### Metrics & Monitoring
- `GET /metrics` - Detailed system metrics
- `GET /health` - Health check
- `GET /dashboard/stats` - Dashboard statistics

## Configuration

### Environment Variables

```bash
# LLM Configuration
LLM_PROVIDER=openai
OPENAI_API_KEY=your-key
ANTHROPIC_API_KEY=your-key

# Database
DATABASE_URL=postgresql://supportmax:password@postgres:5432/supportmax

# Redis
REDIS_URL=redis://redis:6379/0

# Email Integration
EMAIL_IMAP_SERVER=imap.gmail.com
EMAIL_IMAP_PORT=993
EMAIL_USER=support@example.com
EMAIL_PASSWORD=your-password
EMAIL_SMTP_SERVER=smtp.gmail.com
EMAIL_SMTP_PORT=587

# Salesforce (optional)
SALESFORCE_USERNAME=your-username
SALESFORCE_PASSWORD=your-password
SALESFORCE_SECURITY_TOKEN=your-token
SALESFORCE_DOMAIN=login

# Application
DEBUG=false
LOG_LEVEL=INFO
API_PORT=8000
```

## Capabilities

### Processing Capacity
- 100-500 tickets per day
- Multi-turn conversations
- Concurrent users: 50+
- Average response time: 30 seconds

### Automation
- 70% automated resolution rate
- Automatic ticket creation from email
- Intent and urgency classification
- Smart ticket routing
- Escalation to human agents

### Integrations
- Email (IMAP/SMTP) - Ticket intake and responses
- Salesforce - CRM synchronization
- Web chat widget - Real-time chat
- Webhooks - Custom integrations

## Database Schema

### Tables
- `tickets` - Support tickets
- `sessions` - Conversation sessions
- `messages` - Chat messages
- `users` - User information
- `knowledge_articles` - FAQ articles
- `integrations` - Integration configurations

See [`docs/database_schema.md`](docs/database_schema.md) for details.

## Development

### Running Tests

```bash
# Unit tests
pytest tests/unit/ -v

# Integration tests
pytest tests/integration/ -v

# E2E tests
pytest tests/e2e/ -v

# All tests with coverage
pytest tests/ --cov=src --cov-report=html
```

### Database Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

### Local Development (with uv)

We recommend using `uv` for faster dependency management.

```bash
# 1. Setup Python environment and install dependencies
uv sync
source .venv/bin/activate

# 2. Install frontend dependencies
cd frontend && npm install

# 3. Start PostgreSQL and Redis locally
# Update .env with local connection strings

# 4. Run API
python src/api/main.py

# 5. Run frontend (separate terminal)
cd frontend && npm start

# 6. Run background workers
python src/queue/worker.py
```

## Deployment

### Production Deployment

```bash
# Build production images
docker-compose -f docker-compose.prod.yml build

# Deploy with environment-specific config
docker-compose -f docker-compose.prod.yml up -d

# Monitor logs
docker-compose logs -f api
```

### Scaling

```bash
# Scale API servers
docker-compose up -d --scale api=3

# Scale workers
docker-compose up -d --scale worker=2
```

## Monitoring

### Metrics Available
- Total tickets processed
- Resolution rate
- Average response time
- Conversation completion rate
- Integration status
- Database performance
- Queue depth
- Error rates

### Dashboards
- Real-time metrics dashboard (React)
- Grafana dashboards (optional)
- PostgreSQL monitoring
- Redis monitoring

## Troubleshooting

### Common Issues

**Database connection failed**
```bash
# Check PostgreSQL is running
docker-compose ps postgres

# Check logs
docker-compose logs postgres

# Reset database
docker-compose down -v
docker-compose up -d postgres
```

**Redis connection failed**
```bash
# Check Redis is running
docker-compose ps redis

# Test connection
docker-compose exec redis redis-cli ping
```

**Email integration not working**
```bash
# Test IMAP connection
docker-compose exec api python scripts/test_email.py

# Check credentials in .env
```

## Migration from v0.5

To migrate from v0.5:

1. **Data Migration**: v0.5 used in-memory storage, so no data to migrate
2. **Configuration**: Copy API keys from v0.5 `.env`
3. **Code**: v1 is backward compatible with v0.5 API endpoints
4. **Testing**: Run full test suite to verify

## What's New

### Architecture Changes
- Added PostgreSQL for persistence
- Added Redis for queue management
- Added Chroma for semantic search
- Multi-container deployment

### New Features
- Multi-turn conversations with history
- Email ticket intake and responses
- Salesforce CRM integration
- Real-time dashboard
- Advanced classification

### Performance Improvements
- 10x capacity increase (50 → 500 tickets/day)
- Semantic search (vs keyword matching)
- Async processing for emails
- Connection pooling

## Next Steps

To progress to v2 (Cognitive Enhancement):
- Add distributed memory (Redis Cluster, Mem0)
- Implement LangGraph orchestration
- Add CrewAI multi-agent coordination
- Deploy Neo4j knowledge graph
- Advanced RAG with reranking

## Documentation

- [Architecture Overview](architecture/mvp_architecture.md)
- [Database Schema](docs/database_schema.md)
- [API Reference](docs/api_reference.md)
- [Integration Guide](docs/integration_guide.md)
- [Deployment Guide](docs/deployment_guide.md)
- [User Guide](docs/user_guide.md)

## Support

For issues or questions:
- Check [Troubleshooting](#troubleshooting) section
- Review logs: `docker-compose logs -f`
- Check health: `curl http://localhost:8000/health`
- Database status: `docker-compose exec postgres pg_isready`

## License

MIT License