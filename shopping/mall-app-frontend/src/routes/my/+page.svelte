<script lang="ts">
	import { authStore } from '$lib/stores/auth';

	// TODO: API에서 마이페이지 데이터 가져오기
	const recentOrders: Array<{
		id: string;
		order_number: string;
		created_at: string;
		status: string;
		total_amount: number;
	}> = [];
</script>

<svelte:head>
	<title>마이페이지 | ko&clo</title>
</svelte:head>

<div>
	<!-- 회원 정보 요약 -->
	<div class="bg-gray-50 p-6 rounded-lg mb-8">
		<div class="flex items-center justify-between">
			<div class="flex items-center gap-4">
				<div class="w-16 h-16 bg-gray-200 rounded-full flex items-center justify-center text-2xl overflow-hidden">
					{#if $authStore.user?.user_metadata?.profile_image}
						<img
							src={$authStore.user.user_metadata.profile_image}
							alt="프로필"
							class="w-full h-full object-cover"
						/>
					{:else}
						{$authStore.user?.email?.charAt(0).toUpperCase() || '?'}
					{/if}
				</div>
				<div>
					<p class="font-bold text-lg">{$authStore.user?.user_metadata?.name || '회원'}</p>
					<p class="text-gray-500">{$authStore.user?.email}</p>
				</div>
			</div>
			<a
				href="/my/profile"
				class="px-4 py-2 border border-gray-300 rounded-lg text-sm hover:bg-gray-100 transition-colors"
			>
				프로필 수정
			</a>
		</div>
	</div>

	<!-- 빠른 메뉴 -->
	<div class="grid grid-cols-3 gap-4 mb-8">
		<a href="/my/orders" class="p-4 border rounded-lg text-center hover:bg-gray-50 transition-colors">
			<p class="text-2xl font-bold">0</p>
			<p class="text-sm text-gray-500">주문</p>
		</a>
		<a href="/cart" class="p-4 border rounded-lg text-center hover:bg-gray-50 transition-colors">
			<p class="text-2xl font-bold">0</p>
			<p class="text-sm text-gray-500">장바구니</p>
		</a>
		<a href="/my/addresses" class="p-4 border rounded-lg text-center hover:bg-gray-50 transition-colors">
			<p class="text-2xl font-bold">0</p>
			<p class="text-sm text-gray-500">배송지</p>
		</a>
	</div>

	<!-- 최근 주문 -->
	<div>
		<div class="flex justify-between items-center mb-4">
			<h2 class="font-bold">최근 주문</h2>
			<a href="/my/orders" class="text-sm text-gray-500 hover:text-black">전체보기</a>
		</div>
		{#if recentOrders.length > 0}
			<div class="space-y-2">
				{#each recentOrders as order}
					<a
						href="/my/orders/{order.id}"
						class="block p-4 border rounded-lg hover:bg-gray-50 transition-colors"
					>
						<div class="flex justify-between items-center">
							<div>
								<p class="font-medium">{order.order_number}</p>
								<p class="text-sm text-gray-500">{order.created_at}</p>
							</div>
							<div class="text-right">
								<p class="font-bold">{order.total_amount.toLocaleString()}원</p>
								<p class="text-sm">{order.status}</p>
							</div>
						</div>
					</a>
				{/each}
			</div>
		{:else}
			<div class="text-center py-8 text-gray-500">
				주문 내역이 없습니다.
			</div>
		{/if}
	</div>
</div>
