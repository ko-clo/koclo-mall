<script lang="ts">
	import { mockProducts, formatPrice } from '$lib/data/products';

	let searchQuery = $state('');
	let statusFilter = $state('all');

	let filteredProducts = $derived.by(() => {
		let result = [...mockProducts];

		if (searchQuery) {
			const q = searchQuery.toLowerCase();
			result = result.filter(p =>
				p.name.toLowerCase().includes(q) ||
				p.options.some(o => o.sku.toLowerCase().includes(q))
			);
		}

		if (statusFilter === 'active') {
			result = result.filter(p => !p.is_sold_out);
		} else if (statusFilter === 'soldout') {
			result = result.filter(p => p.is_sold_out);
		}

		return result;
	});
</script>

<svelte:head>
	<title>상품 관리 | ko&clo Admin</title>
</svelte:head>

<div class="space-y-6">
	<div class="flex justify-between items-center">
		<div class="flex gap-4">
			<input
				type="text"
				placeholder="상품명, SKU 검색..."
				class="input-field w-64"
				bind:value={searchQuery}
			/>
			<select class="input-field w-40" bind:value={statusFilter}>
				<option value="all">전체 상태</option>
				<option value="active">판매중</option>
				<option value="soldout">품절</option>
			</select>
		</div>
		<a href="/admin/products/new" class="btn-primary">
			+ 상품 등록
		</a>
	</div>

	<div class="bg-white rounded-lg shadow-sm overflow-hidden">
		<table class="w-full">
			<thead class="bg-gray-50 border-b">
				<tr>
					<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">상품</th>
					<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">카테고리</th>
					<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">가격</th>
					<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">재고</th>
					<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">상태</th>
					<th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">관리</th>
				</tr>
			</thead>
			<tbody class="divide-y">
				{#each filteredProducts as product (product.id)}
					<tr class="hover:bg-gray-50">
						<td class="px-6 py-4">
							<div class="flex items-center gap-4">
								<img
									src={product.thumbnail_url}
									alt={product.name}
									class="w-12 h-12 rounded object-cover"
								/>
								<div>
									<p class="font-medium">{product.name}</p>
									<p class="text-sm text-gray-500">{product.options.length}개 옵션</p>
								</div>
							</div>
						</td>
						<td class="px-6 py-4 text-sm text-gray-600">
							{product.category.name}
						</td>
						<td class="px-6 py-4">
							<div>
								<p class="font-medium">{formatPrice(product.display_price)}</p>
								{#if product.discount_rate > 0}
									<p class="text-sm text-gray-400 line-through">{formatPrice(product.original_price)}</p>
								{/if}
							</div>
						</td>
						<td class="px-6 py-4 text-sm">
							{product.options.reduce((sum, o) => sum + o.stock_quantity, 0)}개
						</td>
						<td class="px-6 py-4">
							{#if product.is_sold_out}
								<span class="px-2 py-1 text-xs rounded-full bg-red-100 text-red-700">품절</span>
							{:else}
								<span class="px-2 py-1 text-xs rounded-full bg-green-100 text-green-700">판매중</span>
							{/if}
						</td>
						<td class="px-6 py-4 text-right">
							<a
								href="/admin/products/{product.id}/edit"
								class="text-sm text-blue-600 hover:underline"
							>
								수정
							</a>
						</td>
					</tr>
				{:else}
					<tr>
						<td colspan="6" class="px-6 py-12 text-center text-gray-500">
							등록된 상품이 없습니다.
						</td>
					</tr>
				{/each}
			</tbody>
		</table>
	</div>

	<p class="text-sm text-gray-500">
		총 {filteredProducts.length}개 상품
	</p>
</div>
