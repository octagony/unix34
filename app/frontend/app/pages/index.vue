<template>
  <div class="min-h-screen">
    <!-- Header -->
    <AppHeader/>

    <div class="container mx-auto px-4 py-8">
      <!-- Filters -->
            <!-- Filters -->
      <div class="bg-white rounded-lg shadow-sm p-6 mb-8">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-lg font-semibold">Фильтры по тегам</h2>
          <Button 
            v-if="selectedTags.length > 0"
            label="Сбросить фильтры"
            severity="secondary"
            text
            size="small"
            icon="pi pi-times"
            @click="clearFilters"
          />
        </div>
        
        <div class="flex flex-wrap gap-2">
          <Button
            v-for="tag in allTags"
            :key="tag.slug"
            :label="tag.name"
            :severity="selectedTags.includes(tag.slug) ? 'primary' : 'secondary'"
            :outlined="!selectedTags.includes(tag.slug)"
            size="small"
            @click="toggleTag(tag.slug)"
          />
        </div>
        
        <div v-if="selectedTags.length > 0" class="mt-4 text-sm text-gray-600">
          Активные фильтры: 
          <span v-for="tag in selectedTags" :key="tag" class="font-semibold text-primary">
            {{ tag }}{{ tag !== selectedTags[selectedTags.length - 1] ? ', ' : '' }}
          </span>
        </div>
      </div>

      <div v-if="loading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div v-for="i in 6" :key="i" class="bg-white rounded-lg shadow-sm p-6 animate-pulse">
          <div class="h-48 bg-gray-200 rounded mb-4"></div>
          <div class="h-6 bg-gray-200 rounded mb-2"></div>
          <div class="h-4 bg-gray-200 rounded w-2/3"></div>
        </div>
      </div>

      <div v-else-if="posts.length === 0" class="text-center py-12">
        <p class="text-gray-500 text-lg">Посты не найдены</p>
        <p class="text-gray-400 text-sm mt-2">Попробуйте изменить фильтры</p>
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <PostCard v-for="post in posts" :key="post.id" :post="post" />
      </div>

      <!-- Load More Button -->
      <div v-if="hasMore && !loading" class="text-center mt-8">
        <Button
          label="Загрузить ещё"
          icon="pi pi-refresh"
          :loading="loadingMore"
          @click="loadMore"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import Button from 'primevue/button'
import PostCard from '~/components/PostCard.vue'
import { useUnix34Api, type Post, type Tag } from '~/composables/useUnix34Api'

const api = useUnix34Api()

const allTags = ref<Tag[]>([])
const posts = ref<Post[]>([])
const selectedTags = ref<string[]>([])
const nextCursor = ref<string | null>(null)
const hasMore = ref(false)
const loading = ref(true)
const loadingMore = ref(false)

// ✅ ИСПРАВЛЕННАЯ ФУНКЦИЯ: создаем новый массив вместо мутации старого
const toggleTag = (slug: string) => {
  if (selectedTags.value.includes(slug)) {
    // Убираем тег, создавая новый массив
    selectedTags.value = selectedTags.value.filter(t => t !== slug)
  } else {
    // Добавляем тег, создавая новый массив
    selectedTags.value = [...selectedTags.value, slug]
  }
}

// Функция сброса всех фильтров
const clearFilters = () => {
  selectedTags.value = []
}

const loadPosts = async (append: boolean = false) => {
  if (!append) {
    loading.value = true
    posts.value = []
    nextCursor.value = null
  } else {
    loadingMore.value = true
  }

  try {
    const response = await api.getPosts(
      selectedTags.value,
      nextCursor.value,
      24
    )
    
    if (append) {
      posts.value.push(...response.posts)
    } else {
      posts.value = response.posts
    }
    
    nextCursor.value = response.next_cursor
    hasMore.value = response.has_more
  } catch (error) {
    console.error('Failed to load posts:', error)
  } finally {
    loading.value = false
    loadingMore.value = false
  }
}

const loadMore = () => {
  loadPosts(true)
}

onMounted(async () => {
  try {
    allTags.value = await api.getTags()
    await loadPosts()
  } catch (error) {
    console.error('Failed to initialize:', error)
  }
})

// ✅ ИСПРАВЛЕННЫЙ WATCH: добавлен { deep: true } для гарантированного срабатывания
watch(selectedTags, () => {
  loadPosts()
}, { deep: true })
</script>