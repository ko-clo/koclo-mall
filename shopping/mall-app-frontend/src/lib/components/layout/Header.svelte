<script lang="ts">
	import { authStore } from '$lib/stores/auth';
	import { cartItemCount, cartAnimationTrigger } from '$lib/stores/cart';
	import { supabase } from '$lib/supabase';
	import { goto } from '$app/navigation';

	let isAnimating = $state(false);

	$effect(() => {
		// cartAnimationTrigger가 변경될 때마다 애니메이션 실행
		$cartAnimationTrigger;
		if ($cartAnimationTrigger > 0) {
			isAnimating = true;
			setTimeout(() => {
				isAnimating = false;
			}, 600);
		}
	});

	async function signOut() {
		await supabase.auth.signOut();
		goto('/');
	}
</script>

<style>
	@keyframes cart-bounce {
		0%, 100% { transform: scale(1); }
		25% { transform: scale(1.3); }
		50% { transform: scale(0.95); }
		75% { transform: scale(1.1); }
	}
	.cart-animate {
		animation: cart-bounce 0.6s ease-out;
	}
</style>

<header class="border-b bg-white sticky top-0 z-50">
	<div class="container mx-auto px-4 py-4 flex items-center justify-between">
		<a href="/" class="text-xl font-bold">ko&clo</a>

		<nav class="hidden md:flex items-center gap-6">
			<a href="/products" class="hover:text-gray-600 transition-colors">SHOP</a>
			<a href="/products?category=new" class="hover:text-gray-600 transition-colors">NEW</a>
		</nav>

		<div class="flex items-center gap-4">
			<a href="/cart" class="relative hover:text-gray-600 transition-colors {isAnimating ? 'cart-animate' : ''}">
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
				{#if $cartItemCount > 0}
					<span class="absolute -top-2 -right-2 w-5 h-5 bg-black text-white text-[10px] font-medium rounded-full flex items-center justify-center {isAnimating ? 'bg-green-600' : ''}">
						{$cartItemCount > 99 ? '99+' : $cartItemCount}
					</span>
				{/if}
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
