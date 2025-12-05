from typing import Dict, Any, List
import os
from knowledge.faq_store import FAQStore
from config.settings import settings

# Mock LLM for baseline if no key provided, or use actual API
class Reasoning:
    """
    Handles the core reasoning logic using LLM or heuristics.
    """
    def __init__(self, faq_store: FAQStore):
        self.faq_store = faq_store

    def decide_action(self, perception_output: Dict[str, Any]) -> Dict[str, Any]:
        """
        Decides the next action based on perception and knowledge.
        """
        user_query = perception_output["cleaned_input"]
        
        # 1. Check Knowledge Base
        faq_results = self.faq_store.search(user_query)
        
        if faq_results:
            # Found a relevant FAQ
            best_match = faq_results[0]
            return {
                "action_type": "answer_faq",
                "content": best_match["answer"],
                "confidence": 0.9,
                "source": "knowledge_base"
            }
            
        # 2. If no FAQ, check if it's a ticket request
        if perception_output["intent"] == "support_request":
             return {
                "action_type": "create_ticket",
                "content": "I can help you create a support ticket. Please provide the details.",
                "confidence": 0.8
            }

        # 3. Fallback to LLM
        # Try to use actual LLM if configured
        try:
            if settings.OPENAI_API_KEY and settings.LLM_PROVIDER == "openai":
                from openai import OpenAI
                client = OpenAI(api_key=settings.OPENAI_API_KEY)
                response = client.chat.completions.create(
                    model=settings.OPENAI_MODEL,
                    messages=[
                        {"role": "system", "content": "You are a helpful support assistant for SupportMax Pro. Answer the user's question concisely."},
                        {"role": "user", "content": user_query}
                    ],
                    max_tokens=150
                )
                return {
                    "action_type": "general_response",
                    "content": response.choices[0].message.content,
                    "confidence": 0.7,
                    "source": "llm"
                }
            elif settings.ANTHROPIC_API_KEY and settings.LLM_PROVIDER == "anthropic":
                import anthropic
                client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
                response = client.messages.create(
                    model=settings.ANTHROPIC_MODEL,
                    max_tokens=150,
                    messages=[
                        {"role": "user", "content": user_query}
                    ]
                )
                return {
                    "action_type": "general_response",
                    "content": response.content[0].text,
                    "confidence": 0.7,
                    "source": "llm"
                }
        except Exception as e:
            print(f"LLM Error: {e}")

        # Default fallback if no LLM or error
        return {
            "action_type": "general_response",
            "content": "I'm not sure about that. Would you like to create a support ticket?",
            "confidence": 0.5
        }