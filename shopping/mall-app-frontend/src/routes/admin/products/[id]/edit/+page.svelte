<script lang="ts">
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import { mockProducts, categories } from '$lib/data/products';

	type Tab = 'basic' | 'images' | 'options' | 'price' | 'seo';
	let activeTab = $state<Tab>('basic');

	// 상품 ID로 데이터 로드
	let productId = $derived($page.params.id);
	let product = $derived(mockProducts.find(p => p.id === productId));

	// 기본 정보
	let name = $state('');
	let slug = $state('');
	let originalSlug = $state('');
	let categoryId = $state('');
	let shortDescription = $state('');
	let description = $state('');
	let status = $state<'DRAFT' | 'ACTIVE' | 'INACTIVE'>('ACTIVE');

	// 이미지
	let thumbnailPreview = $state<string | null>(null);
	let additionalImages = $state<string[]>([]);

	// 옵션/재고
	let colors = $state<string[]>(['']);
	let sizes = $state<string[]>(['']);
	let productCode = $state('');
	let originalSkus = $state<string[]>([]);

	// 가격
	let originalPrice = $state<number>(0);
	let discountType = $state<'rate' | 'price'>('rate');
	let discountRate = $state<number>(0);
	let sellingPrice = $state<number>(0);

	// SEO
	let seoTitle = $state('');
	let seoDescription = $state('');

	// 경고 모달
	let showSkuWarning = $state(false);
	let showSlugWarning = $state(false);

	// 상품 데이터 로드
	$effect(() => {
		if (product) {
			name = product.name;
			slug = product.slug;
			originalSlug = product.slug;
			categoryId = product.category.id;
			shortDescription = product.short_description;
			description = product.description;
			status = product.is_sold_out ? 'INACTIVE' : 'ACTIVE';

			thumbnailPreview = product.thumbnail_url;
			additionalImages = product.images.filter(img => !img.is_thumbnail).map(img => img.url);

			const uniqueColors = [...new Set(product.options.map(o => o.color))];
			const uniqueSizes = [...new Set(product.options.map(o => o.size))];
			colors = uniqueColors.length > 0 ? uniqueColors : [''];
			sizes = uniqueSizes.length > 0 ? uniqueSizes : [''];
			
			originalSkus = product.options.map(o => o.sku);
			productCode = product.options[0]?.sku.split('-')[0] || '';

			originalPrice = product.original_price;
			sellingPrice = product.display_price;
			discountRate = product.discount_rate;
		}
	});

	// 자동 슬러그 생성
	function generateSlug() {
		const newSlug = name
			.toLowerCase()
			.replace(/[^a-z0-9가-힣\s]/g, '')
			.replace(/\s+/g, '-')
			.replace(/-+/g, '-');
		
		if (newSlug !== originalSlug) {
			showSlugWarning = true;
		}
		slug = newSlug;
	}

	// 할인가 계산
	function calculateSellingPrice() {
		if (discountType === 'rate' && discountRate > 0) {
			const discounted = originalPrice * (1 - discountRate / 100);
			sellingPrice = Math.round(discounted / 5000) * 5000;
		}
	}

	function calculateDiscountRate() {
		if (discountType === 'price' && sellingPrice > 0 && originalPrice > 0) {
			discountRate = Math.round((1 - sellingPrice / originalPrice) * 100);
		}
	}

	// SKU 자동 생성
	let generatedSkus = $derived.by(() => {
		const skus: { color: string; size: string; sku: string; isNew: boolean }[] = [];
		const validColors = colors.filter(c => c.trim());
		const validSizes = sizes.filter(s => s.trim());
		const code = productCode || 'PRD';

		for (const color of validColors) {
			for (const size of validSizes) {
				const colorCode = color.substring(0, 3).toUpperCase();
				const sku = `${code}-${colorCode}-${size}`;
				skus.push({
					color,
					size,
					sku,
					isNew: !originalSkus.includes(sku)
				});
			}
		}
		return skus;
	});

	// SKU 변경 확인
	let skuChanged = $derived(() => {
		const currentSkus = generatedSkus.map(s => s.sku);
		const removed = originalSkus.filter(s => !currentSkus.includes(s));
		const added = currentSkus.filter(s => !originalSkus.includes(s));
		return removed.length > 0 || added.length > 0;
	});

	// 색상/사이즈 관리
	function addColor() { colors = [...colors, '']; }
	function removeColor(index: number) { colors = colors.filter((_, i) => i !== index); }
	function addSize() { sizes = [...sizes, '']; }
	function removeSize(index: number) { sizes = sizes.filter((_, i) => i !== index); }

	// 이미지 관리
	function handleThumbnail(e: Event) {
		const input = e.target as HTMLInputElement;
		const file = input.files?.[0];
		if (file) {
			thumbnailPreview = URL.createObjectURL(file);
		}
	}

	function handleAdditionalImages(e: Event) {
		const input = e.target as HTMLInputElement;
		const files = input.files;
		if (files) {
			const urls = Array.from(files).map(f => URL.createObjectURL(f));
			additionalImages = [...additionalImages, ...urls].slice(0, 10);
		}
	}

	function removeAdditionalImage(index: number) {
		additionalImages = additionalImages.filter((_, i) => i !== index);
	}

	// 저장
	async function handleSubmit() {
		if (!name.trim()) {
			alert('상품명을 입력해주세요.');
			activeTab = 'basic';
			return;
		}
		if (!categoryId) {
			alert('카테고리를 선택해주세요.');
			activeTab = 'basic';
			return;
		}
		if (!thumbnailPreview) {
			alert('대표 이미지를 등록해주세요.');
			activeTab = 'images';
			return;
		}
		if (generatedSkus.length === 0) {
			alert('최소 1개 이상의 옵션을 입력해주세요.');
			activeTab = 'options';
			return;
		}
		if (originalPrice < 1000) {
			alert('정가는 1,000원 이상이어야 합니다.');
			activeTab = 'price';
			return;
		}

		// SKU 변경 경고
		if (skuChanged() && !showSkuWarning) {
			showSkuWarning = true;
			return;
		}

		// TODO: API 호출
		alert('상품이 수정되었습니다. (Mock)');
		goto('/admin/products');
	}

	const tabs: { id: Tab; label: string }[] = [
		{ id: 'basic', label: '기본 정보' },
		{ id: 'images', label: '이미지' },
		{ id: 'options', label: '옵션/재고' },
		{ id: 'price', label: '가격' },
		{ id: 'seo', label: 'SEO' }
	];

	const flatCategories = $derived.by(() => {
		const result: { id: string; name: string; depth: number }[] = [];
		for (const cat of categories) {
			result.push({ id: cat.id, name: cat.name, depth: 0 });
			for (const child of cat.children) {
				result.push({ id: child.id, name: child.name, depth: 1 });
			}
		}
		return result;
	});
