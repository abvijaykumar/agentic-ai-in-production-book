import sys
import os
import uvicorn

# Add 'src' to sys.path to resolve 'agent' imports
# This must happen BEFORE importing from agent or config
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi import FastAPI, HTTPException, BackgroundTasks, Request
from pydantic import BaseModel
from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Dict, Any, Optional
from agent.baseline_agent import BaselineAgent
from config.settings import settings
import logging
import sys
import os
import uvicorn

# Configure logging
log_dir = "../../../logs"
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "api_v0.5.log")

logging.basicConfig(
    level=settings.LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Initialize agent
agent = BaselineAgent()

class ChatRequest(BaseModel):
    message: str
    user_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    action_taken: str
    metadata: Dict[str, Any]

@app.get("/")
async def root():
    return {"message": "SupportMax Pro v0.5 Baseline Agent is running"}

@app.post(f"{settings.API_V1_STR}/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Main chat endpoint.
    """
    try:
        result = agent.process_message(request.message, request.user_id)
        
        return ChatResponse(
            response=result["text"],
            action_taken=result["action_taken"],
            metadata=result.get("metadata", {})
        )
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get(f"{settings.API_V1_STR}/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)