<script setup lang="ts">
import { useColorMode } from '@vueuse/core';
import {
  ThemeToggler,
  type ThemeSelection,
} from '@animate-ui/vue/primitives/effects/theme-toggler';

const { store, system, } = useColorMode();

const getThemeIcon = computed(() => {
  return store.value === 'dark' ? 'i-lucide-sun' : 'i-lucide-moon'
});
</script>

<template>
  <ThemeToggler :theme="store as ThemeSelection"
    :resolved-theme="system === 'dark' || store === 'dark' ? 'dark' : 'light'"
    :set-theme="(theme) => (store = theme === 'system' ? 'auto' : theme)" :direction="'btt'"
    
    >
    <template #default="{ effective, toggleTheme }">
      <button @click="toggleTheme(effective === 'dark' ? 'light' : 'dark')" class="cursor-pointer hover:bg-accented transition-all">
        <UIcon :name=getThemeIcon class="size-5" />
      </button>
    </template>
  </ThemeToggler>
</template>