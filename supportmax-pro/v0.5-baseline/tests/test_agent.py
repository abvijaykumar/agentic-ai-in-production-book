"""Tests for baseline agent."""
import pytest
from unittest.mock import Mock, patch
from src.agent.baseline_agent import BaselineAgent


class TestBaselineAgent:
    """Test cases for BaselineAgent."""
    
    @pytest.fixture
    def agent(self):
        """Create agent instance for testing."""
        with patch('src.agent.reasoning.openai'):
            with patch('src.agent.reasoning.anthropic'):
                agent = BaselineAgent(llm_provider="openai")
                return agent
    
    def test_agent_initialization(self, agent):
        """Test agent initializes correctly."""
        assert agent is not None
        assert agent.perception is not None
        assert agent.reasoning is not None
        assert agent.action is not None
        assert agent.faq_store is not None
        assert agent.ticket_creator is not None
    
    def test_metrics_initialization(self, agent):
        """Test metrics are initialized correctly."""
        metrics = agent.get_metrics()
        assert metrics["total_queries"] == 0
        assert metrics["successful_responses"] == 0
        assert metrics["tickets_created"] == 0
        assert metrics["total_tokens_used"] == 0
        assert metrics["total_cost"] == 0.0
    
    @patch('src.agent.reasoning.Reasoning.generate_response')
    def test_process_greeting(self, mock_generate, agent):
        """Test processing greeting query."""
        response = agent.process_query("Hello", "user123")
        
        assert response is not None
        assert response["source"] == "greeting"
        assert response["ticket_created"] is False
        assert "Hello" in response["response"] or "help" in response["response"]
    
    @patch('src.agent.reasoning.Reasoning.generate_response')
    def test_process_valid_query(self, mock_generate, agent):
        """Test processing valid query."""
        mock_generate.return_value = {
            "response": "Here's how to reset your password...",
            "tokens_used": 150,
            "model": "gpt-4",
            "provider": "openai"
        }
        
        response = agent.process_query(
            "How do I reset my password?",
            "user123"
        )
        
        assert response is not None
        assert "response" in response
        assert response["tokens_used"] > 0
        assert "latency_ms" in response
        assert "cost" in response
    
    def test_process_invalid_query_empty(self, agent):
        """Test processing empty query."""
        response = agent.process_query("", "user123")
        
        assert response is not None
        assert response["source"] == "error"
        assert "error" in response
    
    def test_process_invalid_query_too_long(self, agent):
        """Test processing query that's too long."""
        long_query = "a" * 1001
        response = agent.process_query(long_query, "user123")
        
        assert response is not None
        assert response["source"] == "error"
    
    def test_metrics_tracking(self, agent):
        """Test metrics are tracked correctly."""
        initial_metrics = agent.get_metrics()
        initial_queries = initial_metrics["total_queries"]
        
        # Process a greeting (doesn't use LLM)
        agent.process_query("Hello", "user123")
        
        updated_metrics = agent.get_metrics()
        assert updated_metrics["total_queries"] == initial_queries + 1
    
    def test_reset_metrics(self, agent):
        """Test metrics reset."""
        # Process a query to generate metrics
        agent.process_query("Hello", "user123")
        
        # Reset metrics
        agent.reset_metrics()
        
        metrics = agent.get_metrics()
        assert metrics["total_queries"] == 0
        assert metrics["successful_responses"] == 0
    
    def test_determine_category_billing(self, agent):
        """Test category determination for billing."""
        parsed_input = {
            "intent_signals": {
                "mentions_billing": True,
                "mentions_account": False,
                "mentions_technical": False
            }
        }
        category = agent._determine_category(parsed_input)
        assert category == "billing"
    
    def test_determine_category_account(self, agent):
        """Test category determination for account."""
        parsed_input = {
            "intent_signals": {
                "mentions_billing": False,
                "mentions_account": True,
                "mentions_technical": False
            }
        }
        category = agent._determine_category(parsed_input)
        assert category == "account"
    
    def test_determine_priority_urgent(self, agent):
        """Test priority determination for urgent."""
        parsed_input = {
            "cleaned_query": "urgent need help asap",
            "intent_signals": {
                "is_complaint": False
            }
        }
        priority = agent._determine_priority(parsed_input)
        assert priority == "urgent"
    
    def test_determine_priority_normal(self, agent):
        """Test priority determination for normal."""
        parsed_input = {
            "cleaned_query": "how do I reset password",
            "intent_signals": {
                "is_complaint": False
            }
        }
        priority = agent._determine_priority(parsed_input)
        assert priority == "normal"


class TestPerception:
    """Test cases for Perception."""
    
    @pytest.fixture
    def perception(self):
        """Create perception instance."""
        from src.agent.perception import Perception
        return Perception()
    
    def test_parse_input(self, perception):
        """Test input parsing."""
        result = perception.parse_input("  How  do I reset password?  ", "user123")
        
        assert result["original_query"] == "  How  do I reset password?  "
        assert result["cleaned_query"] == "How do I reset password?"
        assert result["user_id"] == "user123"
        assert result["word_count"] == 5
    
    def test_intent_signals_question(self, perception):
        """Test question detection."""
        result = perception.parse_input("How do I reset password?", "user123")
        assert result["intent_signals"]["is_question"] is True
    
    def test_intent_signals_greeting(self, perception):
        """Test greeting detection."""
        result = perception.parse_input("Hello, how are you?", "user123")
        assert result["intent_signals"]["is_greeting"] is True
    
    def test_validate_input_valid(self, perception):
        """Test input validation for valid input."""
        parsed = perception.parse_input("How do I reset password?", "user123")
        is_valid, error = perception.validate_input(parsed)
        assert is_valid is True
        assert error == ""
    
    def test_validate_input_empty(self, perception):
        """Test input validation for empty input."""
        parsed = perception.parse_input("", "user123")
        is_valid, error = perception.validate_input(parsed)
        assert is_valid is False
        assert "empty" in error.lower()


class TestAction:
    """Test cases for Action."""
    
    @pytest.fixture
    def action(self):
        """Create action instance."""
        from src.agent.action import Action
        return Action()
    
    def test_format_response_basic(self, action):
        """Test basic response formatting."""
        response = action.format_response(
            llm_response="Here's how to reset your password...",
            source="llm"
        )
        
        assert response["response"] == "Here's how to reset your password..."
        assert response["source"] == "llm"
        assert response["ticket_created"] is False
    
    def test_format_response_with_ticket(self, action):
        """Test response formatting with ticket."""
        response = action.format_response(
            llm_response="I'll help you with that.",
            source="llm",
            ticket_created=True,
            ticket_id="TKT-12345678"
        )
        
        assert response["ticket_created"] is True
        assert response["ticket_id"] == "TKT-12345678"
        assert "TKT-12345678" in response["response"]
    
    def test_generate_greeting_response(self, action):
        """Test greeting response generation."""
        response = action.generate_greeting_response()
        assert "hello" in response.lower() or "hi" in response.lower()
        assert "help" in response.lower()
    
    def test_generate_no_answer_response(self, action):
        """Test no answer response generation."""
        response = action.generate_no_answer_response()
        assert "apologize" in response.lower() or "sorry" in response.lower()
        assert "ticket" in response.lower()
    
    def test_generate_error_response(self, action):
        """Test error response generation."""
        response = action.generate_error_response("timeout")
        assert "sorry" in response.lower() or "apologize" in response.lower()