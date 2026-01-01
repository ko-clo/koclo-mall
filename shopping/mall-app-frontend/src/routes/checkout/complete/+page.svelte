<script lang="ts">
	import { goto } from '$app/navigation';
	import { browser } from '$app/environment';
	import { formatPrice } from '$lib/data/products';
	import { onMount } from 'svelte';

	interface CompletedOrder {
		orderNumber: string;
		impUid: string;
		paidAt: string;
		items: {
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
			};
			subtotal: number;
		}[];
		orderer: {
			name: string;
			phone: string;
			email: string;
		};
		shipping: {
			recipient: string;
			phone: string;
			postalCode: string;
			address: string;
			addressDetail: string;
			memo: string;
		};
		amounts: {
			itemsTotal: number;
			shippingFee: number;
			discount: number;
			total: number;
		};
	}

	let order = $state<CompletedOrder | null>(null);
	let isLoading = $state(true);

	onMount(() => {
		if (!browser) return;

		const orderData = sessionStorage.getItem('completedOrder');
		if (!orderData) {
			goto('/');
			return;
		}

		try {
			order = JSON.parse(orderData);
			// 주문 정보 확인 후 세션 스토리지에서 삭제 (새로고침 시 다시 접근 불가)
			// sessionStorage.removeItem('completedOrder');
		} catch {
			goto('/');
			return;
		}

		isLoading = false;
	});

	function formatDate(dateString: string): string {
		const date = new Date(dateString);
		return date.toLocaleString('ko-KR', {
			year: 'numeric',
			month: 'long',
			day: 'numeric',
			hour: '2-digit',
			minute: '2-digit'
		});
	}
</script>

<svelte:head>
	<title>주문 완료 | ko&clo</title>
</svelte:head>

<div class="container mx-auto px-4 py-8 max-w-2xl">
	{#if isLoading}
		<div class="flex justify-center py-20">
			<svg class="animate-spin h-8 w-8 text-gray-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
				<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
				<path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
			</svg>
		</div>
	{:else if order}
		<!-- 완료 메시지 -->
		<div class="text-center mb-8">
			<div class="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
				<svg class="w-8 h-8 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
				</svg>
			</div>
			<h1 class="text-2xl font-bold mb-2">주문이 완료되었습니다</h1>
			<p class="text-gray-500">주문 확인 이메일이 발송되었습니다.</p>
		</div>

		<!-- 주문 정보 -->
		<div class="space-y-6">
			<!-- 주문 번호 -->
			<section class="border rounded-lg p-6 bg-gray-50">
				<div class="flex justify-between items-center mb-4">
					<span class="text-sm text-gray-500">주문번호</span>
					<span class="font-mono font-medium">{order.orderNumber}</span>
				</div>
				<div class="flex justify-between items-center">
					<span class="text-sm text-gray-500">결제일시</span>
					<span class="text-sm">{formatDate(order.paidAt)}</span>
				</div>
			</section>

			<!-- 주문 상품 -->
			<section class="border rounded-lg p-6">
				<h2 class="font-bold mb-4">주문 상품 ({order.items.length})</h2>
				<div class="space-y-4">
					{#each order.items as item}
						<div class="flex gap-4">
							<div class="w-16 h-16 bg-gray-100 rounded flex-shrink-0">
								{#if item.product.thumbnail_url}
									<img
										src={item.product.thumbnail_url}
										alt={item.product.name}
										class="w-full h-full object-cover rounded"
									/>
								{/if}
							</div>
							<div class="flex-1 min-w-0">
								<p class="font-medium truncate text-sm">{item.product.name}</p>
								<p class="text-xs text-gray-500">{item.option.color} / {item.option.size}</p>
								<p class="text-xs text-gray-500">수량: {item.quantity}개</p>
							</div>
							<div class="text-right flex-shrink-0">
								<p class="font-bold text-sm">{formatPrice(item.subtotal)}</p>
							</div>
						</div>
					{/each}
				</div>
			</section>

			<!-- 배송지 정보 -->
			<section class="border rounded-lg p-6">
				<h2 class="font-bold mb-4">배송지 정보</h2>
				<div class="space-y-2 text-sm">
					<div class="flex">
						<span class="w-20 text-gray-500 flex-shrink-0">수령인</span>
						<span>{order.shipping.recipient}</span>
					</div>
					<div class="flex">
						<span class="w-20 text-gray-500 flex-shrink-0">연락처</span>
						<span>{order.shipping.phone}</span>
					</div>
					<div class="flex">
						<span class="w-20 text-gray-500 flex-shrink-0">주소</span>
						<span>({order.shipping.postalCode}) {order.shipping.address} {order.shipping.addressDetail}</span>
					</div>
					{#if order.shipping.memo}
						<div class="flex">
							<span class="w-20 text-gray-500 flex-shrink-0">배송메모</span>
							<span>{order.shipping.memo}</span>
						</div>
					{/if}
				</div>
			</section>

			<!-- 결제 금액 -->
			<section class="border rounded-lg p-6">
				<h2 class="font-bold mb-4">결제 금액</h2>
				<div class="space-y-2 text-sm">
					<div class="flex justify-between">
						<span class="text-gray-500">상품 금액</span>
						<span>{formatPrice(order.amounts.itemsTotal)}</span>
					</div>
					<div class="flex justify-between">
						<span class="text-gray-500">배송비</span>
						<span>{order.amounts.shippingFee === 0 ? '무료' : formatPrice(order.amounts.shippingFee)}</span>
					</div>
					{#if order.amounts.discount > 0}
						<div class="flex justify-between text-red-500">
							<span>할인</span>
							<span>-{formatPrice(order.amounts.discount)}</span>
						</div>
					{/if}
				</div>
				<div class="border-t mt-4 pt-4 flex justify-between font-bold">
					<span>총 결제 금액</span>
					<span class="text-lg">{formatPrice(order.amounts.total)}</span>
				</div>
			</section>

			<!-- 버튼 -->
			<div class="flex gap-4">
				<a
					href="/my/orders"
					class="flex-1 py-3 border border-black text-center rounded-lg font-medium hover:bg-gray-50 transition-colors"
				>
					주문 내역 보기
				</a>
				<a
					href="/"
					class="flex-1 py-3 bg-black text-white text-center rounded-lg font-medium hover:bg-gray-800 transition-colors"
				>
					쇼핑 계속하기
				</a>
			</div>
		</div>
	{:else}
		<div class="text-center py-20">
			<p class="text-gray-500 text-lg mb-4">주문 정보를 찾을 수 없습니다.</p>
			<a href="/" class="btn-primary inline-block">홈으로 이동</a>
		</div>
	{/if}
</div>
