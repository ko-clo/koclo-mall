<script lang="ts">
	import { cartStore } from '$lib/stores/cart';
	import { getProductByOptionId, formatPrice } from '$lib/data/products';
	import { toastStore } from '$lib/stores/toast';

	type CartItemStatus = 'available' | 'out_of_stock' | 'insufficient_stock' | 'deleted';

	interface EnrichedCartItem {
		product_option_id: string;
		quantity: number;
		product: {
			id: string;
			name: string;
			slug: string;
			thumbnail_url: string;
		};
		option: {
			color: string;
			size: string;
			price: number;
			stock: number;
		};
		status: CartItemStatus;
	}

	let isLoading = $state(true);
	let enrichedItems = $state<EnrichedCartItem[]>([]);

	// cartStore 변경 시 상품 정보 조회
	$effect(() => {
		const items = $cartStore;
		enrichedItems = items.map((item) => {
			const data = getProductByOptionId(item.product_option_id);
			if (!data) {
				return {
					product_option_id: item.product_option_id,
					quantity: item.quantity,
					product: {
						id: '',
						name: '삭제된 상품',
						slug: '',
						thumbnail_url: ''
					},
					option: {
						color: '-',
						size: '-',
						price: 0,
						stock: 0
					},
					status: 'deleted' as CartItemStatus
				};
			}

			const { product, option } = data;
			let status: CartItemStatus = 'available';

			if (product.is_deleted) {
				status = 'deleted';
			} else if (option.stock_quantity === 0) {
				status = 'out_of_stock';
			} else if (item.quantity > option.stock_quantity) {
				status = 'insufficient_stock';
			}

			return {
				product_option_id: item.product_option_id,
				quantity: item.quantity,
				product: {
					id: product.id,
					name: product.name,
					slug: product.slug,
					thumbnail_url: product.thumbnail_url
				},
				option: {
					color: option.color,
					size: option.size,
					price: product.display_price + option.additional_price,
					stock: option.stock_quantity
				},
				status
			};
		});
		isLoading = false;
	});

	// 구매 가능한 상품만 필터링
	let availableItems = $derived(
		enrichedItems.filter((item) => item.status === 'available' || item.status === 'insufficient_stock')
	);

	let unavailableItems = $derived(
		enrichedItems.filter((item) => item.status === 'out_of_stock' || item.status === 'deleted')
	);

	// 총 금액 계산 (구매 가능한 상품만)
	let totalPrice = $derived(
		availableItems.reduce((sum, item) => {
			const qty = item.status === 'insufficient_stock' ? item.option.stock : item.quantity;
			return sum + item.option.price * qty;
		}, 0)
	);

	let shippingFee = $derived(totalPrice >= 50000 ? 0 : 3000);

	let selectedItems = $state<Set<string>>(new Set());
	let selectAll = $derived(
		availableItems.length > 0 && availableItems.every((item) => selectedItems.has(item.product_option_id))
	);

	function toggleSelectAll() {
		if (selectAll) {
			selectedItems = new Set();
		} else {
			selectedItems = new Set(availableItems.map((item) => item.product_option_id));
		}
	}

	function toggleSelectItem(productOptionId: string) {
		const newSet = new Set(selectedItems);
		if (newSet.has(productOptionId)) {
			newSet.delete(productOptionId);
		} else {
			newSet.add(productOptionId);
		}
		selectedItems = newSet;
	}

	async function updateQuantity(productOptionId: string, newQuantity: number) {
		if (newQuantity < 1) return;
		await cartStore.updateQuantity(productOptionId, newQuantity);
	}

	async function removeItem(productOptionId: string) {
		await cartStore.removeItem(productOptionId);
		toastStore.success('상품이 삭제되었습니다.');
	}

	async function removeSelectedItems() {
		if (selectedItems.size === 0) {
			toastStore.error('선택된 상품이 없습니다.');
			return;
		}
		await cartStore.removeItems([...selectedItems]);
		selectedItems = new Set();
		toastStore.success(`${selectedItems.size}개 상품이 삭제되었습니다.`);
	}

	async function removeUnavailableItems() {
		const ids = unavailableItems.map((item) => item.product_option_id);
		if (ids.length === 0) return;
		await cartStore.removeItems(ids);
		toastStore.success('품절/판매종료 상품이 삭제되었습니다.');
	}

	function getStatusBadge(status: CartItemStatus) {
		switch (status) {
			case 'out_of_stock':
				return { text: '품절', class: 'bg-gray-500' };
			case 'insufficient_stock':
				return { text: '재고 부족', class: 'bg-orange-500' };
			case 'deleted':
				return { text: '판매 종료', class: 'bg-red-500' };
			default:
				return null;
		}
	}
