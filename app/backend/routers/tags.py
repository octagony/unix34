from fastapi import APIRouter
from database import supabase_reader
from schemas import TagResponse

router = APIRouter(prefix="/tags", tags=["Tags"])

@router.get("/", response_model=list[TagResponse])
async def get_tags(category: str | None = None):
    query = supabase_reader.table("tags").select("*").order("name")
    
    if category:
        query = query.eq("category", category)
        
    response = query.execute()
    return response.data or []