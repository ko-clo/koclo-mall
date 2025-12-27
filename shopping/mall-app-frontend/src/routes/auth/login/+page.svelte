<script lang="ts">
	import { getSupabase } from '$lib/supabase';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';

	let email = $state('');
	let password = $state('');
	let loading = $state(false);
	let error = $state('');

	const redirectTo = $page.url.searchParams.get('redirect') || '/';

	async function signInWithEmail() {
		const supabase = getSupabase();
		if (!supabase) {
			error = 'Supabase가 설정되지 않았습니다.';
			return;
		}

		loading = true;
		error = '';

		const { error: authError } = await supabase.auth.signInWithPassword({
			email,
			password
		});

		if (authError) {
			if (authError.message.includes('Invalid login credentials')) {
				error = '이메일 또는 비밀번호가 일치하지 않습니다.';
			} else if (authError.message.includes('Email not confirmed')) {
				error = '이메일 인증이 완료되지 않았습니다. 이메일을 확인해주세요.';
			} else {
				error = authError.message;
			}
			loading = false;
			return;
		}

		goto(redirectTo);
	}

	async function signInWithSocial(provider: 'kakao' | 'naver' | 'google') {
		const supabase = getSupabase();
		if (!supabase) {
			error = 'Supabase가 설정되지 않았습니다.';
			return;
		}

		await supabase.auth.signInWithOAuth({
			provider,
			options: {
				redirectTo: `${$page.url.origin}/auth/callback?redirect=${redirectTo}`
			}
		});
	}
</script>

<svelte:head>
	<title>로그인 | ko&clo</title>
</svelte:head>

<div class="max-w-md mx-auto mt-16 p-6">
	<h1 class="text-2xl font-bold text-center mb-8">로그인</h1>

	<!-- 소셜 로그인 버튼 -->
	<div class="space-y-3 mb-8">
		<button
			onclick={() => signInWithSocial('kakao')}
			class="w-full py-3 bg-[#FEE500] text-black rounded-lg font-medium hover:bg-[#e6cf00] transition-colors"
		>
			카카오로 시작하기
		</button>
		<button
			onclick={() => signInWithSocial('naver')}
			class="w-full py-3 bg-[#03C75A] text-white rounded-lg font-medium hover:bg-[#02b350] transition-colors"
		>
			네이버로 시작하기
		</button>
		<button
			onclick={() => signInWithSocial('google')}
			class="w-full py-3 bg-white border border-gray-300 rounded-lg font-medium hover:bg-gray-50 transition-colors"
		>
			Google로 시작하기
		</button>
	</div>

	<div class="relative my-6">
		<hr class="border-gray-200" />
		<span
			class="absolute left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white px-4 text-gray-400 text-sm"
		>
			또는
		</span>
	</div>

	<!-- 이메일 로그인 폼 -->
	<form onsubmit={(e) => { e.preventDefault(); signInWithEmail(); }} class="space-y-4">
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
		<input
			type="password"
			bind:value={password}
			placeholder="비밀번호"
			class="input-field"
			required
		/>

		<button
			type="submit"
			disabled={loading}
			class="w-full py-3 bg-black text-white rounded-lg font-medium disabled:opacity-50 hover:bg-gray-800 transition-colors"
		>
			{loading ? '로그인 중...' : '로그인'}
		</button>
	</form>

	<div class="mt-6 text-center text-sm text-gray-500">
		<a href="/auth/password-reset" class="hover:underline">비밀번호 찾기</a>
		<span class="mx-2">|</span>
		<a href="/auth/signup" class="hover:underline">회원가입</a>
	</div>
</div>
