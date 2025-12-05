"""
Production Constraints Definition for v1 MVP.
These constraints are enforced to ensure the agent meets production standards.
"""

# Latency Constraints (in seconds)
MAX_RESPONSE_TIME_SECONDS = 2.0

# Cost Constraints
MAX_TOKENS_PER_QUERY = 1000
MAX_DAILY_COST_USD = 5.0

# Reliability Constraints
MAX_RETRIES = 3
TIMEOUT_SECONDS = 5.0

# Knowledge Constraints
MIN_CONFIDENCE_SCORE = 0.7
MAX_FAQ_RESULTS = 3
