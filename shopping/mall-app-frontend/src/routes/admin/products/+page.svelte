<script lang="ts">
	import { mockProducts, formatPrice, type Product } from '$lib/data/products';

	let searchQuery = $state('');
	let statusFilter = $state('all');
	let showDeleted = $state(false);

	// 복구 중인 상품 ID
	let restoringId = $state<string | null>(null);

	let filteredProducts = $derived.by(() => {
		let result = [...mockProducts];

		// 삭제된 상품 필터
		if (showDeleted) {
			result = result.filter(p => p.is_deleted);
		} else {
			result = result.filter(p => !p.is_deleted);
		}

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

	// 삭제된 상품 복구
	async function handleRestore(product: Product) {
		restoringId = product.id;

		// TODO: 실제 API 호출로 대체
		// PATCH /api/v1/admin/products/{id}/restore
		await new Promise(resolve => setTimeout(resolve, 500));

		// Mock: 실제로는 서버에서 처리
		alert(`'${product.name}' 상품이 복구되었습니다.`);
		restoringId = null;

		// 새로고침 (실제로는 상태 업데이트)
		location.reload();
	}
</script>

<svelte:head>
	<title>상품 관리 | ko&clo Admin</title>
</svelte:head>

<div class="space-y-6">
	<div class="flex justify-between items-center">
		<div class="flex gap-4 items-center">
			<input
				type="text"
				placeholder="상품명, SKU 검색..."
				class="input-field w-64"
				bind:value={searchQuery}
			/>
			<select class="input-field w-40" bind:value={statusFilter} disabled={showDeleted}>
				<option value="all">전체 상태</option>
				<option value="active">판매중</option>
				<option value="soldout">품절</option>
			</select>
			<label class="flex items-center gap-2 text-sm text-gray-600 cursor-pointer">
				<input
					type="checkbox"
					bind:checked={showDeleted}
					class="w-4 h-4 rounded border-gray-300"
				/>
				삭제된 상품 보기
			</label>
		</div>
		<a href="/admin/products/new" class="btn-primary">
			+ 상품 등록
		</a>
	</div>

	{#if showDeleted}
		<div class="bg-amber-50 border border-amber-200 rounded-lg p-4 text-sm text-amber-800">
			삭제된 상품을 보고 있습니다. 복구 버튼을 클릭하여 상품을 다시 판매할 수 있습니다.
		</div>
	{/if}

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
					<tr class="hover:bg-gray-50 {product.is_deleted ? 'opacity-60 bg-gray-50' : ''}">
						<td class="px-6 py-4">
							<div class="flex items-center gap-4">
								<img
									src={product.thumbnail_url}
									alt={product.name}
									class="w-12 h-12 rounded object-cover {product.is_deleted ? 'grayscale' : ''}"
								/>
								<div>
									<p class="font-medium">
										{product.name}
										{#if product.is_deleted}
											<span class="text-xs text-gray-500 font-normal">(삭제됨)</span>
										{/if}
									</p>
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
							{#if product.is_deleted}
								<span class="px-2 py-1 text-xs rounded-full bg-gray-100 text-gray-600">삭제됨</span>
							{:else if product.is_sold_out}
								<span class="px-2 py-1 text-xs rounded-full bg-red-100 text-red-700">품절</span>
							{:else}
								<span class="px-2 py-1 text-xs rounded-full bg-green-100 text-green-700">판매중</span>
							{/if}
						</td>
						<td class="px-6 py-4 text-right">
							{#if product.is_deleted}
								<button
									class="text-sm text-green-600 hover:underline disabled:opacity-50"
									onclick={() => handleRestore(product)}
									disabled={restoringId === product.id}
								>
									{restoringId === product.id ? '복구 중...' : '복구'}
								</button>
							{:else}
								<a
									href="/admin/products/{product.id}/edit"
									class="text-sm text-blue-600 hover:underline"
								>
									수정
								</a>
							{/if}
						</td>
					</tr>
				{:else}
					<tr>
						<td colspan="6" class="px-6 py-12 text-center text-gray-500">
							{#if showDeleted}
								삭제된 상품이 없습니다.
							{:else}
								등록된 상품이 없습니다.
							{/if}
						</td>
					</tr>
				{/each}
			</tbody>
		</table>
	</div>

	<p class="text-sm text-gray-500">
		{#if showDeleted}
			삭제된 상품 {filteredProducts.length}개
		{:else}
			총 {filteredProducts.length}개 상품
		{/if}
	</p>
</div>
