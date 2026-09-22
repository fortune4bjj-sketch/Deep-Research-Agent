import os

from crewai_tools import TavilySearchTool
from dotenv import load_dotenv

from composio import Composio, SESSION_PRESET_DIRECT_TOOLS
from composio_crewai import CrewAIProvider


load_dotenv()


USER_ID = os.getenv(
    "COMPOSIO_USER_ID",
    "deep-research-agent"
)


def create_search_tools():

    search = TavilySearchTool(
        max_results=5
    )

    return [search]


def create_delivery_tools():

    composio = Composio(
        provider=CrewAIProvider()
    )

    session = composio.sessions.create(
        user_id=USER_ID,

        toolkits=[
            "gmail",
            "googledrive",
        ],

        tools={
            "gmail": {
                "enable": [
                    "GMAIL_SEND_EMAIL"
                ]
            },

            "googledrive": {
                "enable": [
                    "GOOGLEDRIVE_UPLOAD_FILE"
                ]
            },
        },

        session_preset=SESSION_PRESET_DIRECT_TOOLS,
    )

    return session.tools()