"""Tests for tools module."""
import pytest
from src.tools.ticket_creator import TicketCreator
from src.knowledge.faq_store import FAQStore


class TestTicketCreator:
    """Test cases for TicketCreator."""
    
    @pytest.fixture
    def ticket_creator(self):
        """Create ticket creator instance."""
        return TicketCreator()
    
    def test_create_ticket(self, ticket_creator):
        """Test ticket creation."""
        ticket = ticket_creator.create_ticket(
            query="I need help with my account",
            user_id="user123",
            category="account",
            priority="normal"
        )
        
        assert ticket is not None
        assert ticket["id"].startswith("TKT-")
        assert ticket["query"] == "I need help with my account"
        assert ticket["user_id"] == "user123"
        assert ticket["category"] == "account"
        assert ticket["priority"] == "normal"
        assert ticket["status"] == "open"
        assert "created_at" in ticket
        assert "updated_at" in ticket
    
    def test_create_ticket_with_metadata(self, ticket_creator):
        """Test ticket creation with metadata."""
        metadata = {"source": "api", "ip": "192.168.1.1"}
        ticket = ticket_creator.create_ticket(
            query="Test query",
            user_id="user123",
            metadata=metadata
        )
        
        assert ticket["metadata"] == metadata
    
    def test_get_ticket(self, ticket_creator):
        """Test retrieving a ticket."""
        created = ticket_creator.create_ticket(
            query="Test query",
            user_id="user123"
        )
        
        retrieved = ticket_creator.get_ticket(created["id"])
        assert retrieved is not None
        assert retrieved["id"] == created["id"]
    
    def test_get_nonexistent_ticket(self, ticket_creator):
        """Test retrieving non-existent ticket."""
        ticket = ticket_creator.get_ticket("TKT-INVALID")
        assert ticket is None
    
    def test_update_ticket(self, ticket_creator):
        """Test updating a ticket."""
        ticket = ticket_creator.create_ticket(
            query="Test query",
            user_id="user123"
        )
        
        updated = ticket_creator.update_ticket(
            ticket["id"],
            {"status": "closed", "resolution": "Solved"}
        )
        
        assert updated is not None
        assert updated["status"] == "closed"
        assert updated["resolution"] == "Solved"
    
    def test_get_all_tickets(self, ticket_creator):
        """Test retrieving all tickets."""
        ticket_creator.create_ticket("Query 1", "user1")
        ticket_creator.create_ticket("Query 2", "user2")
        
        all_tickets = ticket_creator.get_all_tickets()
        assert len(all_tickets) == 2
    
    def test_get_tickets_by_user(self, ticket_creator):
        """Test retrieving tickets by user."""
        ticket_creator.create_ticket("Query 1", "user1")
        ticket_creator.create_ticket("Query 2", "user1")
        ticket_creator.create_ticket("Query 3", "user2")
        
        user1_tickets = ticket_creator.get_tickets_by_user("user1")
        assert len(user1_tickets) == 2
        
        user2_tickets = ticket_creator.get_tickets_by_user("user2")
        assert len(user2_tickets) == 1
    
    def test_get_tickets_by_status(self, ticket_creator):
        """Test retrieving tickets by status."""
        ticket1 = ticket_creator.create_ticket("Query 1", "user1")
        ticket2 = ticket_creator.create_ticket("Query 2", "user2")
        
        # Update one ticket status
        ticket_creator.update_ticket(ticket1["id"], {"status": "closed"})
        
        open_tickets = ticket_creator.get_tickets_by_status("open")
        assert len(open_tickets) == 1
        
        closed_tickets = ticket_creator.get_tickets_by_status("closed")
        assert len(closed_tickets) == 1
    
    def test_count_tickets(self, ticket_creator):
        """Test counting tickets."""
        assert ticket_creator.count_tickets() == 0
        
        ticket_creator.create_ticket("Query 1", "user1")
        assert ticket_creator.count_tickets() == 1
        
        ticket_creator.create_ticket("Query 2", "user2")
        assert ticket_creator.count_tickets() == 2
    
    def test_get_stats(self, ticket_creator):
        """Test getting ticket statistics."""
        ticket_creator.create_ticket("Query 1", "user1", category="billing", priority="high")
        ticket_creator.create_ticket("Query 2", "user2", category="account", priority="normal")
        ticket_creator.create_ticket("Query 3", "user3", category="billing", priority="urgent")
        
        stats = ticket_creator.get_stats()
        
        assert stats["total_tickets"] == 3
        assert stats["by_category"]["billing"] == 2
        assert stats["by_category"]["account"] == 1
        assert stats["by_priority"]["high"] == 1
        assert stats["by_priority"]["normal"] == 1
        assert stats["by_priority"]["urgent"] == 1
        assert stats["by_status"]["open"] == 3


class TestFAQStore:
    """Test cases for FAQStore."""
    
    @pytest.fixture
    def faq_store(self):
        """Create FAQ store instance."""
        return FAQStore()
    
    def test_faq_store_initialization(self, faq_store):
        """Test FAQ store initializes with data."""
        assert faq_store.size() > 0
    
    def test_search_relevant_faq(self, faq_store):
        """Test searching for relevant FAQ."""
        results = faq_store.search("password reset", top_k=3)
        
        assert len(results) > 0
        assert results[0]["relevance_score"] > 0
        assert "password" in results[0]["question"].lower() or "password" in results[0]["answer"].lower()
    
    def test_search_with_top_k(self, faq_store):
        """Test search respects top_k parameter."""
        results = faq_store.search("billing payment", top_k=2)
        assert len(results) <= 2
    
    def test_search_no_results(self, faq_store):
        """Test search with no matching results."""
        results = faq_store.search("xyzabc123nonexistent", top_k=3)
        assert len(results) == 0
    
    def test_get_by_id(self, faq_store):
        """Test retrieving FAQ by ID."""
        all_faqs = faq_store.get_all()
        if len(all_faqs) > 0:
            first_faq = all_faqs[0]
            retrieved = faq_store.get_by_id(first_faq["id"])
            assert retrieved is not None
            assert retrieved["id"] == first_faq["id"]
    
    def test_get_by_id_nonexistent(self, faq_store):
        """Test retrieving non-existent FAQ."""
        faq = faq_store.get_by_id("nonexistent_id")
        assert faq is None
    
    def test_get_all(self, faq_store):
        """Test retrieving all FAQs."""
        all_faqs = faq_store.get_all()
        assert len(all_faqs) == faq_store.size()
    
    def test_get_categories(self, faq_store):
        """Test retrieving categories."""
        categories = faq_store.get_categories()
        assert len(categories) > 0
        assert isinstance(categories, list)
    
    def test_get_by_category(self, faq_store):
        """Test retrieving FAQs by category."""
        categories = faq_store.get_categories()
        if len(categories) > 0:
            category = categories[0]
            faqs = faq_store.get_by_category(category)
            assert len(faqs) > 0
            for faq in faqs:
                assert faq["category"] == category
    
    def test_relevance_calculation(self, faq_store):
        """Test relevance score calculation."""
        # Search for password - should have high relevance for password FAQ
        results = faq_store.search("password", top_k=5)
        
        if len(results) > 0:
            # First result should be most relevant
            assert results[0]["relevance_score"] > 0
            
            # Results should be sorted by relevance
            if len(results) > 1:
                assert results[0]["relevance_score"] >= results[1]["relevance_score"]