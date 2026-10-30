from supabase import create_client, Client
from config import settings


def get_supabase_client(*, use_service_role: bool = False) -> Client:
    key = settings.supabase_service_role_key if use_service_role else settings.supabase_anon_key
    return create_client(settings.supabase_url, key)

supabase_writer: Client = get_supabase_client(use_service_role=True)

supabase_reader: Client = get_supabase_client(use_service_role=False)