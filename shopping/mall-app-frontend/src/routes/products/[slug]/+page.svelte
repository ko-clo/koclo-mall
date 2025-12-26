<script lang="ts">
	import { page } from '$app/stores';

	// TODO: API에서 상품 상세 가져오기
	const product = {
		id: '',
		name: '상품명',
		slug: $page.params.slug,
		short_description: '상품 간단 설명',
		description: '<p>상품 상세 설명</p>',
		original_price: 89000,
		selling_price: 60000,
		discount_rate: 32,
		seo_title: '',
		seo_description: '',
		images: [{ url: '', alt: '' }],
		options: [] as Array<{
			id: string;
			color: string;
			size: string;
			stock_quantity: number;
			additional_price: number;
		}>
	};

	let selectedColor = $state('');
	let selectedSize = $state('');
	let quantity = $state(1);

	$: availableSizes = product.options
		.filter((opt) => opt.color === selectedColor)
		.map((opt) => opt.size);

	$: selectedOption = product.options.find(
		(opt) => opt.color === selectedColor && opt.size === selectedSize
	);

	$: uniqueColors = [...new Set(product.options.map((o) => o.color))];

	function selectColor(color: string) {
		selectedColor = color;
		selectedSize = '';
	}

	async function addToCart() {
		if (!selectedOption) return;
		// TODO: 장바구니 추가 API 호출
		alert('장바구니에 추가되었습니다.');
	}

	async function buyNow() {
		if (!selectedOption) return;
		// TODO: 바로 구매 로직
	}
</script>

<svelte:head>
	<title>{product.seo_title || product.name} | ko&clo</title>
	<meta name="description" content={product.seo_description || product.short_description} />
</svelte:head>

<div class="container mx-auto px-4 py-8">
	<div class="grid md:grid-cols-2 gap-8">
		<!-- 이미지 갤러리 -->
		<div class="space-y-4">
			<div class="aspect-square bg-gray-100 rounded-lg overflow-hidden">
				{#if product.images[0]?.url}
					<img
						src={product.images[0].url}
						alt={product.images[0].alt || product.name}
						class="w-full h-full object-cover"
					/>
				{/if}
			</div>
			<!-- 썸네일 -->
			{#if product.images.length > 1}
				<div class="flex gap-2 overflow-x-auto">
					{#each product.images as image, i}
						<button class="w-20 h-20 bg-gray-100 rounded overflow-hidden flex-shrink-0">
							<img src={image.url} alt={image.alt} class="w-full h-full object-cover" />
						</button>
					{/each}
				</div>
			{/if}
		</div>

		<!-- 상품 정보 -->
		<div>
			<h1 class="text-2xl font-bold">{product.name}</h1>
			<p class="mt-2 text-gray-600">{product.short_description}</p>

			<!-- 가격 -->
			<div class="mt-4 flex items-center gap-3">
				{#if product.discount_rate}
					<span class="text-red-500 text-xl font-bold">{product.discount_rate}%</span>
					<span class="text-gray-400 line-through">
						{product.original_price.toLocaleString()}원
					</span>
				{/if}
				<span class="text-2xl font-bold">{product.selling_price.toLocaleString()}원</span>
			</div>

			<!-- 색상 선택 -->
			{#if uniqueColors.length > 0}
				<div class="mt-6">
					<p class="font-medium mb-2">색상</p>
					<div class="flex flex-wrap gap-2">
						{#each uniqueColors as color}
							<button
								onclick={() => selectColor(color)}
								class="px-4 py-2 border rounded transition-colors {selectedColor === color
									? 'border-black bg-black text-white'
									: 'hover:border-gray-400'}"
							>
								{color}
							</button>
						{/each}
					</div>
				</div>
			{/if}

			<!-- 사이즈 선택 -->
			{#if selectedColor && availableSizes.length > 0}
				<div class="mt-4">
					<p class="font-medium mb-2">사이즈</p>
					<div class="flex flex-wrap gap-2">
						{#each availableSizes as size}
							<button
								onclick={() => (selectedSize = size)}
								class="px-4 py-2 border rounded transition-colors {selectedSize === size
									? 'border-black bg-black text-white'
									: 'hover:border-gray-400'}"
							>
								{size}
							</button>
						{/each}
					</div>
				</div>
			{/if}

			<!-- 수량 선택 -->
			{#if selectedOption}
				<div class="mt-4">
					<p class="font-medium mb-2">수량</p>
					<div class="flex items-center gap-3">
						<button
							onclick={() => quantity > 1 && quantity--}
							class="w-10 h-10 border rounded hover:bg-gray-50 transition-colors"
						>
							-
						</button>
						<span class="w-12 text-center">{quantity}</span>
						<button
							onclick={() => quantity < selectedOption!.stock_quantity && quantity++}
							class="w-10 h-10 border rounded hover:bg-gray-50 transition-colors"
						>
							+
						</button>
						<span class="text-sm text-gray-500">(재고: {selectedOption.stock_quantity}개)</span>
					</div>
				</div>
			{/if}

			<!-- 액션 버튼 -->
			<div class="mt-8 flex gap-4">
				<button
					onclick={addToCart}
					disabled={!selectedOption}
					class="flex-1 py-4 bg-black text-white rounded-lg font-medium disabled:opacity-50 hover:bg-gray-800 transition-colors"
				>
					장바구니 담기
				</button>
				<button
					onclick={buyNow}
					disabled={!selectedOption}
					class="flex-1 py-4 border border-black rounded-lg font-medium disabled:opacity-50 hover:bg-gray-50 transition-colors"
				>
					바로 구매
				</button>
			</div>
		</div>
	</div>

	<!-- 상세 설명 -->
	<div class="mt-12 border-t pt-8">
		<h2 class="text-xl font-bold mb-4">상세 설명</h2>
		<div class="prose max-w-none">
			{@html product.description}
		</div>
	</div>
</div>
