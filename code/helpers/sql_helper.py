from supabase import create_client, Client
from config import SUPABASE_KEY

SUPABASE_URL = "https://xmizehbrdpjyffsdvuif.supabase.co"

def connect_to_supabase() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)

def get_data_by_id(table_name: str, object_id: int, columns):
    client = connect_to_supabase()
    columns_str = ", ".join(f'"{col}"' for col in columns)
    response = client.table(table_name).select(columns_str).eq("Object ID", object_id).execute()
    return response.data