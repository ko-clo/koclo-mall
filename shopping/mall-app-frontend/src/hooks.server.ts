import { createSupabaseServerClient } from '$lib/server/supabase';
import { redirect, type Handle } from '@sveltejs/kit';

export const handle: Handle = async ({ event, resolve }) => {
	// Supabase 클라이언트 생성 (환경변수 없으면 null)
	const supabase = createSupabaseServerClient(event.cookies);

	if (!supabase) {
		// 개발 모드: Supabase 없이 진행
		event.locals.supabase = null as any;
		event.locals.user = null;
		event.locals.session = null;
		return resolve(event);
	}

	event.locals.supabase = supabase;

	// 세션 검증
	const {
		data: { session },
		error
	} = await supabase.auth.getSession();

	if (session) {
		event.locals.user = session.user;
		event.locals.session = session;
	} else {
		event.locals.user = null;
		event.locals.session = null;
	}

	// 보호된 라우트 정의
	const protectedRoutes = ['/my', '/admin', '/cart'];
	const adminRoutes = ['/admin'];

	const isProtected = protectedRoutes.some((route) => event.url.pathname.startsWith(route));
	const isAdmin = adminRoutes.some((route) => event.url.pathname.startsWith(route));

	// 보호된 라우트 접근 시 로그인 필요
	if (isProtected && !event.locals.user) {
		const redirectTo = encodeURIComponent(event.url.pathname);
		throw redirect(302, `/auth/login?redirect=${redirectTo}`);
	}

	// Admin 권한 검증 (TODO: DB에서 role 조회)
	if (isAdmin && event.locals.user) {
		// const member = await getMemberRole(event.locals.user.id);
		// if (member?.role !== 'admin') {
		//   throw redirect(302, '/');
		// }
	}

	return resolve(event);
};
