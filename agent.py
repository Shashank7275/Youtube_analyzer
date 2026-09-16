from agno.agent import Agent

from agno.models.google import Gemini

from agno.tools.websearch import WebSearchTools

from agno.tools.yfinance import YFinanceTools


from dotenv import load_dotenv

load_dotenv()

def build_agent():
    return Agent(
        model=Gemini(id="gemini-2.5-flash"),
        tools=[YFinanceTools() , WebSearchTools()], 
        markdown=True,
        description="You are in investment analyst that researches stock prices, analyst recommendations, and stock",
        instructions="use given tools whenever possible. Format your response using markdown and use tables disp",
        add_datetime_to_context=True,
        debug_mode=True
    )

gemini_agent = build_agent()

gemini_agent.print_response(
    "Share the MSFT stock price and analyst recommendations"
)