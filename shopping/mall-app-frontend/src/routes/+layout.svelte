<script lang="ts">
	import { onMount } from 'svelte';
	import { supabase } from '$lib/supabase';
	import { authStore } from '$lib/stores/auth';
	import Header from '$lib/components/layout/Header.svelte';
	import Footer from '$lib/components/layout/Footer.svelte';
	import '../app.css';

	let { data, children } = $props();

	// 초기 상태 설정
	$effect(() => {
		authStore.set({
			user: data.user,
			session: data.session,
			loading: false,
			initialized: true
		});
	});

	onMount(() => {
		// Supabase가 없으면 구독하지 않음
		if (!supabase) return;

		// 인증 상태 변화 구독
		const {
			data: { subscription }
		} = supabase.auth.onAuthStateChange((event, session) => {
			if (event === 'SIGNED_IN' || event === 'TOKEN_REFRESHED') {
				authStore.update((state) => ({
					...state,
					user: session?.user ?? null,
					session
				}));
			} else if (event === 'SIGNED_OUT') {
				authStore.update((state) => ({
					...state,
					user: null,
					session: null
				}));
			}
		});

		return () => subscription.unsubscribe();
	});
</script>

<div class="min-h-screen flex flex-col">
	<Header />
	<main class="flex-1">
		{@render children()}
	</main>
	<Footer />
</div>
