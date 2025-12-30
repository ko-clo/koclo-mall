<script lang="ts">
	import { page } from '$app/stores';
	import { getProductBySlug, formatPrice, type ProductOption } from '$lib/data/products';
	import { cartStore, triggerCartAnimation } from '$lib/stores/cart';
	import { toastStore } from '$lib/stores/toast';

	let slug = $derived($page.params.slug);
	let product = $derived(getProductBySlug(slug));

	let selectedColor = $state<string | null>(null);
	let selectedSize = $state<string | null>(null);
	let quantity = $state(1);
	let currentImageIndex = $state(0);
	let showOptionHint = $state(false);
	let isAddingToCart = $state(false);
	let addToCartSuccess = $state(false);

	let availableColors = $derived(() => {
		if (!product) return [];
		return [...new Set(product.options.map(o => o.color))];
	});

	let availableSizes = $derived(() => {
		if (!product || !selectedColor) return [];
		return product.options
			.filter(o => o.color === selectedColor)
			.map(o => ({ size: o.size, stock: o.stock_quantity }));
	});

	let selectedOption = $derived(() => {
		if (!product || !selectedColor || !selectedSize) return null;
		return product.options.find(o => o.color === selectedColor && o.size === selectedSize);
	});

	let maxQuantity = $derived(() => {
		return selectedOption()?.stock_quantity || 1;
	});

	function selectColor(color: string) {
		selectedColor = color;
		selectedSize = null;
		quantity = 1;
	}

	function selectSize(size: string, stock: number) {
		if (stock === 0) return;
		selectedSize = size;
		quantity = 1;
	}

	function updateQuantity(delta: number) {
		const newQty = quantity + delta;
		if (newQty >= 1 && newQty <= maxQuantity()) {
			quantity = newQty;
		}
	}

	async function addToCart() {
		if (isAddingToCart) return;

		const option = selectedOption();
		if (!option) {
			showOptionHint = true;
			return;
		}

		showOptionHint = false;
		isAddingToCart = true;

		try {
			const result = await cartStore.addItem(option.id, quantity);

			if (result.success) {
				addToCartSuccess = true;
				triggerCartAnimation();
				toastStore.success(result.message, {
					label: '장바구니 보기',
					href: '/cart'
				});
				setTimeout(() => {
					addToCartSuccess = false;
				}, 1500);
			} else {
				toastStore.error(result.message);
			}
		} finally {
			isAddingToCart = false;
		}
	}

	function buyNow() {
		if (!selectedOption()) {
			alert('옵션을 선택해주세요.');
			return;
		}
		alert('바로 구매 기능은 준비 중입니다.');
	}
</script>

