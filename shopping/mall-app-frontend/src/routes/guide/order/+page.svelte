<svelte:head>
	<title>주문/결제 안내 | ko&clo</title>
</svelte:head>

<div class="max-w-4xl mx-auto py-12 px-4">
	<h1 class="text-3xl font-bold mb-8">주문/결제 안내</h1>

	<div class="space-y-8">
		<!-- 주문 방법 -->
		<section class="bg-white border rounded-lg p-6">
			<h2 class="text-xl font-bold mb-4">주문 방법</h2>
			<ol class="space-y-4">
				<li class="flex gap-4">
					<span class="flex-shrink-0 w-8 h-8 bg-black text-white rounded-full flex items-center justify-center font-bold">1</span>
					<div>
						<h3 class="font-bold mb-1">상품 선택</h3>
						<p class="text-gray-600 text-sm">원하시는 상품을 선택하고 색상, 사이즈를 선택해주세요.</p>
					</div>
				</li>
				<li class="flex gap-4">
					<span class="flex-shrink-0 w-8 h-8 bg-black text-white rounded-full flex items-center justify-center font-bold">2</span>
					<div>
						<h3 class="font-bold mb-1">장바구니 담기</h3>
						<p class="text-gray-600 text-sm">장바구니에 담거나 바로 구매하기를 선택해주세요.</p>
					</div>
				</li>
				<li class="flex gap-4">
					<span class="flex-shrink-0 w-8 h-8 bg-black text-white rounded-full flex items-center justify-center font-bold">3</span>
					<div>
						<h3 class="font-bold mb-1">배송지 입력</h3>
						<p class="text-gray-600 text-sm">배송받으실 주소와 연락처를 정확하게 입력해주세요.</p>
					</div>
				</li>
				<li class="flex gap-4">
					<span class="flex-shrink-0 w-8 h-8 bg-black text-white rounded-full flex items-center justify-center font-bold">4</span>
					<div>
						<h3 class="font-bold mb-1">결제하기</h3>
						<p class="text-gray-600 text-sm">원하시는 결제 수단을 선택하고 결제를 완료해주세요.</p>
					</div>
				</li>
			</ol>
		</section>

		<!-- 결제 수단 -->
		<section class="bg-white border rounded-lg p-6">
			<h2 class="text-xl font-bold mb-4">결제 수단</h2>
			<div class="grid md:grid-cols-2 gap-4">
				<div class="p-4 bg-gray-50 rounded-lg">
					<h3 class="font-bold mb-2">신용/체크카드</h3>
					<p class="text-gray-600 text-sm">국내 모든 신용카드 및 체크카드 결제 가능</p>
				</div>
				<div class="p-4 bg-gray-50 rounded-lg">
					<h3 class="font-bold mb-2">실시간 계좌이체</h3>
					<p class="text-gray-600 text-sm">국내 주요 은행 계좌에서 실시간 이체</p>
				</div>
				<div class="p-4 bg-gray-50 rounded-lg">
					<h3 class="font-bold mb-2">가상계좌</h3>
					<p class="text-gray-600 text-sm">입금 전용 계좌번호 발급 후 이체</p>
				</div>
				<div class="p-4 bg-gray-50 rounded-lg">
					<h3 class="font-bold mb-2">간편결제</h3>
					<p class="text-gray-600 text-sm">카카오페이, 네이버페이, 토스페이 등</p>
				</div>
			</div>
		</section>

		<!-- 주문 확인 -->
		<section class="bg-white border rounded-lg p-6">
			<h2 class="text-xl font-bold mb-4">주문 확인</h2>
			<ul class="space-y-2 text-gray-700">
				<li class="flex items-start gap-2">
					<svg class="w-5 h-5 text-black mt-0.5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
					</svg>
					<span>주문 완료 시 입력하신 이메일로 주문 확인서가 발송됩니다.</span>
				</li>
				<li class="flex items-start gap-2">
					<svg class="w-5 h-5 text-black mt-0.5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
					</svg>
					<span>마이페이지 > 주문내역에서 주문 상태를 확인할 수 있습니다.</span>
				</li>
				<li class="flex items-start gap-2">
					<svg class="w-5 h-5 text-black mt-0.5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
					</svg>
					<span>비회원 주문의 경우 주문번호와 비밀번호로 조회 가능합니다.</span>
				</li>
			</ul>
		</section>

		<!-- 주의사항 -->
		<section class="bg-yellow-50 border border-yellow-200 rounded-lg p-6">
			<h2 class="text-xl font-bold mb-4 text-yellow-800">주의사항</h2>
			<ul class="space-y-2 text-yellow-800 text-sm">
				<li>• 가상계좌 입금은 주문일로부터 3일 이내에 완료해주세요. 기한 내 미입금 시 자동 취소됩니다.</li>
				<li>• 품절 상품은 결제가 완료되어도 자동 취소될 수 있습니다.</li>
				<li>• 주문 후 배송지 변경은 배송 준비 전까지만 가능합니다.</li>
				<li>• 해외 배송은 현재 지원하지 않습니다.</li>
			</ul>
		</section>

		<!-- 문의 -->
		<section class="text-center py-8 border-t">
			<p class="text-gray-600 mb-4">주문/결제 관련 문의사항이 있으시면 고객센터로 연락해주세요.</p>
			<p class="text-2xl font-bold">1234-5678</p>
			<p class="text-gray-500 text-sm mt-1">평일 10:00 - 18:00 (점심 12:00 - 13:00)</p>
		</section>
	</div>
</div>
