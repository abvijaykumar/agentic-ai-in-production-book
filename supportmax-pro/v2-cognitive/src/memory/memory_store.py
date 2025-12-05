import json
import os
from typing import Dict, List
from config.settings import settings

class MemoryStore:
    """
    Manages Short-term (Session) memory with JSON persistence.
    """
    def __init__(self):
        self.file_path = os.path.join(settings.MEMORY_STORAGE_PATH, "session_memory.json")
        self._ensure_storage()
        self.session_memory = self._load_memory()

    def _ensure_storage(self):
        if not os.path.exists(settings.MEMORY_STORAGE_PATH):
            os.makedirs(settings.MEMORY_STORAGE_PATH)
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as f:
                json.dump({}, f)

    def _load_memory(self) -> Dict[str, List[Dict[str, str]]]:
        try:
            with open(self.file_path, 'r') as f:
                return json.load(f)
        except Exception:
            return {}

    def _save_memory(self):
        with open(self.file_path, 'w') as f:
            json.dump(self.session_memory, f, indent=2)

    def add_message(self, session_id: str, role: str, content: str):
        if session_id not in self.session_memory:
            self.session_memory[session_id] = []
        self.session_memory[session_id].append({"role": role, "content": content})
        self._save_memory()

    def get_history(self, session_id: str) -> List[Dict[str, str]]:
        return self.session_memory.get(session_id, [])
    
    def get_formatted_history(self, session_id: str) -> str:
        history = self.get_history(session_id)
        if not history:
            return "No previous conversation history."
        
        formatted = ""
        for msg in history[-5:]: # Keep last 5 turns to avoid context overflow
            formatted += f"{msg['role'].capitalize()}: {msg['content']}\n"
        return formatted

    def clear_history(self, session_id: str):
        if session_id in self.session_memory:
            del self.session_memory[session_id]
            self._save_memory()
