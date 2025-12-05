from crewai import Agent
from langchain_openai import ChatOpenAI
from config.settings import settings
from tools.rag_tool import RAGTool
from tools.ticket_creator import TicketTools

class SupportAgents:
    def __init__(self):
        self.llm = ChatOpenAI(
            model=settings.OPENAI_MODEL,
            api_key=settings.OPENAI_API_KEY,
            temperature=0
        )

    def support_specialist(self):
        return Agent(
            role='Senior Support Specialist',
            goal='Resolve general user queries and triage complex issues.',
            backstory="""You are the first line of defense for SupportMax Pro. 
            You answer general questions using the Knowledge Base. 
            If a query is technical or requires deep troubleshooting, you delegate it to the Technical Expert.
            If the user explicitly asks for a ticket or reports a bug you can't solve, you create a ticket.""",
            tools=[RAGTool.search_knowledge, TicketTools.create_ticket],
            llm=self.llm,
            verbose=True,
            allow_delegation=True
        )

    def technical_expert(self):
        return Agent(
            role='Technical Support Expert',
            goal='Analyze and resolve complex technical issues.',
            backstory="""You are a deep technical expert. 
            You handle complex queries that the Support Specialist cannot resolve.
            You use the Knowledge Base to find detailed technical documentation.
            If you cannot resolve the issue, you advise creating a high-priority ticket.""",
            tools=[RAGTool.search_knowledge, TicketTools.create_ticket],
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )
