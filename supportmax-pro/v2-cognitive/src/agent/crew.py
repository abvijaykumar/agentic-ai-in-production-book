from crewai import Crew, Process
from agent.agents import SupportAgents
from agent.tasks import SupportTasks

class SupportCrew:
    def __init__(self):
        agents = SupportAgents()
        self.support_specialist = agents.support_specialist()
        self.technical_expert = agents.technical_expert()
        self.qa_specialist = agents.quality_assurance()
        
        self.tasks = SupportTasks()

    def run(self, message: str, user_id: str = "default_user", chat_history: str = ""):
        # Define tasks
        triage_task = self.tasks.triage_and_resolve(self.support_specialist, message)
        review_task = self.tasks.quality_review(self.qa_specialist, [triage_task])

        # Create the crew with Memory enabled
        crew = Crew(
            agents=[self.support_specialist, self.technical_expert, self.qa_specialist],
            tasks=[triage_task, review_task],
            verbose=2,
            process=Process.hierarchical, # Enable delegation
            manager_llm=self.support_specialist.llm,
            memory=True, # Enable Global Memory
            embedder={
                "provider": "openai",
                "config": {
                    "model": "text-embedding-3-small"
                }
            }
        )

        # Pass inputs for memory context
        inputs = {
            "message": message,
            "user_id": user_id,
            "chat_history": chat_history
        }
        
        result = crew.kickoff(inputs=inputs)
        return result
