from crewai import Task

class SupportTasks:
    def triage_and_resolve(self, agent, message):
        return Task(
            description=f"""Analyze the user message: "{message}"
            
            1. If it's a general question, use the Knowledge Base to answer it.
            2. If it's a complex technical issue, delegate to the Technical Expert.
            3. If it's a request for a ticket or a bug report, create a ticket.
            
            Provide a helpful, professional response to the user.""",
            agent=agent,
            expected_output="A final response to the user, answering their question or confirming ticket creation."
        )
