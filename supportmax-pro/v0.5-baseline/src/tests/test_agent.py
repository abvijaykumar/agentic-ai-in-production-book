import pytest
from agent.baseline_agent import BaselineAgent
from knowledge.faq_store import FAQStore

def test_faq_store_search():
    store = FAQStore()
    # Assuming sample_faqs.json is loaded or we mock it
    # For unit test, we might want to mock, but for simplicity in this baseline:
    results = store.search("password")
    assert isinstance(results, list)
    # If sample data is loaded
    if results:
        assert "password" in results[0]['question'].lower() or "password" in results[0]['answer'].lower()

def test_agent_initialization():
    agent = BaselineAgent()
    assert agent.perception is not None
    assert agent.reasoning is not None
    assert agent.action is not None

def test_agent_process_message_faq():
    agent = BaselineAgent()
    response = agent.process_message("How do I reset my password?")
    assert response["action_taken"] == "answer_faq"
    assert "reset your password" in response["text"]

def test_agent_process_message_ticket():
    agent = BaselineAgent()
    response = agent.process_message("I need to create a support ticket")
    assert response["action_taken"] == "create_ticket"
