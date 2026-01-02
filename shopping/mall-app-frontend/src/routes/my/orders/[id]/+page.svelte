<script lang="ts">
	import { page } from '$app/stores';
	import { goto } from '$app/navigation';
	import {
		getOrderById,
		orderStatusLabels,
		orderStatusColors,
		formatOrderDateTime,
		cancelOrder,
		getDeliveryTracking,
		type Order,
		type DeliveryTracking
	} from '$lib/data/orders';
	import { formatPrice } from '$lib/data/products';
	import { toastStore } from '$lib/stores/toast';

	let id = $derived($page.params.id);
	let order = $derived(id ? getOrderById(id) : undefined);

	// 주문 취소 가능 여부
	let canCancel = $derived(order?.status === 'PENDING' || order?.status === 'PAID');

	// 배송 조회 가능 여부
	let canTrackShipping = $derived(
		(order?.status === 'SHIPPING' || order?.status === 'DELIVERED') &&
			order?.shipping.tracking_number
	);

	// 취소 모달 상태
	let showCancelModal = $state(false);
	let cancelReason = $state('');
	let customReason = $state('');
	let isCancelling = $state(false);

	// 배송 추적 모달 상태
	let showTrackingModal = $state(false);
	let trackingData = $state<DeliveryTracking[]>([]);
	let isLoadingTracking = $state(false);

	const cancelReasons = [
		'단순 변심',
		'상품 정보 상이',
		'배송 지연',
		'다른 상품 구매',
		'기타'
	];

	function openCancelModal() {
		showCancelModal = true;
		cancelReason = '';
		customReason = '';
	}

	function closeCancelModal() {
		showCancelModal = false;
		cancelReason = '';
		customReason = '';
	}

	async function handleCancelOrder() {
		if (!order) return;

		if (!cancelReason) {
			toastStore.error('취소 사유를 선택해주세요.');
			return;
		}

		if (cancelReason === '기타' && !customReason.trim()) {
			toastStore.error('취소 사유를 입력해주세요.');
			return;
		}

		try {
			isCancelling = true;
			const reason = cancelReason === '기타' ? customReason : cancelReason;
			await cancelOrder(order.id, reason);
			toastStore.success('주문이 취소되었습니다.');
			closeCancelModal();

			// 페이지 새로고침하여 변경사항 반영
			window.location.reload();
		} catch (error) {
			toastStore.error(error instanceof Error ? error.message : '주문 취소에 실패했습니다.');
		} finally {
			isCancelling = false;
		}
	}

	async function handleTrackShipping() {
		if (!order) return;

		try {
			isLoadingTracking = true;
			showTrackingModal = true;
			trackingData = await getDeliveryTracking(order.id);
		} catch (error) {
			toastStore.error(error instanceof Error ? error.message : '배송 조회에 실패했습니다.');
			showTrackingModal = false;
		} finally {
			isLoadingTracking = false;
		}
	}

	function closeTrackingModal() {
		showTrackingModal = false;
		trackingData = [];
	}

	function getTrackingStatusLabel(status: DeliveryTracking['status']): string {
		const labels = {
			IN_TRANSIT: '이동중',
			OUT_FOR_DELIVERY: '배송중',
			DELIVERED: '배송완료'
		};
		return labels[status];
	}

	function getTrackingStatusIcon(status: DeliveryTracking['status']): string {
		const icons = {
			IN_TRANSIT: '🚚',
			OUT_FOR_DELIVERY: '📦',
			DELIVERED: '✅'
		};
		return icons[status];
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
						onclick={openCancelModal}
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

			<!-- 결제/배송/취소 일시 -->
			{#if order.paid_at || order.shipped_at || order.delivered_at || order.cancelled_at}
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
					{#if order.cancelled_at}
						<div class="flex justify-between text-red-500">
							<span>취소일시</span>
							<span>{formatOrderDateTime(order.cancelled_at)}</span>
						</div>
						{#if order.cancel_reason}
							<div class="flex justify-between">
								<span class="text-gray-500">취소사유</span>
								<span>{order.cancel_reason}</span>
							</div>
						{/if}
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

<!-- 주문 취소 모달 -->
{#if showCancelModal}
	<div
		class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50"
		onclick={(e) => {
			if (e.target === e.currentTarget) closeCancelModal();
		}}
	>
		<div class="bg-white rounded-lg max-w-md w-full p-6">
			<h2 class="text-xl font-bold mb-4">주문 취소</h2>

			<p class="text-gray-600 text-sm mb-6">
				주문을 취소하시겠습니까?<br />
				취소 사유를 선택해주세요.
			</p>

			<!-- 취소 사유 선택 -->
			<div class="space-y-2 mb-4">
				{#each cancelReasons as reason}
					<label class="flex items-center gap-2 cursor-pointer">
						<input
							type="radio"
							name="cancel_reason"
							value={reason}
							bind:group={cancelReason}
							class="w-4 h-4"
						/>
						<span class="text-sm">{reason}</span>
					</label>
				{/each}
			</div>

			<!-- 기타 사유 입력 -->
			{#if cancelReason === '기타'}
				<div class="mb-4">
					<textarea
						bind:value={customReason}
						placeholder="취소 사유를 입력해주세요"
						class="input-field resize-none h-24"
						maxlength="200"
					></textarea>
					<p class="text-xs text-gray-500 mt-1 text-right">
						{customReason.length}/200
					</p>
				</div>
			{/if}

			<!-- 버튼 -->
			<div class="flex gap-3">
				<button
					type="button"
					onclick={closeCancelModal}
					disabled={isCancelling}
					class="flex-1 py-3 border border-gray-300 rounded-lg font-medium hover:bg-gray-50 transition-colors disabled:opacity-50"
				>
					닫기
				</button>
				<button
					type="button"
					onclick={handleCancelOrder}
					disabled={isCancelling}
					class="flex-1 py-3 bg-red-500 text-white rounded-lg font-medium hover:bg-red-600 transition-colors disabled:opacity-50"
				>
					{isCancelling ? '취소 중...' : '주문 취소'}
				</button>
			</div>
		</div>
	</div>
{/if}

<!-- 배송 추적 모달 -->
{#if showTrackingModal}
	<div
		class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50"
		onclick={(e) => {
			if (e.target === e.currentTarget) closeTrackingModal();
		}}
	>
		<div class="bg-white rounded-lg max-w-2xl w-full p-6 max-h-[80vh] overflow-y-auto">
			<div class="flex items-center justify-between mb-6">
				<h2 class="text-xl font-bold">배송 조회</h2>
				<button
					type="button"
					onclick={closeTrackingModal}
					class="text-gray-400 hover:text-gray-600"
				>
					<svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
					</svg>
				</button>
			</div>

			{#if order}
				<!-- 운송장 정보 -->
				<div class="bg-gray-50 rounded-lg p-4 mb-6">
					<div class="grid grid-cols-2 gap-3 text-sm">
						<div>
							<span class="text-gray-500">택배사</span>
							<p class="font-medium">{order.shipping.carrier}</p>
						</div>
						<div>
							<span class="text-gray-500">운송장 번호</span>
							<p class="font-medium font-mono">{order.shipping.tracking_number}</p>
						</div>
					</div>
				</div>

				<!-- 배송 추적 타임라인 -->
				{#if isLoadingTracking}
					<div class="flex items-center justify-center py-12">
						<div class="text-center">
							<div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-black mb-2"></div>
							<p class="text-gray-500 text-sm">배송 정보를 조회하는 중...</p>
						</div>
					</div>
				{:else if trackingData.length === 0}
					<div class="text-center py-12">
						<p class="text-gray-500">배송 추적 정보가 없습니다.</p>
					</div>
				{:else}
					<div class="space-y-4">
						{#each trackingData as tracking, index}
							<div class="flex gap-4">
								<!-- 아이콘 -->
								<div class="flex-shrink-0">
									<div
										class="w-10 h-10 rounded-full flex items-center justify-center text-lg {index === 0
											? 'bg-black text-white'
											: 'bg-gray-100'}"
									>
										{getTrackingStatusIcon(tracking.status)}
									</div>
									{#if index < trackingData.length - 1}
										<div class="w-0.5 h-12 bg-gray-200 mx-auto mt-2"></div>
									{/if}
								</div>

								<!-- 내용 -->
								<div class="flex-1 pb-4">
									<div class="flex items-center gap-2 mb-1">
										<span
											class="px-2 py-0.5 rounded text-xs font-medium {index === 0
												? 'bg-black text-white'
												: 'bg-gray-100 text-gray-600'}"
										>
											{getTrackingStatusLabel(tracking.status)}
										</span>
										<span class="text-sm text-gray-500">
											{formatOrderDateTime(tracking.timestamp)}
										</span>
									</div>
									<p class="font-medium">{tracking.description}</p>
									<p class="text-sm text-gray-500">{tracking.location}</p>
								</div>
							</div>
						{/each}
					</div>
				{/if}
			{/if}
		</div>
	</div>
{/if}
