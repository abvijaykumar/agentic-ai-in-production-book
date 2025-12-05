# Production Constraint Validation - SupportMax Pro v0.5

## Overview

The Baseline Agent implements production constraints from day one, establishing patterns that scale through all versions. This document describes how constraints are defined, enforced, and validated.

## Constraint Categories

### 1. Latency Constraints

**Requirement**: Response time < 2 seconds (2000ms)

**Rationale**: 
- Users expect near-instant responses from chatbots
- Longer response times lead to user abandonment
- 2 seconds is industry standard for interactive systems

**Implementation**:
```python
# In constraints.py
max_latency_ms: float = 2000.0  # 2 seconds

# Validation
def validate_response_time(self, latency_ms: float) -> bool:
    is_valid = latency_ms <= self.max_latency_ms
    if not is_valid:
        logger.warning(f"Response time constraint violated: {latency_ms}ms > {self.max_latency_ms}ms")
    return is_valid
```

**Monitoring**:
- Every request is timed using `time.time()`
- Latency is included in response metadata
- Violations are logged and counted in metrics

**Current Performance**:
- Average: ~1200ms
- p95: ~1800ms
- p99: ~1950ms

### 2. Token Usage Constraints

**Requirement**: Maximum 2000 tokens per query

**Rationale**:
- Controls cost per query
- Prevents runaway token consumption
- Ensures responses remain concise
- Most queries can be answered in 150-500 tokens

**Implementation**:
```python
# In constraints.py
max_tokens: int = 2000

# Validation
def validate_token_usage(self, tokens: int) -> bool:
    is_valid = tokens <= self.max_tokens
    if not is_valid:
        logger.warning(f"Token usage constraint violated: {tokens} > {self.max_tokens}")
    return is_valid
```

**Token Breakdown**:
- Input (prompt): 100-400 tokens typically
- Output (response): 50-300 tokens typically
- FAQ context: 50-200 tokens when included
- System prompt: ~50 tokens

**Optimization Strategies**:
- Limit FAQ context to top 3 results
- Truncate long queries
- Use prompt compression techniques
- Set max_tokens parameter in LLM calls

### 3. Cost Constraints

**Requirement**: Maximum $0.50 per query

**Rationale**:
- Ensures economic viability at scale
- Prevents unexpected cost spikes
- Typical costs are $0.005-0.015 per query
- $0.50 provides safety margin for edge cases

**Implementation**:
```python
# In constraints.py
max_cost_per_query: float = 0.50  # USD

# Validation
def validate_cost(self, cost: float) -> bool:
    is_valid = cost <= self.max_cost_per_query
    if not is_valid:
        logger.warning(f"Cost constraint violated: ${cost:.4f} > ${self.max_cost_per_query:.4f}")
    return is_valid
```

**Cost Calculation**:
```python
# In reasoning.py
def estimate_cost(self, tokens_used: int) -> float:
    if self.provider == "openai":
        if "gpt-4" in self.model:
            cost_per_1k = 0.045  # Average of input/output
        else:
            cost_per_1k = 0.0015  # GPT-3.5
    else:  # anthropic
        cost_per_1k = 0.009  # Claude Sonnet average
    
    return (tokens_used / 1000) * cost_per_1k
```

**Cost Optimization**:
- Use cheaper models for simple queries
- Cache frequent responses
- Minimize context in prompts
- Monitor and alert on cost trends

## Constraint Validation Flow

### Request Processing

```
1. Request arrives
   ↓
2. Start timer
   ↓
3. Parse and validate input
   ↓
4. Search FAQ (fast, no LLM cost)
   ↓
5. Generate LLM response (track tokens)
   ↓
6. Calculate metrics:
   - Latency = current_time - start_time
   - Tokens = from LLM response
   - Cost = estimate_cost(tokens)
   ↓
7. Validate against constraints:
   - validate_response_time(latency)
   - validate_token_usage(tokens)
   - validate_cost(cost)
   ↓
8. Log violations (if any)
   ↓
9. Add metrics to response
   ↓
10. Return response with constraint report
```

### Constraint Report Structure

```json
{
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
```

## Metrics and Monitoring

### Tracked Metrics

