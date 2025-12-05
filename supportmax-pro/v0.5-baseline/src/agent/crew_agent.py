import os
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from tools.crew_tools import CrewTools
from config.settings import settings

class SupportCrew:
    def __init__(self):
        # Initialize LLM
        # CrewAI uses LangChain LLMs. We need to configure it based on settings.
        # For v0.5 baseline, we default to OpenAI if key is present, otherwise we might fail or need a mock.
        
        self.llm = None
        if settings.OPENAI_API_KEY:
            self.llm = ChatOpenAI(
                model=settings.OPENAI_MODEL,
                api_key=settings.OPENAI_API_KEY,
                temperature=0
            )
        # Note: Anthropic support in CrewAI/LangChain requires different setup, 
        # keeping it simple for OpenAI first as per typical CrewAI usage.

    def run(self, message: str):
        if not self.llm:
            return "Error: LLM not configured. Please set OPENAI_API_KEY.", []

        steps = []
        
        def step_callback(step_output):
            # Capture the step output
            # step_output is usually a tuple or object representing the thought/action
            # We convert to string for display safety
            steps.append(str(step_output))

        # Define Agent
        support_agent = Agent(
            role='Senior Support Representative',
            goal='Resolve user queries efficiently using FAQs or by creating tickets.',
            backstory="""You are an expert support agent for SupportMax Pro. 
            You are helpful, concise, and professional. 
            You always check the FAQ first. If the answer is there, you provide it.
            If the user has a problem that requires a ticket (like "create ticket", "broken", "error"), you create one.
            If you can't help, you politely say so.""",
            verbose=True,
            allow_delegation=False,
            tools=[CrewTools.search_faq, CrewTools.create_ticket, CrewTools.check_ticket_status],
            llm=self.llm,
            step_callback=step_callback
        )

        # Define Task
        task = Task(
            description=f"""Analyze the following user message: "{message}"
            
            1. If it's a question, use the 'Search FAQs' tool to find an answer.
            2. If it's a request to create a ticket or report a bug/issue, use the 'Create Support Ticket' tool.
            3. If the user asks about an existing ticket (status, details), use 'Check Ticket Status'.
            4. If it's general chit-chat, respond politely.
            
            Provide the final answer to the user.""",
            agent=support_agent,
            expected_output="A helpful response to the user, either answering their question, providing ticket details, or confirming ticket creation."
        )

        # Define Crew
        crew = Crew(
            agents=[support_agent],
            tasks=[task],
            verbose=2,
            process=Process.sequential
        )

        # Execute
        result = crew.kickoff()
        return result, steps
