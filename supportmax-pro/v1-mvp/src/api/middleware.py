import time
import logging
import re
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from config.constraints import MAX_RESPONSE_TIME_SECONDS

logger = logging.getLogger(__name__)

class SLAMonitorMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        
        # Log SLA warning if threshold exceeded
        if process_time > MAX_RESPONSE_TIME_SECONDS:
            logger.warning(
                f"SLA VIOLATION: Request processed in {process_time:.2f}s "
                f"(Limit: {MAX_RESPONSE_TIME_SECONDS}s)"
            )
        
        response.headers["X-Process-Time"] = str(process_time)
        return response

class PIIRedactionMiddleware(BaseHTTPMiddleware):
    """
    Middleware to redact PII from logs.
    Note: Real PII redaction should happen before logging contents. 
    This middleware intercepts the response body for logging purposes if needed,
    but standard logging often happens in the route handler. 
    For this 'book code' example, we'll assume this middleware 
    is a placeholder for deeper integration or intercepts request logging.
    """
    async def dispatch(self, request: Request, call_next):
        # In a real app, we'd wrap the request body to redact PII before logging
        # Here we just pass through, but provide the utility function standard.
        return await call_next(request)

def redact_pii(text: str) -> str:
    """
    Simple PII redaction for emails and phone numbers.
    """
    # Email regex
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    text = re.sub(email_pattern, '[EMAIL_REDACTED]', text)
    
    # Simple phone regex (US style)
    phone_pattern = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
    text = re.sub(phone_pattern, '[PHONE_REDACTED]', text)
    
    return text
