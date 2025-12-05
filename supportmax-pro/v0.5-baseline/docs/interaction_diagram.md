# v0.5 Baseline Agent Interaction Diagram

This diagram illustrates the request/response flow for the SupportMax Pro v0.5 Baseline Agent, incorporating the CrewAI integration.

```mermaid
sequenceDiagram
    actor User
    participant UI as Streamlit Frontend
    participant API as FastAPI Backend
    participant BaseAgent as BaselineAgent
    participant Crew as SupportCrew (CrewAI)
    participant LLM as LLM (OpenAI)
    participant Tools as CrewTools

    User->>UI: Types message ("How do I reset my password?")
    UI->>API: POST /api/v1/chat (message)
    API->>BaseAgent: process_message(message)
    BaseAgent->>Crew: run(message)
    
    rect rgb(240, 248, 255)
        note right of Crew: CrewAI Execution Loop
        Crew->>LLM: Analyze intent & choose tool
        LLM-->>Crew: Action: Search FAQs
        Crew->>Tools: search_faq("reset password")
        Tools-->>Crew: Found: "Go to login page..."
        Crew->>LLM: Synthesize final answer
        LLM-->>Crew: "To reset your password..."
    end

    Crew-->>BaseAgent: Final Answer String
    BaseAgent-->>API: JSON Response (text, action_taken)
    API-->>UI: JSON Response
    UI->>User: Displays Agent Response
```

## Component Roles

1.  **Streamlit Frontend**: Captures user input and displays chat history.
2.  **FastAPI Backend**: Exposes the agent logic via a REST API.
3.  **BaselineAgent**: Wrapper class that maintains the API interface and orchestrates the Crew.
4.  **SupportCrew**: The CrewAI container that defines the Agent, Task, and Process.
5.  **LLM**: The brain (OpenAI GPT-4) that decides which tool to use.
6.  **CrewTools**: Wrappers for the `FAQStore` and `TicketCreator` to make them compatible with CrewAI.
