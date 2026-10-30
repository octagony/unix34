from fastapi import APIRouter, Query, HTTPException
from typing import List, Optional
from database import supabase_reader
from schemas import PostResponse, PostsListResponse, PostTagResponse

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.get("/", response_model=PostsListResponse)
async def get_posts(
    tags: List[str] = Query(default=[]),
    cursor: Optional[str] = Query(default=None),
    limit: int = Query(default=24, ge=1, le=100)
):
    query = supabase_reader.table("posts").select("""
        id,
        reddit_id,
        subreddit,
        url,
        title,
        body,
        author,
        post_type,
        flair,
        score,
        comment_count,
        external_url,
        thumbnail_url,
        gallery_urls,
        posted_at,
        post_tags!inner (
            tags (
                slug,
                name,
                color
            )
        )
    """).order("posted_at", desc=True).order("id", desc=True).limit(limit)

    if cursor:
        try:
            posted_at_str, post_id = cursor.split(",")
            query = query.lt("posted_at", posted_at_str)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid cursor format")

    response = query.execute()
    
    if not response.data:
        return PostsListResponse(posts=[], has_more=False, next_cursor=None)

    formatted_posts = []
    for post in response.data:
        raw_tags = post.pop("post_tags", [])
        post["tags"] = [
            PostTagResponse(
                slug=pt["tags"]["slug"],
                name=pt["tags"]["name"],
                color=pt["tags"]["color"]
            )
            for pt in raw_tags if pt.get("tags")
        ]
        formatted_posts.append(PostResponse(**post))

    if tags:
        filtered_posts = []
        for post in formatted_posts:
            post_tag_slugs = [tag.slug for tag in post.tags]
            if any(t in post_tag_slugs for t in tags):
                filtered_posts.append(post)
        formatted_posts = filtered_posts

    has_more = len(formatted_posts) == limit
    next_cursor = None
    if has_more and formatted_posts:
        last_post = formatted_posts[-1]
        next_cursor = f"{last_post.posted_at.isoformat()},{last_post.id}"

    return PostsListResponse(
        posts=formatted_posts,
        has_more=has_more,
        next_cursor=next_cursor
    )

@router.get("/{reddit_id}", response_model=PostResponse)
async def get_post(reddit_id: str):
    response = supabase_reader.table("posts").select("""
        id, 
        reddit_id, 
        subreddit, 
        url, 
        title, 
        body, 
        author, 
        post_type, 
        flair,
        score, 
        comment_count, 
        external_url, 
        thumbnail_url, 
        gallery_urls, 
        posted_at,
        post_tags!inner ( tags ( slug, name, color ) )
    """).eq("reddit_id", reddit_id).single().execute()

    if not response.data:
        raise HTTPException(status_code=404, detail="Post not found")

    post = response.data
    raw_tags = post.pop("post_tags", [])
    post["tags"] = [
        PostTagResponse(slug=pt["tags"]["slug"], name=pt["tags"]["name"], color=pt["tags"]["color"])
        for pt in raw_tags if pt.get("tags")
    ]
    
    return PostResponse(**post)