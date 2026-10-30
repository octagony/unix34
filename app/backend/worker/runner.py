import logging
from datetime import datetime, timezone
from typing import Dict, Any

from reddrix import Reddrix
from config import settings
from database import supabase_writer
from services.post_service import normalize_reddrix_post, upsert_post

logger = logging.getLogger(__name__)


async def run_sync() -> Dict[str, Any]:
    sync_run = supabase_writer.table("sync_runs").insert({
        "started_at": datetime.now(timezone.utc).isoformat(),
        "status": "running"
    }).execute()
    
    sync_run_id = sync_run.data[0]["id"]
    posts_seen = 0
    posts_created = 0
    errors = []
    
    try:
        async with Reddrix(
            mode=settings.reddrix_mode,
            subreddit_urls=settings.subreddit_urls,
            sort=settings.reddrix_sort,
            include_comments=settings.reddrix_include_comments,
            max_posts_per_collection=settings.reddrix_max_posts,
            max_results=settings.reddrix_max_posts,
            stealth=settings.reddrix_stealth,
        ) as reddrix:
            async for item in reddrix.get_items():
                posts_seen += 1
                
                if item.get("submissionType") != "post":
                    logger.debug(f"⏭️ Пропуск (тип: {item.get('submissionType')}): {item.get('title', 'No title')[:30]}")
                    continue
                
                try:
                    normalized = normalize_reddrix_post(item)
                    
                    if normalized is None:
                        continue
                    
                    result = upsert_post(normalized)
                    
                    if result["status"] == "success":
                        posts_created += 1
                        logger.info(f"Saved: '{normalized['title'][:40]}...' | Теги: {result['tags_found']}")
                    else:
                        logger.warning(f"NOT SAVED {normalized.get('reddit_id')}: {result.get('reason') or result.get('error')}")
                        
                except Exception as e:
                    err_msg = f"{item.get('id')}: {e}"
                    errors.append(err_msg)
        
        status = "success" if not errors else "partial_success"
        finished_at = datetime.now(timezone.utc).isoformat()
        
        supabase_writer.table("sync_runs").update({
            "finished_at": finished_at,
            "status": status,
            "posts_seen": posts_seen,
            "posts_created": posts_created,
            "posts_updated": 0,
            "error": "\n".join(errors) if errors else None
        }).eq("id", sync_run_id).execute()
        
        logger.info(f"SYNC FINISHED: SEEN={posts_seen}, SAVED={posts_created}, ERRORs={len(errors)}")
        
        return {"status": status, "posts_seen": posts_seen, "posts_created": posts_created}
    
    except Exception as e:
        error_msg = str(e)
        logger.error(f"{error_msg}")
        
        supabase_writer.table("sync_runs").update({
            "finished_at": datetime.now(timezone.utc).isoformat(),
            "status": "failed",
            "error": error_msg
        }).eq("id", sync_run_id).execute()
        
        return {"status": "failed", "error": error_msg}