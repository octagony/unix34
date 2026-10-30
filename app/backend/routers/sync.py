from fastapi import APIRouter
from database import supabase_reader
from schemas import SyncStatusResponse

router = APIRouter(prefix="/sync", tags=["Sync"])

@router.get("status", response_model=SyncStatusResponse | None)
async def get_sync_status():
    response = supabase_reader.table("sync_runs").select("*").order("started_at", desc=True).limit(1).single().execute()
    return response.data if response.data else None