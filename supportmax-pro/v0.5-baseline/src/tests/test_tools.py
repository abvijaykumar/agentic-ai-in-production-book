import pytest
from tools.ticket_creator import TicketCreator

def test_ticket_creation():
    creator = TicketCreator()
    result = creator.create_ticket(
        subject="Test Issue",
        description="This is a test ticket",
        email="test@example.com"
    )
    
    assert result["success"] is True
    assert "ticket_id" in result
    assert len(result["ticket_id"]) > 0
