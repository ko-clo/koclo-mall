<script lang="ts">
	import { getSupabase } from '$lib/supabase';
	import { authStore } from '$lib/stores/auth';
	import { goto } from '$app/navigation';

	type WithdrawReason =
		| 'SERVICE_UNSATISFIED'
		| 'RARELY_USED'
		| 'FOUND_ALTERNATIVE'
		| 'PRIVACY_CONCERN'
		| 'OTHER';

	const reasonLabels: Record<WithdrawReason, string> = {
		SERVICE_UNSATISFIED: '서비스 불만족',
		RARELY_USED: '이용 빈도 낮음',
		FOUND_ALTERNATIVE: '다른 서비스 이용',
		PRIVACY_CONCERN: '개인정보 우려',
		OTHER: '기타'
	};

	let selectedReason = $state<WithdrawReason | ''>('');
	let password = $state('');
	let confirmText = $state('');
	let loading = $state(false);
	let error = $state('');
	let step = $state(1); // 1: 안내, 2: 확인

	// 소셜 로그인 여부 확인
	const isSocialLogin = $derived(
		$authStore.user?.app_metadata?.provider !== 'email' &&
			$authStore.user?.app_metadata?.providers?.length > 0
	);

	function proceedToConfirm() {
		if (!selectedReason) {
			error = '탈퇴 사유를 선택해주세요.';
			return;
		}
		error = '';
		step = 2;
	}

	async function handleWithdraw() {
		const supabase = getSupabase();
		if (!supabase) {
			error = 'Supabase가 설정되지 않았습니다.';
			return;
		}

		// 이메일 가입인 경우 비밀번호 확인
		if (!isSocialLogin) {
			const { error: signInError } = await supabase.auth.signInWithPassword({
				email: $authStore.user?.email || '',
				password
			});

			if (signInError) {
				error = '비밀번호가 일치하지 않습니다.';
				return;
			}
		} else {
			// 소셜 로그인인 경우 확인 텍스트 검증
			if (confirmText !== '탈퇴합니다') {
				error = '"탈퇴합니다"를 정확히 입력해주세요.';
				return;
			}
		}

		loading = true;
		error = '';

		// TODO: Backend API 호출 - 탈퇴 처리
		// 현재는 Supabase 사용자 삭제만 수행
		// 실제로는 Backend에서 탈퇴 가능 여부 확인 후 처리해야 함

		try {
			// Supabase에서는 클라이언트에서 직접 사용자 삭제가 불가능
			// Backend API를 통해 처리해야 함
			// 여기서는 로그아웃만 수행
			await supabase.auth.signOut();

			authStore.set({
				user: null,
				session: null,
				loading: false,
				initialized: true
			});

			goto('/auth/login?withdrawn=true');
		} catch (err) {
			error = '탈퇴 처리 중 오류가 발생했습니다.';
			loading = false;
		}
	}
</script>

<svelte:head>
	<title>회원 탈퇴 | ko&clo</title>
</svelte:head>

<div class="max-w-md mx-auto">
	<h1 class="text-2xl font-bold mb-8">회원 탈퇴</h1>

	{#if step === 1}
		<!-- Step 1: 탈퇴 안내 -->
		<div class="space-y-6">
			<div class="p-4 bg-red-50 border border-red-200 rounded-lg">
				<p class="font-medium text-red-800 mb-2">탈퇴 전 확인해주세요</p>
				<ul class="text-sm text-red-700 space-y-1">
					<li>• 탈퇴 후 개인정보는 5일 이내에 삭제됩니다.</li>
					<li>• 보유 중인 포인트와 쿠폰은 즉시 소멸됩니다.</li>
					<li>• 작성한 리뷰는 익명화 처리됩니다.</li>
					<li>• 주문 기록은 법적 의무에 따라 5년간 보관됩니다.</li>
				</ul>
			</div>

			{#if error}
				<div class="p-3 bg-red-50 text-red-600 rounded-lg text-sm">{error}</div>
			{/if}

			<div>
				<label class="block text-sm font-medium text-gray-700 mb-2">탈퇴 사유</label>
				<div class="space-y-2">
					{#each Object.entries(reasonLabels) as [value, label]}
						<label class="flex items-center gap-3 p-3 border rounded-lg cursor-pointer hover:bg-gray-50">
							<input
								type="radio"
								name="reason"
								{value}
								bind:group={selectedReason}
								class="w-4 h-4"
							/>
							<span>{label}</span>
						</label>
					{/each}
				</div>
			</div>

			<div class="flex gap-3">
				<a
					href="/my/profile"
					class="flex-1 py-3 border border-gray-300 rounded-lg text-center hover:bg-gray-50 transition-colors"
				>
					취소
				</a>
				<button
					onclick={proceedToConfirm}
					class="flex-1 py-3 bg-red-500 text-white rounded-lg font-medium hover:bg-red-600 transition-colors"
				>
					다음
				</button>
			</div>
		</div>
	{:else}
		<!-- Step 2: 최종 확인 -->
		<div class="space-y-6">
			<div class="p-4 bg-gray-50 rounded-lg">
				<p class="text-sm text-gray-600">선택한 탈퇴 사유</p>
				<p class="font-medium">{reasonLabels[selectedReason as WithdrawReason]}</p>
			</div>

			{#if error}
				<div class="p-3 bg-red-50 text-red-600 rounded-lg text-sm">{error}</div>
			{/if}

			{#if isSocialLogin}
				<div>
					<label class="block text-sm font-medium text-gray-700 mb-1">
						탈퇴를 확인하려면 "탈퇴합니다"를 입력하세요
					</label>
					<input
						type="text"
						bind:value={confirmText}
						placeholder="탈퇴합니다"
						class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500"
					/>
				</div>
			{:else}
				<div>
					<label class="block text-sm font-medium text-gray-700 mb-1">
						비밀번호 확인
					</label>
					<input
						type="password"
						bind:value={password}
						placeholder="비밀번호를 입력하세요"
						class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500"
					/>
				</div>
			{/if}

			<div class="flex gap-3">
				<button
					onclick={() => (step = 1)}
					class="flex-1 py-3 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
				>
					이전
				</button>
				<button
					onclick={handleWithdraw}
					disabled={loading}
					class="flex-1 py-3 bg-red-500 text-white rounded-lg font-medium disabled:opacity-50 hover:bg-red-600 transition-colors"
				>
					{loading ? '처리 중...' : '탈퇴하기'}
				</button>
			</div>
		</div>
	{/if}
</div>
