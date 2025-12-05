import json
import os
from typing import List, Dict, Optional
from config.constraints import MAX_FAQ_RESULTS, MIN_CONFIDENCE_SCORE

class FAQStore:
    """
    Simple in-memory FAQ store for the baseline agent.
    """
    def __init__(self, faq_file_path: str = "src/v0.5-baseline/src/knowledge/sample_faqs.json"):
        self.faqs = self._load_faqs(faq_file_path)

    def _load_faqs(self, file_path: str) -> List[Dict]:
        """Loads FAQs from a JSON file."""
        try:
            # Adjust path if running from root or src/chapter1
            if not os.path.exists(file_path):
                # Try relative path if absolute/project-relative fails
                # Fallback to looking relative to this file
                file_path = os.path.join(os.path.dirname(__file__), "sample_faqs.json")
            
            with open(file_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: FAQ file not found at {file_path}. Starting with empty knowledge base.")
            return []

    def search(self, query: str) -> List[Dict]:
        """
        Basic keyword search for FAQs.
        In a real system, this would use vector embeddings.
        """
        query = query.lower()
        results = []
        
        for faq in self.faqs:
            # Simple keyword matching
            if query in faq['question'].lower() or query in faq['answer'].lower():
                results.append(faq)
                
        return results[:MAX_FAQ_RESULTS]

    def get_faq_by_id(self, faq_id: str) -> Optional[Dict]:
        """Retrieve a specific FAQ by ID."""
        for faq in self.faqs:
            if faq['id'] == faq_id:
                return faq
        return None