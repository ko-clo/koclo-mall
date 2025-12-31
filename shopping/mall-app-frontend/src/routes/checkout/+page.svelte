<script lang="ts">
	import { cartStore } from '$lib/stores/cart';
	import { authStore } from '$lib/stores/auth';
	import { getProductByOptionId, formatPrice } from '$lib/data/products';
	import { toastStore } from '$lib/stores/toast';
	import { goto } from '$app/navigation';
	import { browser } from '$app/environment';

	interface CheckoutItem {
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
	}

	// 주문 상품 목록
	let checkoutItems = $state<CheckoutItem[]>([]);
	let isLoading = $state(true);

	// 주문자 정보
	let sameAsAccount = $state(true);
	let ordererName = $state('');
	let ordererPhone = $state('');
	let ordererEmail = $state('');

	// 배송지 정보
	let sameAsOrderer = $state(true);
	let recipientName = $state('');
	let recipientPhone = $state('');
	let postalCode = $state('');
	let address = $state('');
	let addressDetail = $state('');
	let shippingMemo = $state('');
	let customMemo = $state('');

	// 배송 메모 옵션
	const memoOptions = [
		{ value: '', label: '배송 메모를 선택해주세요' },
		{ value: '문 앞에 놔주세요', label: '문 앞에 놔주세요' },
		{ value: '경비실에 맡겨주세요', label: '경비실에 맡겨주세요' },
		{ value: '배송 전 연락 부탁드립니다', label: '배송 전 연락 부탁드립니다' },
		{ value: 'custom', label: '직접 입력' }
	];

	// 금액 계산
	let itemsTotal = $derived(checkoutItems.reduce((sum, item) => sum + item.subtotal, 0));
	let shippingFee = $derived(itemsTotal >= 50000 ? 0 : 3000);
	let totalAmount = $derived(itemsTotal + shippingFee);

	// 장바구니에서 상품 로드
	$effect(() => {
		const items = $cartStore;
		if (items.length === 0) {
			if (browser && !isLoading) {
				toastStore.error('주문할 상품이 없습니다.');
				goto('/cart');
			}
			return;
		}

		checkoutItems = items
			.map((item) => {
				const data = getProductByOptionId(item.product_option_id);
				if (!data) return null;

				const { product, option } = data;
				if (product.is_deleted || option.stock_quantity === 0) return null;

				const price = product.display_price + option.additional_price;
				return {
					product_option_id: item.product_option_id,
					quantity: Math.min(item.quantity, option.stock_quantity),
					product: {
						id: product.id,
						name: product.name,
						slug: product.slug,
						thumbnail_url: product.thumbnail_url
					},
					option: {
						color: option.color,
						size: option.size,
						price
					},
					subtotal: price * Math.min(item.quantity, option.stock_quantity)
				};
			})
			.filter((item): item is CheckoutItem => item !== null);

		isLoading = false;
	});

	// 로그인 사용자 정보
	let isLoggedIn = $derived($authStore.user !== null);
	let accountName = $derived($authStore.user?.user_metadata?.name || $authStore.user?.user_metadata?.full_name || '');
	let accountPhone = $derived($authStore.user?.user_metadata?.phone || '');
	let accountEmail = $derived($authStore.user?.email || '');

	// 계정 정보와 동일 체크
	$effect(() => {
		if (sameAsAccount && isLoggedIn) {
			ordererName = accountName;
			ordererPhone = accountPhone;
			ordererEmail = accountEmail;
		}
	});

	// 계정 정보와 동일 체크 해제 시 필드 비우기
	function handleSameAsAccountChange(checked: boolean) {
		sameAsAccount = checked;
		if (!checked) {
			ordererName = '';
			ordererPhone = '';
			ordererEmail = '';
		}
	}

	// 주문자 정보와 동일 체크
	$effect(() => {
		if (sameAsOrderer) {
			recipientName = ordererName;
			recipientPhone = ordererPhone;
		}
	});

	// 주문자 정보와 동일 체크 해제 시 필드 비우기
	function handleSameAsOrdererChange(checked: boolean) {
		sameAsOrderer = checked;
		if (!checked) {
			recipientName = '';
			recipientPhone = '';
		}
	}

	// 다음 주소 API 호출
	function openAddressSearch() {
		if (!browser) return;

		// @ts-ignore - Daum Postcode API
		new daum.Postcode({
			oncomplete: function (data: any) {
				postalCode = data.zonecode;
				address = data.roadAddress || data.jibunAddress;
			}
		}).open();
	}

	// 폼 유효성 검사
	function validateForm(): boolean {
		if (!ordererName.trim()) {
			toastStore.error('주문자 이름을 입력해주세요.');
			return false;
		}
		if (!ordererPhone.trim()) {
			toastStore.error('주문자 연락처를 입력해주세요.');
			return false;
		}
		if (!ordererEmail.trim()) {
			toastStore.error('이메일을 입력해주세요.');
			return false;
		}
		if (!recipientName.trim()) {
			toastStore.error('수령인 이름을 입력해주세요.');
			return false;
		}
		if (!recipientPhone.trim()) {
			toastStore.error('수령인 연락처를 입력해주세요.');
			return false;
		}
		if (!postalCode || !address) {
			toastStore.error('배송지 주소를 입력해주세요.');
			return false;
		}
		return true;
	}

	// 결제하기
	async function handlePayment() {
		if (!validateForm()) return;

		const finalMemo = shippingMemo === 'custom' ? customMemo : shippingMemo;

		// TODO: 실제 결제 처리 (ORD-002에서 구현)
		const orderData = {
			items: checkoutItems,
			orderer: {
				name: ordererName,
				phone: ordererPhone,
				email: ordererEmail
			},
			shipping: {
				recipient: recipientName,
				phone: recipientPhone,
				postalCode,
				address,
				addressDetail,
				memo: finalMemo
			},
			amounts: {
				itemsTotal,
				shippingFee,
				discount: 0,
				total: totalAmount
			}
		};

		console.log('Order data:', orderData);
		toastStore.info('결제 기능은 준비 중입니다.');
	}
