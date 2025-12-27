import type { LayoutServerLoad } from './$types';
import { getSupabaseEnv } from '$lib/server/supabase';

export const load: LayoutServerLoad = async ({ locals }) => {
	return {
		session: locals.session,
		user: locals.user,
		supabaseEnv: getSupabaseEnv()
	};
};
