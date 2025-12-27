<script lang="ts">
	import { getSupabase } from '$lib/supabase';
	import { authStore } from '$lib/stores/auth';
	import { goto } from '$app/navigation';

	let currentPassword = $state('');
	let newPassword = $state('');
	let newPasswordConfirm = $state('');
	let loading = $state(false);
	let error = $state('');
	let success = $state(false);

	// 비밀번호 검증 규칙: 8~20자, 영문+숫자+특수문자
	const passwordRegex = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,20}$/;

	async function handleSubmit() {
		const supabase = getSupabase();
		if (!supabase) {
			error = 'Supabase가 설정되지 않았습니다.';
			return;
		}

		// 클라이언트 검증
		if (!passwordRegex.test(newPassword)) {
			error = '새 비밀번호는 8~20자, 영문/숫자/특수문자를 포함해야 합니다.';
			return;
		}

		if (newPassword !== newPasswordConfirm) {
			error = '새 비밀번호가 일치하지 않습니다.';
			return;
		}

		loading = true;
		error = '';

		// 1. 현재 비밀번호 확인
		const { error: signInError } = await supabase.auth.signInWithPassword({
			email: $authStore.user?.email || '',
			password: currentPassword
		});

		if (signInError) {
			error = '현재 비밀번호가 일치하지 않습니다.';
			loading = false;
			return;
		}

		// 2. 새 비밀번호로 변경
		const { error: updateError } = await supabase.auth.updateUser({
			password: newPassword
		});

		if (updateError) {
			if (updateError.message.includes('same as')) {
				error = '기존 비밀번호와 동일합니다. 다른 비밀번호를 입력해주세요.';
			} else {
				error = updateError.message;
			}
			loading = false;
			return;
		}

		success = true;
		loading = false;

		// 2초 후 프로필 페이지로 이동
		setTimeout(() => {
			goto('/my/profile');
		}, 2000);
	}
</script>

<svelte:head>
	<title>비밀번호 변경 | ko&clo</title>
</svelte:head>

<div class="max-w-md mx-auto">
	<h1 class="text-2xl font-bold mb-8">비밀번호 변경</h1>

	{#if success}
		<div class="p-4 bg-green-50 text-green-600 rounded-lg text-center">
			<p class="font-medium">비밀번호가 변경되었습니다.</p>
			<p class="text-sm mt-2">잠시 후 프로필 페이지로 이동합니다...</p>
		</div>
	{:else}
		<form onsubmit={(e) => { e.preventDefault(); handleSubmit(); }} class="space-y-6">
			{#if error}
				<div class="p-3 bg-red-50 text-red-600 rounded-lg text-sm">{error}</div>
			{/if}

			<div>
				<label class="block text-sm font-medium text-gray-700 mb-1">현재 비밀번호</label>
				<input
					type="password"
					bind:value={currentPassword}
					placeholder="현재 비밀번호"
					class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-black"
					required
				/>
			</div>

			<div>
				<label class="block text-sm font-medium text-gray-700 mb-1">새 비밀번호</label>
				<input
					type="password"
					bind:value={newPassword}
					placeholder="새 비밀번호 (8~20자, 영문/숫자/특수문자)"
					class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-black"
					required
				/>
			</div>

			<div>
				<label class="block text-sm font-medium text-gray-700 mb-1">새 비밀번호 확인</label>
				<input
					type="password"
					bind:value={newPasswordConfirm}
					placeholder="새 비밀번호 확인"
					class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-black"
					required
				/>
			</div>

			<button
				type="submit"
				disabled={loading}
				class="w-full py-3 bg-black text-white rounded-lg font-medium disabled:opacity-50 hover:bg-gray-800 transition-colors"
			>
				{loading ? '변경 중...' : '비밀번호 변경'}
			</button>
		</form>

		<div class="mt-6 text-center">
			<a href="/my/profile" class="text-gray-500 hover:underline text-sm">취소</a>
		</div>
	{/if}
</div>
