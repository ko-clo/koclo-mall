<script lang="ts">
	import { goto } from '$app/navigation';
</script>

<svelte:head>
	<title>ko&clo - 패션 쇼핑몰</title>
	<meta name="description" content="ko&clo 공식 온라인 쇼핑몰" />
</svelte:head>

<!-- 히어로 섹션 -->
<section class="relative h-[600px] bg-gray-100 flex items-center justify-center">
	<div class="text-center">
		<h1 class="text-5xl font-bold mb-4">ko&clo</h1>
		<p class="text-xl text-gray-600 mb-8">스타일을 완성하는 선택</p>
		<a href="/products" class="btn-primary">쇼핑하기</a>
	</div>
</section>

<!-- 카테고리 섹션 -->
<section class="container mx-auto px-4 py-16">
	<h2 class="text-2xl font-bold mb-8 text-center">CATEGORY</h2>
	<div class="grid grid-cols-2 md:grid-cols-4 gap-4">
		<a href="/products?category=outer" class="group">
			<div class="aspect-square bg-gray-100 rounded-lg flex items-center justify-center group-hover:bg-gray-200 transition-colors">
				<span class="font-medium">OUTER</span>
			</div>
		</a>
		<a href="/products?category=top" class="group">
			<div class="aspect-square bg-gray-100 rounded-lg flex items-center justify-center group-hover:bg-gray-200 transition-colors">
				<span class="font-medium">TOP</span>
			</div>
		</a>
		<a href="/products?category=bottom" class="group">
			<div class="aspect-square bg-gray-100 rounded-lg flex items-center justify-center group-hover:bg-gray-200 transition-colors">
				<span class="font-medium">BOTTOM</span>
			</div>
		</a>
		<a href="/products?category=acc" class="group">
			<div class="aspect-square bg-gray-100 rounded-lg flex items-center justify-center group-hover:bg-gray-200 transition-colors">
				<span class="font-medium">ACC</span>
			</div>
		</a>
	</div>
</section>

<!-- 신상품 섹션 -->
<section class="container mx-auto px-4 py-16">
	<div class="flex justify-between items-center mb-8">
		<h2 class="text-2xl font-bold">NEW ARRIVALS</h2>
		<a href="/products?category=new" class="text-gray-600 hover:text-black transition-colors">
			더보기 &rarr;
		</a>
	</div>
	<div class="grid grid-cols-2 md:grid-cols-4 gap-4">
		<!-- 상품 카드 플레이스홀더 -->
		{#each Array(4) as _, i}
			<div class="group">
				<div class="aspect-square bg-gray-100 rounded-lg mb-3"></div>
				<h3 class="font-medium text-gray-400">상품명</h3>
				<p class="text-gray-300">가격</p>
			</div>
		{/each}
	</div>
</section>
