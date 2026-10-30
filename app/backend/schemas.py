from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class TagResponse(BaseModel):
    id: int
    slug: str
    name: str
    category: str
    color: str
    is_active: bool

class PostTagResponse(BaseModel):
    slug: str
    name: str
    color: str

class PostResponse(BaseModel):
    id: str
    reddit_id: str
    subreddit: str
    url: str
    title: str
    body: Optional[str] = None
    author: str
    post_type: str
    flair: Optional[str] = None
    score: int
    comment_count: int
    external_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    gallery_urls: List[str] = []
    posted_at: datetime
    tags: List[PostTagResponse] = []

class SyncStatusResponse(BaseModel):
    id: str
    started_at: datetime
    finished_at: Optional[datetime] = None
    status: str
    posts_seen: int
    posts_created: int
    posts_updated: int
    error: Optional[str] = None

class PostsListResponse(BaseModel):
    posts: List[PostResponse]
    next_cursor: Optional[str] = None
    has_more: bool