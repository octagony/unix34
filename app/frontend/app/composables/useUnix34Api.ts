
export const useUnix34Api = () => {
  const config = useRuntimeConfig()
  const baseUrl = config.public.apiBaseUrl || 'http://localhost:8000'

  const getPosts = async (
  tags: string[] = [],
  cursor: string | null = null,
  limit: number = 24
): Promise<IPostsResponse> => {
  const params = new URLSearchParams()
  
  if (tags.length > 0) {
    tags.forEach(tag => params.append('tags', tag))
  }
  
  if (cursor) {
    params.append('cursor', cursor)
  }
  
  params.append('limit', limit.toString())

  const url = `${baseUrl}/api/posts?${params.toString()}`

  try {
    const response = await fetch(url)
    
    if (!response.ok) {
      throw new Error(`Failed to fetch posts: ${response.statusText}`)
    }

    const data = await response.json()
    return data
  } catch (error) {
    console.error('Fetch error:', error)
    throw error
  }
}

  const getPost = async (redditId: string): Promise<IPost> => {
    const response = await fetch(`${baseUrl}/api/posts${redditId}`)
    
    if (!response.ok) {
      throw new Error(`Failed to fetch post: ${response.statusText}`)
    }

    return response.json()
  }

  const getTags = async (category?: string): Promise<ITag[]> => {
    const params = category ? `?category=${category}` : ''
    const response = await fetch(`${baseUrl}/api/tags${params}`)
    
    if (!response.ok) {
      throw new Error(`Failed to fetch tags: ${response.statusText}`)
    }

    return response.json()
  }

  const getSyncStatus = async (): Promise<SyncStatus | null> => {
    const response = await fetch(`${baseUrl}/api/sync/status`)
    
    if (!response.ok) {
      return null
    }

    return response.json()
  }

  return {
    getPosts,
    getPost,
    getTags,
    getSyncStatus
  }
}