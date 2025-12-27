<script lang="ts">
	import { getSupabase } from '$lib/supabase';
	import { authStore } from '$lib/stores/auth';
	import { goto } from '$app/navigation';

	let name = $state($authStore.user?.user_metadata?.name || '');
	let phone = $state($authStore.user?.user_metadata?.phone || '');
	let loading = $state(false);
	let error = $state('');
	let success = $state('');

	// 소셜 로그인 여부 확인
	const isSocialLogin = $derived(
		$authStore.user?.app_metadata?.provider !== 'email' &&
			$authStore.user?.app_metadata?.providers?.length > 0
	);

	async function handleSubmit() {
		const supabase = getSupabase();
		if (!supabase) {
			error = 'Supabase가 설정되지 않았습니다.';
			return;
		}

		loading = true;
		error = '';
		success = '';

		const { error: updateError } = await supabase.auth.updateUser({
			data: {
				name,
				phone
			}
		});

		if (updateError) {
			error = updateError.message;
			loading = false;
			return;
		}

		// authStore 업데이트
		authStore.update((state) => ({
			...state,
			user: state.user
				? {
						...state.user,
						user_metadata: {
							...state.user.user_metadata,
							name,
							phone
						}
					}
				: null
		}));

		success = '프로필이 수정되었습니다.';
		loading = false;
	}
</script>

<svelte:head>
	<title>프로필 수정 | ko&clo</title>
</svelte:head>

<div class="max-w-md mx-auto">
	<h1 class="text-2xl font-bold mb-8">프로필 수정</h1>

	<form onsubmit={(e) => { e.preventDefault(); handleSubmit(); }} class="space-y-6">
		{#if error}
			<div class="p-3 bg-red-50 text-red-600 rounded-lg text-sm">{error}</div>
		{/if}

		{#if success}
			<div class="p-3 bg-green-50 text-green-600 rounded-lg text-sm">{success}</div>
		{/if}

		<!-- 이메일 (수정 불가) -->
		<div>
			<label class="block text-sm font-medium text-gray-700 mb-1">이메일</label>
			<input
				type="email"
				value={$authStore.user?.email || ''}
				disabled
				class="w-full px-4 py-3 border border-gray-300 rounded-lg bg-gray-100 text-gray-500"
			/>
			<p class="text-xs text-gray-500 mt-1">이메일은 변경할 수 없습니다.</p>
		</div>

		<!-- 이름 -->
		<div>
			<label class="block text-sm font-medium text-gray-700 mb-1">이름</label>
			<input
				type="text"
				bind:value={name}
				placeholder="이름을 입력하세요"
				class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-black"
				required
			/>
		</div>

		<!-- 연락처 -->
		<div>
			<label class="block text-sm font-medium text-gray-700 mb-1">연락처</label>
			<input
				type="tel"
				bind:value={phone}
				placeholder="010-0000-0000"
				class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-black"
			/>
		</div>

		<button
			type="submit"
			disabled={loading}
			class="w-full py-3 bg-black text-white rounded-lg font-medium disabled:opacity-50 hover:bg-gray-800 transition-colors"
		>
			{loading ? '저장 중...' : '저장'}
		</button>
	</form>

	<!-- 비밀번호 변경 (이메일 가입만) -->
	{#if !isSocialLogin}
		<div class="mt-8 pt-8 border-t">
			<h2 class="font-bold mb-4">비밀번호 변경</h2>
			<a
				href="/my/profile/password"
				class="block w-full py-3 border border-gray-300 rounded-lg text-center hover:bg-gray-50 transition-colors"
			>
				비밀번호 변경하기
			</a>
		</div>
	{/if}

	<!-- 회원 탈퇴 -->
	<div class="mt-8 pt-8 border-t">
		<a href="/my/withdraw" class="text-sm text-gray-500 hover:text-red-500 transition-colors">
			회원 탈퇴
		</a>
	</div>
</div>
