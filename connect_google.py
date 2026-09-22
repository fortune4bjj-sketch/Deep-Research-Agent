from dotenv import load_dotenv
from composio import Composio
from composio_crewai import CrewAIProvider

load_dotenv()

USER_ID = "deep-research-agent"

composio = Composio(
    provider=CrewAIProvider()
)

session = composio.sessions.create(
    user_id=USER_ID
)

print("\nConnecting Gmail...")
gmail_auth = session.authorize("gmail")

print("\nOpen this URL in your browser:")
print(gmail_auth.redirect_url)

gmail_connection = gmail_auth.wait_for_connection()

print("\nGmail connected successfully!")
print("Connection ID:", gmail_connection.id)


print("\nConnecting Google Drive...")
drive_auth = session.authorize("googledrive")

print("\nOpen this URL in your browser:")
print(drive_auth.redirect_url)

drive_connection = drive_auth.wait_for_connection()

print("\nGoogle Drive connected successfully!")
print("Connection ID:", drive_connection.id)

print("\nGoogle connections are ready.")