</script>

<svelte:head>
	<title>주문/결제 | ko&clo</title>
	<script src="//t1.daumcdn.net/mapjsapi/bundle/postcode/prod/postcode.v2.js"></script>
</svelte:head>

<div class="container mx-auto px-4 py-8 max-w-4xl">
	<h1 class="text-2xl font-bold mb-8">주문/결제</h1>

	{#if isLoading}
		<div class="flex justify-center py-20">
			<svg class="animate-spin h-8 w-8 text-gray-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
				<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
				<path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
			</svg>
		</div>
	{:else if checkoutItems.length === 0}
		<div class="text-center py-20">
			<p class="text-gray-500 text-lg mb-4">주문할 상품이 없습니다.</p>
			<a href="/cart" class="btn-primary inline-block">장바구니로 이동</a>
		</div>
	{:else}
		<div class="space-y-8">
			<!-- 주문 상품 -->
			<section class="border rounded-lg p-6">
				<h2 class="text-lg font-bold mb-4">주문 상품 ({checkoutItems.length})</h2>
				<div class="space-y-4">
					{#each checkoutItems as item}
						<div class="flex gap-4">
							<div class="w-20 h-20 bg-gray-100 rounded flex-shrink-0">
								{#if item.product.thumbnail_url}
									<img
										src={item.product.thumbnail_url}
										alt={item.product.name}
										class="w-full h-full object-cover rounded"
									/>
								{/if}
							</div>
							<div class="flex-1 min-w-0">
								<p class="font-medium truncate">{item.product.name}</p>
								<p class="text-sm text-gray-500">{item.option.color} / {item.option.size}</p>
								<p class="text-sm text-gray-500">수량: {item.quantity}개</p>
							</div>
							<div class="text-right flex-shrink-0">
								<p class="font-bold">{formatPrice(item.subtotal)}</p>
							</div>
						</div>
					{/each}
				</div>
			</section>

			<!-- 주문자 정보 -->
			<section class="border rounded-lg p-6">
				<div class="flex items-center justify-between mb-4">
					<h2 class="text-lg font-bold">주문자 정보</h2>
					{#if isLoggedIn}
						<label class="flex items-center gap-2 cursor-pointer">
							<input
								type="checkbox"
								checked={sameAsAccount}
								onchange={(e) => handleSameAsAccountChange(e.currentTarget.checked)}
								class="w-4 h-4 rounded border-gray-300"
							/>
							<span class="text-sm">계정 정보와 동일</span>
						</label>
					{/if}
				</div>
				<div class="space-y-4">
					<div>
						<label for="ordererName" class="block text-sm font-medium mb-1">
							이름 <span class="text-red-500">*</span>
						</label>
						<input
							type="text"
							id="ordererName"
							bind:value={ordererName}
							disabled={sameAsAccount && isLoggedIn}
							placeholder="이름을 입력해주세요"
							class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-black disabled:bg-gray-100"
						/>
					</div>
					<div>
						<label for="ordererPhone" class="block text-sm font-medium mb-1">
							연락처 <span class="text-red-500">*</span>
						</label>
						<input
							type="tel"
							id="ordererPhone"
							bind:value={ordererPhone}
							disabled={sameAsAccount && isLoggedIn}
							placeholder="010-0000-0000"
							class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-black disabled:bg-gray-100"
						/>
					</div>
					<div>
						<label for="ordererEmail" class="block text-sm font-medium mb-1">
							이메일 <span class="text-red-500">*</span>
						</label>
						<input
							type="email"
							id="ordererEmail"
							bind:value={ordererEmail}
							disabled={sameAsAccount && isLoggedIn}
							placeholder="email@example.com"
							class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-black disabled:bg-gray-100"
						/>
					</div>
				</div>
			</section>

			<!-- 배송지 정보 -->
			<section class="border rounded-lg p-6">
				<div class="flex items-center justify-between mb-4">
					<h2 class="text-lg font-bold">배송지 정보</h2>
					<label class="flex items-center gap-2 cursor-pointer">
						<input
							type="checkbox"
							checked={sameAsOrderer}
							onchange={(e) => handleSameAsOrdererChange(e.currentTarget.checked)}
							class="w-4 h-4 rounded border-gray-300"
						/>
						<span class="text-sm">주문자 정보와 동일</span>
					</label>
				</div>
				<div class="space-y-4">
					<div>
						<label for="recipientName" class="block text-sm font-medium mb-1">
							수령인 <span class="text-red-500">*</span>
						</label>
						<input
							type="text"
							id="recipientName"
							bind:value={recipientName}
							disabled={sameAsOrderer}
							placeholder="수령인 이름을 입력해주세요"
							class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-black disabled:bg-gray-100"
						/>
					</div>
					<div>
						<label for="recipientPhone" class="block text-sm font-medium mb-1">
							연락처 <span class="text-red-500">*</span>
						</label>
						<input
							type="tel"
							id="recipientPhone"
							bind:value={recipientPhone}
							disabled={sameAsOrderer}
							placeholder="010-0000-0000"
							class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-black disabled:bg-gray-100"
						/>
					</div>
					<div>
						<label class="block text-sm font-medium mb-1">
							주소 <span class="text-red-500">*</span>
						</label>
						<div class="flex gap-2 mb-2">
							<input
								type="text"
								value={postalCode}
								readonly
								placeholder="우편번호"
								class="w-28 px-4 py-2 border rounded-lg bg-gray-50"
							/>
							<button
								type="button"
								onclick={openAddressSearch}
								class="px-4 py-2 border border-black rounded-lg hover:bg-gray-50 transition-colors"
							>
								주소 검색
							</button>
						</div>
						<input
							type="text"
							value={address}
							readonly
							placeholder="주소를 검색해주세요"
							class="w-full px-4 py-2 border rounded-lg bg-gray-50 mb-2"
						/>
						<input
							type="text"
							bind:value={addressDetail}
							placeholder="상세주소를 입력해주세요"
							class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-black"
						/>
					</div>
					<div>
						<label for="shippingMemo" class="block text-sm font-medium mb-1">배송 메모</label>
						<select
							id="shippingMemo"
							bind:value={shippingMemo}
							class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-black"
						>
							{#each memoOptions as option}
								<option value={option.value}>{option.label}</option>
							{/each}
						</select>
						{#if shippingMemo === 'custom'}
							<input
								type="text"
								bind:value={customMemo}
								placeholder="배송 메모를 입력해주세요"
								class="w-full px-4 py-2 border rounded-lg mt-2 focus:outline-none focus:ring-2 focus:ring-black"
							/>
						{/if}
					</div>
				</div>
			</section>

			<!-- 결제 금액 -->
			<section class="border rounded-lg p-6 bg-gray-50">
				<h2 class="text-lg font-bold mb-4">결제 금액</h2>
				<div class="space-y-2 text-sm">
					<div class="flex justify-between">
						<span>상품 금액</span>
						<span>{formatPrice(itemsTotal)}</span>
					</div>
					<div class="flex justify-between">
						<span>배송비</span>
						<span>{shippingFee === 0 ? '무료' : formatPrice(shippingFee)}</span>
					</div>
					{#if shippingFee > 0}
						<p class="text-xs text-gray-500">
							{formatPrice(50000 - itemsTotal)} 더 구매 시 무료배송
						</p>
					{/if}
				</div>
				<div class="border-t mt-4 pt-4 flex justify-between font-bold text-lg">
					<span>총 결제 금액</span>
					<span class="text-xl">{formatPrice(totalAmount)}</span>
				</div>
			</section>

			<!-- 결제하기 버튼 -->
			<button
				onclick={handlePayment}
				class="w-full py-4 bg-black text-white text-center rounded-lg font-medium hover:bg-gray-800 transition-colors text-lg"
			>
				{formatPrice(totalAmount)} 결제하기
			</button>

			<p class="text-xs text-gray-500 text-center">
				주문 내용을 확인하였으며, 결제에 동의합니다.
			</p>
		</div>
	{/if}
</div>
