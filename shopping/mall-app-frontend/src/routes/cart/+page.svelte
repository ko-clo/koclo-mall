<script lang="ts">
	// TODO: API에서 장바구니 데이터 가져오기
	const cartItems: Array<{
		id: string;
		product: {
			name: string;
			thumbnail_url: string;
			slug: string;
		};
		option: {
			color: string;
			size: string;
		};
		quantity: number;
		price: number;
	}> = [];

	$: totalPrice = cartItems.reduce((sum, item) => sum + item.price * item.quantity, 0);
	const shippingFee = totalPrice >= 50000 ? 0 : 3000;

	function removeItem(id: string) {
		// TODO: 장바구니에서 삭제 API 호출
	}

	function updateQuantity(id: string, quantity: number) {
		// TODO: 수량 업데이트 API 호출
	}
</script>

<svelte:head>
	<title>장바구니 | ko&clo</title>
</svelte:head>

<div class="container mx-auto px-4 py-8">
	<h1 class="text-2xl font-bold mb-8">장바구니</h1>

	{#if cartItems.length > 0}
		<div class="grid md:grid-cols-3 gap-8">
			<!-- 상품 목록 -->
			<div class="md:col-span-2 space-y-4">
				{#each cartItems as item}
					<div class="flex gap-4 p-4 border rounded-lg">
						<a href="/products/{item.product.slug}" class="w-24 h-24 bg-gray-100 rounded">
							{#if item.product.thumbnail_url}
								<img
									src={item.product.thumbnail_url}
									alt={item.product.name}
									class="w-full h-full object-cover rounded"
								/>
							{/if}
						</a>
						<div class="flex-1">
							<a href="/products/{item.product.slug}" class="font-medium hover:underline">
								{item.product.name}
							</a>
							<p class="text-sm text-gray-500">
								{item.option.color} / {item.option.size}
							</p>
							<div class="flex items-center gap-2 mt-2">
								<button
									onclick={() => updateQuantity(item.id, item.quantity - 1)}
									disabled={item.quantity <= 1}
									class="w-8 h-8 border rounded disabled:opacity-50"
								>
									-
								</button>
								<span class="w-8 text-center">{item.quantity}</span>
								<button
									onclick={() => updateQuantity(item.id, item.quantity + 1)}
									class="w-8 h-8 border rounded"
								>
									+
								</button>
							</div>
						</div>
						<div class="text-right">
							<p class="font-bold">{(item.price * item.quantity).toLocaleString()}원</p>
							<button
								onclick={() => removeItem(item.id)}
								class="text-sm text-gray-500 hover:text-red-500 mt-2"
							>
								삭제
							</button>
						</div>
					</div>
				{/each}
			</div>

			<!-- 결제 요약 -->
			<div class="bg-gray-50 p-6 rounded-lg h-fit sticky top-24">
				<h2 class="font-bold mb-4">주문 요약</h2>
				<div class="space-y-2 text-sm">
					<div class="flex justify-between">
						<span>상품 금액</span>
						<span>{totalPrice.toLocaleString()}원</span>
					</div>
					<div class="flex justify-between">
						<span>배송비</span>
						<span>{shippingFee === 0 ? '무료' : `${shippingFee.toLocaleString()}원`}</span>
					</div>
					{#if shippingFee > 0}
						<p class="text-xs text-gray-500">5만원 이상 구매 시 무료배송</p>
					{/if}
				</div>
				<div class="border-t mt-4 pt-4 flex justify-between font-bold">
					<span>총 결제 금액</span>
					<span>{(totalPrice + shippingFee).toLocaleString()}원</span>
				</div>
				<a
					href="/checkout"
					class="block w-full mt-4 py-3 bg-black text-white text-center rounded-lg font-medium hover:bg-gray-800 transition-colors"
				>
					주문하기
				</a>
			</div>
		</div>
	{:else}
		<div class="text-center py-20">
			<p class="text-gray-500 text-lg mb-4">장바구니가 비어있습니다.</p>
			<a href="/products" class="btn-primary">쇼핑 계속하기</a>
		</div>
	{/if}
</div>
