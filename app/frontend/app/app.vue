<template>
  <div
    class="min-h-screen bg-gradient-to-br from-slate-900 to-slate-700 flex items-center justify-center p-8"
  >
    <div class="bg-white/10 backdrop-blur-lg rounded-2xl p-8 shadow-2xl max-w-md">
      <h1 class="text-4xl font-bold text-white mb-4">Unix34 <span class="text-nixos">🐧</span></h1>
      <p class="text-slate-300 mb-6">Tailwind v4 + PrimeVue работают вместе!</p>
      <div class="flex gap-2 flex-wrap mb-6">
        <span class="px-3 py-1 rounded-full text-white text-sm bg-nixos">NixOS</span>
        <span class="px-3 py-1 rounded-full text-white text-sm bg-ubuntu">Ubuntu</span>
        <span class="px-3 py-1 rounded-full text-white text-sm bg-mangowm">MangoWM</span>
      </div>
      <Button label="Кнопка PrimeVue" severity="success" class="w-full" />
    </div>
  </div>
</template>

<style scoped>
@import 'tailwindcss';

@theme {
  --color-nixos: #5277c1;
  --color-ubuntu: #e95420;
  --color-mangowm: #ff6b35;
}
</style>
