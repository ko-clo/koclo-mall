<svelte:head>
	<title>배송 안내 | ko&clo</title>
</svelte:head>

<div class="max-w-4xl mx-auto py-12 px-4">
	<h1 class="text-3xl font-bold mb-8">배송 안내</h1>

	<div class="space-y-8">
		<!-- 배송 정보 -->
		<section class="bg-white border rounded-lg p-6">
			<h2 class="text-xl font-bold mb-4">배송 정보</h2>
			<div class="grid md:grid-cols-2 gap-6">
				<div>
					<h3 class="font-bold text-gray-500 text-sm mb-1">배송 업체</h3>
					<p class="text-lg">CJ대한통운</p>
				</div>
				<div>
					<h3 class="font-bold text-gray-500 text-sm mb-1">배송비</h3>
					<p class="text-lg">3,000원 <span class="text-sm text-gray-500">(50,000원 이상 무료배송)</span></p>
				</div>
				<div>
					<h3 class="font-bold text-gray-500 text-sm mb-1">배송 기간</h3>
					<p class="text-lg">결제 완료 후 1~3일 (영업일 기준)</p>
				</div>
				<div>
					<h3 class="font-bold text-gray-500 text-sm mb-1">도서산간 추가 배송비</h3>
					<p class="text-lg">3,000원</p>
				</div>
			</div>
		</section>

		<!-- 배송 과정 -->
		<section class="bg-white border rounded-lg p-6">
			<h2 class="text-xl font-bold mb-4">배송 과정</h2>
			<div class="relative">
				<div class="absolute left-4 top-0 bottom-0 w-0.5 bg-gray-200"></div>
				<div class="space-y-6">
					<div class="relative flex gap-4">
						<div class="w-8 h-8 bg-black text-white rounded-full flex items-center justify-center text-sm font-bold z-10">1</div>
						<div>
							<h3 class="font-bold">결제 완료</h3>
							<p class="text-gray-600 text-sm">주문이 정상적으로 접수되었습니다.</p>
						</div>
					</div>
					<div class="relative flex gap-4">
						<div class="w-8 h-8 bg-black text-white rounded-full flex items-center justify-center text-sm font-bold z-10">2</div>
						<div>
							<h3 class="font-bold">상품 준비중</h3>
							<p class="text-gray-600 text-sm">상품을 포장하고 출고 준비 중입니다.</p>
						</div>
					</div>
					<div class="relative flex gap-4">
						<div class="w-8 h-8 bg-black text-white rounded-full flex items-center justify-center text-sm font-bold z-10">3</div>
						<div>
							<h3 class="font-bold">배송중</h3>
							<p class="text-gray-600 text-sm">택배사에 인계되어 배송 중입니다.</p>
						</div>
					</div>
					<div class="relative flex gap-4">
						<div class="w-8 h-8 bg-black text-white rounded-full flex items-center justify-center text-sm font-bold z-10">4</div>
						<div>
							<h3 class="font-bold">배송 완료</h3>
							<p class="text-gray-600 text-sm">상품이 배송 완료되었습니다.</p>
						</div>
					</div>
				</div>
			</div>
		</section>

		<!-- 배송 조회 -->
		<section class="bg-white border rounded-lg p-6">
			<h2 class="text-xl font-bold mb-4">배송 조회</h2>
			<ul class="space-y-2 text-gray-700">
				<li class="flex items-start gap-2">
					<svg class="w-5 h-5 text-black mt-0.5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
					</svg>
					<span>마이페이지 > 주문내역에서 배송 조회가 가능합니다.</span>
				</li>
				<li class="flex items-start gap-2">
					<svg class="w-5 h-5 text-black mt-0.5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
					</svg>
					<span>상품 발송 시 운송장 번호가 포함된 알림이 발송됩니다.</span>
				</li>
				<li class="flex items-start gap-2">
					<svg class="w-5 h-5 text-black mt-0.5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
					</svg>
					<span>CJ대한통운 고객센터: 1588-1255</span>
				</li>
			</ul>
		</section>

		<!-- 주의사항 -->
		<section class="bg-gray-50 rounded-lg p-6">
			<h2 class="text-xl font-bold mb-4">배송 관련 안내</h2>
			<ul class="space-y-2 text-gray-700 text-sm">
				<li>• 주문 폭주, 천재지변, 택배사 사정 등으로 배송이 지연될 수 있습니다.</li>
				<li>• 도서산간 지역은 배송에 1~2일이 추가 소요될 수 있습니다.</li>
				<li>• 주말 및 공휴일에는 배송 업무가 진행되지 않습니다.</li>
				<li>• 배송지 오입력으로 인한 오배송은 재배송이 어려울 수 있습니다.</li>
				<li>• 부재 시 경비실이나 무인택배함에 보관될 수 있습니다.</li>
			</ul>
		</section>

		<!-- 문의 -->
		<section class="text-center py-8 border-t">
			<p class="text-gray-600 mb-4">배송 관련 문의사항이 있으시면 고객센터로 연락해주세요.</p>
			<p class="text-2xl font-bold">1234-5678</p>
			<p class="text-gray-500 text-sm mt-1">평일 10:00 - 18:00 (점심 12:00 - 13:00)</p>
		</section>
	</div>
</div>