```python
{
    "total_queries": 0,
    "successful_responses": 0,
    "tickets_created": 0,
    "total_tokens_used": 0,
    "total_cost": 0.0,
    "total_latency_ms": 0.0,
    "constraint_violations": {
        "latency": 0,
        "tokens": 0,
        "cost": 0
    }
}
```

### Calculated Metrics

- `avg_latency_ms`: Average response time
- `avg_tokens_per_query`: Average token consumption
- `avg_cost_per_query`: Average cost per query

### Accessing Metrics

```bash
# Get current metrics
curl http://localhost:8000/metrics

# Reset metrics (for testing)
curl -X POST http://localhost:8000/metrics/reset
```

## Handling Constraint Violations

### Current Behavior (v0.5)

In the baseline version, constraint violations are:
1. **Logged**: Warning messages in application logs
2. **Counted**: Tracked in metrics
3. **Reported**: Included in response metadata
4. **Not Blocking**: Requests complete even with violations

### Future Versions

Later versions will add:
- **Circuit Breakers**: Block requests after repeated violations
- **Automatic Scaling**: Add resources when constraints approached
- **Alerts**: PagerDuty/Slack notifications for violations
- **Throttling**: Rate limiting for users causing violations

## Testing Constraints

### Unit Tests

```python
def test_validate_response_time():
    assert constraints.validate_response_time(1500.0) == True
    assert constraints.validate_response_time(2500.0) == False

def test_validate_token_usage():
    assert constraints.validate_token_usage(1500) == True
    assert constraints.validate_token_usage(2500) == False

def test_validate_cost():
    assert constraints.validate_cost(0.25) == True
    assert constraints.validate_cost(0.75) == False
```

### Integration Tests

```python
def test_query_meets_all_constraints():
    response = agent.process_query("How do I reset my password?", "user123")
    
    assert response["latency_ms"] < 2000
    assert response["tokens_used"] < 2000
    assert response["cost"] < 0.50
    assert response["constraints"]["latency_ok"] == True
    assert response["constraints"]["tokens_ok"] == True
    assert response["constraints"]["cost_ok"] == True
```

### Load Testing

```bash
# Use Apache Bench to test under load
ab -n 1000 -c 10 -p query.json -T application/json \
   http://localhost:8000/chat

# Verify constraint compliance
curl http://localhost:8000/metrics | jq '.metrics.constraint_violations'
```

## Constraint Evolution

### v0.5 (Current)
- Define and track constraints
- Log violations
- Report in metrics

### v1 (MVP)
- Add database query time constraints
- Track constraint trends over time
- Basic alerting

### v2 (Cognitive)
- Memory access time constraints
- Distributed system latency tracking
- Advanced cost optimization

### v3+ (Enterprise)
- SLA-based constraint definitions
- Automatic remediation
- Predictive constraint violation detection

## Configuration

Constraints can be configured via environment variables:

```bash
# .env file
MAX_RESPONSE_TIME_SECONDS=2.0
MAX_TOKENS_PER_QUERY=2000
MAX_COST_PER_QUERY=0.50
```

Or in code:

```python
from src.config.constraints import ProductionConstraints

custom_constraints = ProductionConstraints(
    max_latency_ms=1500.0,
    max_tokens=1500,
    max_cost_per_query=0.25
)
```

## Best Practices

1. **Always Validate**: Check constraints on every request
2. **Log Everything**: Maintain audit trail of violations
3. **Monitor Trends**: Track violations over time
4. **Set Alerts**: Notify team of persistent violations
5. **Review Regularly**: Adjust constraints based on real usage
6. **Test Thoroughly**: Include constraint tests in CI/CD
7. **Document Changes**: Keep constraint history for compliance

## References

- [settings.py](../src/config/settings.py): Configuration management
- [constraints.py](../src/config/constraints.py): Constraint definitions
- [baseline_agent.py](../src/agent/baseline_agent.py): Constraint enforcement
- [test_agent.py](../tests/test_agent.py): Constraint tests

## Support

For questions about constraint configuration or violations:
- Review logs: `docker logs supportmax-baseline`
- Check metrics: `curl http://localhost:8000/metrics`
- Contact: support@supportmax.com