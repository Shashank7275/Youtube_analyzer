from agno.agent import Agent

from agno.models.google import Gemini

from agno.team import Team

from dotenv import load_dotenv
load_dotenv()



eng_agent = Agent(name="English Agent", role="You answer questions in English")
chi_agent = Agent(name="Chinese Agent", role="You answer questions in Chinese")
hindi_agent = Agent(name="Hindi Agent", role="You answer questions in Hindi")




team_leader = Team(
    name = "Answer and Translation Team",
    members=[eng_agent, chi_agent, hindi_agent],
    model=Gemini(id="gemini-2.5-flash"),
    markdown=True,
    show_members_responses=True,
    instructions="""All members agents must response to answer the query in their specific lang.
                    Do not route to just one agent.
                    Output the respone to all agent
    
    
                """

)

team_leader.print_response(
    "what is the captial of india?"
)