</script>

<svelte:head>
	<title>상품 수정 | ko&clo Admin</title>
</svelte:head>

{#if !product}
	<div class="text-center py-20">
		<p class="text-gray-500">상품을 찾을 수 없습니다.</p>
		<a href="/admin/products" class="btn-primary mt-4 inline-block">목록으로</a>
	</div>
{:else}
	<div class="max-w-4xl">
		<div class="flex items-center justify-between mb-6">
			<h2 class="text-lg font-bold">상품 수정</h2>
			<a href="/admin/products" class="text-gray-500 hover:text-gray-700">← 목록으로</a>
		</div>

		<!-- 탭 네비게이션 -->
		<div class="border-b mb-6">
			<nav class="flex gap-1">
				{#each tabs as tab}
					<button
						class="px-4 py-2 border-b-2 transition-colors {activeTab === tab.id
							? 'border-black text-black font-medium'
							: 'border-transparent text-gray-500 hover:text-gray-700'}"
						onclick={() => (activeTab = tab.id)}
					>
						{tab.label}
					</button>
				{/each}
			</nav>
		</div>

		<form onsubmit={(e) => { e.preventDefault(); handleSubmit(); }}>
			<!-- 기본 정보 탭 -->
			{#if activeTab === 'basic'}
				<div class="bg-white rounded-lg shadow-sm p-6 space-y-6">
					<div>
						<label for="name" class="block text-sm font-medium mb-1">
							상품명 <span class="text-red-500">*</span>
						</label>
						<input
							id="name"
							type="text"
							class="input-field"
							bind:value={name}
							onblur={generateSlug}
							placeholder="상품명을 입력하세요"
							maxlength={100}
						/>
						<p class="text-xs text-gray-500 mt-1">{name.length}/100</p>
					</div>

					<div>
						<label for="slug" class="block text-sm font-medium mb-1">
							슬러그 <span class="text-red-500">*</span>
						</label>
						<input
							id="slug"
							type="text"
							class="input-field"
							bind:value={slug}
							placeholder="product-slug"
						/>
						{#if slug !== originalSlug}
							<p class="text-xs text-amber-600 mt-1">
								⚠️ 슬러그 변경 시 기존 URL이 작동하지 않을 수 있습니다.
							</p>
						{:else}
							<p class="text-xs text-gray-500 mt-1">URL: /products/{slug}</p>
						{/if}
					</div>

					<div>
						<label for="category" class="block text-sm font-medium mb-1">
							카테고리 <span class="text-red-500">*</span>
						</label>
						<select id="category" class="input-field" bind:value={categoryId}>
							<option value="">카테고리 선택</option>
							{#each flatCategories as cat}
								<option value={cat.id}>
									{cat.depth === 1 ? '└ ' : ''}{cat.name}
								</option>
							{/each}
						</select>
					</div>

					<div>
						<label for="shortDesc" class="block text-sm font-medium mb-1">간략 설명</label>
						<textarea
							id="shortDesc"
							class="input-field"
							rows={2}
							bind:value={shortDescription}
							placeholder="상품에 대한 간략한 설명"
							maxlength={200}
						></textarea>
						<p class="text-xs text-gray-500 mt-1">{shortDescription.length}/200</p>
					</div>

					<div>
						<label for="desc" class="block text-sm font-medium mb-1">상세 설명</label>
						<textarea
							id="desc"
							class="input-field"
							rows={6}
							bind:value={description}
							placeholder="상품에 대한 상세 설명 (HTML 지원)"
						></textarea>
					</div>

					<div>
						<label for="status" class="block text-sm font-medium mb-1">상태</label>
						<select id="status" class="input-field w-48" bind:value={status}>
							<option value="DRAFT">임시저장</option>
							<option value="ACTIVE">판매중</option>
							<option value="INACTIVE">판매중지</option>
						</select>
					</div>
				</div>
			{/if}

			<!-- 이미지 탭 -->
			{#if activeTab === 'images'}
				<div class="bg-white rounded-lg shadow-sm p-6 space-y-6">
					<div>
						<label class="block text-sm font-medium mb-2">
							대표 이미지 <span class="text-red-500">*</span>
						</label>
						<div class="flex items-start gap-4">
							{#if thumbnailPreview}
								<div class="relative">
									<img src={thumbnailPreview} alt="thumbnail" class="w-40 h-40 object-cover rounded-lg" />
									<button
										type="button"
										class="absolute -top-2 -right-2 w-6 h-6 bg-red-500 text-white rounded-full text-sm"
										onclick={() => (thumbnailPreview = null)}
									>
										×
									</button>
								</div>
							{/if}
							<label class="flex flex-col items-center justify-center w-40 h-40 border-2 border-dashed rounded-lg cursor-pointer hover:border-gray-400 transition-colors">
								<span class="text-gray-400 text-3xl">+</span>
								<span class="text-sm text-gray-500 mt-1">이미지 선택</span>
								<input
									type="file"
									class="hidden"
									accept="image/jpeg,image/png,image/webp"
									onchange={handleThumbnail}
								/>
							</label>
						</div>
					</div>

					<div>
						<label class="block text-sm font-medium mb-2">추가 이미지 (최대 10장)</label>
						<div class="flex flex-wrap gap-4">
							{#each additionalImages as img, i}
								<div class="relative">
									<img src={img} alt="additional" class="w-24 h-24 object-cover rounded-lg" />
									<button
										type="button"
										class="absolute -top-2 -right-2 w-5 h-5 bg-red-500 text-white rounded-full text-xs"
										onclick={() => removeAdditionalImage(i)}
									>
										×
									</button>
								</div>
							{/each}
							{#if additionalImages.length < 10}
								<label class="flex flex-col items-center justify-center w-24 h-24 border-2 border-dashed rounded-lg cursor-pointer hover:border-gray-400 transition-colors">
									<span class="text-gray-400 text-xl">+</span>
									<input
										type="file"
										class="hidden"
										accept="image/jpeg,image/png,image/webp"
										multiple
										onchange={handleAdditionalImages}
									/>
								</label>
							{/if}
						</div>
					</div>
				</div>
			{/if}

			<!-- 옵션/재고 탭 -->
			{#if activeTab === 'options'}
				<div class="bg-white rounded-lg shadow-sm p-6 space-y-6">
					<div>
						<label for="productCode" class="block text-sm font-medium mb-1">상품 코드</label>
						<input
							id="productCode"
							type="text"
							class="input-field w-32"
							bind:value={productCode}
							placeholder="PRD"
							maxlength={10}
						/>
					</div>

					<div>
						<label class="block text-sm font-medium mb-2">
							색상 <span class="text-red-500">*</span>
						</label>
						<div class="space-y-2">
							{#each colors as color, i}
								<div class="flex gap-2">
									<input
										type="text"
										class="input-field w-40"
										placeholder="예: Black"
										bind:value={colors[i]}
									/>
									{#if colors.length > 1}
										<button
											type="button"
											class="px-3 py-2 text-red-500 hover:bg-red-50 rounded"
											onclick={() => removeColor(i)}
										>
											삭제
										</button>
									{/if}
								</div>
							{/each}
							<button type="button" class="text-sm text-blue-600 hover:underline" onclick={addColor}>
								+ 색상 추가
							</button>
						</div>
					</div>

					<div>
						<label class="block text-sm font-medium mb-2">
							사이즈 <span class="text-red-500">*</span>
						</label>
						<div class="space-y-2">
							{#each sizes as size, i}
								<div class="flex gap-2">
									<input
										type="text"
										class="input-field w-40"
										placeholder="예: M"
										bind:value={sizes[i]}
									/>
									{#if sizes.length > 1}
										<button
											type="button"
											class="px-3 py-2 text-red-500 hover:bg-red-50 rounded"
											onclick={() => removeSize(i)}
										>
											삭제
										</button>
									{/if}
								</div>
							{/each}
							<button type="button" class="text-sm text-blue-600 hover:underline" onclick={addSize}>
								+ 사이즈 추가
							</button>
						</div>
					</div>

					{#if generatedSkus.length > 0}
						<div>
							<label class="block text-sm font-medium mb-2">
								SKU 목록 ({generatedSkus.length}개)
								{#if skuChanged()}
									<span class="text-amber-600 font-normal">- 변경됨</span>
								{/if}
							</label>
							<div class="bg-gray-50 rounded-lg p-4 max-h-60 overflow-y-auto">
								<table class="w-full text-sm">
									<thead>
										<tr class="text-left text-gray-500">
											<th class="pb-2">색상</th>
											<th class="pb-2">사이즈</th>
											<th class="pb-2">SKU</th>
											<th class="pb-2">상태</th>
										</tr>
									</thead>
									<tbody class="divide-y">
										{#each generatedSkus as sku}
											<tr>
												<td class="py-2">{sku.color}</td>
												<td class="py-2">{sku.size}</td>
												<td class="py-2 font-mono text-xs">{sku.sku}</td>
												<td class="py-2">
													{#if sku.isNew}
														<span class="text-xs text-green-600">NEW</span>
													{:else}
														<span class="text-xs text-gray-400">기존</span>
													{/if}
												</td>
											</tr>
										{/each}
									</tbody>
								</table>
							</div>
						</div>
					{/if}
				</div>
			{/if}

			<!-- 가격 탭 -->
			{#if activeTab === 'price'}
				<div class="bg-white rounded-lg shadow-sm p-6 space-y-6">
					<div>
						<label for="originalPrice" class="block text-sm font-medium mb-1">
							정가 <span class="text-red-500">*</span>
						</label>
						<div class="flex items-center gap-2">
							<input
								id="originalPrice"
								type="number"
								class="input-field w-48"
								bind:value={originalPrice}
								oninput={calculateSellingPrice}
								min={1000}
								step={1000}
							/>
							<span class="text-gray-500">원</span>
						</div>
					</div>

					<div>
						<label class="block text-sm font-medium mb-2">할인 설정</label>
						<div class="flex gap-4 mb-3">
							<label class="flex items-center gap-2">
								<input type="radio" name="discountType" value="rate" bind:group={discountType} />
								<span class="text-sm">할인율로 입력</span>
							</label>
							<label class="flex items-center gap-2">
								<input type="radio" name="discountType" value="price" bind:group={discountType} />
								<span class="text-sm">할인가 직접 입력</span>
							</label>
						</div>

						{#if discountType === 'rate'}
							<div class="flex items-center gap-2">
								<input
									type="number"
									class="input-field w-24"
									bind:value={discountRate}
									oninput={calculateSellingPrice}
									min={0}
									max={99}
								/>
								<span class="text-gray-500">%</span>
							</div>
						{:else}
							<div class="flex items-center gap-2">
								<input
									type="number"
									class="input-field w-48"
									bind:value={sellingPrice}
									oninput={calculateDiscountRate}
									min={0}
									step={1000}
								/>
								<span class="text-gray-500">원</span>
							</div>
						{/if}
					</div>

					<div class="bg-gray-50 rounded-lg p-4">
						<div class="flex justify-between items-center">
							<span class="text-gray-600">최종 판매가</span>
							<span class="text-2xl font-bold">
								{(sellingPrice || originalPrice).toLocaleString()}원
								{#if discountRate > 0}
									<span class="text-accent text-lg ml-2">({discountRate}% 할인)</span>
								{/if}
							</span>
						</div>
					</div>
				</div>
			{/if}

			<!-- SEO 탭 -->
			{#if activeTab === 'seo'}
				<div class="bg-white rounded-lg shadow-sm p-6 space-y-6">
					<div>
						<label for="seoTitle" class="block text-sm font-medium mb-1">SEO 타이틀</label>
						<input
							id="seoTitle"
							type="text"
							class="input-field"
							bind:value={seoTitle}
							placeholder={name || '상품명이 자동으로 사용됩니다'}
							maxlength={70}
						/>
						<p class="text-xs text-gray-500 mt-1">{seoTitle.length}/70</p>
					</div>

					<div>
						<label for="seoDesc" class="block text-sm font-medium mb-1">SEO 설명</label>
						<textarea
							id="seoDesc"
							class="input-field"
							rows={3}
							bind:value={seoDescription}
							placeholder={shortDescription || '간략 설명이 자동으로 사용됩니다'}
							maxlength={160}
						></textarea>
						<p class="text-xs text-gray-500 mt-1">{seoDescription.length}/160</p>
					</div>

					<div class="bg-gray-50 rounded-lg p-4">
						<p class="text-sm font-medium text-blue-600 mb-1">
							{seoTitle || name || '상품명'} | ko&clo
						</p>
						<p class="text-sm text-green-700 mb-1">
							koclo.com/products/{slug}
						</p>
						<p class="text-sm text-gray-600">
							{seoDescription || shortDescription || '상품 설명이 여기에 표시됩니다.'}
						</p>
					</div>
				</div>
			{/if}

			<!-- 하단 버튼 -->
			<div class="flex justify-between mt-6">
				<button
					type="button"
					class="px-4 py-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
					onclick={() => {
						if (confirm('이 상품을 삭제하시겠습니까?')) {
							alert('삭제 기능은 준비 중입니다. (Mock)');
						}
					}}
				>
					상품 삭제
				</button>
				<div class="flex gap-3">
					<a href="/admin/products" class="btn-secondary">취소</a>
					<button type="submit" class="btn-primary">저장</button>
				</div>
			</div>
		</form>
	</div>

	<!-- SKU 변경 경고 모달 -->
	{#if showSkuWarning}
		<div class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
			<div class="bg-white rounded-lg p-6 max-w-md mx-4">
				<h3 class="text-lg font-bold mb-2">SKU 변경 경고</h3>
				<p class="text-gray-600 mb-4">
					SKU가 변경되었습니다. SKU 변경 시 Midas ERP 동기화에 문제가 발생할 수 있습니다.
					<br /><br />
					계속 진행하시겠습니까?
				</p>
				<div class="flex justify-end gap-3">
					<button
						class="btn-secondary"
						onclick={() => (showSkuWarning = false)}
					>
						취소
					</button>
					<button
						class="btn-primary"
						onclick={() => {
							showSkuWarning = false;
							handleSubmit();
						}}
					>
						계속 진행
					</button>
				</div>
			</div>
		</div>
	{/if}
{/if}
