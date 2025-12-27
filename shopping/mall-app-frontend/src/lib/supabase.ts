import { createBrowserClient, type SupabaseClient } from '@supabase/ssr';
import { browser } from '$app/environment';

let supabaseInstance: SupabaseClient | null = null;

export function getSupabase(): SupabaseClient | null {
	if (!browser) return null;

	if (supabaseInstance) return supabaseInstance;

	// 런타임에 window에서 환경변수 읽기 (SSR에서 주입됨)
	const url = (window as any).__SUPABASE_URL__;
	const key = (window as any).__SUPABASE_ANON_KEY__;

	if (url && key) {
		supabaseInstance = createBrowserClient(url, key);
	}

	return supabaseInstance;
}

// 기존 코드 호환성을 위한 export (deprecated)
export const supabase = null;
