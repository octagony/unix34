<script setup lang="ts">
</script>

<template>
	<UHeader>
		<template #title>
			<Logo class="h-6 w-auto" />
		</template>

		<template #right>
			<div class="flex gap-2 items-baseline">
				<AppThemeSwitcher />
				<UTooltip text="Open on GitHub">
					<UButton color="neutral" variant="ghost" to="https://github.com/octagony" target="_blank"
						icon="i-simple-icons-github" aria-label="GitHub" />
				</UTooltip>
			</div>
		</template>
	</UHeader>
</template>