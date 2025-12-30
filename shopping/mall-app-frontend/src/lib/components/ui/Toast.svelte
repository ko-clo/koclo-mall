<script lang="ts">
	import { toastStore, type Toast } from '$lib/stores/toast';
	import { fly } from 'svelte/transition';

	let toasts: Toast[] = $state([]);
	toastStore.subscribe((value) => (toasts = value));
</script>

{#if toasts.length > 0}
	<div class="fixed bottom-4 left-1/2 -translate-x-1/2 z-[100] flex flex-col gap-2 w-full max-w-sm px-4">
		{#each toasts as toast (toast.id)}
			<div
				class="flex items-center justify-between gap-3 px-4 py-3 rounded-lg shadow-lg {toast.type === 'success'
					? 'bg-green-600 text-white'
					: toast.type === 'error'
						? 'bg-red-600 text-white'
						: 'bg-gray-800 text-white'}"
				transition:fly={{ y: 50, duration: 200 }}
			>
				<div class="flex items-center gap-2">
					{#if toast.type === 'success'}
						<svg class="w-5 h-5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
						</svg>
					{:else if toast.type === 'error'}
						<svg class="w-5 h-5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
						</svg>
					{/if}
					<span class="text-sm">{toast.message}</span>
				</div>
				<div class="flex items-center gap-2">
					{#if toast.action}
						<a
							href={toast.action.href}
							class="text-sm font-medium underline underline-offset-2 hover:opacity-80"
						>
							{toast.action.label}
						</a>
					{/if}
					<button
						onclick={() => toastStore.remove(toast.id)}
						class="p-1 hover:opacity-80"
						aria-label="닫기"
					>
						<svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
						</svg>
					</button>
				</div>
			</div>
		{/each}
	</div>
{/if}
