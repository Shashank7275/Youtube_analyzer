from agno.agent import Agent
from agno.models.google import Gemini
from agno.db.sqlite import SqliteDb
from rich.pretty import pprint
from dotenv import load_dotenv

load_dotenv()

db = SqliteDb(db_file="agno.db")

db.clear_memories()


def build_agent():
    return Agent(
        model=Gemini(id="gemini-2.5-flash"),
        db=db,
        markdown=True,
        add_history_to_context=True,
        enable_user_memories=True
    )


user_id = "rahul@gmail.com"

agent = build_agent()

agent.print_response(
    "I am Rahul and I am an AI engineer.",
    user_id=user_id
)

agent.print_response(
    "Who am I?",
    user_id=user_id
)

memories = agent.get_user_memories(
    user_id=user_id
)

print("MEMORIES:")
pprint(memories)