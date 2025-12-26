<script lang="ts">
	import { page } from '$app/stores';

	let { children } = $props();

	const menuItems = [
		{ href: '/admin', label: '대시보드', icon: 'home' },
		{ href: '/admin/products', label: '상품 관리', icon: 'box' },
		{ href: '/admin/categories', label: '카테고리 관리', icon: 'folder' },
		{ href: '/admin/inventory', label: '재고 관리', icon: 'package' },
		{ href: '/admin/orders', label: '주문 관리', icon: 'shopping-cart' },
		{ href: '/admin/members', label: '회원 관리', icon: 'users' }
	];

	function isActive(href: string) {
		if (href === '/admin') {
			return $page.url.pathname === '/admin';
		}
		return $page.url.pathname.startsWith(href);
	}
</script>

<div class="flex min-h-screen">
	<!-- 사이드바 -->
	<aside class="w-64 bg-gray-900 text-white">
		<div class="p-6">
			<a href="/admin" class="text-xl font-bold">ko&clo Admin</a>
		</div>
		<nav class="px-4 space-y-1">
			{#each menuItems as item}
				<a
					href={item.href}
					class="block px-4 py-3 rounded-lg transition-colors {isActive(item.href)
						? 'bg-gray-800 text-white'
						: 'text-gray-400 hover:bg-gray-800 hover:text-white'}"
				>
					{item.label}
				</a>
			{/each}
		</nav>
		<div class="absolute bottom-0 w-64 p-4 border-t border-gray-700">
			<a href="/" class="block px-4 py-2 text-gray-400 hover:text-white transition-colors">
				← 쇼핑몰로 돌아가기
			</a>
		</div>
	</aside>

	<!-- 메인 컨텐츠 -->
	<main class="flex-1 bg-gray-50">
		<header class="bg-white border-b px-8 py-4">
			<div class="flex justify-between items-center">
				<h1 class="text-xl font-bold">
					{#if $page.url.pathname === '/admin'}
						대시보드
					{:else if $page.url.pathname.startsWith('/admin/products')}
						상품 관리
					{:else if $page.url.pathname.startsWith('/admin/categories')}
						카테고리 관리
					{:else if $page.url.pathname.startsWith('/admin/inventory')}
						재고 관리
					{:else if $page.url.pathname.startsWith('/admin/orders')}
						주문 관리
					{:else if $page.url.pathname.startsWith('/admin/members')}
						회원 관리
					{/if}
				</h1>
			</div>
		</header>
		<div class="p-8">
			{@render children()}
		</div>
	</main>
</div>
