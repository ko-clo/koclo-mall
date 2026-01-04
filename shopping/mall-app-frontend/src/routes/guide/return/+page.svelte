<svelte:head>
	<title>교환/반품 안내 | ko&clo</title>
</svelte:head>

<div class="max-w-4xl mx-auto py-12 px-4">
	<h1 class="text-3xl font-bold mb-8">교환/반품 안내</h1>

	<div class="space-y-8">
		<!-- 교환/반품 신청 -->
		<section class="bg-white border rounded-lg p-6">
			<h2 class="text-xl font-bold mb-4">교환/반품 신청 방법</h2>
			<ol class="space-y-4">
				<li class="flex gap-4">
					<span class="flex-shrink-0 w-8 h-8 bg-black text-white rounded-full flex items-center justify-center font-bold">1</span>
					<div>
						<h3 class="font-bold mb-1">신청하기</h3>
						<p class="text-gray-600 text-sm">마이페이지 > 주문내역에서 교환/반품 신청을 해주세요.</p>
					</div>
				</li>
				<li class="flex gap-4">
					<span class="flex-shrink-0 w-8 h-8 bg-black text-white rounded-full flex items-center justify-center font-bold">2</span>
					<div>
						<h3 class="font-bold mb-1">상품 포장</h3>
						<p class="text-gray-600 text-sm">상품을 받으셨을 때와 동일한 상태로 포장해주세요.</p>
					</div>
				</li>
				<li class="flex gap-4">
					<span class="flex-shrink-0 w-8 h-8 bg-black text-white rounded-full flex items-center justify-center font-bold">3</span>
					<div>
						<h3 class="font-bold mb-1">수거/반송</h3>
						<p class="text-gray-600 text-sm">택배 기사가 방문하여 상품을 수거합니다.</p>
					</div>
				</li>
				<li class="flex gap-4">
					<span class="flex-shrink-0 w-8 h-8 bg-black text-white rounded-full flex items-center justify-center font-bold">4</span>
					<div>
						<h3 class="font-bold mb-1">처리 완료</h3>
						<p class="text-gray-600 text-sm">상품 확인 후 교환 발송 또는 환불 처리됩니다.</p>
					</div>
				</li>
			</ol>
		</section>

		<!-- 교환/반품 기준 -->
		<section class="bg-white border rounded-lg p-6">
			<h2 class="text-xl font-bold mb-4">교환/반품 기준</h2>
			<div class="grid md:grid-cols-2 gap-6">
				<div>
					<h3 class="font-bold text-gray-500 text-sm mb-1">신청 기간</h3>
					<p class="text-lg">수령일로부터 7일 이내</p>
				</div>
				<div>
					<h3 class="font-bold text-gray-500 text-sm mb-1">처리 기간</h3>
					<p class="text-lg">상품 수령 후 2~3일 (영업일 기준)</p>
				</div>
				<div>
					<h3 class="font-bold text-gray-500 text-sm mb-1">단순 변심 배송비</h3>
					<p class="text-lg">왕복 6,000원 (고객 부담)</p>
				</div>
				<div>
					<h3 class="font-bold text-gray-500 text-sm mb-1">불량/오배송 배송비</h3>
					<p class="text-lg">무료 (회사 부담)</p>
				</div>
			</div>
		</section>

		<!-- 교환/반품 가능 -->
		<section class="bg-white border rounded-lg p-6">
			<h2 class="text-xl font-bold mb-4 text-green-700">교환/반품이 가능한 경우</h2>
			<ul class="space-y-2 text-gray-700">
				<li class="flex items-start gap-2">
					<svg class="w-5 h-5 text-green-600 mt-0.5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
					</svg>
					<span>상품 수령 후 7일 이내 (단순 변심)</span>
				</li>
				<li class="flex items-start gap-2">
					<svg class="w-5 h-5 text-green-600 mt-0.5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
					</svg>
					<span>상품이 표시/광고 내용과 다른 경우</span>
				</li>
				<li class="flex items-start gap-2">
					<svg class="w-5 h-5 text-green-600 mt-0.5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
					</svg>
					<span>배송 중 파손 또는 불량 상품인 경우</span>
				</li>
				<li class="flex items-start gap-2">
					<svg class="w-5 h-5 text-green-600 mt-0.5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
					</svg>
					<span>주문한 상품과 다른 상품이 배송된 경우</span>
				</li>
			</ul>
		</section>

		<!-- 교환/반품 불가 -->
		<section class="bg-white border rounded-lg p-6">
			<h2 class="text-xl font-bold mb-4 text-red-700">교환/반품이 불가능한 경우</h2>
			<ul class="space-y-2 text-gray-700">
				<li class="flex items-start gap-2">
					<svg class="w-5 h-5 text-red-500 mt-0.5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
					</svg>
					<span>수령일로부터 7일이 경과한 경우</span>
				</li>
				<li class="flex items-start gap-2">
					<svg class="w-5 h-5 text-red-500 mt-0.5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
					</svg>
					<span>착용 흔적이 있거나 세탁, 수선한 경우</span>
				</li>
				<li class="flex items-start gap-2">
					<svg class="w-5 h-5 text-red-500 mt-0.5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
					</svg>
					<span>상품 태그가 제거되었거나 분실된 경우</span>
				</li>
				<li class="flex items-start gap-2">
					<svg class="w-5 h-5 text-red-500 mt-0.5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
					</svg>
					<span>향수, 화장품 등의 냄새가 배어있는 경우</span>
				</li>
				<li class="flex items-start gap-2">
					<svg class="w-5 h-5 text-red-500 mt-0.5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
					</svg>
					<span>고객 부주의로 상품이 훼손된 경우</span>
				</li>
				<li class="flex items-start gap-2">
					<svg class="w-5 h-5 text-red-500 mt-0.5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
					</svg>
					<span>속옷, 수영복 등 위생상 반품이 불가한 상품</span>
				</li>
			</ul>
		</section>

		<!-- 환불 안내 -->
		<section class="bg-blue-50 border border-blue-200 rounded-lg p-6">
			<h2 class="text-xl font-bold mb-4 text-blue-800">환불 안내</h2>
			<ul class="space-y-2 text-blue-800 text-sm">
				<li>• 신용카드 결제: 카드사에 따라 3~7일 내 취소 처리</li>
				<li>• 실시간 계좌이체: 1~3일 내 환불 계좌로 입금</li>
				<li>• 가상계좌: 1~3일 내 환불 계좌로 입금</li>
				<li>• 간편결제: 각 결제 수단별 취소 정책에 따름</li>
			</ul>
		</section>

		<!-- 문의 -->
		<section class="text-center py-8 border-t">
			<p class="text-gray-600 mb-4">교환/반품 관련 문의사항이 있으시면 고객센터로 연락해주세요.</p>
			<p class="text-2xl font-bold">1234-5678</p>
			<p class="text-gray-500 text-sm mt-1">평일 10:00 - 18:00 (점심 12:00 - 13:00)</p>
		</section>
	</div>
</div>
