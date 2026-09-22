from crewai import Crew, Process

from src.agents import create_agents
from src.tasks import create_tasks


def create_crew():

    researcher, analyst, writer = create_agents()

    tasks = create_tasks(
        researcher,
        analyst,
        writer,
    )

    return Crew(
        agents=[
            researcher,
            analyst,
            writer,
        ],
        tasks=tasks,
        process=Process.sequential,
        verbose=True,
    )