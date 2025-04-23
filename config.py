import os
import streamlit as st

def get_keys():
    # On Streamlit Cloud, use st.secrets
    if "SUPABASE_KEY" in st.secrets:
        return {
            "OPENAI_API_KEY": st.secrets.get("OPENAI_API_KEY"),
            "SUPABASE_KEY": st.secrets.get("SUPABASE_KEY"),
            "DIFY_API_KEY": st.secrets.get("DIFY_API_KEY"),
        }
    else:
        # Locally, use .env
        from dotenv import load_dotenv
        load_dotenv()
        return {
            "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
            "SUPABASE_KEY": os.getenv("SUPABASE_KEY"),
            "DIFY_API_KEY": os.getenv("DIFY_API_KEY"),
        }

# Usage
keys = get_keys()
OPENAI_API_KEY = keys["OPENAI_API_KEY"]
SUPABASE_KEY = keys["SUPABASE_KEY"]
DIFY_API_KEY = keys["DIFY_API_KEY"]