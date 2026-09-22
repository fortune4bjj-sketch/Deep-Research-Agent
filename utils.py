import os 
from dotenv import load_dotenv, find_dotenv

def load_env():
    _ = load_dotenv(find_dotenv())

def get_groq_api_key():
    load_dotenv() 
    return os.getenv("GROQ_API_KEY")

def get_gemini_api_key():
    load_dotenv() 
    return os.getenv("GEMINI_API_KEY")

def get_tavily_api_key():
    load_dotenv() 
    return os.getenv("TAVILY_API_KEY")

def get_composio_api_key():
    load_dotenv() 
    return os.getenv("COMPOSIO_API_KEY")

def get_exa_api_key():
    load_dotenv() 
    return os.getenv("EXA_API_KEY")

def get_openai_api_key():
    load_dotenv() 
    return os.getenv("OPENAI_API_KEY")