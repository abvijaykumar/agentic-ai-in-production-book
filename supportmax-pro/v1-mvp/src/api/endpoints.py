from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Dict, Any, Optional
from agent.crew import SupportCrew
from config.settings import settings
import uvicorn
import logging
import sys
import os

# Configure logging
log_dir = "../../../logs"
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "api_v1.log")

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
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs"
)

class ChatRequest(BaseModel):
    message: str
    user_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    action_taken: str
    metadata: Dict[str, Any] = {}

@app.get(f"{settings.API_V1_STR}/health")
async def health_check():
    return {"status": "healthy", "version": "v1.0"}

@app.post(f"{settings.API_V1_STR}/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        crew = SupportCrew()
        result = crew.run(request.message)
        
        # Heuristic to determine action taken for UI
        action_taken = "general_response"
        result_str = str(result)
        
        if "Ticket created" in result_str:
            action_taken = "create_ticket"
        elif "Found relevant information" in result_str or "knowledge base" in result_str.lower():
            action_taken = "answer_rag"
            
        return ChatResponse(
            response=result_str,
            action_taken=action_taken,
            metadata={"engine": "crewai-v1-hierarchical"}
        )
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("api.endpoints:app", host="0.0.0.0", port=8001, reload=True)