<svelte:head>
	{#if product}
		<title>{product.name} | ko&clo</title>
		<meta name="description" content={product.short_description} />
	{:else}
		<title>상품을 찾을 수 없습니다 | ko&clo</title>
	{/if}
</svelte:head>

{#if product}
	<div class="section-container">
		<div class="grid grid-cols-1 lg:grid-cols-2 gap-8 lg:gap-12">
			<div class="space-y-4">
				<div class="aspect-product rounded-lg overflow-hidden bg-gray-100">
					<img
						src={product.images[currentImageIndex]?.url || product.thumbnail_url}
						alt={product.name}
						class="w-full h-full object-cover"
					/>
				</div>

				{#if product.images.length > 1}
					<div class="flex gap-2 overflow-x-auto">
						{#each product.images as image, i}
							<button
								class="flex-shrink-0 w-20 h-20 rounded-lg overflow-hidden border-2 transition-colors {currentImageIndex === i ? 'border-black' : 'border-transparent'}"
								onclick={() => currentImageIndex = i}
							>
								<img src={image.url} alt="" class="w-full h-full object-cover" />
							</button>
						{/each}
					</div>
				{/if}
			</div>

			<div class="space-y-6">
				<div>
					<p class="text-sm text-gray-500 mb-1">{product.category.name}</p>
					<h1 class="text-2xl font-bold">{product.name}</h1>
					<p class="text-gray-600 mt-2">{product.short_description}</p>
				</div>

				<div class="flex items-baseline gap-3">
					{#if product.discount_rate > 0}
						<span class="text-2xl font-bold text-accent">{product.discount_rate}%</span>
					{/if}
					<span class="text-2xl font-bold">{formatPrice(product.display_price)}</span>
					{#if product.discount_rate > 0}
						<span class="text-gray-400 line-through">{formatPrice(product.original_price)}</span>
					{/if}
				</div>

				<div class="border-t pt-6 space-y-4">
					{#if showOptionHint && !selectedOption()}
						<p class="text-sm text-red-500 font-medium">옵션을 선택해주세요.</p>
					{/if}

					<div>
						<p class="text-sm font-medium mb-2">색상 {#if showOptionHint && !selectedColor}<span class="text-red-500">*</span>{/if}</p>
						<div class="flex flex-wrap gap-2">
							{#each availableColors() as color}
								<button
									class="px-4 py-2 border rounded-lg transition-colors {selectedColor === color ? 'border-black bg-black text-white' : showOptionHint && !selectedColor ? 'border-red-300 hover:border-red-400' : 'border-gray-300 hover:border-gray-400'}"
									onclick={() => { selectColor(color); showOptionHint = false; }}
								>
									{color}
								</button>
							{/each}
						</div>
					</div>

					{#if selectedColor}
						<div>
							<p class="text-sm font-medium mb-2">사이즈 {#if showOptionHint && !selectedSize}<span class="text-red-500">*</span>{/if}</p>
							<div class="flex flex-wrap gap-2">
								{#each availableSizes() as { size, stock }}
									<button
										class="px-4 py-2 border rounded-lg transition-colors {selectedSize === size ? 'border-black bg-black text-white' : stock === 0 ? 'border-gray-200 text-gray-300 cursor-not-allowed' : showOptionHint && !selectedSize ? 'border-red-300 hover:border-red-400' : 'border-gray-300 hover:border-gray-400'}"
										onclick={() => { selectSize(size, stock); showOptionHint = false; }}
										disabled={stock === 0}
									>
										{size}
										{#if stock === 0}
											<span class="text-xs ml-1">(품절)</span>
										{:else if stock <= 5}
											<span class="text-xs ml-1 text-accent">({stock}개)</span>
										{/if}
									</button>
								{/each}
							</div>
						</div>
					{/if}

					{#if selectedOption()}
						<div>
							<p class="text-sm font-medium mb-2">수량</p>
							<div class="flex items-center gap-3">
								<button
									class="w-10 h-10 border rounded-lg flex items-center justify-center hover:bg-gray-50 disabled:opacity-50"
									onclick={() => updateQuantity(-1)}
									disabled={quantity <= 1}
								>
									-
								</button>
								<span class="w-12 text-center font-medium">{quantity}</span>
								<button
									class="w-10 h-10 border rounded-lg flex items-center justify-center hover:bg-gray-50 disabled:opacity-50"
									onclick={() => updateQuantity(1)}
									disabled={quantity >= maxQuantity()}
								>
									+
								</button>
								<span class="text-sm text-gray-500">
									(재고: {selectedOption()?.stock_quantity}개)
								</span>
							</div>
						</div>
					{/if}
				</div>

				<div class="border-t pt-6 space-y-3">
					<div class="flex items-center justify-between text-lg font-bold">
						<span>총 상품 금액</span>
						<span>{formatPrice(product.display_price * quantity)}</span>
					</div>

					<div class="grid grid-cols-2 gap-3">
						<button
							class="btn-secondary h-12 transition-colors duration-200 {addToCartSuccess ? '!bg-green-600 !text-white !border-green-600' : ''}"
							onclick={addToCart}
							disabled={product.is_sold_out || isAddingToCart}
						>
							{#if isAddingToCart}
								<svg class="animate-spin h-5 w-5 mx-auto" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
									<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
									<path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
								</svg>
							{:else if addToCartSuccess}
								<svg class="h-5 w-5 mx-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor">
									<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
								</svg>
							{:else}
								장바구니
							{/if}
						</button>
						<button
							class="btn-primary h-12"
							onclick={buyNow}
							disabled={product.is_sold_out}
						>
							바로 구매
						</button>
					</div>
				</div>

				<div class="border-t pt-6">
					<h2 class="font-bold mb-4">상품 상세</h2>
					<div class="prose prose-sm max-w-none">
						{@html product.description}
					</div>
				</div>
			</div>
		</div>
	</div>
{:else}
	<div class="section-container text-center py-20">
		<h1 class="text-2xl font-bold mb-4">상품을 찾을 수 없습니다</h1>
		<p class="text-gray-500 mb-6">요청하신 상품이 존재하지 않거나 삭제되었습니다.</p>
		<a href="/products" class="btn-primary inline-block">상품 목록으로</a>
	</div>
{/if}
