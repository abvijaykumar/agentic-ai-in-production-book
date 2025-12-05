from typing import Dict, Optional, List
import uuid
import json
import os
from datetime import datetime

class TicketCreator:
    """
    Tool for creating and managing support tickets with JSON persistence.
    """
    def __init__(self):
        self.data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")
        self.tickets_file = os.path.join(self.data_dir, "tickets.json")
        os.makedirs(self.data_dir, exist_ok=True)
        
    def _load_tickets(self) -> List[Dict]:
        if not os.path.exists(self.tickets_file):
            return []
        try:
            with open(self.tickets_file, 'r') as f:
                return json.load(f)
        except:
            return []
            
    def _save_tickets(self, tickets: List[Dict]):
        with open(self.tickets_file, 'w') as f:
            json.dump(tickets, f, indent=2)

    def create_ticket(self, subject: str, description: str, priority: str = "Normal", email: Optional[str] = None) -> Dict:
        """
        Creates a new support ticket and saves it to JSON.
        """
        ticket_id = str(uuid.uuid4())[:8]
        ticket = {
            "id": ticket_id,
            "subject": subject,
            "description": description,
            "priority": priority,
            "status": "Open",
            "created_at": datetime.now().isoformat(),
            "contact_email": email
        }
        
        # Save to JSON
        tickets = self._load_tickets()
        tickets.append(ticket)
        self._save_tickets(tickets)
        
        print(f"Ticket created: {ticket}")
        
        return {
            "success": True,
            "ticket_id": ticket_id,
            "message": f"Ticket #{ticket_id} has been created. We will contact you shortly."
        }
        
    def get_ticket(self, ticket_id: str) -> Optional[Dict]:
        """
        Retrieves a ticket by ID.
        """
        tickets = self._load_tickets()
        for ticket in tickets:
            if ticket["id"] == ticket_id:
                return ticket
        return None