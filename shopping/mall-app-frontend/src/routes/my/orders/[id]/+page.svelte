<script lang="ts">
	import { page } from '$app/stores';
	import {
		getOrderById,
		orderStatusLabels,
		orderStatusColors,
		formatOrderDateTime,
		type Order
	} from '$lib/data/orders';
	import { formatPrice } from '$lib/data/products';

	let id = $derived($page.params.id);
	let order = $derived(id ? getOrderById(id) : undefined);

	// 주문 취소 가능 여부
	let canCancel = $derived(order?.status === 'PENDING' || order?.status === 'PAID');

	// 배송 조회 가능 여부
	let canTrackShipping = $derived(
		(order?.status === 'SHIPPING' || order?.status === 'DELIVERED') &&
			order?.shipping.tracking_number
	);

	function handleCancelOrder() {
		if (confirm('주문을 취소하시겠습니까?')) {
			alert('주문 취소 기능은 준비 중입니다.');
		}
	}

	function handleTrackShipping() {
		alert('배송 추적 기능은 준비 중입니다.');
	}
</script>

<svelte:head>
	<title>{order ? `주문 상세 - ${order.order_number}` : '주문 상세'} | ko&clo</title>
</svelte:head>

<div class="max-w-3xl mx-auto">
	{#if !order}
		<div class="text-center py-20">
			<svg
				class="mx-auto h-16 w-16 text-gray-300 mb-4"
				fill="none"
				viewBox="0 0 24 24"
				stroke="currentColor"
			>
				<path
					stroke-linecap="round"
					stroke-linejoin="round"
					stroke-width="1.5"
					d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
				/>
			</svg>
			<p class="text-gray-500 text-lg mb-4">주문을 찾을 수 없습니다.</p>
			<a href="/my/orders" class="btn-primary inline-block">주문 내역으로 돌아가기</a>
		</div>
	{:else}
		<!-- 뒤로가기 -->
		<a href="/my/orders" class="inline-flex items-center gap-1 text-gray-500 hover:text-black mb-6">
			<svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
				<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
			</svg>
			주문 내역
		</a>

		<!-- 주문 상태 헤더 -->
		<div class="border rounded-lg p-6 mb-6">
			<div class="flex items-center justify-between mb-4">
				<span class="px-3 py-1 rounded-full text-sm font-medium {orderStatusColors[order.status]}">
					{orderStatusLabels[order.status]}
				</span>
				<span class="text-sm text-gray-500">{formatOrderDateTime(order.ordered_at)}</span>
			</div>
			<p class="font-mono text-sm text-gray-600">주문번호: {order.order_number}</p>

			<!-- 액션 버튼 -->
			<div class="flex gap-3 mt-4">
				{#if canTrackShipping}
					<button
						class="flex-1 py-2 border border-black rounded-lg text-sm font-medium hover:bg-gray-50 transition-colors"
						onclick={handleTrackShipping}
					>
						배송 조회
					</button>
				{/if}
				{#if canCancel}
					<button
						class="flex-1 py-2 border border-red-500 text-red-500 rounded-lg text-sm font-medium hover:bg-red-50 transition-colors"
						onclick={handleCancelOrder}
					>
						주문 취소
					</button>
				{/if}
			</div>
		</div>

		<!-- 주문 상품 -->
		<section class="border rounded-lg p-6 mb-6">
			<h2 class="font-bold mb-4">주문 상품 ({order.items.length})</h2>
			<div class="space-y-4">
				{#each order.items as item}
					<div class="flex gap-4">
						<a
							href="/products/{item.product.slug}"
							class="w-20 h-20 bg-gray-100 rounded flex-shrink-0 overflow-hidden"
						>
							{#if item.product.thumbnail_url}
								<img
									src={item.product.thumbnail_url}
									alt={item.product.name}
									class="w-full h-full object-cover hover:scale-105 transition-transform"
								/>
							{/if}
						</a>
						<div class="flex-1 min-w-0">
							<a href="/products/{item.product.slug}" class="font-medium hover:underline">
								{item.product.name}
							</a>
							<p class="text-sm text-gray-500 mt-1">
								{item.option.color} / {item.option.size}
							</p>
							<p class="text-sm text-gray-500">수량: {item.quantity}개</p>
						</div>
						<div class="text-right flex-shrink-0">
							<p class="font-bold">{formatPrice(item.subtotal)}</p>
							{#if item.quantity > 1}
								<p class="text-xs text-gray-500">({formatPrice(item.unit_price)} x {item.quantity})</p>
							{/if}
						</div>
					</div>
				{/each}
			</div>
		</section>

		<!-- 배송 정보 -->
		<section class="border rounded-lg p-6 mb-6">
			<h2 class="font-bold mb-4">배송 정보</h2>
			<div class="space-y-3 text-sm">
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
					<span>({order.shipping.postal_code}) {order.shipping.address} {order.shipping.address_detail}</span>
				</div>
				{#if order.shipping.memo}
					<div class="flex">
						<span class="w-20 text-gray-500 flex-shrink-0">배송메모</span>
						<span>{order.shipping.memo}</span>
					</div>
				{/if}
				{#if order.shipping.tracking_number}
					<div class="flex items-center">
						<span class="w-20 text-gray-500 flex-shrink-0">운송장</span>
						<span>{order.shipping.carrier} {order.shipping.tracking_number}</span>
					</div>
				{/if}
			</div>
		</section>

		<!-- 주문자 정보 -->
		<section class="border rounded-lg p-6 mb-6">
			<h2 class="font-bold mb-4">주문자 정보</h2>
			<div class="space-y-3 text-sm">
				<div class="flex">
					<span class="w-20 text-gray-500 flex-shrink-0">이름</span>
					<span>{order.orderer.name}</span>
				</div>
				<div class="flex">
					<span class="w-20 text-gray-500 flex-shrink-0">연락처</span>
					<span>{order.orderer.phone}</span>
				</div>
				<div class="flex">
					<span class="w-20 text-gray-500 flex-shrink-0">이메일</span>
					<span>{order.orderer.email}</span>
				</div>
			</div>
		</section>

		<!-- 결제 정보 -->
		<section class="border rounded-lg p-6 mb-6">
			<h2 class="font-bold mb-4">결제 정보</h2>
			<div class="space-y-2 text-sm">
				<div class="flex justify-between">
					<span class="text-gray-500">상품 금액</span>
					<span>{formatPrice(order.amounts.items_total)}</span>
				</div>
				<div class="flex justify-between">
					<span class="text-gray-500">배송비</span>
					<span>{order.amounts.shipping_fee === 0 ? '무료' : formatPrice(order.amounts.shipping_fee)}</span>
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

			<!-- 결제/배송 일시 -->
			{#if order.paid_at || order.shipped_at || order.delivered_at}
				<div class="border-t mt-4 pt-4 space-y-2 text-sm">
					{#if order.paid_at}
						<div class="flex justify-between">
							<span class="text-gray-500">결제일시</span>
							<span>{formatOrderDateTime(order.paid_at)}</span>
						</div>
					{/if}
					{#if order.shipped_at}
						<div class="flex justify-between">
							<span class="text-gray-500">발송일시</span>
							<span>{formatOrderDateTime(order.shipped_at)}</span>
						</div>
					{/if}
					{#if order.delivered_at}
						<div class="flex justify-between">
							<span class="text-gray-500">배송완료</span>
							<span>{formatOrderDateTime(order.delivered_at)}</span>
						</div>
					{/if}
				</div>
			{/if}
		</section>

		<!-- 하단 버튼 -->
		<div class="flex gap-4">
			<a
				href="/my/orders"
				class="flex-1 py-3 border border-black text-center rounded-lg font-medium hover:bg-gray-50 transition-colors"
			>
				목록으로
			</a>
			<a
				href="/"
				class="flex-1 py-3 bg-black text-white text-center rounded-lg font-medium hover:bg-gray-800 transition-colors"
			>
				쇼핑 계속하기
			</a>
		</div>
	{/if}
</div>
