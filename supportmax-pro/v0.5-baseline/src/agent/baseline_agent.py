from typing import Dict, Any
from agent.crew_agent import SupportCrew

class BaselineAgent:
    """
    Orchestrates the agent using CrewAI.
    """
    def __init__(self):
        self.crew = SupportCrew()

    def process_message(self, message: str, user_id: str = None) -> Dict[str, Any]:
        """
        Main entry point for processing a user message.
        """
        # Execute Crew
        try:
            result, steps = self.crew.run(message)
            
            # CrewAI returns a string result. We need to structure it for our API.
            # In a real app, we might parse the output or have the agent return JSON.
            # For now, we wrap the string.
            
            # Simple heuristic to determine action_taken for UI display
            action_taken = "general_response"
            if "Ticket created" in result:
                action_taken = "create_ticket"
            elif "FAQ" in result or "reset" in result.lower() or "billing" in result.lower():
                action_taken = "answer_faq"

            return {
                "text": str(result),
                "action_taken": action_taken,
                "metadata": {
                    "engine": "crewai",
                    "steps": steps
                }
            }
        except Exception as e:
            return {
                "text": f"Error processing request: {str(e)}",
                "action_taken": "error",
                "metadata": {"error": str(e)}
            }