<template>
  <Card class="post-card shadow-lg hover:shadow-xl transition-shadow duration-300">
    <template #header>
      <div v-if="post.thumbnail_url || post.external_url" class="relative">
        <img 
          :src="post.thumbnail_url || post.external_url" 
          :alt="post.title"
          class="w-full h-48 object-cover rounded-t-lg"
          @error="handleImageError"
        />
        <div v-if="post.post_type === 'video'" class="absolute top-2 right-2 bg-black/70 text-white px-2 py-1 rounded text-xs">
          🎥 Видео
        </div>
        <div v-if="post.post_type === 'gallery'" class="absolute top-2 right-2 bg-black/70 text-white px-2 py-1 rounded text-xs">
          🖼️ Галерея
        </div>
      </div>
    </template>
    
    <template #title>
      <a :href="post.url" target="_blank" class="text-lg font-bold hover:text-primary transition-colors line-clamp-2">
        {{ post.title }}
      </a>
    </template>
    
    <template #subtitle>
      <div class="flex items-center gap-2 text-sm text-gray-500 mb-2">
        <span>r/{{ post.subreddit }}</span>
        <span>•</span>
        <span>{{ formatDate(post.posted_at) }}</span>
        <span>•</span>
        <span>u/{{ post.author }}</span>
      </div>
    </template>
    
    <template #content>
      <p v-if="post.body" class="text-gray-700 line-clamp-3 mb-3">
        {{ post.body }}
      </p>
      
      <div class="flex flex-wrap gap-2 mb-3">
        <Tag 
          v-for="tag in post.tags" 
          :key="tag.slug"
          :value="tag.name"
          :style="{ backgroundColor: tag.color, color: '#fff' }"
          class="text-xs"
        />
      </div>
      
      <div class="flex items-center gap-4 text-sm text-gray-600">
        <div class="flex items-center gap-1">
          <span>⬆️</span>
          <span class="font-semibold">{{ post.score }}</span>
        </div>
        <div class="flex items-center gap-1">
          <span>💬</span>
          <span>{{ post.comment_count }} комментариев</span>
        </div>
      </div>
    </template>
  </Card>
</template>

<script setup lang="ts">
import Card from 'primevue/card'
import Tag from 'primevue/tag'
import type { Post } from '~/composables/useUnix34Api'

const props = defineProps<{
  post: Post
}>()

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  const now = new Date()
  const diffMs = now.getTime() - date.getTime()
  const diffHours = Math.floor(diffMs / (1000 * 60 * 60))
  
  if (diffHours < 1) return 'только что'
  if (diffHours < 24) return `${diffHours} ч. назад`
  
  const diffDays = Math.floor(diffHours / 24)
  if (diffDays < 7) return `${diffDays} дн. назад`
  
  return date.toLocaleDateString('ru-RU', { day: 'numeric', month: 'short' })
}

const handleImageError = (e: Event) => {
  const target = e.target as HTMLImageElement
  target.style.display = 'none'
}
</script>

<style scoped>
.post-card {
  border-radius: 12px;
  overflow: hidden;
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>