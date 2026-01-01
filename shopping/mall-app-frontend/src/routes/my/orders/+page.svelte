<script lang="ts">
	import {
		mockOrders,
		orderStatusLabels,
		orderStatusColors,
		formatOrderDate,
		type Order,
		type OrderStatus
	} from '$lib/data/orders';
	import { formatPrice } from '$lib/data/products';

	// 필터 상태
	let statusFilter = $state<OrderStatus | 'all'>('all');

	// 필터된 주문 목록
	let filteredOrders = $derived(
		statusFilter === 'all'
			? mockOrders
			: mockOrders.filter((order) => order.status === statusFilter)
	);

	// 필터 옵션
	const filterOptions: { value: OrderStatus | 'all'; label: string }[] = [
		{ value: 'all', label: '전체' },
		{ value: 'PENDING', label: '결제 대기' },
		{ value: 'PAID', label: '결제 완료' },
		{ value: 'PREPARING', label: '상품 준비중' },
		{ value: 'SHIPPING', label: '배송중' },
		{ value: 'DELIVERED', label: '배송 완료' },
		{ value: 'CANCELLED', label: '취소/환불' }
	];

	// 대표 상품 정보
	function getRepresentativeInfo(order: Order) {
		const firstItem = order.items[0];
		const additionalCount = order.items.length - 1;
		return {
			item: firstItem,
			additionalCount
		};
	}
</script>

<svelte:head>
	<title>주문 내역 | ko&clo</title>
</svelte:head>

<div>
	<h1 class="text-2xl font-bold mb-6">주문 내역</h1>

	<!-- 필터 -->
	<div class="flex flex-wrap gap-2 mb-6">
		{#each filterOptions as option}
			<button
				class="px-4 py-2 rounded-full text-sm transition-colors {statusFilter === option.value
					? 'bg-black text-white'
					: 'bg-gray-100 hover:bg-gray-200'}"
				onclick={() => (statusFilter = option.value)}
			>
				{option.label}
			</button>
		{/each}
	</div>

	<!-- 주문 목록 -->
	{#if filteredOrders.length === 0}
		<div class="text-center py-20">
			<svg class="mx-auto h-16 w-16 text-gray-300 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
				<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
			</svg>
			<p class="text-gray-500 text-lg mb-4">주문 내역이 없습니다.</p>
			<a href="/products" class="btn-primary inline-block">쇼핑하러 가기</a>
		</div>
	{:else}
		<div class="space-y-4">
			{#each filteredOrders as order}
				{@const rep = getRepresentativeInfo(order)}
				<a
					href="/my/orders/{order.id}"
					class="block border rounded-lg p-4 hover:border-gray-400 transition-colors"
				>
					<!-- 주문 헤더 -->
					<div class="flex items-center justify-between mb-4">
						<div class="flex items-center gap-3">
							<span class="text-sm text-gray-500">{formatOrderDate(order.ordered_at)}</span>
							<span class="text-sm font-mono text-gray-400">{order.order_number}</span>
						</div>
						<span class="px-3 py-1 rounded-full text-xs font-medium {orderStatusColors[order.status]}">
							{orderStatusLabels[order.status]}
						</span>
					</div>

					<!-- 주문 상품 -->
					<div class="flex gap-4">
						<div class="w-20 h-20 bg-gray-100 rounded flex-shrink-0">
							{#if rep.item.product.thumbnail_url}
								<img
									src={rep.item.product.thumbnail_url}
									alt={rep.item.product.name}
									class="w-full h-full object-cover rounded"
								/>
							{/if}
						</div>
						<div class="flex-1 min-w-0">
							<p class="font-medium truncate">
								{rep.item.product.name}
								{#if rep.additionalCount > 0}
									<span class="text-gray-500">외 {rep.additionalCount}건</span>
								{/if}
							</p>
							<p class="text-sm text-gray-500 mt-1">
								{rep.item.option.color} / {rep.item.option.size}
								{#if rep.item.quantity > 1}
									· {rep.item.quantity}개
								{/if}
							</p>
							<p class="font-bold mt-2">{formatPrice(order.amounts.total)}</p>
						</div>
						<div class="flex items-center text-gray-400">
							<svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
							</svg>
						</div>
					</div>

					<!-- 배송 추적 (배송중인 경우) -->
					{#if order.status === 'SHIPPING' && order.shipping.tracking_number}
						<div class="mt-4 pt-4 border-t">
							<div class="flex items-center justify-between text-sm">
								<span class="text-gray-500">
									{order.shipping.carrier} {order.shipping.tracking_number}
								</span>
								<button
									class="text-blue-600 hover:underline"
									onclick={(e) => {
										e.preventDefault();
										e.stopPropagation();
										// TODO: 배송 추적 페이지 이동
										alert('배송 추적 기능은 준비 중입니다.');
									}}
								>
									배송 조회
								</button>
							</div>
						</div>
					{/if}
				</a>
			{/each}
		</div>
	{/if}
</div>
