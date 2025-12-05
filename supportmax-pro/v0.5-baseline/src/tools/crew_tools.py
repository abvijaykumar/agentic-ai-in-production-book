from langchain.tools import tool
from knowledge.faq_store import FAQStore
from tools.ticket_creator import TicketCreator

class CrewTools:
    @tool("Search FAQs")
    def search_faq(query: str):
        """Useful to answer questions about passwords, billing, support hours, etc. 
        Input should be a search query string."""
        store = FAQStore()
        results = store.search(query)
        if not results:
            return "No relevant FAQ found."
        
        # Format results for the agent
        response = "Found the following FAQs:\n"
        for faq in results:
            response += f"- Q: {faq['question']}\n  A: {faq['answer']}\n"
        return response

    @tool("Create Support Ticket")
    def create_ticket(description: str):
        """Useful to create a support ticket when the user has an issue that cannot be solved by FAQs.
        Input should be a detailed description of the issue."""
        creator = TicketCreator()
        # For simplicity in this baseline, we infer subject from description
        subject = description[:50] + "..." if len(description) > 50 else description
        result = creator.create_ticket(subject=subject, description=description)
        return f"Ticket created successfully. ID: {result['ticket_id']}"

    @tool("Check Ticket Status")
    def check_ticket_status(query: str):
        """Useful to check the status or details of a specific ticket.
        Input should be the ticket ID or a string containing the ticket ID."""
        creator = TicketCreator()
        
        # Simple extraction - assume query might contain just the ID or "ticket ID"
        # In a real app, we'd use regex or smarter extraction
        ticket_id = query.strip()
        # Clean up common prefixes if present
        if "ticket" in ticket_id.lower():
            ticket_id = ticket_id.split()[-1] # Grabs the last word hoping it's the ID
        
        ticket = creator.get_ticket(ticket_id)
        if ticket:
            return f"Ticket Details:\nID: {ticket['id']}\nStatus: {ticket['status']}\nSubject: {ticket['subject']}\nDescription: {ticket['description']}"
        else:
            return f"Ticket ID '{ticket_id}' not found. Please double check the ID."
