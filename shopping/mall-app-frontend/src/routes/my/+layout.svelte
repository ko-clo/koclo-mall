<script lang="ts">
	import { page } from '$app/stores';

	let { children } = $props();

	const menuItems = [
		{ href: '/my', label: '마이페이지' },
		{ href: '/my/orders', label: '주문 내역' },
		{ href: '/my/profile', label: '회원 정보' },
		{ href: '/my/addresses', label: '배송지 관리' }
	];

	function isActive(href: string) {
		if (href === '/my') {
			return $page.url.pathname === '/my';
		}
		return $page.url.pathname.startsWith(href);
	}
</script>

<div class="container mx-auto px-4 py-8">
	<div class="grid md:grid-cols-4 gap-8">
		<!-- 사이드 메뉴 -->
		<aside class="md:col-span-1">
			<h2 class="text-xl font-bold mb-4">마이페이지</h2>
			<nav class="space-y-1">
				{#each menuItems as item}
					<a
						href={item.href}
						class="block px-4 py-2 rounded-lg transition-colors {isActive(item.href)
							? 'bg-black text-white'
							: 'hover:bg-gray-100'}"
					>
						{item.label}
					</a>
				{/each}
			</nav>
		</aside>

		<!-- 컨텐츠 -->
		<main class="md:col-span-3">
			{@render children()}
		</main>
	</div>
</div>
