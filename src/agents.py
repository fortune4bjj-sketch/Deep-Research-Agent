from crewai import Agent
from src.tools import create_search_tools, create_delivery_tools


MODEL = "openai/gpt-4o-mini"


def create_agents():

    researcher = Agent(
        role="Market Research Analyst",
        goal=(
            "Find the latest accurate information about {topic}. "
            "Gather at least five key data points and identify "
            "the source type for each finding."
        ),
        backstory=(
            "You are a senior market research analyst with more than "
            "10 years of experience in technology markets, industry trends, "
            "competitor analysis, and emerging technologies."
        ),
        llm=MODEL,
        tools=create_search_tools(),
        verbose=True,
        allow_delegation=False,
    )

    analyst = Agent(
        role="Industry Analyst",
        goal=(
            "Analyze the research about {topic}. "
            "Identify the top 3 opportunities, "
            "2 major challenges, and 1 actionable recommendation."
        ),
        backstory=(
            "You are an expert industry analyst experienced in evaluating "
            "emerging technology markets, business opportunities, risks, "
            "competitive trends, and strategic implications."
        ),
        llm=MODEL,
        tools=[],
        verbose=True,
        allow_delegation=False,
    )

    writer = Agent(
        role="Professional Report Writer",
        goal=(
            "Write a professional Markdown report about {topic} using "
            "the research and analysis provided. "
            "Do not send, upload, or deliver the report."
        ),
        backstory=(
            "You are an executive-level professional report writer. "
            "You transform research and analysis into concise, clear, "
            "well-structured reports for decision-makers."
        ),
        llm=MODEL,

        # IMPORTANT:
        # Writer cannot send email or upload files.
        tools=[],

        verbose=True,
        allow_delegation=False,
    )

    return researcher, analyst, writer


def create_delivery_agent():

    # This function is called ONLY after human approval.
    delivery_tools = create_delivery_tools()

    delivery_agent = Agent(
        role="Approved Report Delivery Specialist",
        goal=(
            "Deliver the already-approved final report using only "
            "the delivery method explicitly selected by the human operator."
        ),
        backstory=(
            "You are responsible only for delivering reports that have "
            "already received explicit human approval. "
            "You never modify the report or select recipients yourself."
        ),
        llm=MODEL,
        tools=delivery_tools,
        verbose=True,
        allow_delegation=False,
    )

    return delivery_agent