<script lang="ts">
	import { getSupabase } from '$lib/supabase';
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';

	let password = $state('');
	let passwordConfirm = $state('');
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
		if (!passwordRegex.test(password)) {
			error = '비밀번호는 8~20자, 영문/숫자/특수문자를 포함해야 합니다.';
			return;
		}

		if (password !== passwordConfirm) {
			error = '비밀번호가 일치하지 않습니다.';
			return;
		}

		loading = true;
		error = '';

		const { error: updateError } = await supabase.auth.updateUser({
			password
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

		// 3초 후 로그인 페이지로 이동
		setTimeout(() => {
			goto('/auth/login');
		}, 3000);
	}
</script>

<svelte:head>
	<title>비밀번호 재설정 | ko&clo</title>
</svelte:head>

<div class="max-w-md mx-auto mt-16 p-6">
	<h1 class="text-2xl font-bold text-center mb-4">비밀번호 재설정</h1>

	{#if success}
		<div class="p-4 bg-green-50 text-green-600 rounded-lg text-center">
			<p class="font-medium">비밀번호가 변경되었습니다.</p>
			<p class="text-sm mt-2">잠시 후 로그인 페이지로 이동합니다...</p>
		</div>
	{:else}
		<p class="text-gray-600 text-center mb-8">새로운 비밀번호를 입력해주세요.</p>

		<form onsubmit={(e) => { e.preventDefault(); handleSubmit(); }} class="space-y-4">
			{#if error}
				<div class="p-3 bg-red-50 text-red-600 rounded-lg text-sm">{error}</div>
			{/if}

			<div>
				<input
					type="password"
					bind:value={password}
					placeholder="새 비밀번호 (8~20자, 영문/숫자/특수문자)"
					class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-black"
					required
				/>
			</div>

			<div>
				<input
					type="password"
					bind:value={passwordConfirm}
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
	{/if}
</div>
