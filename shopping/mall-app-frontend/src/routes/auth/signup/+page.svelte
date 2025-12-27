<script lang="ts">
	import { getSupabase } from '$lib/supabase';
	import { page } from '$app/stores';
	import { signupSchema, type SignupInput } from '$lib/schemas/auth';

	let formData = $state<Partial<SignupInput>>({
		email: '',
		password: '',
		passwordConfirm: '',
		name: '',
		phone: '',
		agreements: {
			terms: false,
			privacy: false,
			marketing: false
		}
	});

	let loading = $state(false);
	let errors = $state<Record<string, string>>({});
	let successMessage = $state('');

	async function handleSubmit() {
		const supabase = getSupabase();
		if (!supabase) {
			errors.general = 'Supabase가 설정되지 않았습니다.';
			return;
		}

		loading = true;
		errors = {};

		// Zod 검증
		const result = signupSchema.safeParse(formData);
		if (!result.success) {
			result.error.errors.forEach((err) => {
				const path = err.path.join('.');
				errors[path] = err.message;
			});
			loading = false;
			return;
		}

		// Supabase 회원가입
		const { data, error } = await supabase.auth.signUp({
			email: formData.email!,
			password: formData.password!,
			options: {
				emailRedirectTo: `${$page.url.origin}/auth/callback`,
				data: {
					name: formData.name,
					phone: formData.phone,
					marketing_agreed: formData.agreements?.marketing || false
				}
			}
		});

		if (error) {
			if (error.message.includes('already registered')) {
				errors.general = '이미 가입된 이메일입니다.';
			} else {
				errors.general = error.message;
			}
			loading = false;
			return;
		}

		successMessage = '가입 확인 이메일을 보냈습니다. 이메일을 확인해주세요.';
		loading = false;
	}

	async function signUpWithSocial(provider: 'kakao' | 'naver' | 'google') {
		const supabase = getSupabase();
		if (!supabase) {
			errors.general = 'Supabase가 설정되지 않았습니다.';
			return;
		}

		await supabase.auth.signInWithOAuth({
			provider,
			options: {
				redirectTo: `${$page.url.origin}/auth/callback`
			}
		});
	}
</script>

<svelte:head>
	<title>회원가입 | ko&clo</title>
</svelte:head>

<div class="max-w-md mx-auto mt-16 p-6">
	<h1 class="text-2xl font-bold text-center mb-8">회원가입</h1>

	<!-- 소셜 로그인 버튼 -->
	<div class="space-y-3 mb-8">
		<button
			onclick={() => signUpWithSocial('kakao')}
			class="w-full py-3 bg-[#FEE500] text-black rounded-lg font-medium hover:bg-[#e6cf00] transition-colors"
		>
			카카오로 시작하기
		</button>
		<button
			onclick={() => signUpWithSocial('naver')}
			class="w-full py-3 bg-[#03C75A] text-white rounded-lg font-medium hover:bg-[#02b350] transition-colors"
		>
			네이버로 시작하기
		</button>
		<button
			onclick={() => signUpWithSocial('google')}
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
			또는 이메일로 가입
		</span>
	</div>

	{#if successMessage}
		<div class="p-4 bg-green-50 text-green-600 rounded-lg text-center mb-6">
			{successMessage}
		</div>
	{/if}

	<form onsubmit={(e) => { e.preventDefault(); handleSubmit(); }} class="space-y-4">
		{#if errors.general}
			<div class="p-3 bg-red-50 text-red-600 rounded-lg text-sm">{errors.general}</div>
		{/if}

		<div>
			<input
				type="email"
				bind:value={formData.email}
				placeholder="이메일"
				class="input-field"
				required
			/>
			{#if errors.email}
				<p class="text-red-500 text-sm mt-1">{errors.email}</p>
			{/if}
		</div>

		<div>
			<input
				type="password"
				bind:value={formData.password}
				placeholder="비밀번호 (8자 이상, 영문/숫자/특수문자 포함)"
				class="input-field"
				required
			/>
			{#if errors.password}
				<p class="text-red-500 text-sm mt-1">{errors.password}</p>
			{/if}
		</div>

		<div>
			<input
				type="password"
				bind:value={formData.passwordConfirm}
				placeholder="비밀번호 확인"
				class="input-field"
				required
			/>
			{#if errors.passwordConfirm}
				<p class="text-red-500 text-sm mt-1">{errors.passwordConfirm}</p>
			{/if}
		</div>

		<div>
			<input
				type="text"
				bind:value={formData.name}
				placeholder="이름"
				class="input-field"
				required
			/>
			{#if errors.name}
				<p class="text-red-500 text-sm mt-1">{errors.name}</p>
			{/if}
		</div>

		<div>
			<input
				type="tel"
				bind:value={formData.phone}
				placeholder="연락처 (선택)"
				class="input-field"
			/>
		</div>

		<!-- 약관 동의 -->
		<div class="space-y-3 pt-4 border-t">
			<label class="flex items-center gap-2 cursor-pointer">
				<input
					type="checkbox"
					bind:checked={formData.agreements!.terms}
					class="w-5 h-5"
				/>
				<span class="text-sm">
					<span class="text-red-500">[필수]</span> 이용약관에 동의합니다
				</span>
			</label>
			{#if errors['agreements.terms']}
				<p class="text-red-500 text-sm">{errors['agreements.terms']}</p>
			{/if}

			<label class="flex items-center gap-2 cursor-pointer">
				<input
					type="checkbox"
					bind:checked={formData.agreements!.privacy}
					class="w-5 h-5"
				/>
				<span class="text-sm">
					<span class="text-red-500">[필수]</span> 개인정보처리방침에 동의합니다
				</span>
			</label>
			{#if errors['agreements.privacy']}
				<p class="text-red-500 text-sm">{errors['agreements.privacy']}</p>
			{/if}

			<label class="flex items-center gap-2 cursor-pointer">
				<input
					type="checkbox"
					bind:checked={formData.agreements!.marketing}
					class="w-5 h-5"
				/>
				<span class="text-sm text-gray-600">[선택] 마케팅 정보 수신에 동의합니다</span>
			</label>
		</div>

		<button
			type="submit"
			disabled={loading}
			class="w-full py-3 bg-black text-white rounded-lg font-medium disabled:opacity-50 hover:bg-gray-800 transition-colors"
		>
			{loading ? '가입 중...' : '가입하기'}
		</button>
	</form>

	<div class="mt-6 text-center text-sm text-gray-500">
		이미 계정이 있으신가요?
		<a href="/auth/login" class="text-black hover:underline">로그인</a>
	</div>
</div>
