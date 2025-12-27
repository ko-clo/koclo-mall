import { createServerClient } from '@supabase/ssr';
import { env } from '$env/dynamic/public';
import type { Cookies } from '@sveltejs/kit';

export function createSupabaseServerClient(cookies: Cookies) {
	const url = env.PUBLIC_SUPABASE_URL;
	const key = env.PUBLIC_SUPABASE_ANON_KEY;

	if (!url || !key) {
		return null;
	}

	return createServerClient(url, key, {
		cookies: {
			get: (key) => cookies.get(key),
			set: (key, value, options) => {
				cookies.set(key, value, { path: '/', ...options });
			},
			remove: (key, options) => {
				cookies.delete(key, { path: '/', ...options });
			}
		}
	});
}

// 환경변수 getter (레이아웃에서 클라이언트로 전달용)
export function getSupabaseEnv() {
	return {
		url: env.PUBLIC_SUPABASE_URL || '',
		key: env.PUBLIC_SUPABASE_ANON_KEY || ''
	};
}
