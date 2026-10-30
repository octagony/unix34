export interface SyncStatus {
  id: string
  started_at: string
  finished_at: string | null
  status: string
  posts_seen: number
  posts_created: number
  posts_updated: number
  error: string | null
}