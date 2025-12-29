<script lang="ts">
	import { page } from '$app/stores';
	import ProductCard from '$lib/components/product/ProductCard.svelte';
	import { mockProducts, categories } from '$lib/data/products';

	let searchQuery = $derived($page.url.searchParams.get('q') || '');
	let categoryFilter = $derived($page.url.searchParams.get('category') || '');
	let sortOption = $derived($page.url.searchParams.get('sort') || 'newest');

	let filteredProducts = $derived.by(() => {
		let result = [...mockProducts];

		if (searchQuery) {
			const q = searchQuery.toLowerCase();
			result = result.filter(p =>
				p.name.toLowerCase().includes(q) ||
				p.short_description.toLowerCase().includes(q)
			);
		}

		if (categoryFilter) {
			result = result.filter(p =>
				p.category.slug === categoryFilter || p.category.slug.startsWith(categoryFilter + '/')
			);
		}

		switch (sortOption) {
			case 'price_asc':
				result.sort((a, b) => a.display_price - b.display_price);
				break;
			case 'price_desc':
				result.sort((a, b) => b.display_price - a.display_price);
				break;
			case 'newest':
			default:
				break;
		}

		return result;
	});

	function updateUrl(params: Record<string, string>) {
		const url = new URL($page.url);
		Object.entries(params).forEach(([key, value]) => {
			if (value) {
				url.searchParams.set(key, value);
			} else {
				url.searchParams.delete(key);
			}
		});
		window.history.replaceState({}, '', url);
	}

	function handleSortChange(e: Event) {
		const target = e.target as HTMLSelectElement;
		updateUrl({ sort: target.value });
	}

	function handleCategoryClick(slug: string) {
		updateUrl({ category: categoryFilter === slug ? '' : slug });
	}

	function clearFilters() {
		window.history.replaceState({}, '', '/products');
	}

	let pageTitle = $derived(() => {
		if (searchQuery) return `"${searchQuery}" 검색 결과`;
		if (categoryFilter) {
			const cat = categories.flatMap(c => [c, ...c.children]).find(c => c.slug === categoryFilter);
			return cat?.name || '상품';
		}
		return '전체 상품';
	});
</script>

<svelte:head>
	<title>{pageTitle()} | ko&clo</title>
</svelte:head>

<div class="section-container">
	<div class="flex flex-col lg:flex-row gap-8">
		<aside class="lg:w-64 flex-shrink-0">
			<div class="sticky top-4">
				<h2 class="font-semibold text-lg mb-4">카테고리</h2>
				<nav class="space-y-2">
					{#each categories as cat}
						<div>
							<button
								class="w-full text-left py-1 px-2 rounded transition-colors {categoryFilter === cat.slug ? 'bg-black text-white' : 'hover:bg-gray-100'}"
								onclick={() => handleCategoryClick(cat.slug)}
							>
								{cat.name}
							</button>
							{#if cat.children.length > 0}
								<div class="ml-4 mt-1 space-y-1">
									{#each cat.children as child}
										<button
											class="w-full text-left py-1 px-2 text-sm rounded transition-colors {categoryFilter === child.slug ? 'bg-black text-white' : 'text-gray-600 hover:bg-gray-100'}"
											onclick={() => handleCategoryClick(child.slug)}
										>
											{child.name}
										</button>
									{/each}
								</div>
							{/if}
						</div>
					{/each}
				</nav>

				{#if categoryFilter || searchQuery}
					<button
						class="mt-6 w-full py-2 text-sm text-gray-500 hover:text-black transition-colors"
						onclick={clearFilters}
					>
						필터 초기화
					</button>
				{/if}
			</div>
		</aside>

		<main class="flex-1">
			<div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
				<div>
					<h1 class="text-2xl font-bold">{pageTitle()}</h1>
					<p class="text-sm text-gray-500 mt-1">총 {filteredProducts.length}개</p>
				</div>

				<select
					class="input-field w-full sm:w-48"
					value={sortOption}
					onchange={handleSortChange}
				>
					<option value="newest">최신순</option>
					<option value="price_asc">낮은 가격순</option>
					<option value="price_desc">높은 가격순</option>
				</select>
			</div>

			{#if filteredProducts.length > 0}
				<div class="product-grid">
					{#each filteredProducts as product (product.id)}
						<ProductCard {product} />
					{/each}
				</div>
			{:else}
				<div class="text-center py-20">
					<p class="text-gray-500">검색 결과가 없습니다.</p>
					<button
						class="mt-4 btn-secondary"
						onclick={clearFilters}
					>
						전체 상품 보기
					</button>
				</div>
			{/if}
		</main>
	</div>
</div>
