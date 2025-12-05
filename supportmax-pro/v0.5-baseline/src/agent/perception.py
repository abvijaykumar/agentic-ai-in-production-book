from typing import Dict, Any

class Perception:
    """
    Handles input parsing and initial understanding for the agent.
    """
    def process_input(self, user_input: str) -> Dict[str, Any]:
        """
        Analyzes the user input to extract intent and entities.
        For the baseline agent, this is a simple pass-through or basic keyword extraction.
        """
        # Basic normalization
        cleaned_input = user_input.strip()
        
        # Simple heuristic for intent (in a real system, use an LLM or classifier)
        intent = "query"
        if "ticket" in cleaned_input.lower() or "support" in cleaned_input.lower():
            intent = "support_request"
            
        return {
            "raw_input": user_input,
            "cleaned_input": cleaned_input,
            "intent": intent,
            "timestamp": "now" # In real app, use actual timestamp
        }