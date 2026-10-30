import logging
from typing import Dict, Any, List
from datetime import datetime, timezone

from database import supabase_writer
from classifiers.tag_rules import classify_post

logger = logging.getLogger(__name__)


def normalize_reddrix_post(item: Dict[str, Any]) -> Dict[str, Any] | None:
    raw_id = item.get("id") or item.get("submissionId") or item.get("post_id")
    reddit_id = str(raw_id).strip()
    
    if not reddit_id or reddit_id.lower() == "none":
        return None
        
    reddit_fullname = item.get("fullname") or f"t3_{reddit_id}"
    subreddit = item.get("subreddit", "unknown").lower()

    permalink = item.get("permalink")
    if permalink and str(permalink).startswith("/r/"):
        post_url = f"https://www.reddit.com{permalink}"
    else:
        post_url = f"https://www.reddit.com/r/{subreddit}/comments/{reddit_id}/"

    post_type = "text"
    external_url = None
    thumbnail_url = item.get("thumbnailUrl") or item.get("previewUrl")
    gallery_urls = []

    if item.get("isImage"):
        post_type = "image"
        external_url = item.get("url")
    elif item.get("isVideo"):
        post_type = "video"
        external_url = item.get("videoUrl") or item.get("url")
    elif item.get("isGallery"):
        post_type = "gallery"
        gallery_urls = item.get("galleryUrls", [])
        external_url = gallery_urls[0] if gallery_urls else None
    elif item.get("isLink"):
        post_type = "link"
        external_url = item.get("externalUrl") or item.get("url")

    posted_at_raw = item.get("postedAt") or item.get("created_utc")
    if isinstance(posted_at_raw, (int, float)):
        posted_at = datetime.fromtimestamp(posted_at_raw, tz=timezone.utc).isoformat()
    else:
        posted_at = posted_at_raw or datetime.now(timezone.utc).isoformat()

    return {
        "reddit_id": reddit_id,
        "reddit_fullname": reddit_fullname,
        "subreddit": subreddit,
        "url": post_url,
        "title": item.get("title", "Без заголовка"),
        "body": item.get("bodyText") or item.get("selftext"),
        "author": item.get("author") or "[deleted]",
        "post_type": post_type,
        "flair": item.get("postFlair") or item.get("flair"),
        "score": item.get("score") or item.get("upvotes", 0),
        "upvote_ratio": item.get("upvoteRatio"),
        "comment_count": item.get("commentCount") or item.get("num_comments", 0),
        "external_url": external_url,
        "thumbnail_url": thumbnail_url,
        "gallery_urls": gallery_urls,
        "posted_at": posted_at,
        "raw_payload": item,
    }

def upsert_post(normalized_post: Dict[str, Any]) -> Dict[str, str]:
    try:
        reddit_id = normalized_post["reddit_id"]
        if not reddit_id:
            return {"status": "skipped", "reason": "no_reddit_id"}

        tags = classify_post(
            title=normalized_post["title"],
            body=normalized_post["body"] or "",
            flair=normalized_post["flair"] or ""
        )

        post_response = supabase_writer.table("posts").upsert(
            normalized_post,
            on_conflict="reddit_id"
        ).execute()

        status = "updated" 
        
        supabase_writer.table("post_tags").delete().eq("post_id", post_response.data[0]["id"]).eq("source", "rules").execute()

        if tags:
            tags_response = supabase_writer.table("tags").select("id, slug").in_("slug", tags).execute()
            
            post_tags_to_insert = [
                {
                    "post_id": post_response.data[0]["id"],
                    "tag_id": tag_row["id"],
                    "source": "rules"
                }
                for tag_row in tags_response.data
            ]
            
            if post_tags_to_insert:
                supabase_writer.table("post_tags").insert(post_tags_to_insert).execute()

        return {"status": "success", "tags_found": tags}

    except Exception as e:
        logger.error(f"Upsert Error {normalized_post.get('reddit_id')}: {e}")
        return {"status": "error", "error": str(e)}