from dotenv import load_dotenv
import os

load_dotenv()  # Loads from .env by default

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
DIFY_API_KEY = os.getenv("DIFY_API_KEY")