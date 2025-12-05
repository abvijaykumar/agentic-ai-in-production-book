# v1 MVP Agent Interaction Diagram

This diagram illustrates the multi-agent flow in SupportMax Pro v1.0, featuring RAG and hierarchical delegation.

```mermaid
sequenceDiagram
    actor User
    participant UI as Streamlit (v1)
    participant API as FastAPI (v1)
    participant Crew as SupportCrew
    participant Specialist as Support Specialist
    participant Expert as Technical Expert
    participant RAG as RAGTool (ChromaDB)
    participant Ticket as TicketTool

    User->>UI: "I'm getting a 500 error on /chat"
    UI->>API: POST /api/v1/chat
    API->>Crew: run(message)
    
    rect rgb(240, 248, 255)
        note right of Crew: Hierarchical Process
        Crew->>Specialist: Triage Task
        Specialist->>RAG: search("500 error /chat")
        RAG-->>Specialist: Found: "Check logs, payload size..."
        
        opt Complex Issue
            Specialist->>Expert: Delegate: Analyze technical details
            Expert->>RAG: search("stack trace 500")
            RAG-->>Expert: Found: "Stack trace examples..."
            Expert-->>Specialist: Technical Analysis
        end
        
        Specialist->>User: Final Response
    end

    Crew-->>API: Result String
    API-->>UI: JSON Response
    UI->>User: Display Response
```

## Key Components
1.  **Support Specialist**: Front-line agent. Uses RAG for general queries. Delegates complex issues.
2.  **Technical Expert**: Specialist agent for deep dives.
3.  **RAGTool**: Retrieves context from ChromaDB (ingested docs).
4.  **Hierarchical Process**: Allows agents to delegate tasks dynamically.
