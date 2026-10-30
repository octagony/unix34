export interface IPost {
  id: string
  reddit_id: string
  subreddit: string
  url: string
  title: string
  body: string | null
  author: string
  post_type: string
  flair: string | null
  score: number
  comment_count: number
  external_url: string | null
  thumbnail_url: string | null
  gallery_urls: string[]
  posted_at: string
  tags: ITag[]
}

export interface IPostsResponse {
  posts: IPost[]
  next_cursor: string | null
  has_more: boolean
}