from fastapi import FastAPI, HTTPException
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
log_file = os.path.join(log_dir, "api_v2.log")

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
    return {"status": "healthy", "version": "v2.0-cognitive"}

from memory.memory_store import MemoryStore

# Initialize Memory Store
memory_store = MemoryStore()

@app.post(f"{settings.API_V1_STR}/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        user_id = request.user_id if request.user_id else "default_user"
        
        # Get history
        chat_history = memory_store.get_formatted_history(user_id)
        
        # Run Crew
        crew = SupportCrew()
        result = crew.run(request.message, user_id=user_id, chat_history=chat_history)
        
        result_str = str(result)
        
        # Save interaction to memory
        memory_store.add_message(user_id, "user", request.message)
        memory_store.add_message(user_id, "assistant", result_str)
        
        # Heuristic for action taken
        action_taken = "general_response"
        if "Ticket created" in result_str:
            action_taken = "create_ticket"
        elif "Found relevant information" in result_str:
            action_taken = "answer_rag"
            
        return ChatResponse(
            response=result_str,
            action_taken=action_taken,
            metadata={
                "engine": "crewai-v2-cognitive",
                "memory_enabled": True,
                "reflection_enabled": True,
                "history_length": len(memory_store.get_history(user_id))
            }
        )
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("api.endpoints:app", host="0.0.0.0", port=8002, reload=True)
