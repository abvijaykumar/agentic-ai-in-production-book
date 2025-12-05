from langchain.tools import tool
import uuid
import datetime
from typing import Dict, Any

class TicketCreator:
    """
    Simulates a ticketing system integration.
    """
    def create_ticket(self, subject: str, description: str, priority: str = "Normal") -> Dict[str, Any]:
        """
        Creates a support ticket in the system.
        """
        ticket_id = f"TICKET-{uuid.uuid4().hex[:8].upper()}"
        timestamp = datetime.datetime.now().isoformat()
        
        # In a real system, this would make an API call to Jira/Zendesk
        print(f"[System] Creating ticket: {subject} ({priority})")
        
        return {
            "ticket_id": ticket_id,
            "status": "Open",
            "subject": subject,
            "priority": priority,
            "created_at": timestamp,
            "link": f"https://support.example.com/tickets/{ticket_id}"
        }

class TicketTools:
    @tool("Create Support Ticket")
    def create_ticket(description: str):
        """Useful to create a support ticket when the user has an issue that cannot be solved by FAQs.
        Input should be a detailed description of the issue. The tool will automatically infer the subject."""
        
        creator = TicketCreator()
        # Infer subject from description (simple heuristic)
        subject = description[:50] + "..." if len(description) > 50 else description
        
        # Determine priority based on keywords
        priority = "Normal"
        if "urgent" in description.lower() or "critical" in description.lower() or "broken" in description.lower():
            priority = "High"
            
        result = creator.create_ticket(subject=subject, description=description, priority=priority)
        return f"Ticket created successfully. ID: {result['ticket_id']}. Priority: {result['priority']}"
