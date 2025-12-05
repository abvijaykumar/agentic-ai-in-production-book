from crewai import Crew, Process
from agent.agents import SupportAgents
from agent.tasks import SupportTasks

class SupportCrew:
    def __init__(self):
        agents = SupportAgents()
        self.support_specialist = agents.support_specialist()
        self.technical_expert = agents.technical_expert()
        
        self.tasks = SupportTasks()

    def run(self, message: str):
        # Define the primary task
        triage_task = self.tasks.triage_and_resolve(self.support_specialist, message)

        # Create the crew
        crew = Crew(
            agents=[self.support_specialist, self.technical_expert],
            tasks=[triage_task],
            verbose=2,
            process=Process.hierarchical, # Enable delegation
            manager_llm=self.support_specialist.llm # Required for hierarchical process
        )

        result = crew.kickoff()
        return result
