from crewai import Task

class SupportTasks:
    def triage_and_resolve(self, agent, message):
        return Task(
            description=f"""Analyze the user message: "{message}"
            
            Current Conversation Context:
            {{chat_history}}
            
            1. CHECK THE CONTEXT FIRST. If the user is asking about something mentioned previously (like their name), use the context to answer.
            2. If it's a general question, use the Knowledge Base to answer it.
            3. If it's a complex technical issue, delegate to the Technical Expert.
            4. ONLY create a ticket if the user EXPLICITLY asks for one, or if the issue is clearly a bug that cannot be resolved with documentation. Do NOT create tickets for general questions or if you can find the answer in the context.
            
            Provide a helpful, professional response to the user.""",
            agent=agent,
            expected_output="A draft response to the user."
        )

    def quality_review(self, agent, context):
        return Task(
            description="""Review the draft response provided by the Support Team.
            Ensure it meets our quality standards (Accurate, Professional, Complete).
            If it's good, output the final response.
            If it needs improvement, refine it.""",
            agent=agent,
            context=context, # Context from previous task
            expected_output="The final, polished response to the user."
        )
