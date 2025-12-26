<script lang="ts">
	// TODO: API에서 대시보드 데이터 가져오기
	const stats = {
		totalOrders: 0,
		totalRevenue: 0,
		totalMembers: 0,
		totalProducts: 0
	};
</script>

<svelte:head>
	<title>대시보드 | ko&clo Admin</title>
</svelte:head>

<div class="grid md:grid-cols-4 gap-6">
	<div class="bg-white p-6 rounded-lg shadow-sm">
		<p class="text-gray-500 text-sm">총 주문</p>
		<p class="text-2xl font-bold mt-1">{stats.totalOrders.toLocaleString()}건</p>
	</div>
	<div class="bg-white p-6 rounded-lg shadow-sm">
		<p class="text-gray-500 text-sm">총 매출</p>
		<p class="text-2xl font-bold mt-1">{stats.totalRevenue.toLocaleString()}원</p>
	</div>
	<div class="bg-white p-6 rounded-lg shadow-sm">
		<p class="text-gray-500 text-sm">총 회원</p>
		<p class="text-2xl font-bold mt-1">{stats.totalMembers.toLocaleString()}명</p>
	</div>
	<div class="bg-white p-6 rounded-lg shadow-sm">
		<p class="text-gray-500 text-sm">등록 상품</p>
		<p class="text-2xl font-bold mt-1">{stats.totalProducts.toLocaleString()}개</p>
	</div>
</div>

<div class="mt-8 grid md:grid-cols-2 gap-6">
	<div class="bg-white p-6 rounded-lg shadow-sm">
		<h2 class="font-bold mb-4">최근 주문</h2>
		<p class="text-gray-500 text-sm">주문이 없습니다.</p>
	</div>
	<div class="bg-white p-6 rounded-lg shadow-sm">
		<h2 class="font-bold mb-4">재고 부족 상품</h2>
		<p class="text-gray-500 text-sm">재고 부족 상품이 없습니다.</p>
	</div>
</div>
