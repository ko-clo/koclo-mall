<script lang="ts">
	import { authStore } from '$lib/stores/auth';
	import { supabase } from '$lib/supabase';
	import { goto } from '$app/navigation';

	async function signOut() {
		await supabase.auth.signOut();
		goto('/');
	}
</script>

<header class="border-b bg-white sticky top-0 z-50">
	<div class="container mx-auto px-4 py-4 flex items-center justify-between">
		<a href="/" class="text-xl font-bold">ko&clo</a>

		<nav class="hidden md:flex items-center gap-6">
			<a href="/products" class="hover:text-gray-600 transition-colors">SHOP</a>
			<a href="/products?category=new" class="hover:text-gray-600 transition-colors">NEW</a>
		</nav>

		<div class="flex items-center gap-4">
			<a href="/cart" class="hover:text-gray-600 transition-colors">
				<svg
					xmlns="http://www.w3.org/2000/svg"
					class="h-6 w-6"
					fill="none"
					viewBox="0 0 24 24"
					stroke="currentColor"
				>
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						stroke-width="2"
						d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"
					/>
				</svg>
			</a>
			{#if $authStore.user}
				<a href="/my" class="hover:text-gray-600 transition-colors">마이페이지</a>
				<button onclick={signOut} class="hover:text-gray-600 transition-colors">로그아웃</button>
			{:else}
				<a href="/auth/login" class="hover:text-gray-600 transition-colors">로그인</a>
			{/if}
		</div>
	</div>
</header>
