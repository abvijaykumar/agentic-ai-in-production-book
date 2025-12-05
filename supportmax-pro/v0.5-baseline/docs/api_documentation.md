# API Documentation - SupportMax Pro v0.5 Baseline Agent

## Overview

The Baseline Agent API provides endpoints for processing customer support queries with AI-powered responses and automatic ticket creation.

**Base URL**: `http://localhost:8000`

**API Documentation**: `http://localhost:8000/docs` (Interactive Swagger UI)

## Authentication

Currently, the baseline version does not require authentication. Future versions will implement API key authentication.

## Endpoints

### POST /chat

Process a user query and return an AI-generated response.

**Request Body**:
```json
{
  "query": "How do I reset my password?",
  "user_id": "user123"
}
```

**Parameters**:
- `query` (string, required): User's question or issue description (1-1000 characters)
- `user_id` (string, required): Unique user identifier

**Response** (200 OK):
```json
{
  "response": "To reset your password:\n1. Go to the login page\n2. Click 'Forgot Password'...",
  "source": "faq",
  "ticket_created": false,
  "ticket_id": null,
  "faq_references": [
    {
      "id": "faq_001",
      "question": "How do I reset my password?",
      "relevance": 15.0
    }
  ],
  "latency_ms": 1234.56,
  "tokens_used": 150,
  "cost": 0.0068,
  "model": "gpt-4",
  "provider": "openai",
  "constraints": {
    "latency_ok": true,
    "tokens_ok": true,
    "cost_ok": true,
    "metrics": {
      "latency_ms": 1234.56,
      "tokens_used": 150,
      "cost": 0.0068
    },
    "constraints": {
      "max_latency_ms": 2000.0,
      "max_tokens": 2000,
      "max_cost_per_query": 0.5
    }
  }
}
```

**Response Fields**:
- `response` (string): AI-generated answer to the user's query
- `source` (string): Source of the response (`faq`, `llm`, `greeting`, `error`)
- `ticket_created` (boolean): Whether a support ticket was created
- `ticket_id` (string, optional): ID of created ticket if applicable
- `faq_references` (array, optional): List of FAQ entries used to generate the response
- `latency_ms` (number): Response time in milliseconds
- `tokens_used` (number): Number of LLM tokens consumed
- `cost` (number): Estimated cost in USD
- `model` (string): LLM model used
- `provider` (string): LLM provider used
- `constraints` (object): Production constraint validation results

**Error Responses**:

400 Bad Request:
```json
{
  "detail": "Query cannot be empty"
}
```

500 Internal Server Error:
```json
{
  "detail": "An error occurred processing your request"
}
```

**Example**:
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": "How do I reset my password?",
    "user_id": "user123"
  }'
```

---

### GET /health

Health check endpoint returning system status and basic metrics.

**Response** (200 OK):
```json
{
  "status": "healthy",
  "version": "0.5.0",
  "faq_count": 10,
  "metrics": {
    "total_queries": 42,
    "successful_responses": 40,
    "tickets_created": 5,
    "avg_latency_ms": 1156.23
  }
}
```

**Response Fields**:
- `status` (string): Health status (`healthy` or `unhealthy`)
- `version` (string): Application version
- `faq_count` (number): Number of FAQs in knowledge base
- `metrics` (object): Basic system metrics

**Example**:
```bash
curl http://localhost:8000/health
```

---

### GET /metrics

Retrieve detailed system metrics and statistics.

**Response** (200 OK):
```json
{
  "metrics": {
    "total_queries": 100,
    "successful_responses": 95,
    "tickets_created": 12,
    "total_tokens_used": 15000,
    "total_cost": 0.675,
    "total_latency_ms": 123456.78,
    "avg_latency_ms": 1299.55,
    "avg_tokens_per_query": 157.89,
    "avg_cost_per_query": 0.0071,
    "constraint_violations": {
      "latency": 3,
      "tokens": 1,
      "cost": 0
    },
    "ticket_stats": {
      "total_tickets": 12,
      "by_status": {
        "open": 10,
        "closed": 2
      },
      "by_category": {
        "billing": 5,
        "account": 4,
        "technical": 2,
        "general": 1
      },
      "by_priority": {
        "urgent": 2,
        "high": 3,
        "normal": 7
      }
    },
    "faq_count": 10
  }
}
```

**Response Fields**:
- `total_queries` (number): Total queries processed
- `successful_responses` (number): Successfully processed queries
- `tickets_created` (number): Total tickets created
- `total_tokens_used` (number): Cumulative token usage
- `total_cost` (number): Cumulative cost in USD
- `avg_latency_ms` (number): Average response time
- `avg_tokens_per_query` (number): Average tokens per query
- `avg_cost_per_query` (number): Average cost per query
- `constraint_violations` (object): Count of constraint violations
- `ticket_stats` (object): Detailed ticket statistics
- `faq_count` (number): Number of FAQs available

**Example**:
```bash
curl http://localhost:8000/metrics
```

---

### POST /metrics/reset

Reset all collected metrics (useful for testing).

**Response** (200 OK):
```json
{
  "message": "Metrics reset successfully"
}
```

**Example**:
```bash
curl -X POST http://localhost:8000/metrics/reset
```

---

### GET /

Root endpoint providing API information.

**Response** (200 OK):
```json
{
  "name": "SupportMax Pro Baseline",
  "version": "0.5.0",
  "description": "Baseline Agent API for SupportMax Pro",
  "endpoints": {
    "chat": "/chat",
    "health": "/health",
    "metrics": "/metrics",
    "docs": "/docs"
  }
}
```

**Example**:
```bash
curl http://localhost:8000/
```

---

## Rate Limiting

The baseline version does not implement rate limiting. Future versions will include configurable rate limits.

## Production Constraints

The system enforces these production constraints:

- **Maximum Latency**: 2000ms (2 seconds)
- **Maximum Tokens**: 2000 tokens per query
- **Maximum Cost**: $0.50 per query

Violations are tracked in metrics but do not block requests in the baseline version.

## Error Handling

All endpoints return appropriate HTTP status codes:

- `200 OK`: Successful request
- `400 Bad Request`: Invalid input
- `500 Internal Server Error`: Server-side error

Error responses include a `detail` field with the error message.

## Interactive Documentation

Visit `http://localhost:8000/docs` for interactive Swagger UI documentation where you can test all endpoints directly in your browser.

## Examples

### Complete Query Flow

```bash
# 1. Check health
curl http://localhost:8000/health

# 2. Process a query
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are your business hours?",
    "user_id": "user456"
  }'

# 3. Check metrics
curl http://localhost:8000/metrics
```

### Python Client Example

```python
import httpx

# Process a query
response = httpx.post(
    "http://localhost:8000/chat",
    json={
        "query": "How do I update my billing information?",
        "user_id": "user789"
    }
)

result = response.json()
print(f"Response: {result['response']}")
print(f"Latency: {result['latency_ms']}ms")
print(f"Cost: ${result['cost']:.4f}")
```

## Next Steps

For more advanced features, see:
- v1 (MVP System): Multi-turn conversations, persistent storage
- v2 (Cognitive Enhancement): Memory management, orchestration
- v3+ (Enterprise): Platform integrations, production operations