</script>

<svelte:head>
	<title>장바구니 | ko&clo</title>
</svelte:head>

<div class="container mx-auto px-4 py-8">
	<h1 class="text-2xl font-bold mb-8">장바구니</h1>

	{#if isLoading}
		<div class="flex justify-center py-20">
			<svg class="animate-spin h-8 w-8 text-gray-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
				<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
				<path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
			</svg>
		</div>
	{:else if enrichedItems.length === 0}
		<div class="text-center py-20">
			<svg class="mx-auto h-16 w-16 text-gray-300 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
				<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
			</svg>
			<p class="text-gray-500 text-lg mb-4">장바구니가 비어있습니다.</p>
			<a href="/products" class="btn-primary inline-block">쇼핑 계속하기</a>
		</div>
	{:else}
		<div class="grid lg:grid-cols-3 gap-8">
			<!-- 상품 목록 -->
			<div class="lg:col-span-2 space-y-4">
				<!-- 선택 컨트롤 -->
				<div class="flex items-center justify-between pb-4 border-b">
					<label class="flex items-center gap-2 cursor-pointer">
						<input
							type="checkbox"
							checked={selectAll}
							onchange={toggleSelectAll}
							class="w-5 h-5 rounded border-gray-300"
						/>
						<span class="text-sm">전체 선택 ({availableItems.length})</span>
					</label>
					<div class="flex gap-2">
						<button
							onclick={removeSelectedItems}
							class="text-sm text-gray-500 hover:text-red-500"
						>
							선택 삭제
						</button>
						{#if unavailableItems.length > 0}
							<span class="text-gray-300">|</span>
							<button
								onclick={removeUnavailableItems}
								class="text-sm text-gray-500 hover:text-red-500"
							>
								품절 상품 삭제
							</button>
						{/if}
					</div>
				</div>

				<!-- 구매 가능 상품 -->
				{#each availableItems as item (item.product_option_id)}
					{@const badge = getStatusBadge(item.status)}
					<div class="flex gap-4 p-4 border rounded-lg {item.status === 'insufficient_stock' ? 'border-orange-200 bg-orange-50' : ''}">
						<input
							type="checkbox"
							checked={selectedItems.has(item.product_option_id)}
							onchange={() => toggleSelectItem(item.product_option_id)}
							class="w-5 h-5 rounded border-gray-300 mt-1"
						/>
						<a href="/products/{item.product.slug}" class="w-20 h-20 bg-gray-100 rounded flex-shrink-0">
							{#if item.product.thumbnail_url}
								<img
									src={item.product.thumbnail_url}
									alt={item.product.name}
									class="w-full h-full object-cover rounded"
								/>
							{/if}
						</a>
						<div class="flex-1 min-w-0">
							<div class="flex items-start gap-2">
								<a href="/products/{item.product.slug}" class="font-medium hover:underline truncate">
									{item.product.name}
								</a>
								{#if badge}
									<span class="flex-shrink-0 px-2 py-0.5 text-xs text-white rounded {badge.class}">
										{badge.text}
									</span>
								{/if}
							</div>
							<p class="text-sm text-gray-500 mt-1">
								{item.option.color} / {item.option.size}
							</p>
							{#if item.status === 'insufficient_stock'}
								<p class="text-xs text-orange-600 mt-1">
									재고가 {item.option.stock}개만 남았습니다.
								</p>
							{/if}
							<div class="flex items-center gap-2 mt-2">
								<button
									onclick={() => updateQuantity(item.product_option_id, item.quantity - 1)}
									disabled={item.quantity <= 1}
									class="w-8 h-8 border rounded flex items-center justify-center hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
								>
									-
								</button>
								<span class="w-10 text-center">{item.quantity}</span>
								<button
									onclick={() => updateQuantity(item.product_option_id, item.quantity + 1)}
									disabled={item.quantity >= item.option.stock}
									class="w-8 h-8 border rounded flex items-center justify-center hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
								>
									+
								</button>
							</div>
						</div>
						<div class="text-right flex-shrink-0">
							<p class="font-bold">{formatPrice(item.option.price * item.quantity)}</p>
							<button
								onclick={() => removeItem(item.product_option_id)}
								class="text-sm text-gray-400 hover:text-red-500 mt-2"
							>
								삭제
							</button>
						</div>
					</div>
				{/each}

				<!-- 품절/판매종료 상품 -->
				{#if unavailableItems.length > 0}
					<div class="mt-6">
						<p class="text-sm text-gray-500 mb-3">구매 불가 상품 ({unavailableItems.length})</p>
						{#each unavailableItems as item (item.product_option_id)}
							{@const badge = getStatusBadge(item.status)}
							<div class="flex gap-4 p-4 border rounded-lg bg-gray-50 opacity-60">
								<div class="w-5"></div>
								<div class="w-20 h-20 bg-gray-200 rounded flex-shrink-0 relative">
									{#if item.product.thumbnail_url}
										<img
											src={item.product.thumbnail_url}
											alt={item.product.name}
											class="w-full h-full object-cover rounded grayscale"
										/>
									{/if}
								</div>
								<div class="flex-1 min-w-0">
									<div class="flex items-start gap-2">
										<span class="font-medium truncate line-through text-gray-400">
											{item.product.name}
										</span>
										{#if badge}
											<span class="flex-shrink-0 px-2 py-0.5 text-xs text-white rounded {badge.class}">
												{badge.text}
											</span>
										{/if}
									</div>
									<p class="text-sm text-gray-400 mt-1">
										{item.option.color} / {item.option.size}
									</p>
								</div>
								<div class="text-right flex-shrink-0">
									<button
										onclick={() => removeItem(item.product_option_id)}
										class="text-sm text-gray-400 hover:text-red-500"
									>
										삭제
									</button>
								</div>
							</div>
						{/each}
					</div>
				{/if}
			</div>

			<!-- 결제 요약 -->
			<div class="lg:col-span-1">
				<div class="bg-gray-50 p-6 rounded-lg sticky top-24">
					<h2 class="font-bold mb-4">주문 요약</h2>
					<div class="space-y-2 text-sm">
						<div class="flex justify-between">
							<span>상품 금액</span>
							<span>{formatPrice(totalPrice)}</span>
						</div>
						<div class="flex justify-between">
							<span>배송비</span>
							<span>{shippingFee === 0 ? '무료' : formatPrice(shippingFee)}</span>
						</div>
						{#if shippingFee > 0 && totalPrice > 0}
							<p class="text-xs text-gray-500">
								{formatPrice(50000 - totalPrice)} 더 담으면 무료배송
							</p>
						{/if}
					</div>
					<div class="border-t mt-4 pt-4 flex justify-between font-bold text-lg">
						<span>총 결제 금액</span>
						<span>{formatPrice(totalPrice + shippingFee)}</span>
					</div>
					{#if availableItems.length > 0}
						<a
							href="/checkout"
							class="block w-full mt-4 py-3 bg-black text-white text-center rounded-lg font-medium hover:bg-gray-800 transition-colors"
						>
							주문하기 ({availableItems.length})
						</a>
					{:else}
						<button
							disabled
							class="block w-full mt-4 py-3 bg-gray-300 text-white text-center rounded-lg font-medium cursor-not-allowed"
						>
							주문할 상품이 없습니다
						</button>
					{/if}
				</div>
			</div>
		</div>
	{/if}
</div>
