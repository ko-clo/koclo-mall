<script lang="ts">
	import { page } from '$app/stores';

	// URL 파라미터에서 필터 값 추출
	$: category = $page.url.searchParams.get('category');
	$: query = $page.url.searchParams.get('q');
	$: sort = $page.url.searchParams.get('sort') || 'newest';

	// TODO: API에서 상품 목록 가져오기
	const products: Array<{
		id: string;
		slug: string;
		name: string;
		thumbnail_url: string;
		original_price: number;
		display_price: number;
		discount_rate: number | null;
		is_sold_out: boolean;
	}> = [];

	const pagination = {
		total: 0,
		page: 1,
		limit: 20,
		total_pages: 0
	};
</script>

<svelte:head>
	<title>{category || '전체'} 상품 | ko&clo</title>
</svelte:head>

<div class="container mx-auto px-4 py-8">
	<!-- 필터/정렬 영역 -->
	<div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-6">
		<h1 class="text-2xl font-bold">
			{#if category}
				{category.toUpperCase()}
			{:else}
				전체 상품
			{/if}
			{#if query}
				<span class="text-gray-500 text-lg font-normal">"{query}" 검색 결과</span>
			{/if}
		</h1>
		<select
			value={sort}
			onchange={(e) => {
				const url = new URL($page.url);
				url.searchParams.set('sort', e.currentTarget.value);
				window.location.href = url.toString();
			}}
			class="border rounded px-3 py-2"
		>
			<option value="newest">최신순</option>
			<option value="price_asc">낮은 가격순</option>
			<option value="price_desc">높은 가격순</option>
		</select>
	</div>

	<!-- 상품 그리드 -->
	{#if products.length > 0}
		<div class="grid grid-cols-2 md:grid-cols-4 gap-4">
			{#each products as product}
				<a href="/products/{product.slug}" class="group">
					<div class="aspect-square bg-gray-100 rounded-lg overflow-hidden relative">
						<img
							src={product.thumbnail_url}
							alt={product.name}
							class="w-full h-full object-cover group-hover:scale-105 transition-transform"
						/>
						{#if product.is_sold_out}
							<div class="absolute inset-0 bg-black/50 flex items-center justify-center">
								<span class="text-white font-bold">SOLD OUT</span>
							</div>
						{/if}
					</div>
					<div class="mt-3">
						<h3 class="font-medium truncate">{product.name}</h3>
						<div class="flex items-center gap-2 mt-1">
							{#if product.discount_rate}
								<span class="text-red-500 font-bold">{product.discount_rate}%</span>
								<span class="text-gray-400 line-through text-sm">
									{product.original_price.toLocaleString()}원
								</span>
							{/if}
							<span class="font-bold">{product.display_price.toLocaleString()}원</span>
						</div>
					</div>
				</a>
			{/each}
		</div>

		<!-- 페이지네이션 -->
		{#if pagination.total_pages > 1}
			<nav class="mt-8 flex justify-center gap-2">
				{#each Array(pagination.total_pages) as _, i}
					<a
						href="?page={i + 1}"
						class="px-3 py-1 border rounded {pagination.page === i + 1
							? 'bg-black text-white'
							: 'hover:bg-gray-100'}"
					>
						{i + 1}
					</a>
				{/each}
			</nav>
		{/if}
	{:else}
		<!-- 상품 없음 -->
		<div class="text-center py-20">
			<p class="text-gray-500 text-lg">상품이 없습니다.</p>
			<a href="/products" class="mt-4 inline-block text-black hover:underline">
				전체 상품 보기
			</a>
		</div>
	{/if}
</div>
