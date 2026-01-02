<script lang="ts">
	import { goto } from '$app/navigation';
	import { browser } from '$app/environment';
	import { addAddress, getAddresses } from '$lib/data/addresses';
	import { toastStore } from '$lib/stores/toast';

	let name = $state('');
	let recipient = $state('');
	let phone = $state('');
	let postalCode = $state('');
	let address = $state('');
	let addressDetail = $state('');
	let isDefault = $state(false);
	let isSaving = $state(false);

	// 첫 배송지인지 확인
	let isFirstAddress = $state(getAddresses().length === 0);

	function openAddressSearch() {
		if (!browser) return;

		new (window as any).daum.Postcode({
			oncomplete: function (data: any) {
				postalCode = data.zonecode;
				address = data.roadAddress || data.jibunAddress;
			}
		}).open();
	}

	function validateForm(): boolean {
		if (!recipient.trim()) {
			toastStore.error('수령인을 입력해주세요.');
			return false;
		}

		if (!phone.trim()) {
			toastStore.error('연락처를 입력해주세요.');
			return false;
		}

		// 전화번호 형식 검증 (간단한 검증)
		const phoneRegex = /^01[0-9]-?[0-9]{3,4}-?[0-9]{4}$/;
		if (!phoneRegex.test(phone.replace(/\s/g, ''))) {
			toastStore.error('올바른 휴대폰 번호를 입력해주세요.');
			return false;
		}

		if (!postalCode || !address) {
			toastStore.error('주소를 검색해주세요.');
			return false;
		}

		if (name.length > 20) {
			toastStore.error('배송지명은 20자 이내로 입력해주세요.');
			return false;
		}

		if (recipient.length > 50) {
			toastStore.error('수령인은 50자 이내로 입력해주세요.');
			return false;
		}

		if (addressDetail.length > 100) {
			toastStore.error('상세주소는 100자 이내로 입력해주세요.');
			return false;
		}

		return true;
	}

	async function handleSubmit() {
		if (!validateForm()) return;

		try {
			isSaving = true;

			await addAddress({
				name: name.trim() || `배송지 ${getAddresses().length + 1}`,
				recipient: recipient.trim(),
				phone: phone.trim(),
				postal_code: postalCode,
				address: address,
				address_detail: addressDetail.trim(),
				is_default: isDefault
			});

			toastStore.success('배송지가 등록되었습니다.');
			goto('/my/addresses');
		} catch (error) {
			toastStore.error(error instanceof Error ? error.message : '배송지 등록에 실패했습니다.');
		} finally {
			isSaving = false;
		}
	}
</script>

<svelte:head>
	<title>배송지 추가 | ko&clo</title>
	<script src="//t1.daumcdn.net/mapjsapi/bundle/postcode/prod/postcode.v2.js"></script>
</svelte:head>

<div class="max-w-2xl mx-auto">
	<div class="mb-6">
		<a href="/my/addresses" class="inline-flex items-center gap-1 text-gray-500 hover:text-black">
			<svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
				<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
			</svg>
			배송지 관리
		</a>
		<h1 class="text-2xl font-bold mt-4">배송지 추가</h1>
	</div>

	<form onsubmit={(e) => { e.preventDefault(); handleSubmit(); }} class="space-y-6">
		<!-- 배송지명 -->
		<div>
			<label class="block text-sm font-medium mb-2">
				배송지명 <span class="text-gray-400">(선택)</span>
			</label>
			<input
				type="text"
				bind:value={name}
				placeholder="예: 집, 회사"
				maxlength="20"
				class="input-field"
			/>
			<p class="text-xs text-gray-500 mt-1">미입력 시 '배송지 N'으로 자동 설정됩니다.</p>
		</div>

		<!-- 수령인 -->
		<div>
			<label class="block text-sm font-medium mb-2">
				수령인 <span class="text-red-500">*</span>
			</label>
			<input
				type="text"
				bind:value={recipient}
				placeholder="받으실 분 이름"
				maxlength="50"
				required
				class="input-field"
			/>
		</div>

		<!-- 연락처 -->
		<div>
			<label class="block text-sm font-medium mb-2">
				연락처 <span class="text-red-500">*</span>
			</label>
			<input
				type="tel"
				bind:value={phone}
				placeholder="010-1234-5678"
				maxlength="20"
				required
				class="input-field"
			/>
		</div>

		<!-- 주소 -->
		<div>
			<label class="block text-sm font-medium mb-2">
				주소 <span class="text-red-500">*</span>
			</label>
			<div class="flex gap-2 mb-2">
				<input
					type="text"
					bind:value={postalCode}
					placeholder="우편번호"
					readonly
					class="input-field w-32"
				/>
				<button
					type="button"
					onclick={openAddressSearch}
					class="px-4 py-2 border border-black rounded-lg font-medium hover:bg-gray-50 transition-colors"
				>
					주소 검색
				</button>
			</div>
			<input
				type="text"
				bind:value={address}
				placeholder="주소"
				readonly
				class="input-field mb-2"
			/>
			<input
				type="text"
				bind:value={addressDetail}
				placeholder="상세주소 (동/호수 등)"
				maxlength="100"
				class="input-field"
			/>
		</div>

		<!-- 기본 배송지 설정 -->
		<div>
			<label class="flex items-center gap-2 cursor-pointer">
				<input
					type="checkbox"
					bind:checked={isDefault}
					disabled={isFirstAddress}
					class="w-4 h-4"
				/>
				<span class="text-sm">
					기본 배송지로 설정
					{#if isFirstAddress}
						<span class="text-gray-500">(첫 배송지는 자동으로 기본 배송지로 설정됩니다)</span>
					{/if}
				</span>
			</label>
		</div>

		<!-- 버튼 -->
		<div class="flex gap-4">
			<a
				href="/my/addresses"
				class="flex-1 py-3 border border-gray-300 text-center rounded-lg font-medium hover:bg-gray-50 transition-colors"
			>
				취소
			</a>
			<button
				type="submit"
				disabled={isSaving}
				class="flex-1 py-3 bg-black text-white text-center rounded-lg font-medium hover:bg-gray-800 transition-colors disabled:opacity-50"
			>
				{isSaving ? '저장 중...' : '저장'}
			</button>
		</div>
	</form>
</div>
