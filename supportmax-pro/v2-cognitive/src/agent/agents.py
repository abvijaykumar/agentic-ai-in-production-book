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
            allow_delegation=True,
            memory=True # Enable CrewAI Memory
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
            allow_delegation=False,
            memory=True # Enable CrewAI Memory
        )

    def quality_assurance(self):
        return Agent(
            role='Quality Assurance Specialist',
            goal='Ensure all responses are accurate, professional, and helpful.',
            backstory="""You review the final response from the Support Team.
            You check for:
            1. Accuracy (does it answer the user's question?)
            2. Tone (is it polite and professional?)
            3. Completeness (did we miss anything?)
            If the response is good, you approve it. If not, you provide feedback for improvement.""",
            llm=self.llm,
            verbose=True,
            allow_delegation=False,
            memory=True
        )
