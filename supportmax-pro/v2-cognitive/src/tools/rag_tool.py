from langchain.tools import tool
from knowledge.vector_store import VectorStore

class RAGTool:
    @tool("Search Knowledge Base")
    def search_knowledge(query: str):
        """Useful to answer questions about product features, policies, troubleshooting, and documentation.
        Input should be a search query string."""
        
        store = VectorStore()
        results = store.search(query)
        
        if not results:
            return "No relevant information found in the knowledge base."
        
        return f"Found relevant information:\n{results}"
