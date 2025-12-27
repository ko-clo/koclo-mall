<script lang="ts">
	import { getSupabase } from '$lib/supabase';
	import { page } from '$app/stores';

	let email = $state('');
	let loading = $state(false);
	let message = $state('');
	let error = $state('');

	async function handleSubmit() {
		const supabase = getSupabase();
		if (!supabase) {
			error = 'Supabase가 설정되지 않았습니다.';
			return;
		}

		loading = true;
		error = '';
		message = '';

		const { error: resetError } = await supabase.auth.resetPasswordForEmail(email, {
			redirectTo: `${$page.url.origin}/auth/update-password`
		});

		if (resetError) {
			error = resetError.message;
		} else {
			// 보안상 이메일 존재 여부와 관계없이 동일한 메시지 표시
			message = '비밀번호 재설정 링크를 이메일로 보냈습니다. 이메일을 확인해주세요.';
		}

		loading = false;
	}
</script>

<svelte:head>
	<title>비밀번호 찾기 | ko&clo</title>
</svelte:head>

<div class="max-w-md mx-auto mt-16 p-6">
	<h1 class="text-2xl font-bold text-center mb-4">비밀번호 찾기</h1>
	<p class="text-gray-600 text-center mb-8">
		가입한 이메일 주소를 입력하시면<br />비밀번호 재설정 링크를 보내드립니다.
	</p>

	{#if message}
		<div class="p-4 bg-green-50 text-green-600 rounded-lg text-center mb-6">
			{message}
		</div>
	{/if}

	<form onsubmit={(e) => { e.preventDefault(); handleSubmit(); }} class="space-y-4">
		{#if error}
			<div class="p-3 bg-red-50 text-red-600 rounded-lg text-sm">{error}</div>
		{/if}

		<input
			type="email"
			bind:value={email}
			placeholder="이메일"
			class="input-field"
			required
		/>

		<button
			type="submit"
			disabled={loading}
			class="w-full py-3 bg-black text-white rounded-lg font-medium disabled:opacity-50 hover:bg-gray-800 transition-colors"
		>
			{loading ? '전송 중...' : '비밀번호 재설정 링크 받기'}
		</button>
	</form>

	<div class="mt-6 text-center">
		<a href="/auth/login" class="text-gray-500 hover:underline text-sm">로그인으로 돌아가기</a>
	</div>
</div>
